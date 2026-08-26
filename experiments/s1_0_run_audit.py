from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import Lasso
from sklearn.metrics import average_precision_score, precision_recall_curve

from interaction_structure.audits import heredity_classification
from interaction_structure.baselines.hierarchical import heredity_filtered_coefficients
from interaction_structure.baselines.sparse_regression import fit_lasso_grid, fit_omp, select_omp_sparsity
from interaction_structure.datasets.drug import context_stability, load_processed_tables
from interaction_structure.datasets.microbiome import STRAINS, focal_replicate_landscapes, load_raw_cfu
from interaction_structure.datasets.yeast import RAW_COLUMN, TAU_COLUMN, audit_counts, load_kuzmin
from interaction_structure.estimands.mobius import interaction_dictionary, mobius_transform, powerset
from interaction_structure.splits import gene_disjoint_split, overlap_audit, query_pair_disjoint_split, random_split
from interaction_structure.support_metrics import binary_support_metrics
from interaction_structure.uncertainty import bootstrap_mobius

SEED = 20260827
BOOTSTRAPS = 500
MICRO_LOG_MINIMUM = 0.10  # log10 CFU, about a 26% multiplicative change
BASELINE_ALPHAS = (1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1)
MATERIAL_F1 = 0.85
MATERIAL_MISS_RATE = 0.15


def _coefficient_metrics(
    truth_coefficients: np.ndarray,
    predicted_coefficients: np.ndarray,
    truth_support: np.ndarray,
) -> dict[str, float]:
    """Secondary effect metrics; support metrics remain the primary endpoint."""
    truth_coefficients = np.asarray(truth_coefficients, dtype=float)
    predicted_coefficients = np.asarray(predicted_coefficients, dtype=float)
    truth_support = np.asarray(truth_support, dtype=bool)
    k = int(truth_support.sum())
    top_k = np.argsort(np.abs(predicted_coefficients))[-k:] if k else np.asarray([], dtype=int)
    return {
        "signed_support_accuracy": float(
            np.mean(np.sign(predicted_coefficients[truth_support]) == np.sign(truth_coefficients[truth_support]))
        ) if k else np.nan,
        "coefficient_rmse": float(np.sqrt(np.mean((predicted_coefficients - truth_coefficients) ** 2))),
        "coefficient_mae": float(np.mean(np.abs(predicted_coefficients - truth_coefficients))),
        "top_k_precision": float(np.mean(truth_support[top_k])) if k else np.nan,
    }


def _mkdirs(root: Path) -> tuple[Path, Path]:
    raw = root / "raw"
    plots = root / "plots"
    raw.mkdir(parents=True, exist_ok=True)
    plots.mkdir(parents=True, exist_ok=True)
    return raw, plots


def _strong(point: float, lower: float, upper: float, minimum: float) -> str:
    if lower > 0 and abs(point) >= minimum:
        return "STRONG_POSITIVE"
    if upper < 0 and abs(point) >= minimum:
        return "STRONG_NEGATIVE"
    return "UNCERTAIN_OR_NULL"


