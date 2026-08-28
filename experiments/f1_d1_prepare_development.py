from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from vulnerability_repair.f1_d1.adapters import AutoPatchBenchAdapter
from vulnerability_repair.f1_d1.analysis import funnel_summary
from vulnerability_repair.f1_d1.ledger import write_csv
from vulnerability_repair.f1_d1.models import InstanceState
from vulnerability_repair.f1_d1.split import assert_project_disjoint, project_disjoint_split


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results" / "f1_d1"
RAW = RESULT / "raw"
AGG = RESULT / "aggregated"
AUTOPATCH_COMMIT = "4be64c3a24442b51c76175e6ec67722cc3f5fe38"
ANALYSIS_EXPOSED = {"10445"}
BLOCK_REASON = "container_runtime_unavailable_and_host_storage_below_official_minimum"


def _instance_rows(adapter: AutoPatchBenchAdapter) -> tuple[list[dict[str, object]], set[str], set[str]]:
    initial = []
    for instance_id in adapter.lite_ids():
        state = InstanceState.ANALYSIS_EXPOSED if str(instance_id) in ANALYSIS_EXPOSED else InstanceState.UNSEEN
        initial.append(adapter.instance(instance_id, pool_role="unassigned", state=state))
    development, untouched = project_disjoint_split(initial)
    assert_project_disjoint(initial, development, untouched)
    rows = []
    for instance in initial:
        if instance.instance_id in ANALYSIS_EXPOSED:
            pool_role, state, reason = "analysis_sanity", InstanceState.ANALYSIS_EXPOSED, "metadata_schema_inspected"
        elif instance.instance_id in development:
            pool_role, state, reason = "development", InstanceState.INFRA_BLOCKED, BLOCK_REASON
        else:
            pool_role, state, reason = "untouched", InstanceState.UNTOUCHED, "not_accessed"
        rows.append(
            {
                "benchmark": instance.benchmark,
                "benchmark_commit": AUTOPATCH_COMMIT,
                "instance_id": instance.instance_id,
                "project": instance.project,
                "crash_type": instance.crash_type,
                "sanitizer": instance.sanitizer,
                "severity": instance.severity,
                "total_files": instance.metadata["total_files"],
                "total_hunks": instance.metadata["total_hunks"],
                "max_hunk_length": instance.metadata["max_hunk_length"],
                "has_stacktrace": instance.metadata["has_stacktrace"],
                "pool_role": pool_role,
                "instance_state": state.value,
                "included_in_scientific_denominator": False,
                "exclusion_reason": reason,
            }
        )
    return rows, development, untouched


