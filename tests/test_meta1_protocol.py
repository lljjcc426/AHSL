from __future__ import annotations

import inspect

import numpy as np

from interaction_structure.meta1.data import Landscape
from interaction_structure.meta1.estimand import build_reference_estimand, mobius_matrix, zeta_matrix
from interaction_structure.meta1.evaluation import signed_support_metrics
from interaction_structure.meta1.methods import fit_lasso
from interaction_structure.meta1.protocol import AcquisitionState, EvaluationOracle, design_balanced_mask, make_measurement_masks, reveal


def synthetic_landscape(dimension: int = 3) -> Landscape:
    replicates = {mask: np.asarray([1.0 + mask, 1.1 + mask, 0.9 + mask]) for mask in range(1 << dimension)}
    return Landscape("synthetic", "synthetic_1", tuple(f"x{i}" for i in range(dimension)), replicates, "test", {})


def test_community_bitmask_encoding_decoding() -> None:
    for mask in range(256):
        assert int(format(mask, "08b"), 2) == mask


def test_factorial_cell_completeness() -> None:
    landscape = synthetic_landscape(4)
    assert landscape.n_cells == 16
    assert set(landscape.replicates) == set(range(16))


def test_mobius_inverse_consistency() -> None:
    values = np.arange(16, dtype=float) ** 2
    coefficients = mobius_matrix(4) @ values
    np.testing.assert_allclose(zeta_matrix(4) @ coefficients, values, atol=1e-10)


def test_revealed_panel_has_no_hidden_response_access() -> None:
    revealed = reveal(synthetic_landscape(), (0, 1, 3), "raw")
    assert len(revealed.replicates) == 3
    assert not hasattr(revealed, "complete_panel")
    assert not hasattr(revealed, "hidden_responses")


def test_adaptive_policy_interface_has_no_evaluation_oracle() -> None:
    state = AcquisitionState(3, (0, 1), (1.0, 2.0), (0.1, 0.2))
    assert not any(isinstance(value, EvaluationOracle) for value in (state.dimension, state.selected_masks, state.revealed_means, state.revealed_variances))
    assert tuple(inspect.signature(design_balanced_mask).parameters) == ("dimension", "budget", "seed")


def test_measurement_masks_are_deterministic() -> None:
    left = make_measurement_masks(64, (16, 32), (11, 23))
    right = make_measurement_masks(64, (16, 32), (11, 23))
    assert left.equals(right)


def test_replicate_bootstrap_is_seed_reproducible() -> None:
    landscape = synthetic_landscape()
    left = build_reference_estimand(landscape, scale="raw", n_bootstrap=50, seed=7)
    right = build_reference_estimand(landscape, scale="raw", n_bootstrap=50, seed=7)
    np.testing.assert_array_equal(left.support_sign, right.support_sign)
    np.testing.assert_allclose(left.lower, right.lower)


def test_signed_support_metrics_count_sign_flip_as_error() -> None:
    landscape = synthetic_landscape()
    reference = build_reference_estimand(landscape, scale="raw", n_bootstrap=50, seed=9)
    reference.support_sign[7] = 1
    coefficient = np.zeros(8)
    coefficient[7] = -1.0
    selected = np.abs(coefficient) > 0
    metrics = signed_support_metrics(reference, coefficient, selected)
    assert metrics["sign_flips"] == 1
    assert metrics["primary_f1"] == 0.0


def test_pure_hoi_requires_no_active_immediate_parent() -> None:
    landscape = synthetic_landscape()
    reference = build_reference_estimand(landscape, scale="raw", n_bootstrap=50, seed=5)
    reference.support_sign[:] = 0
    reference.support_sign[7] = 1
    assert reference.pure_high_order[7]
    reference.support_sign[3] = 1
    assert not reference.pure_high_order[7]


def test_model_tuning_interface_cannot_receive_reference_support() -> None:
    assert tuple(inspect.signature(fit_lasso).parameters) == ("panel", "seed")
    revealed = reveal(synthetic_landscape(), tuple(range(8)), "raw")
    fit = fit_lasso(revealed, seed=3)
    assert fit.trials
    assert all("support" not in key for trial in fit.trials for key in trial)
