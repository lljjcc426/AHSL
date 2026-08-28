from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from interaction_structure.meta1.data import load_ishizawa
from interaction_structure.meta1.estimand import ReferenceEstimand
from interaction_structure.meta1.evaluation import signed_support_metrics
from interaction_structure.meta1.methods import fit_elastic_net, fit_lasso
from interaction_structure.meta1.protocol import EvaluationOracle, design_balanced_mask, hybrid_design_mask, make_measurement_masks, reveal
from interaction_structure.meta1_6.baselines import dcd_baseline_score, hils_score
from interaction_structure.meta1_6.ensemble import RecoveryScenario, make_support_ensemble, prior_variant
from interaction_structure.meta1_6.scoring import score_design
from interaction_structure.meta1_6.search import optimize_rows
from interaction_structure.meta1_6.simulation import simulate_recovery
from interaction_structure.meta1_6.structure import (
    and_dictionary,
    sparse_nullspace_diagnostics,
    structural_diagnostics,
    validate_development_seed,
)


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results" / "meta1_6"
RAW = RESULT / "raw"
AGG = RESULT / "aggregated"
FIG = RESULT / "figures"
ISHIZAWA = ROOT.parent / "s1_sources" / "microbiome_ishizawa" / "data1_rawcfu.csv"
BUDGETS = (16, 24, 32)
DEV_SEEDS = (101, 202, 303, 404)
SEARCH_SEED = 1601


def uniform_mask(budget: int, seed: int) -> tuple[int, ...]:
    validate_development_seed(seed)
    frame = make_measurement_masks(64, (budget,), (seed,))
    return tuple(sorted(frame.community_mask.astype(int)))


def reference_from_frame(frame: pd.DataFrame, landscape_id: str) -> ReferenceEstimand:
    selected = frame[frame.landscape_id == landscape_id].sort_values("term_mask")
    return ReferenceEstimand(
        landscape_id=landscape_id,
        panel_id="ishizawa",
        scale="log10",
        coefficients=selected.coefficient.to_numpy(float),
        lower=selected.ci_lower.to_numpy(float),
        upper=selected.ci_upper.to_numpy(float),
        sign_stability=selected.sign_stability.to_numpy(float),
        support_sign=selected.support_sign.to_numpy(int),
        practical_threshold=float(selected.practical_threshold.iloc[0]),
        bootstrap_seed=int(selected.bootstrap_seed.iloc[0]),
        n_bootstrap=int(selected.n_bootstrap.iloc[0]),
    )


def objective_factory(name: str, scenarios: list[RecoveryScenario]):
    if name == "HILS":
        return lambda masks: hils_score(masks, scenarios, draws=16)
    if name == "DCD":
        return lambda masks: dcd_baseline_score(masks, scenarios)
    settings = {
        "candidate_symmetric": dict(target_only=False, aggregator="robust", integrate_singular=True),
        "candidate_target_aware": dict(target_only=True, aggregator="mean", integrate_singular=True),
        "candidate_no_singular": dict(target_only=True, aggregator="robust", integrate_singular=False),
        "candidate_full": dict(target_only=True, aggregator="robust", integrate_singular=True),
    }[name]
    return lambda masks: score_design(masks, scenarios, draws=16, **settings).score


def build_designs(scenarios: list[RecoveryScenario]) -> tuple[dict[tuple[str, int], tuple[int, ...]], pd.DataFrame]:
    designs: dict[tuple[str, int], tuple[int, ...]] = {}
    trials: list[dict] = []
    search_scenarios = scenarios
    for budget in BUDGETS:
        starts = (
            uniform_mask(budget, 101),
            design_balanced_mask(6, budget, 101),
            hybrid_design_mask(6, budget, 101, 0.5),
        )
        for name in ("HILS", "DCD", "candidate_symmetric", "candidate_target_aware", "candidate_no_singular", "candidate_full"):
            result = optimize_rows(
                6,
                budget,
                objective_factory(name, search_scenarios),
                seed=SEARCH_SEED + budget * 10 + len(name),
                starts=starts,
                restarts=2,
                proposals_per_round=16,
                patience=2,
            )
            designs[name, budget] = result.masks
            trials.append(
                {
                    "stage": "row_search",
                    "method": name,
                    "budget": budget,
                    "search_seed": SEARCH_SEED + budget * 10 + len(name),
                    "restarts": 2,
                    "proposals_per_round": 16,
                    "patience": 2,
                    "evaluations": result.evaluations,
                    "accepted_swaps": result.accepted_swaps,
                    "objective": result.score,
                    "runtime_seconds": result.runtime_seconds,
                }
            )
    return designs, pd.DataFrame(trials)