def _report(instances: pd.DataFrame) -> str:
    dev = instances[instances.pool_role == "development"]
    untouched = instances[instances.pool_role == "untouched"]
    projects = ", ".join(sorted(dev.project.unique()))
    crash_types = ", ".join(sorted(dev.crash_type.unique()))
    sections = [
        ("1. Executive decision", "**F1-D1-C（基础设施限定的歧义结论）**。研究对象和协议可执行化已完成，但当前主机无法启动 Linux 容器，且存储低于官方最小要求；因此没有把任何 F9 记录伪装成 repair failure，也没有声称存在 intervention signal。"),
        ("2. Exact research problem", "目标是以固定预算产生通过 build、原始 PoC、benchmark fuzzing 和 white-box differential verification 的 C/C++ 漏洞补丁；V4 是唯一主成功。"),
        ("3. Benchmark choice", "主基准为 AutoPatchBench-Lite；当前 artifact 的实际 Lite 列表为113例。Lite 只代表单 hunk root-cause 路线。"),
        ("4. AutoPatchBench setup", f"官方 PurpleLlama commit `{AUTOPATCH_COMMIT}` 已做 sparse checkout。官方要求 Podman/Linux、约2TB用于 Lite；当前 Windows 主机无 Docker/Podman，WSL2 报虚拟化不可用，E盘剩余约268GB。"),
        ("5. Secondary benchmark route", "SEC-Bench 支持 patch/poc 任务与 SWE-agent、OpenHands、Aider、smolagents，但要求 Python>=3.12、Docker 和>200GB。其正确性语义与 AutoPatchBench 的固定程序 differential verifier不同，只能作为后续独立安全修复路线。"),
        ("6. Agent/model access", "Codex CLI 0.149.1 使用 ChatGPT 登录可启动；gpt-5.6-luna ephemeral 只读探针最终返回 ACCESS_OK，但经历 WebSocket 超时和 HTTPS 回退。API key 型官方 reference agent 当前不可执行。"),
        ("7. Frozen baseline", "预注册候选 baseline 为 Codex CLI 0.149.1 + gpt-5.6-luna，同一 vulnerable-container workspace；每实例1条 outer trajectory、1个候选补丁、3600秒，plugins disabled、ephemeral。CLI 不暴露 sampling temperature 或硬 token cap，因此记录实际 token，并以同一 trajectory/wall envelope 做配对。由于容器未通过 sanity，该配置尚未产生 scientific baseline。"),
        ("8. Development/untouched split", f"按 project 整组、固定 seed 20260828 生成：Development {len(dev)}例、{dev.project.nunique()}个项目；untouched {len(untouched)}例。10445 因 schema 审计标为 ANALYSIS-EXPOSED。"),
        ("9. Verification protocol", "V0 patch produced；V1 build；V2 original crash stopped；V3 benchmark fuzz；V4 differential behavior。任一失败终止后续阶段。"),
        ("10. Ground-truth firewall", "适配器不读取 `*-patch.json`，generation metadata 丢弃 fix/fix_commit；fixed container、differential label 和 reference state 只属于 EvaluationOracle。"),
        ("11. Infrastructure sanity", "未通过：无容器运行时、WSL2 虚拟化不可用、存储不足。因而 vulnerable build、crash reproduction、reference-patch evaluator sanity 和 final verifier 均未运行。"),
        ("12. Baseline repair success", "不可估计；科学分母为0。25个预注册 Development 实例均为 INFRA-BLOCKED，而非 agent failure。"),
        ("13. Verification funnel", "V0-V4 均无合格 trajectory；baseline_funnel.csv 明确记录每阶段25个 infrastructure-blocked。"),
        ("14. Failure taxonomy", "只有 F9 infrastructure 记录；不存在可用于方法选择的 F0-F8 分布。"),
        ("15. Semantic failure taxonomy", "未建立；没有 candidate patch 或 V3/V4 失败证据。"),
        ("16. Patch-pattern analysis", "未建立；patches.csv 为空，不能推断 guard、clamp 或 multi-location pattern。"),
        ("17. Project/crash-type heterogeneity", f"Development 项目：{projects}。crash 类型：{crash_types}。这里只是预注册覆盖，不是效果异质性。"),
        ("18. Current prior-art boundary", "AutoPatchBench 官方 reference agent只在 generation 时使用 build+原始 crash；其公开案例显示 V2 与完整正确性存在明显落差。"),
        ("19. ContraFix overlap", "ContraFix 已占据 failure-boundary mutation、crash/non-crash state differential、repair specification 和 skill reuse。当前没有基线机制证据，故未进行8-15篇候选机制深审。"),
        ("20. Selected mechanism", "未选择。基础设施 F9 不能支持 M1/M2/M3 任一科学机制。"),
        ("21. Intervention 1", "未运行；禁止在真实 failure taxonomy 前设计。"),
        ("22. Intervention 2", "未运行。"),
        ("23. Intervention 3 if needed", "未运行。"),
        ("24. Same-backbone comparisons", "协议与测试已实现，但没有 paired outcome。"),
        ("25. Fully verified success", "NA；不能把0/0写成0%。"),
        ("26. V2->V4 promotion", "NA；无 V2-valid patch。"),
        ("27. Guardrails", "build、repro、fuzz、differential、tests、patch size 和修复成本均未产生；基础设施阻塞率为100%（25/25 Development）。"),
        ("28. Cost analysis", "repair model calls/tokens/cost为0。agent access probe使用1次 ephemeral 调用、6366 tokens，不属于 baseline。"),
        ("29. Agent stochasticity", "未估计；没有 baseline trajectory。"),
        ("30. Mechanism analysis", "未进行；不存在合法 failure evidence。"),
        ("31. Conditional regime analysis", "未定义；不能以未来 candidate 胜负定义 regime。"),
        ("32. Failure cases", "25例均为环境阻塞，详见 instances.csv；不计为科学失败。"),
        ("33. Selection-bias audit", "Development split只使用 project/crash/sanitizer和补丁规模元数据，不使用修复结果。没有读取 untouched outcome。"),
        ("34. Strongest evidence FOR continuation", "官方 benchmark 明确存在 crash-stopping 到完整验证的语义缺口；当前协议和113例 project-disjoint split 已可复现。"),
        ("35. Strongest evidence AGAINST continuation", "本机无法运行任何 V1-V4，agent transport probe也不稳定；当前没有真实 Development leverage 证据。"),
        ("36. Publication-shape assessment", "尚不能判断；benchmark/failure-study或方法论文均无数据支撑。"),
        ("37. F1-D1-A/B/C/D classification", "**F1-D1-C**，仅表示一次有界基础设施澄清被授权；不是 intervention signal，也不是 F1-D1-D。"),
        ("38. Untouched-pool status", f"{len(untouched)}例保持 UNTOUCHED；未构建镜像、未运行 agent、未读取 evaluator outcome。"),
        ("39. Exact next action", "在具备 x86-64 Linux、Podman/Docker、至少500GB可用空间的主机上，先运行2-3个 ANALYSIS-EXPOSED sanity case；通过后才对25例 Development 启动同骨干 baseline。"),
    ]
    return "# F1-D1 Development Report\n\n" + "\n\n".join(f"## {name}\n\n{text}" for name, text in sections) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--artifact-root",
        type=Path,
        default=ROOT.parent / "external" / "PurpleLlama" / "CybersecurityBenchmarks" / "datasets" / "autopatch",
    )
    args = parser.parse_args()
    adapter = AutoPatchBenchAdapter(args.artifact_root, AUTOPATCH_COMMIT)
    rows, development, untouched = _instance_rows(adapter)
    instances = pd.DataFrame(rows)
    RAW.mkdir(parents=True, exist_ok=True)
    AGG.mkdir(parents=True, exist_ok=True)
    instances.to_csv(RAW / "instances.csv", index=False)

    run_columns = [
        "run_id", "benchmark", "instance_id", "project", "crash_type", "agent", "model", "method", "method_variant", "seed",
        "repair_budget", "attempt_index", "patch_hash", "build_pass", "repro_pass", "fuzz_pass", "differential_pass", "test_pass",
        "terminal_stage", "failure_taxonomy", "tokens", "model_calls", "runtime", "patch_lines", "files_changed", "notes",
    ]
    agent_runs = []
    stages = []
    costs = []
    failures = []
    for row in rows:
        if row["pool_role"] != "development":
            continue
        run_id = f"F1-INFRA-{row['instance_id']}"
        agent_runs.append(
            {
                "run_id": run_id,
                "benchmark": "AutoPatchBench-Lite",
                "instance_id": row["instance_id"],
                "project": row["project"],
                "crash_type": row["crash_type"],
                "agent": "NOT_RUN",
                "model": "NOT_RUN",
                "method": "infrastructure_preflight",
                "method_variant": "container_runtime_check",
                "seed": "",
                "repair_budget": "0",
                "attempt_index": 0,
                "patch_hash": "",
                "build_pass": "",
                "repro_pass": "",
                "fuzz_pass": "",
                "differential_pass": "",
                "test_pass": "",
                "terminal_stage": "INFRA",
                "failure_taxonomy": "F9_INFRASTRUCTURE",
                "tokens": 0,
                "model_calls": 0,
                "runtime": 0.0,
                "patch_lines": 0,
                "files_changed": 0,
                "notes": BLOCK_REASON,
            }
        )
        for stage in ("V0", "V1", "V2", "V3", "V4"):
            stages.append(
                {
                    "run_id": run_id,
                    "instance_id": row["instance_id"],
                    "stage": stage,
                    "status": "BLOCKED",
                    "included_in_scientific_denominator": False,
                    "reason": BLOCK_REASON,
                }
            )
        failures.append(
            {
                "run_id": run_id,
                "instance_id": row["instance_id"],
                "failure_taxonomy": "F9_INFRASTRUCTURE",
                "semantic_failure": "NOT_APPLICABLE",
                "patch_pattern": "NOT_APPLICABLE",
                "included_in_scientific_denominator": False,
                "reason": BLOCK_REASON,
            }
        )
        costs.append(
            {
                "run_id": run_id,
                "instance_id": row["instance_id"],
                "model_calls": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "model_cost_usd": 0.0,
                "verifier_seconds": 0.0,
                "fuzz_seconds": 0.0,
                "wall_seconds": 0.0,
            }
        )
    write_csv(RAW / "agent_runs.csv", agent_runs, run_columns)
    write_csv(RAW / "verification_stages.csv", stages, ["run_id", "instance_id", "stage", "status", "included_in_scientific_denominator", "reason"])
    write_csv(RAW / "patches.csv", [], ["run_id", "instance_id", "patch_path", "patch_lines", "files_changed", "functions_changed", "patch_pattern", "analysis_exposed_after_scoring"])
    write_csv(RAW / "costs.csv", costs, ["run_id", "instance_id", "model_calls", "prompt_tokens", "completion_tokens", "total_tokens", "model_cost_usd", "verifier_seconds", "fuzz_seconds", "wall_seconds"])
    write_csv(RAW / "failure_taxonomy.csv", failures, ["run_id", "instance_id", "failure_taxonomy", "semantic_failure", "patch_pattern", "included_in_scientific_denominator", "reason"])
    write_csv(RAW / "intervention_runs.csv", [], run_columns + ["intervention", "paired_control_run_id"])

    stage_frame = pd.DataFrame(stages)
    funnel_summary(stage_frame).to_csv(AGG / "baseline_funnel.csv", index=False)
    pd.DataFrame([{"failure_taxonomy": "F9_INFRASTRUCTURE", "count": len(development), "scientific_count": 0}]).to_csv(AGG / "failure_summary.csv", index=False)
    write_csv(AGG / "patch_pattern_summary.csv", [], ["patch_pattern", "count", "v2_pass", "v4_pass", "v4_given_v2"])
    write_csv(AGG / "intervention_summary.csv", [], ["intervention", "instances", "v4_rate", "paired_wins", "paired_losses", "net_rescued", "cost_delta"])
    dev_frame = instances[instances.pool_role == "development"]
    dev_frame.groupby("project", as_index=False).agg(instances=("instance_id", "count")).assign(infrastructure_blocked=lambda frame: frame.instances).to_csv(AGG / "project_summary.csv", index=False)
    dev_frame.groupby("crash_type", as_index=False).agg(instances=("instance_id", "count")).assign(infrastructure_blocked=lambda frame: frame.instances).to_csv(AGG / "crash_type_summary.csv", index=False)
    pd.DataFrame([{"scope": "repair_baseline", "model_calls": 0, "tokens": 0, "model_cost_usd": 0.0, "verifier_seconds": 0.0, "fuzz_seconds": 0.0, "wall_seconds": 0.0}]).to_csv(AGG / "cost_summary.csv", index=False)
    (RESULT / "F1_D1_DEVELOPMENT_REPORT.md").write_text(_report(instances), encoding="utf-8")
    environment = {
        "autopatchbench_commit": AUTOPATCH_COMMIT,
        "lite_instances": len(instances),
        "development_instances": len(development),
        "untouched_instances": len(untouched),
        "analysis_exposed_instances": sorted(ANALYSIS_EXPOSED),
        "docker": "unavailable",
        "podman": "unavailable",
        "wsl2": "installed_but_virtualization_unavailable",
        "workspace_free_gb": 268.2,
        "official_lite_storage_guidance_gb": 2000,
        "classification": "F1-D1-C",
    }
    (RESULT / "environment_audit.json").write_text(json.dumps(environment, indent=2), encoding="utf-8")
    print(json.dumps(environment, indent=2))


if __name__ == "__main__":
    main()