def analyze_microbiome(source: Path, raw_dir: Path, plot_dir: Path) -> dict:
    frame = load_raw_cfu(source / "data1_rawcfu.csv")
    all_rows: list[dict] = []
    coefficients: dict[str, dict[str, dict]] = {scale: {} for scale in ("raw", "log10")}
    for scale in ("raw", "log10"):
        landscapes = focal_replicate_landscapes(frame, scale=scale)
        for focal, replicates in landscapes.items():
            universe = tuple(strain for strain in STRAINS if strain != focal)
            point = mobius_transform({key: float(np.mean(value)) for key, value in replicates.items()}, universe)
            boot = bootstrap_mobius(replicates, universe, n_bootstrap=BOOTSTRAPS, seed=SEED + STRAINS.index(focal))
            minimum = MICRO_LOG_MINIMUM if scale == "log10" else 0.10 * float(np.mean(replicates[frozenset()]))
            labels = {}
            for subset, value in point.items():
                lower, upper = np.quantile(boot[subset], [0.025, 0.975])
                label = _strong(value, lower, upper, minimum)
                labels[subset] = label
                all_rows.append(
                    {
                        "focal": focal,
                        "scale": scale,
                        "subset": "+".join(sorted(subset)) or "INTERCEPT",
                        "order": len(subset),
                        "coefficient": value,
                        "ci_lower": lower,
                        "ci_upper": upper,
                        "minimum_effect": minimum,
                        "label": label,
                    }
                )
            coefficients[scale][focal] = {"point": point, "labels": labels}
    coefficient_frame = pd.DataFrame(all_rows)
    coefficient_frame.to_csv(raw_dir / "microbiome_coefficients.csv", index=False)

    stability_rows = []
    for focal in STRAINS:
        left = coefficients["raw"][focal]
        right = coefficients["log10"][focal]
        terms = [term for term in left["point"] if len(term) >= 3]
        support_raw = {term for term in terms if left["labels"][term].startswith("STRONG")}
        support_log = {term for term in terms if right["labels"][term].startswith("STRONG")}
        overlap = support_raw & support_log
        union = support_raw | support_log
        k = min(len(support_raw), len(support_log))
        top_raw = set(sorted(terms, key=lambda x: abs(left["point"][x]), reverse=True)[:k])
        top_log = set(sorted(terms, key=lambda x: abs(right["point"][x]), reverse=True)[:k])
        stability_rows.append(
            {
                "focal": focal,
                "raw_support": len(support_raw),
                "log_support": len(support_log),
                "overlap": len(overlap),
                "jaccard": len(overlap) / len(union) if union else 1.0,
                "sign_agreement": float(np.mean([np.sign(left["point"][x]) == np.sign(right["point"][x]) for x in overlap])) if overlap else np.nan,
                "effect_rank_spearman": float(spearmanr([left["point"][x] for x in terms], [right["point"][x] for x in terms]).statistic),
                "top_k": k,
                "top_k_overlap": len(top_raw & top_log) / k if k else 1.0,
            }
        )
    stability = pd.DataFrame(stability_rows)
    stability.to_csv(raw_dir / "microbiome_estimand_stability.csv", index=False)

    heredity_rows = []
    for focal in STRAINS:
        item = coefficients["log10"][focal]
        active = {term for term, label in item["labels"].items() if label.startswith("STRONG")}
        for term in sorted(active, key=lambda x: (len(x), sorted(x))):
            if len(term) >= 3:
                heredity_rows.append(
                    {
                        "focal": focal,
                        "subset": "+".join(sorted(term)),
                        "order": len(term),
                        "label": item["labels"][term],
                        "heredity": heredity_classification(term, active),
                    }
                )
    heredity = pd.DataFrame(heredity_rows)
    heredity.to_csv(raw_dir / "microbiome_heredity.csv", index=False)

    baseline_rows = []
    curve_truth, curve_scores = [], []
    rng = np.random.default_rng(SEED)
    log_landscapes = focal_replicate_landscapes(frame, scale="log10")
    for focal in STRAINS:
        universe = tuple(strain for strain in STRAINS if strain != focal)
        observed_sets = powerset(universe)
        design, terms = interaction_dictionary(observed_sets, universe)
        response = np.asarray([np.mean(log_landscapes[focal][subset]) for subset in observed_sets])
        true_labels = coefficients["log10"][focal]["labels"]
        target = np.asarray([len(term) >= 3 and true_labels[term].startswith("STRONG") for term in terms])
        high_order = np.asarray([len(term) >= 3 for term in terms])
        pure = np.asarray([
            len(term) >= 3 and target[index] and heredity_classification(term, {t for t, label in true_labels.items() if label.startswith("STRONG")}) == "PURE_NON_HEREDITARY"
            for index, term in enumerate(terms)
        ])
        exact = mobius_transform(dict(zip(observed_sets, response, strict=True)), universe)
        exact_coef = np.asarray([exact[term] for term in terms])
        exact_metrics = binary_support_metrics(target[high_order], np.abs(exact_coef[high_order]), target[high_order])
        exact_effect_metrics = _coefficient_metrics(exact_coef[high_order], exact_coef[high_order], target[high_order])
        baseline_rows.append({"focal": focal, "budget": 64, "repeat": 0, "method": "exact_mobius", **exact_metrics, **exact_effect_metrics, "pure_recall": 1.0 if pure.any() else np.nan, "response_rmse": 0.0, "tuning": "none"})
        for budget in (16, 24, 32, 48):
            for repeat in range(5):
                sampled = rng.choice(len(observed_sets), size=budget, replace=False)
                split = max(2, int(round(0.8 * budget)))
                train_index, validation_index = sampled[:split], sampled[split:]
                lasso_fit = fit_lasso_grid(design[train_index], response[train_index], design[validation_index], response[validation_index], alphas=BASELINE_ALPHAS)
                lasso = Lasso(alpha=lasso_fit.alpha, fit_intercept=False, max_iter=20_000, selection="cyclic")
                lasso.fit(design[sampled], response[sampled])
                lasso_coef = lasso.coef_
                lasso_selected = np.abs(lasso_coef) > 1e-10
                metrics = binary_support_metrics(target[high_order], np.abs(lasso_coef[high_order]), lasso_selected[high_order])
                effect_metrics = _coefficient_metrics(exact_coef[high_order], lasso_coef[high_order], target[high_order])
                pure_recall = float(np.mean(lasso_selected[pure])) if pure.any() else np.nan
                rmse = float(np.sqrt(np.mean((design @ lasso_coef - response) ** 2)))
                baseline_rows.append({"focal": focal, "budget": budget, "repeat": repeat, "method": "lasso", **metrics, **effect_metrics, "pure_recall": pure_recall, "response_rmse": rmse, "tuning": f"alpha={lasso_fit.alpha:g}"})
                weak_coef = heredity_filtered_coefficients(lasso_coef, terms, rule="weak")
                weak_selected = np.abs(weak_coef) > 1e-10
                metrics = binary_support_metrics(target[high_order], np.abs(weak_coef[high_order]), weak_selected[high_order])
                effect_metrics = _coefficient_metrics(exact_coef[high_order], weak_coef[high_order], target[high_order])
                baseline_rows.append({"focal": focal, "budget": budget, "repeat": repeat, "method": "weak_heredity_lasso", **metrics, **effect_metrics, "pure_recall": float(np.mean(weak_selected[pure])) if pure.any() else np.nan, "response_rmse": float(np.sqrt(np.mean((design @ weak_coef - response) ** 2))), "tuning": f"alpha={lasso_fit.alpha:g}"})
                omp_sparsity, omp_val = select_omp_sparsity(design[train_index], response[train_index], design[validation_index], response[validation_index])
                omp_coef = fit_omp(design[sampled], response[sampled], nonzero_terms=omp_sparsity)
                omp_selected = np.abs(omp_coef) > 1e-10
                metrics = binary_support_metrics(target[high_order], np.abs(omp_coef[high_order]), omp_selected[high_order])
                effect_metrics = _coefficient_metrics(exact_coef[high_order], omp_coef[high_order], target[high_order])
                baseline_rows.append({"focal": focal, "budget": budget, "repeat": repeat, "method": "omp", **metrics, **effect_metrics, "pure_recall": float(np.mean(omp_selected[pure])) if pure.any() else np.nan, "response_rmse": float(np.sqrt(np.mean((design @ omp_coef - response) ** 2))), "tuning": f"sparsity={omp_sparsity};val_mse={omp_val:.6g}"})
                if budget == 32 and repeat == 0:
                    curve_truth.extend(target[high_order].tolist())
                    curve_scores.extend(np.abs(lasso_coef[high_order]).tolist())
    baselines = pd.DataFrame(baseline_rows)
    baselines.to_csv(raw_dir / "microbiome_classical_baselines.csv", index=False)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    shown = coefficient_frame[(coefficient_frame.scale == "log10") & (coefficient_frame.order >= 1)]
    for order, group in shown.groupby("order"):
        ax.boxplot(group.coefficient, positions=[order], widths=0.55, showfliers=False)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set(xlabel="interaction order", ylabel="Möbius coefficient (log10 CFU)", title="Complete microbial landscapes")
    fig.tight_layout(); fig.savefig(plot_dir / "01_interaction_order_effect_distribution.png", dpi=180); plt.close(fig)

    prevalence = shown.assign(strong=shown.label.str.startswith("STRONG")).groupby("order").strong.mean()
    fig, ax = plt.subplots(figsize=(7, 4)); prevalence.plot.bar(ax=ax, color="#4472C4")
    ax.set(ylabel="strong-support fraction", title="Support prevalence by order"); fig.tight_layout(); fig.savefig(plot_dir / "02_support_prevalence_by_order.png", dpi=180); plt.close(fig)

    matrix = np.asarray([[1.0, stability.jaccard.median()], [stability.jaccard.median(), 1.0]])
    fig, ax = plt.subplots(figsize=(4.5, 4)); im = ax.imshow(matrix, vmin=0, vmax=1, cmap="viridis")
    ax.set_xticks([0, 1], ["raw CFU", "log10 CFU"]); ax.set_yticks([0, 1], ["raw CFU", "log10 CFU"])
    for i in range(2):
        for j in range(2): ax.text(j, i, f"{matrix[i,j]:.2f}", ha="center", va="center", color="white")
    fig.colorbar(im, ax=ax); ax.set_title("Median strong-support Jaccard"); fig.tight_layout(); fig.savefig(plot_dir / "03_estimand_support_overlap.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4)); heredity.heredity.value_counts(normalize=True).plot.bar(ax=ax, color="#70AD47")
    ax.set(ylabel="fraction of strong order>=3 effects", title="Heredity audit"); fig.tight_layout(); fig.savefig(plot_dir / "04_heredity_violation_rate.png", dpi=180); plt.close(fig)

    precision, recall, _ = precision_recall_curve(np.asarray(curve_truth, bool), np.asarray(curve_scores, float))
    fig, ax = plt.subplots(figsize=(5, 4)); ax.plot(recall, precision); ax.set(xlabel="recall", ylabel="precision", title="Lasso support PR, budget 32"); fig.tight_layout(); fig.savefig(plot_dir / "06_classical_support_pr.png", dpi=180); plt.close(fig)

    agg = baselines[baselines.budget < 64].groupby(["budget", "method"])["f1"].mean().unstack()
    fig, ax = plt.subplots(figsize=(7, 4)); agg.plot(ax=ax, marker="o"); ax.axhline(MATERIAL_F1, color="black", linestyle="--", linewidth=0.8); ax.set(ylabel="support F1", title="Measurement budget versus recovery"); fig.tight_layout(); fig.savefig(plot_dir / "09_budget_vs_support_recovery.png", dpi=180); plt.close(fig)

    pure_plot = baselines[baselines.budget.eq(48)].groupby("method").pure_recall.mean()
    fig, ax = plt.subplots(figsize=(6, 4)); pure_plot.plot.bar(ax=ax, color="#ED7D31"); ax.set(ylabel="pure-HOI recall", title="Pure higher-order recovery, budget 48"); fig.tight_layout(); fig.savefig(plot_dir / "07_pure_hoi_performance.png", dpi=180); plt.close(fig)

    return {
        "measurements": int(len(frame)),
        "systems": int(frame["system"].nunique()),
        "replicate_range": [int(frame.groupby(["strain", "system"]).size().min()), int(frame.groupby(["strain", "system"]).size().max())],
        "strong_order_ge3_log": int(((coefficient_frame.scale == "log10") & (coefficient_frame.order >= 3) & coefficient_frame.label.str.startswith("STRONG")).sum()),
        "median_estimand_jaccard": float(stability.jaccard.median()),
        "median_sign_agreement": float(stability.sign_agreement.median()),
        "pure_fraction": float((heredity.heredity == "PURE_NON_HEREDITARY").mean()) if len(heredity) else np.nan,
        "weak_heredity_fraction": float((heredity.heredity != "PURE_NON_HEREDITARY").mean()) if len(heredity) else np.nan,
        "best_budget_48_f1": float(baselines[baselines.budget.eq(48)].groupby("method").f1.mean().max()),
        "best_budget_48_pure_recall": float(baselines[baselines.budget.eq(48)].groupby("method").pure_recall.mean().max()),
        "response_scale_gate": bool(stability.jaccard.median() >= 0.60 and stability.sign_agreement.median() >= 0.80),
    }


def analyze_yeast(source: Path, raw_dir: Path, plot_dir: Path) -> dict:
    all_rows = pd.read_csv(source / "AdditionalDataS1.tsv", sep="\t")
    triples = load_kuzmin(source / "AdditionalDataS1.tsv")
    summary = audit_counts(all_rows, triples)
    split_rows = []
    train, test = random_split(len(triples))
    split_rows.append({"split": "random_triple", **overlap_audit(triples, train, test)})
    train, test, _ = gene_disjoint_split(triples)
    split_rows.append({"split": "gene_disjoint_any_held_gene", **overlap_audit(triples, train, test)})
    train, test = query_pair_disjoint_split(triples)
    split_rows.append({"split": "query_pair_disjoint", **overlap_audit(triples, train, test)})

    query_genes = np.unique(triples[["gene_1", "gene_2"]].to_numpy().ravel())
    rng = np.random.default_rng(SEED)
    held_query = set(rng.choice(query_genes, size=max(1, int(round(0.2 * len(query_genes)))), replace=False))
    membership = triples[["gene_1", "gene_2"]].isin(held_query).sum(axis=1)
    train = np.flatnonzero(membership.eq(0).to_numpy()); test = np.flatnonzero(membership.gt(0).to_numpy())
    split_rows.append({"split": "query_gene_disjoint", **overlap_audit(triples, train, test)})
    splits = pd.DataFrame(split_rows)
    splits.to_csv(raw_dir / "yeast_split_leakage.csv", index=False)

    baseline_rows = []
    for split_name in ("random_triple", "query_pair_disjoint"):
        if split_name == "random_triple": train, test = random_split(len(triples))
        else: train, test = query_pair_disjoint_split(triples)
        train_frame, test_frame = triples.iloc[train], triples.iloc[test]
        global_rate = float(train_frame["strong_negative_tau"].mean())
        rates = train_frame.groupby("query_pair")["strong_negative_tau"].mean()
        score = test_frame["query_pair"].map(rates).fillna(global_rate).to_numpy(float)
        truth = test_frame["strong_negative_tau"].to_numpy(bool)
        selected = score >= 0.05
        metrics = binary_support_metrics(truth, score, selected)
        baseline_rows.append({"split": split_name, "method": "query_pair_empirical_rate", **metrics, "prevalence": float(truth.mean())})
    yeast_baselines = pd.DataFrame(baseline_rows)
    yeast_baselines.to_csv(raw_dir / "yeast_classical_diagnostic.csv", index=False)

    fig, ax = plt.subplots(figsize=(8, 4)); plot = splits.set_index("split")[["test_with_any_gene_overlap", "test_with_any_pair_overlap"]]
    plot.plot.bar(ax=ax); ax.set(ylabel="test fraction", title="Yeast split leakage"); ax.legend(["any gene", "any pair"]); fig.tight_layout(); fig.savefig(plot_dir / "05_split_leakage_statistics.png", dpi=180); plt.close(fig)
    summary["split_rows"] = split_rows
    summary["query_baselines"] = baseline_rows
    return summary


def analyze_drug(source: Path, raw_dir: Path, plot_dir: Path) -> dict:
    frame = load_processed_tables(source)
    stability = context_stability(frame)
    stability.to_csv(raw_dir / "drug_context_stability.csv", index=False)
    counts = frame.groupby("order").agg(measurements=("drug_set", "size"), drug_sets=("drug_set", "nunique"), net_support=("net_support", "sum"), emergent_support=("emergent_support", "sum")).reset_index()
    counts.to_csv(raw_dir / "drug_order_counts.csv", index=False)
    context_summary = stability.groupby("order").agg(net_modal_fraction=("net_modal_fraction", "median"), emergent_modal_fraction=("emergent_modal_fraction", "median"), net_sign_flip_fraction=("net_sign_flip", "mean"), emergent_sign_flip_fraction=("emergent_sign_flip", "mean")).reset_index()
    context_summary.to_csv(raw_dir / "drug_context_summary.csv", index=False)
    fig, ax = plt.subplots(figsize=(7, 4)); context_summary.set_index("order")[["net_modal_fraction", "emergent_modal_fraction"]].plot.bar(ax=ax); ax.set(ylabel="median modal-label fraction", title="Dose-context structural stability"); fig.tight_layout(); fig.savefig(plot_dir / "08_effect_stability_across_dose.png", dpi=180); plt.close(fig)
    return {
        "measurements_order_3_to_5": int(len(frame)),
        "independent_drug_sets": int(frame["drug_set"].nunique()),
        "unique_drugs": int(len(set().union(*frame["drug_set"]))),
        "order_counts": counts.to_dict(orient="records"),
        "median_net_modal_fraction": float(stability.net_modal_fraction.median()),
        "median_emergent_modal_fraction": float(stability.emergent_modal_fraction.median()),
        "net_sign_flip_set_fraction": float(stability.net_sign_flip.mean()),
        "emergent_sign_flip_set_fraction": float(stability.emergent_sign_flip.mean()),
    }


def make_domain_comparison(micro: dict, yeast: dict, drug: dict, plot_dir: Path) -> None:
    rows = pd.DataFrame(
        [
            {"domain": "microbiome", "direct_identifiable": 1.0, "context_or_scale_stability": float(micro["median_estimand_jaccard"]), "classical_residual": 1.0 - float(micro["best_budget_48_f1"])},
            {"domain": "yeast", "direct_identifiable": 1.0, "context_or_scale_stability": float(yeast["tau_raw_support_jaccard"]), "classical_residual": 1.0 - float(yeast["query_baselines"][1]["f1"])},
            {"domain": "drug", "direct_identifiable": 1.0, "context_or_scale_stability": float(drug["median_emergent_modal_fraction"]), "classical_residual": np.nan},
        ]
    ).set_index("domain")
    fig, ax = plt.subplots(figsize=(7, 4)); rows.plot.bar(ax=ax); ax.set_ylim(0, 1); ax.set(title="Decision diagnostics by domain", ylabel="fraction / residual"); fig.tight_layout(); fig.savefig(plot_dir / "10_baseline_comparison_by_domain.png", dpi=180); plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--yeast", type=Path, required=True)
    parser.add_argument("--microbiome", type=Path, required=True)
    parser.add_argument("--drug", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("results/s1_0"))
    args = parser.parse_args()
    raw_dir, plot_dir = _mkdirs(args.output)
    micro = analyze_microbiome(args.microbiome, raw_dir, plot_dir)
    yeast = analyze_yeast(args.yeast, raw_dir, plot_dir)
    drug = analyze_drug(args.drug, raw_dir, plot_dir)
    make_domain_comparison(micro, yeast, drug, plot_dir)
    summary = {
        "frozen_thresholds": {
            "microbiome_log_minimum": MICRO_LOG_MINIMUM,
            "bootstrap_confidence": 0.95,
            "bootstraps": BOOTSTRAPS,
            "estimand_jaccard": 0.60,
            "sign_agreement": 0.80,
            "classical_sufficiency_f1": MATERIAL_F1,
            "material_miss_rate": MATERIAL_MISS_RATE,
            "yeast_p": 0.05,
            "yeast_tau": -0.08,
        },
        "microbiome": micro,
        "yeast": yeast,
        "drug": drug,
    }
    (raw_dir / "s1_0_summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