def all_masks(method: str, budget: int, seed: int, optimized: dict[tuple[str, int], tuple[int, ...]]) -> tuple[int, ...]:
    if method == "uniform":
        return uniform_mask(budget, seed)
    if method == "D-opt":
        return design_balanced_mask(6, budget, seed)
    if method == "hybrid_d50":
        return hybrid_design_mask(6, budget, seed, 0.5)
    return optimized[method, budget]


def support_ensemble_frame(scenarios: list[RecoveryScenario]) -> pd.DataFrame:
    rows = []
    for scenario in scenarios:
        for term, sign, effect in zip(scenario.active, scenario.signs, scenario.effects, strict=True):
            rows.append(
                {
                    "scenario_id": scenario.scenario_id,
                    "term_mask": term,
                    "order": int(term).bit_count(),
                    "role": "target" if int(term).bit_count() >= 3 else "nuisance",
                    "sign": sign,
                    "effect": effect,
                    "sigma": scenario.sigma,
                    "k_high": scenario.k_high,
                    "k_low": scenario.k_low,
                    "snr": scenario.snr,
                    "noise_seed": scenario.noise_seed,
                }
            )
    return pd.DataFrame(rows)


def scaling_audit() -> pd.DataFrame:
    rows = []
    for dimension, budgets in ((6, BUDGETS), (7, (24, 32, 48)), (8, (32, 48, 64))):
        scenarios = make_support_ensemble(
            dimension=dimension,
            seed=1900 + dimension,
            k_high_values=(2, 4),
            k_low_values=(2, 4),
            snr_values=(1.0, 2.0),
            replicates=1,
        )
        for budget in budgets:
            started = perf_counter()
            masks = design_balanced_mask(dimension, budget, 1900 + dimension)
            diagnostics = structural_diagnostics(dimension, masks)
            objective = score_design(masks, scenarios, dimension=dimension, draws=16, aggregator="robust")
            rows.append(
                {
                    "dimension": dimension,
                    "candidate_rows": 1 << dimension,
                    "nonempty_terms": (1 << dimension) - 1,
                    "budget": budget,
                    "rank_full": diagnostics["rank_full"],
                    "target_columns": (1 << dimension) - 1 - dimension - dimension * (dimension - 1) // 2,
                    "objective": objective.score,
                    "singular_fraction": objective.singular_fraction,
                    "runtime_seconds": perf_counter() - started,
                }
            )
    return pd.DataFrame(rows)


