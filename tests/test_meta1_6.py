from __future__ import annotations

import numpy as np
import pytest

from interaction_structure.meta1.protocol import design_balanced_mask
from interaction_structure.meta1_6.baselines import dcd_baseline_score, hils_score
from interaction_structure.meta1_6.ensemble import make_support_ensemble
from interaction_structure.meta1_6.scoring import score_design
from interaction_structure.meta1_6.search import optimize_rows
from interaction_structure.meta1_6.simulation import simulate_recovery
from interaction_structure.meta1_6.structure import (
    and_dictionary,
    numerical_rank,
    partition_terms,
    residualize_targets,
    sparse_nullspace_diagnostics,
    structural_diagnostics,
    validate_development_seed,
)


def _scenarios():
    return make_support_ensemble(k_high_values=(2,), k_low_values=(2,), snr_values=(1.5,), replicates=2)


def test_boolean_and_dictionary_is_exact():
    matrix, terms = and_dictionary(6)
    assert matrix.shape == (64, 63)
    assert np.array_equal(matrix[7], ((7 & terms) == terms).astype(float))


def test_low_target_partition_is_21_plus_42():
    _, low, high = partition_terms(6)
    assert (len(low), len(high)) == (21, 42)


def test_rank_uses_explicit_relative_tolerance():
    matrix = np.diag([1.0, 1e-12])
    assert numerical_rank(matrix) == 1


def test_dense_nuisance_residualizer_annihilates_low_space():
    full, _ = and_dictionary(6)
    _, low, high = partition_terms(6)
    selected = full[np.asarray(design_balanced_mask(6, 24, 101))]
    residual = residualize_targets(selected, low, high)
    assert np.linalg.norm(selected[:, low].T @ residual) < 1e-7


def test_structural_diagnostics_report_singular_targets():
    diagnostics = structural_diagnostics(6, tuple(range(16)))
    assert diagnostics["rank_low"] <= 15
    assert diagnostics["residual_nullity"] >= 27


def test_sparse_nullspace_enumeration_is_bounded_and_deterministic():
    first = sparse_nullspace_diagnostics(6, tuple(range(16)), sampled_four_sets=16, seed=9)
    second = sparse_nullspace_diagnostics(6, tuple(range(16)), sampled_four_sets=16, seed=9)
    assert first == second and first["q4_tested"] == 16


def test_support_ensemble_is_reproducible_and_signed():
    left = _scenarios()
    right = _scenarios()
    assert left == right
    assert {sign for scenario in left for sign in scenario.signs} == {-1, 1}


def test_kkt_score_is_bounded_and_deterministic():
    masks = design_balanced_mask(6, 24, 101)
    first = score_design(masks, _scenarios(), draws=8, aggregator="robust")
    second = score_design(masks, _scenarios(), draws=8, aggregator="robust")
    assert first == second and 0.0 <= first.score <= 1.0


def test_singular_scenario_contributes_zero_instead_of_being_skipped():
    masks = tuple(range(16))
    integrated = score_design(masks, _scenarios(), draws=8, integrate_singular=True)
    assert integrated.singular_fraction > 0 and 0.0 in integrated.scenario_probabilities


def test_hils_wrapper_matches_full_event_mean():
    masks = design_balanced_mask(6, 24, 101)
    direct = score_design(masks, _scenarios(), target_only=False, aggregator="mean", draws=8).score
    assert hils_score(masks, _scenarios(), draws=8) == direct


def test_dcd_baseline_is_finite_and_deterministic():
    masks = design_balanced_mask(6, 24, 101)
    value = dcd_baseline_score(masks, _scenarios())
    assert np.isfinite(value) and value == dcd_baseline_score(masks, _scenarios())


def test_row_search_preserves_budget_and_empty_row():
    result = optimize_rows(6, 8, lambda masks: float(sum(masks)), seed=19, restarts=1, proposals_per_round=4, patience=1)
    assert len(result.masks) == 8 and result.masks[0] == 0 and len(set(result.masks)) == 8


def test_synthetic_lasso_and_elastic_net_return_target_metrics():
    masks = design_balanced_mask(6, 24, 101)
    scenario = _scenarios()[0]
    assert "signed_f1" in simulate_recovery(masks, scenario, estimator="lasso")
    assert "signed_f1" in simulate_recovery(masks, scenario, estimator="elastic_net")


def test_retired_reserve_seeds_are_rejected_before_design_generation():
    validate_development_seed(101)
    with pytest.raises(ValueError):
        validate_development_seed(505)
    with pytest.raises(ValueError):
        validate_development_seed(606)
