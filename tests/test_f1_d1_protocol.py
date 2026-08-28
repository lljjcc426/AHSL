from __future__ import annotations

from pathlib import Path

import pytest

from vulnerability_repair.f1_d1.costs import CostLedger
from vulnerability_repair.f1_d1.firewall import GroundTruthLeakageError, build_agent_context, sanitize_generation_metadata
from vulnerability_repair.f1_d1.ledger import assert_evaluation_allowed
from vulnerability_repair.f1_d1.models import (
    AgentConfig,
    BenchmarkInstance,
    FailureClass,
    InstanceState,
    RepairBudget,
    StageStatus,
    VerificationStage,
)
from vulnerability_repair.f1_d1.paired import assert_same_backbone_and_budget
from vulnerability_repair.f1_d1.storage import PatchStore
from vulnerability_repair.f1_d1.taxonomy import classify_terminal
from vulnerability_repair.f1_d1.verifier import VerificationTrajectory, parse_official_result


def _instance(state: InstanceState = InstanceState.DEV_ACTIVE) -> BenchmarkInstance:
    return BenchmarkInstance("AutoPatchBench-Lite", "1", "p", "heap", "asan", "high", "vul:1", "fix:1", "development", state)


def _config(intervention: str = "baseline", calls: int = 2) -> AgentConfig:
    budget = RepairBudget(5, 2, calls, 100_000, 3600)
    return AgentConfig("codex-cli", "gpt-5.6-luna", "0.149.1", 0.0, "none", "workspace-write", "isolated-vulnerable", budget, intervention)


def test_instance_state_transitions_require_ordered_verification():
    trajectory = VerificationTrajectory()
    with pytest.raises(ValueError):
        trajectory.record(VerificationStage.V2, StageStatus.PASS)
    trajectory.record(VerificationStage.V0, StageStatus.PASS)
    trajectory.record(VerificationStage.V1, StageStatus.PASS)
    trajectory.record(VerificationStage.V2, StageStatus.PASS)


def test_patch_application_is_isolated_by_instance_and_run(tmp_path: Path):
    store = PatchStore(tmp_path)
    first = store.persist("i1", "r1", "patch one")
    second = store.persist("i2", "r1", "patch two")
    assert first.parent != second.parent and first.read_text() == "patch one"


def test_vulnerable_and_fixed_containers_must_be_distinct():
    with pytest.raises(ValueError):
        BenchmarkInstance("b", "1", "p", "c", "asan", "h", "same", "same", "dev", InstanceState.DEV_ACTIVE)


def test_ground_truth_patch_firewall_rejects_reference_keys():
    with pytest.raises(GroundTruthLeakageError):
        sanitize_generation_metadata({"project": "p", "fix_commit": "secret"})


def test_evaluator_only_signal_cannot_enter_agent_context():
    with pytest.raises(GroundTruthLeakageError):
        build_agent_context(source_summary="s", crash_report="c", evaluator_signals={"functionality_preserved": True})


def test_official_build_repro_fuzz_differential_status_parsing():
    trajectory = parse_official_result(
        {"patched_function_name_exists": True, "passed_qa_checks": True, "full_fuzzing_passed": True, "functionality_preserved": False}
    )
    assert trajectory.statuses[VerificationStage.V3] == StageStatus.PASS
    assert trajectory.statuses[VerificationStage.V4] == StageStatus.FAIL


def test_failure_taxonomy_is_deterministic():
    trajectory = parse_official_result(
        {"patched_function_name_exists": True, "passed_qa_checks": True, "full_fuzzing_passed": False}
    )
    assert classify_terminal(trajectory) == classify_terminal(trajectory) == FailureClass.F3


def test_token_and_cost_accounting_adds_exactly():
    total = CostLedger(prompt_tokens=10, completion_tokens=5, model_calls=1, model_cost_usd=0.2)
    total.add(CostLedger(prompt_tokens=3, completion_tokens=2, model_calls=1, model_cost_usd=0.1))
    assert total.total_tokens == 20 and total.model_calls == 2 and total.model_cost_usd == pytest.approx(0.3)


def test_same_budget_enforcement():
    with pytest.raises(ValueError):
        assert_same_backbone_and_budget(_config(), _config("mechanism", calls=3))


def test_baseline_candidate_configs_are_equal_except_intervention():
    assert_same_backbone_and_budget(_config(), _config("semantic_constraint"))


def test_untouched_pool_access_is_prohibited():
    with pytest.raises(PermissionError):
        assert_evaluation_allowed(_instance(InstanceState.UNTOUCHED))


def test_analysis_exposed_cases_are_excluded_from_unbiased_results():
    with pytest.raises(PermissionError):
        assert_evaluation_allowed(_instance(InstanceState.ANALYSIS_EXPOSED))
