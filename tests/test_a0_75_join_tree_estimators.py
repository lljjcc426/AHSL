import networkx as nx
import numpy as np
import pytest

from ahsl.join_tree_estimators import (
    BinaryMWST,
    BootstrapStabilityMWST,
    DataAgnosticRandomTree,
    NoiseCorrectedMWST,
    noise_corrected_intersection_weights,
)
from ahsl.join_tree_recovery import IntersectionMWSTJoinTree


def _noisy_repetitions(
    clean: np.ndarray,
    p_false_negative: float,
    p_false_positive: float,
    repetitions: int,
    rng: np.random.Generator,
) -> np.ndarray:
    draws = rng.random((repetitions, *clean.shape))
    clean_stack = np.broadcast_to(clean, draws.shape)
    observed = clean_stack.copy()
    observed[(clean_stack == 1) & (draws < p_false_negative)] = 0
    observed[(clean_stack == 0) & (draws < p_false_positive)] = 1
    return observed.astype(np.int8)


@pytest.mark.parametrize(
    ("p_false_negative", "p_false_positive", "repetitions"),
    [(0.2, 0.2, 1), (0.2, 0.2, 5), (0.3, 0.1, 1), (0.3, 0.1, 5)],
)
def test_corrected_intersections_are_monte_carlo_unbiased(
    p_false_negative: float,
    p_false_positive: float,
    repetitions: int,
) -> None:
    clean = np.array(
        [
            [1, 1, 0, 0],
            [1, 0, 1, 0],
            [0, 1, 1, 0],
            [1, 1, 1, 0],
            [0, 0, 1, 1],
        ],
        dtype=np.int8,
    )
    expected = clean.T @ clean
    np.fill_diagonal(expected, 0)
    rng = np.random.default_rng(701 + repetitions)
    estimates = np.zeros((2500, clean.shape[1], clean.shape[1]))
    for index in range(len(estimates)):
        observed = _noisy_repetitions(
            clean,
            p_false_negative,
            p_false_positive,
            repetitions,
            rng,
        )
        estimates[index] = noise_corrected_intersection_weights(
            observed if repetitions > 1 else observed[0],
            p_false_negative,
            p_false_positive,
        )
    assert np.allclose(estimates.mean(axis=0), expected, atol=0.12)


def test_zero_noise_corrected_weights_and_tree_equal_clean_mwst() -> None:
    clean = np.array(
        [[1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 1, 1]], dtype=np.int8
    )
    weights = noise_corrected_intersection_weights(clean, 0.0, 0.0)
    expected = clean.T @ clean
    np.fill_diagonal(expected, 0)
    assert np.array_equal(weights, expected)
    corrected = NoiseCorrectedMWST(0.0, 0.0).fit(clean).predict_tree()
    classical = IntersectionMWSTJoinTree().fit(clean).predict_tree()
    assert sorted(corrected.edges()) == sorted(classical.edges())


def test_corrected_mwst_is_deterministic_tree_and_supports_negative_weights() -> None:
    observed = np.array(
        [[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 0]], dtype=np.int8
    )
    first = NoiseCorrectedMWST(0.2, 0.2).fit(observed)
    second = NoiseCorrectedMWST(0.2, 0.2).fit(observed)
    upper_triangle = first.intersection_weights_[np.triu_indices(4, 1)]
    assert upper_triangle.min() < 0.0
    assert nx.is_tree(first.predict_tree())
    assert sorted(first.predict_tree().edges()) == sorted(second.predict_tree().edges())


def test_degenerate_noise_channel_is_rejected() -> None:
    with pytest.raises(ValueError, match="delta is zero"):
        NoiseCorrectedMWST(0.7, 0.3).fit(np.zeros((3, 4), dtype=np.int8))


def test_bootstrap_stability_is_deterministic_and_bounded() -> None:
    observed = np.random.default_rng(4).integers(0, 2, size=(20, 7), dtype=np.int8)
    first = BootstrapStabilityMWST(0.2, 0.2, 100, seed=9).fit(observed)
    second = BootstrapStabilityMWST(0.2, 0.2, 100, seed=9).fit(observed)
    assert nx.is_tree(first.predict_tree())
    assert np.array_equal(first.edge_frequencies_, second.edge_frequencies_)
    assert np.all((first.edge_frequencies_ >= 0.0) & (first.edge_frequencies_ <= 1.0))
    assert sorted(first.predict_tree().edges()) == sorted(second.predict_tree().edges())


def test_data_agnostic_random_tree_does_not_depend_on_observation_values() -> None:
    zeros = np.zeros((10, 8), dtype=np.int8)
    ones = np.ones((10, 8), dtype=np.int8)
    first = DataAgnosticRandomTree(8, seed=51).fit(zeros).predict_tree()
    second = DataAgnosticRandomTree(8, seed=51).fit(ones).predict_tree()
    assert nx.is_tree(first)
    assert sorted(first.edges()) == sorted(second.edges())


def test_binary_sources_can_be_recorded_without_duplicate_evidence() -> None:
    observed = np.random.default_rng(10).integers(0, 2, size=(12, 6), dtype=np.int8)
    direct = BinaryMWST(0.2, 0.2, "observed").fit(observed)
    independent = BinaryMWST(0.2, 0.2, "independent_mle").fit(observed)
    assert np.array_equal(direct.binary_incidence_, independent.binary_incidence_)
    assert sorted(direct.predict_tree().edges()) == sorted(independent.predict_tree().edges())