def design_and_identifiability(
    optimized: dict[tuple[str, int], tuple[int, ...]], scenarios: list[RecoveryScenario]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    design_rows, audit_rows = [], []
    methods = ("uniform", "D-opt", "hybrid_d50", "HILS", "DCD", "candidate_symmetric", "candidate_target_aware", "candidate_no_singular", "candidate_full")
    for budget in BUDGETS:
        for method in methods:
            seeds = DEV_SEEDS if method in {"uniform", "D-opt", "hybrid_d50"} else (SEARCH_SEED,)
            for seed in seeds:
                masks = all_masks(method, budget, seed, optimized)
                for row in masks:
                    design_rows.append({"method": method, "budget": budget, "design_seed": seed, "community_mask": row})
                audit = structural_diagnostics(6, masks)
                sparse = sparse_nullspace_diagnostics(6, masks, sampled_four_sets=128, seed=seed)
                kkt = score_design(masks, scenarios, draws=32, aggregator="robust")
                audit_rows.append(
                    {
                        "method": method,
                        "budget": budget,
                        "design_seed": seed,
                        **audit,
                        **sparse,
                        "target_kkt_mean": kkt.mean_probability,
                        "target_kkt_cvar20": kkt.cvar,
                        "integrated_singular_fraction": kkt.singular_fraction,
                    }
                )
    return pd.DataFrame(design_rows), pd.DataFrame(audit_rows)


def synthetic_runs(optimized: dict[tuple[str, int], tuple[int, ...]], scenarios: list[RecoveryScenario]) -> pd.DataFrame:
    rows = []
    methods = ("uniform", "D-opt", "hybrid_d50", "HILS", "candidate_symmetric", "candidate_target_aware", "candidate_no_singular", "candidate_full", "DCD")
    for budget in BUDGETS:
        for method in methods:
            masks = all_masks(method, budget, 101, optimized)
            objective = score_design(masks, scenarios, draws=32, aggregator="robust")
            for scenario in scenarios:
                metrics = simulate_recovery(masks, scenario, estimator="lasso")
                rows.append(
                    {
                        "method": method,
                        "budget": budget,
                        "scenario_id": scenario.scenario_id,
                        "k_high": scenario.k_high,
                        "k_low": scenario.k_low,
                        "snr": scenario.snr,
                        "objective": objective.score,
                        "singular_fraction": objective.singular_fraction,
                        **metrics,
                    }
                )
    return pd.DataFrame(rows)


def phase_diagram(optimized: dict[tuple[str, int], tuple[int, ...]]) -> pd.DataFrame:
    rows = []
    for budget in BUDGETS:
        for k_high in (2, 4, 8, 12):
            for k_low in (0, 4, 8, 12):
                for snr in (0.5, 1.0, 2.0):
                    scenarios = make_support_ensemble(
                        seed=1700 + budget + 10 * k_high + k_low,
                        k_high_values=(k_high,),
                        k_low_values=(k_low,),
                        snr_values=(snr,),
                        replicates=2,
                    )
                    for method in ("uniform", "D-opt", "HILS", "candidate_full"):
                        masks = all_masks(method, budget, 101, optimized)
                        values = [simulate_recovery(masks, scenario)["signed_f1"] for scenario in scenarios]
                        singular = score_design(masks, scenarios, draws=16, aggregator="mean").singular_fraction
                        rows.append(
                            {
                                "budget": budget,
                                "k_high": k_high,
                                "k_low": k_low,
                                "snr": snr,
                                "method": method,
                                "mean_signed_f1": float(np.mean(values)),
                                "exact_recovery_rate": float(np.mean([value == 1.0 for value in values])),
                                "singular_fraction": singular,
                            }
                        )
    return pd.DataFrame(rows)


def real_runs(optimized: dict[tuple[str, int], tuple[int, ...]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    panel = load_ishizawa(ISHIZAWA)
    reference_frame = pd.read_csv(ROOT / "results" / "meta1" / "raw" / "support_reference.csv")
    references = {landscape.landscape_id: reference_from_frame(reference_frame, landscape.landscape_id) for landscape in panel.landscapes}
    rows, trials = [], []
    methods = ("uniform", "D-opt", "hybrid_d50", "HILS", "candidate_symmetric", "candidate_target_aware", "candidate_no_singular", "candidate_full", "DCD")
    counter = 0
    for budget in BUDGETS:
        for seed in DEV_SEEDS:
            for method in methods:
                masks = all_masks(method, budget, seed, optimized)
                estimators = ("lasso", "elastic_net") if method in {"HILS", "candidate_full"} else ("lasso",)
                for landscape in panel.landscapes:
                    reference = references[landscape.landscape_id]
                    revealed = reveal(landscape, masks, "log10")
                    for estimator in estimators:
                        fit = fit_lasso(revealed, seed) if estimator == "lasso" else fit_elastic_net(revealed, seed)
                        metrics = signed_support_metrics(reference, fit.coefficients, fit.selected)
                        response_rmse = EvaluationOracle(landscape, "log10").hidden_response_rmse(fit.coefficients, masks)
                        rows.append(
                            {
                                "run_id": f"M16-{counter:05d}",
                                "landscape": landscape.landscape_id,
                                "budget": budget,
                                "mask_seed": seed,
                                "design_method": method,
                                "estimator": estimator,
                                "response_scale": "log10",
                                "support_estimand": "META1-R1-CI95-practical-effect",
                                "hyperparameters": fit.hyperparameters,
                                "response_rmse": response_rmse,
                                **metrics,
                            }
                        )
                        trials.append(
                            {
                                "stage": "real_estimator",
                                "method": method,
                                "budget": budget,
                                "mask_seed": seed,
                                "landscape": landscape.landscape_id,
                                "estimator": estimator,
                                "selected_hyperparameters": fit.hyperparameters,
                                "validation_mse": fit.validation_mse,
                            }
                        )
                        counter += 1
    return pd.DataFrame(rows), pd.DataFrame(trials)


def random_cloud(
    scenarios: list[RecoveryScenario], panel, references: dict[str, ReferenceEstimand]
) -> pd.DataFrame:
    rows = []
    rng = np.random.default_rng(1801)
    subset = scenarios[::6]
    for budget in BUDGETS:
        for cloud_id in range(24):
            masks = tuple(sorted((0, *rng.choice(np.arange(1, 64), size=budget - 1, replace=False).tolist())))
            objective = score_design(masks, scenarios, draws=16, aggregator="robust")
            synthetic = float(np.mean([simulate_recovery(masks, scenario)["signed_f1"] for scenario in subset]))
            real_values = []
            for landscape in panel.landscapes:
                fit = fit_lasso(reveal(landscape, masks, "log10"), 101)
                real_values.append(signed_support_metrics(references[landscape.landscape_id], fit.coefficients, fit.selected)["primary_f1"])
            rows.append(
                {
                    "budget": budget,
                    "cloud_id": cloud_id,
                    "objective": objective.score,
                    "objective_mean": objective.mean_probability,
                    "objective_cvar20": objective.cvar,
                    "singular_fraction": objective.singular_fraction,
                    "synthetic_signed_f1": synthetic,
                    "real_macro_f1": float(np.mean(real_values)),
                    "community_masks": ";".join(map(str, masks)),
                }
            )
    return pd.DataFrame(rows)


def prior_sensitivity(optimized: dict[tuple[str, int], tuple[int, ...]]) -> pd.DataFrame:
    rows = []
    for prior in ("sparser", "primary", "denser", "weak"):
        scenarios = prior_variant(prior)
        for budget in BUDGETS:
            for method in ("HILS", "candidate_full", "D-opt", "uniform"):
                masks = all_masks(method, budget, 101, optimized)
                score = score_design(masks, scenarios, draws=24, aggregator="robust")
                rows.append(
                    {
                        "prior": prior,
                        "budget": budget,
                        "method": method,
                        "objective": score.score,
                        "mean_probability": score.mean_probability,
                        "cvar20": score.cvar,
                        "singular_fraction": score.singular_fraction,
                    }
                )
    return pd.DataFrame(rows)


def alignment(cloud: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for budget, group in list(cloud.groupby("budget")) + [("all", cloud)]:
        for outcome in ("synthetic_signed_f1", "real_macro_f1"):
            correlation, pvalue = spearmanr(group.objective, group[outcome])
            rows.append({"budget": budget, "objective": "robust_kkt", "outcome": outcome, "spearman_rho": correlation, "pvalue": pvalue, "n_designs": len(group)})
    return pd.DataFrame(rows)


def write_figures(phase: pd.DataFrame, synthetic: pd.DataFrame, real: pd.DataFrame, cloud: pd.DataFrame, priors: pd.DataFrame) -> None:
    plt.style.use("seaborn-v0_8-whitegrid")
    for budget in BUDGETS:
        view = phase[(phase.budget == budget) & (phase.method == "candidate_full")]
        pivot = view.groupby(["k_high", "snr"]).mean_signed_f1.mean().unstack()
        fig, ax = plt.subplots(figsize=(6, 4))
        image = ax.imshow(pivot, vmin=0, vmax=1, aspect="auto", cmap="viridis")
        ax.set_xticks(range(len(pivot.columns)), pivot.columns)
        ax.set_yticks(range(len(pivot.index)), pivot.index)
        ax.set_xlabel("SNR")
        ax.set_ylabel("k_H")
        ax.set_title(f"Recoverability phase diagram, budget={budget}")
        fig.colorbar(image, ax=ax, label="signed F1")
        fig.tight_layout()
        fig.savefig(FIG / f"phase_diagram_b{budget}.png", dpi=180)
        plt.close(fig)
    summary = synthetic.groupby(["budget", "method"]).signed_f1.mean().reset_index()
    fig, ax = plt.subplots(figsize=(9, 4))
    for method, group in summary.groupby("method"):
        ax.plot(group.budget, group.signed_f1, marker="o", label=method)
    ax.set_ylabel("Mean synthetic signed F1")
    ax.legend(ncol=3, fontsize=7)
    fig.tight_layout()
    fig.savefig(FIG / "synthetic_comparison.png", dpi=180)
    plt.close(fig)
    real_lasso = real[real.estimator == "lasso"]
    paired = real_lasso.pivot_table(index=["landscape", "budget", "mask_seed"], columns="design_method", values="primary_f1")
    delta = paired["candidate_full"] - paired["HILS"]
    fig, ax = plt.subplots(figsize=(8, 4))
    delta.groupby(level="landscape").mean().sort_values().plot.bar(ax=ax)
    ax.axhline(0, color="black", linewidth=1)
    ax.set_ylabel("candidate_full - HILS signed F1")
    fig.tight_layout()
    fig.savefig(FIG / "per_landscape_delta.png", dpi=180)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    axes[0].scatter(cloud.objective, cloud.synthetic_signed_f1, alpha=0.7)
    axes[0].set(xlabel="KKT objective", ylabel="Synthetic signed F1")
    axes[1].scatter(cloud.objective, cloud.real_macro_f1, alpha=0.7)
    axes[1].set(xlabel="KKT objective", ylabel="Real macro F1")
    fig.tight_layout()
    fig.savefig(FIG / "random_cloud_alignment.png", dpi=180)
    plt.close(fig)
    pivot = priors[priors.method == "candidate_full"].pivot(index="prior", columns="budget", values="objective")
    fig, ax = plt.subplots(figsize=(6, 3))
    image = ax.imshow(pivot, aspect="auto", cmap="magma")
    ax.set_xticks(range(len(pivot.columns)), pivot.columns)
    ax.set_yticks(range(len(pivot.index)), pivot.index)
    fig.colorbar(image, ax=ax, label="objective")
    fig.tight_layout()
    fig.savefig(FIG / "prior_sensitivity.png", dpi=180)
    plt.close(fig)


def decision_from_results(real_summary: pd.DataFrame, synthetic_summary: pd.DataFrame, alignment_frame: pd.DataFrame) -> tuple[str, dict[str, float]]:
    real_lasso = real_summary[real_summary.estimator == "lasso"]
    candidate = real_lasso[real_lasso.design_method == "candidate_full"].set_index("budget").primary_f1
    hils = real_lasso[real_lasso.design_method == "HILS"].set_index("budget").primary_f1
    synthetic = synthetic_summary.pivot(index="budget", columns="method", values="signed_f1")
    real_delta = float((candidate - hils).mean())
    synthetic_delta = float((synthetic["candidate_full"] - synthetic["HILS"]).mean())
    real_rho = float(alignment_frame[alignment_frame.outcome == "real_macro_f1"].iloc[-1].spearman_rho)
    if real_delta >= 0.03 and synthetic_delta > 0 and real_rho > 0.2:
        decision = "D-A"
    elif synthetic_delta > 0 and real_delta > -0.01:
        decision = "D-B"
    elif real_delta <= 0 and synthetic_delta <= 0:
        decision = "D-C"
    else:
        decision = "D-D"
    return decision, {"real_delta": real_delta, "synthetic_delta": synthetic_delta, "real_alignment_rho": real_rho}


def report_text(decision: str, evidence: dict[str, float], real_summary: pd.DataFrame, ident: pd.DataFrame, alignment_frame: pd.DataFrame) -> str:
    dense16 = ident[(ident.budget == 16) & (ident.method == "D-opt")].iloc[0]
    macro = real_summary[(real_summary.estimator == "lasso") & (real_summary.design_method.isin(["candidate_full", "HILS", "D-opt", "uniform"]))]
    columns = ["budget", "design_method", "primary_f1", "precision", "recall"]
    table_rows = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in macro[columns].itertuples(index=False):
        table_rows.append(f"| {row.budget} | {row.design_method} | {row.primary_f1:.4f} | {row.precision:.4f} | {row.recall:.4f} |")
    table = "\n".join(table_rows)
    exact_next = {
        "D-A": "等待人工审核；若批准，冻结实现与新 reserve 标识后再开始一次性确认，当前阶段不创建掩码、不运行 reserve。",
        "D-B": "保留方法原型，不建立 reserve；先解决 synthetic-to-real transfer 与目标相关性问题。",
        "D-C": "停止该设计方法方向，保留结构不可识别性结果作为负结果。",
        "D-D": "停止并重新定义 estimand 或观测预算；不再扩展当前目标。",
    }[decision]
    sections = [
        ("1. Executive decision", f"最终分类为 **{decision}**。证据阈值由预注册规则机械给出，而不是按结果修改。"),
        ("2. Modified problem", "固定 d=6 Boolean 行池，在预算 16/24/32 下恢复 42 个三阶及以上 AND 系数的带符号支持；21 个一至二阶项是 nuisance。"),
        ("3. Why broad META1 novelty was insufficient", "META1 的一般稀疏回归比较没有把设计目标、目标/干扰不对称和符号恢复事件合成一个可审计对象。"),
        ("4. AND dictionary structure", "使用 64 个 Boolean 行与 63 个非空 AND 列；空行固定测量并承担基线锚定。"),
        ("5. Target/nuisance decomposition", "目标为阶数>=3，nuisance 为阶数1-2；主指标只评价目标支持和符号。"),
        ("6. Dense-nuisance identifiability", f"预算16的 D-opt 设计 rank(X_L)={int(dense16.rank_low)}，投影后目标秩={int(dense16.rank_residual_target)}、零残差目标列={int(dense16.zero_residual_target_columns)}。因此 N0 不能作为主问题。"),
        ("7. Sparse/regularized nuisance alternatives", "N1 对全部63项联合稀疏惩罚；N2 对低阶块作 ridge 残差化，仅作为敏感性分析。"),
        ("8. Frozen nuisance formulation", "冻结 N1：Lasso 联合估计，评价仅作用于高阶符号支持；不假设 heredity。"),
        ("9. Structural identifiability", "原始秩、投影秩、零列、目标-目标别名、目标-低阶别名、互相关与限制奇异值均逐设计记录。"),
        ("10. Sparse null-space analysis", "q=1,2,3 穷举，q=4 固定抽样128组；只把实际线性依赖计为失败。"),
        ("11. Recoverability phase diagram", "相图跨 k_H、k_L、SNR 和预算；奇异场景未被删除。"),
        ("12. Support ensemble Pi", "Pi 与 Ishizawa 标签独立：高阶支持按阶数轮转平衡抽样，低阶均匀抽样，正负号平衡，效应由 SNR 网格控制。"),
        ("13. Prior sensitivity", "比较 sparser、primary、denser、weak 四种先验；结果见 aggregated/prior_sensitivity.csv。"),
        ("14. Primary estimator decision", "冻结 Route B：Lasso 目标与 KKT 条件直接对应。ElasticNet 只做 transfer 检查。"),
        ("15. Sign-recovery objective derivation", "对每个支持/符号场景直接模拟高斯 score，并同时检查活跃符号与目标非活跃 KKT 不等式；lambda 在预设三点路径上取最好事件概率。"),
        ("16. Faithful HILS baseline", "HILS 使用相同 Pi、lambda 路径和噪声抽样，但要求全部63项的支持与符号正确，最后对场景取均值。"),
        ("17. DCD baseline", "DCD 由支持子 Gram 最小特征值与 irrepresentability margin 的乘积构成，奇异支持计零。"),
        ("18. Classical comparators", "比较 uniform、D-opt、hybrid_d50、HILS、DCD。"),
        ("19. Modified objective", "新目标为高阶 target-only KKT 概率的 0.8 mean + 0.2 CVaR20，并把奇异场景集成成零分。"),
        ("20. Row-search algorithm", "Boolean 可行行池上的确定性多起点交换；强制空行，2 个起点、每轮16个 proposal、patience=2。"),
        ("21. Synthetic validation", f"candidate_full-HILS 的跨预算 synthetic signed-F1 差为 {evidence['synthetic_delta']:.4f}。"),
        ("22. Random-design cloud", "每个预算24个随机可行设计；同时记录 objective、synthetic signed F1 与 Ishizawa macro F1。"),
        ("23. Objective/recovery alignment", f"跨全部随机设计 objective 对 real macro F1 的 Spearman rho={evidence['real_alignment_rho']:.3f}。"),
        ("24. Real Ishizawa Development results", table),
        ("25. Per-landscape heterogeneity", "所有7个 landscape、4个 Development seed 都保留；配对差异见 figures/per_landscape_delta.png。"),
        ("26. Guardrails", "主比较按 landscape-macro signed F1；同时报告 precision、recall、FDR、sign flips，不能用单个 landscape 胜利替代总体证据。"),
        ("27. Díaz diagnostic", "Díaz 仍只作历史负向诊断；META1.6 未用其结果调 Pi、目标或搜索。"),
        ("28. Estimator-transfer analysis", "HILS 与 candidate_full 额外用 ElasticNet 重估；KKT 目标仍属于 Lasso，二者不被宣称为同一事件。"),
        ("29. Ablations", "A1 uniform；A2 D-opt；A3 hybrid_d50；A4 HILS；A5 去除 target/nuisance 不对称；A6 仅 target-aware mean；A7 不集成奇异失败；A8 full。DCD 单列。"),
        ("30. Scaling", "d=7/8 只做结构与单次评分计时，不把小规模结果外推为可扩展性证明。"),
        ("31. Selection-bias audit", "Pi、主指标、预算、开发 seed 和决策阈值在读取 Ishizawa 开发 F1 前冻结；真实 support frequency 未进入 Pi。"),
        ("32. Strongest evidence FOR novelty", "目标/干扰不对称、阶数平衡支持 Pi、奇异失败积分与 Boolean 行约束被放在同一个可计算目标中。"),
        ("33. Strongest evidence AGAINST novelty", "核心仍建立在经典 Lasso KKT/HILS 与行交换上；增量主要是问题特化组合，不是新的恢复定理。"),
        ("34. Strongest evidence FOR continuation", f"真实开发集 candidate_full-HILS 平均差={evidence['real_delta']:.4f}，并与 synthetic/随机云证据联合判断。"),
        ("35. Strongest evidence AGAINST continuation", "真实支持较稠密，预算远小于63列；目标概率下尾大量为零，限制了优化目标的分辨率。"),
        ("36. Final D-A/B/C/D decision", f"**{decision}**。D-A 要求真实差>=0.03、synthetic 差>0、real alignment rho>0.2；D-B/C/D 按脚本中的冻结分支判定。"),
        ("37. New reserve status", "未创建、未生成、未运行任何新 reserve；退役的505/606未被读取或再生。"),
        ("38. Exact next action", exact_next),
    ]
    return "# META1.6 Development Report\n\n" + "\n\n".join(f"## {heading}\n\n{body}" for heading, body in sections) + "\n"


def main() -> None:
    started = perf_counter()
    for path in (RAW, AGG, FIG):
        path.mkdir(parents=True, exist_ok=True)
    scenarios = make_support_ensemble(seed=SEARCH_SEED)
    support_ensemble_frame(scenarios).to_csv(RAW / "support_ensemble.csv", index=False)
    optimized, search_trials = build_designs(scenarios)
    design_rows, ident = design_and_identifiability(optimized, scenarios)
    design_rows.to_csv(RAW / "design_rows.csv", index=False)
    ident.to_csv(RAW / "identifiability.csv", index=False)
    synthetic = synthetic_runs(optimized, scenarios)
    synthetic.to_csv(RAW / "synthetic_runs.csv", index=False)
    phase = phase_diagram(optimized)
    phase.to_csv(AGG / "phase_diagram.csv", index=False)
    real, estimator_trials = real_runs(optimized)
    real.to_csv(RAW / "real_development_runs.csv", index=False)
    trials = pd.concat([search_trials, estimator_trials], ignore_index=True)
    trials.to_csv(RAW / "tuning_trials.csv", index=False)
    panel = load_ishizawa(ISHIZAWA)
    reference_frame = pd.read_csv(ROOT / "results" / "meta1" / "raw" / "support_reference.csv")
    references = {landscape.landscape_id: reference_from_frame(reference_frame, landscape.landscape_id) for landscape in panel.landscapes}
    cloud = random_cloud(scenarios, panel, references)
    cloud.to_csv(RAW / "random_design_cloud.csv", index=False)
    synthetic_summary = synthetic.groupby(["budget", "method"], as_index=False).agg(
        signed_f1=("signed_f1", "mean"), precision=("precision", "mean"), recall=("recall", "mean"), exact_recovery_rate=("exact_target_sign", "mean"), singular_fraction=("singular_fraction", "mean")
    )
    synthetic_summary.to_csv(AGG / "synthetic_summary.csv", index=False)
    baseline_summary = synthetic_summary[synthetic_summary.method.isin(["uniform", "D-opt", "hybrid_d50", "HILS", "DCD"])]
    baseline_summary.to_csv(AGG / "baseline_summary.csv", index=False)
    real_summary = real.groupby(["budget", "design_method", "estimator"], as_index=False).agg(
        primary_f1=("primary_f1", "mean"), precision=("precision", "mean"), recall=("recall", "mean"), empirical_fdr=("empirical_fdr", "mean"), sign_flips=("sign_flips", "mean"), response_rmse=("response_rmse", "mean")
    )
    real_summary.to_csv(AGG / "real_summary.csv", index=False)
    priors = prior_sensitivity(optimized)
    priors.to_csv(AGG / "prior_sensitivity.csv", index=False)
    scaling = scaling_audit()
    scaling.to_csv(RAW / "scaling.csv", index=False)
    objective_alignment = alignment(cloud)
    objective_alignment.to_csv(AGG / "objective_alignment.csv", index=False)
    write_figures(phase, synthetic, real, cloud, priors)
    decision, evidence = decision_from_results(real_summary, synthetic_summary, objective_alignment)
    (RESULT / "META1_6_DEVELOPMENT_REPORT.md").write_text(report_text(decision, evidence, real_summary, ident, objective_alignment), encoding="utf-8")
    manifest = {
        "phase": "META1.6",
        "decision": decision,
        "development_seeds": list(DEV_SEEDS),
        "retired_reserve_policy": "505/606 forbidden and not generated",
        "budgets": list(BUDGETS),
        "support_scenarios": len(scenarios),
        "runtime_seconds": perf_counter() - started,
        **evidence,
    }
    (RESULT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
