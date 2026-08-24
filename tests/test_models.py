import numpy as np

from ahsl.acyclicity import running_intersection_violations
from ahsl.models import (
    FixedTreeAHSL,
    NearestConnectedSubtree,
    NoiseAwareMAPSubtree,
    UnconstrainedIncidence,
)
from ahsl.subtree import enumerate_connected_subtrees, subtree_incidence_matrix
from ahsl.trees import generate_tree


def _path_candidates(m: int) -> tuple[object, np.ndarray]:
    tree = generate_tree(m, "path", 0)
    candidates = subtree_incidence_matrix(enumerate_connected_subtrees(tree), m)
    return tree, candidates


def test_nearest_projection_is_connected() -> None:
    tree, candidates = _path_candidates(4)
    observed = np.array([[1, 0, 1, 0], [1, 0, 0, 1]], dtype=np.int8)
    prediction = NearestConnectedSubtree(candidates).fit(observed).predict()
    assert running_intersection_violations(prediction, tree)["num_violating_vertices"] == 0


def test_noise_aware_map_recovers_noise_free_connected_rows() -> None:
    _, candidates = _path_candidates(4)
    clean = np.array([[1, 1, 0, 0], [0, 1, 1, 1]], dtype=np.int8)
    prediction = NoiseAwareMAPSubtree(candidates, 0.0, 0.0).fit(clean).predict()
    assert np.array_equal(prediction, clean)


def test_symmetric_noise_map_matches_hamming_projection_with_repetitions() -> None:
    _, candidates = _path_candidates(5)
    observed = np.array(
        [
            [[1, 0, 1, 0, 0], [0, 1, 0, 1, 1]],
            [[1, 1, 0, 0, 0], [0, 1, 1, 0, 1]],
            [[1, 0, 1, 0, 0], [0, 0, 0, 1, 1]],
        ],
        dtype=np.int8,
    )
    projected = NearestConnectedSubtree(candidates).fit(observed).predict()
    mapped = NoiseAwareMAPSubtree(candidates, 0.2, 0.2).fit(observed).predict()
    assert np.array_equal(mapped, projected)


def test_fixed_tree_ahsl_discrete_predictions_are_always_connected() -> None:
    tree, candidates = _path_candidates(5)
    observed = np.array(
        [[1, 0, 1, 0, 0], [0, 1, 0, 1, 1], [1, 0, 0, 0, 1]], dtype=np.int8
    )
    prediction = FixedTreeAHSL(candidates, epochs=30, seed=8).fit(observed).predict()
    assert running_intersection_violations(prediction, tree)["num_violating_vertices"] == 0


def test_unconstrained_model_memorizes_binary_observation() -> None:
    observed = np.array([[1, 0, 1], [0, 1, 0]], dtype=np.int8)
    prediction = UnconstrainedIncidence(epochs=60, seed=2).fit(observed).predict()
    assert np.array_equal(prediction, observed)
