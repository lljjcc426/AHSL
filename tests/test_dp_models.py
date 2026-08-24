import networkx as nx
import numpy as np

from ahsl.models import (
    DPNearestConnectedSubtree,
    DPNoiseAwareConnectedMLE,
    GeneratorPriorConnectedMAP,
    NoiseAwareIndependentMLE,
    NoiseAwareIndependentNonemptyMLE,
)
from ahsl.models.noise_likelihood import node_log_likelihoods
from ahsl.subtree import enumerate_connected_subtrees, subtree_incidence_matrix
from ahsl.synthetic import generate_alpha_acyclic_hypergraph
from ahsl.tree_dp import generator_subtree_probability
from ahsl.trees import SUPPORTED_TOPOLOGIES, generate_tree


def _canonical_brute(
    tree: nx.Graph, scores: list[tuple[float, frozenset[int]]]
) -> tuple[float, frozenset[int], bool]:
    best = max(score for score, _ in scores)
    optima = [nodes for score, nodes in scores if np.isclose(score, best)]
    chosen = min(optima, key=lambda nodes: (len(nodes), tuple(sorted(nodes))))
    return best, chosen, len(optima) > 1


def test_dp_hamming_matches_brute_force_on_repeated_observations() -> None:
    comparisons = 0
    for topology in SUPPORTED_TOPOLOGIES:
        for seed in range(25):
            m = 3 + seed % 6
            tree = generate_tree(m, topology, seed)
            rng = np.random.default_rng(seed + 200)
            observed = rng.integers(0, 2, size=(3, 4, m), dtype=np.int8)
            prediction = DPNearestConnectedSubtree(tree).fit(observed).predict()
            candidates = enumerate_connected_subtrees(tree)
            for row in range(4):
                scores = []
                for nodes in candidates:
                    mask = np.zeros(m, dtype=np.int8)
                    mask[list(nodes)] = 1
                    hamming = np.not_equal(mask[None, :], observed[:, row, :]).sum()
                    scores.append((-float(hamming), nodes))
                _, expected, _ = _canonical_brute(tree, scores)
                assert frozenset(np.flatnonzero(prediction[row])) == expected
                comparisons += 1
    assert comparisons == 400


def test_dp_noise_likelihood_matches_brute_force_across_noise_conditions() -> None:
    conditions = [(0.0, 0.0), (0.0, 0.2), (0.2, 0.0), (0.2, 0.2)]
    comparisons = 0
    for topology in SUPPORTED_TOPOLOGIES:
        tree = generate_tree(7, topology, seed=5)
        clean = generate_alpha_acyclic_hypergraph(8, 7, tree, 0.4, seed=7)[
            "incidence"
        ]
        for p_false_negative, p_false_positive in conditions:
            rng = np.random.default_rng(
                100 + int(10 * p_false_negative) + int(100 * p_false_positive)
            )
            observations = []
            for _ in range(3):
                draws = rng.random(clean.shape)
                noisy = clean.copy()
                noisy[(clean == 1) & (draws < p_false_negative)] = 0
                noisy[(clean == 0) & (draws < p_false_positive)] = 1
                observations.append(noisy)
            observed = np.stack(observations)
            model = DPNoiseAwareConnectedMLE(
                tree, p_false_negative, p_false_positive
            ).fit(observed)
            log_zero, log_one, _ = node_log_likelihoods(
                observed, p_false_negative, p_false_positive
            )
            candidates = enumerate_connected_subtrees(tree)
            for row in range(clean.shape[0]):
                scores = []
                for nodes in candidates:
                    selected = np.zeros(7, dtype=bool)
                    selected[list(nodes)] = True
                    score = float(
                        log_one[row, selected].sum()
                        + log_zero[row, ~selected].sum()
                    )
                    scores.append((score, nodes))
                best, expected, tied = _canonical_brute(tree, scores)
                assert np.isclose(model.row_objectives_[row], best)
                assert frozenset(np.flatnonzero(model.predict()[row])) == expected
                assert model.row_ties_[row] == tied
                comparisons += 1
    assert comparisons == 128


def test_zero_noise_connected_mle_recovers_clean_rows_exactly() -> None:
    tree = generate_tree(10, "random", 3)
    clean = generate_alpha_acyclic_hypergraph(30, 10, tree, 0.5, seed=4)[
        "incidence"
    ]
    prediction = DPNoiseAwareConnectedMLE(tree, 0.0, 0.0).fit(clean).predict()
    assert np.array_equal(prediction, clean)


def test_independent_mle_and_nonempty_repair_manual_example() -> None:
    observed = np.array([[0, 0, 1]], dtype=np.int8)
    independent = NoiseAwareIndependentMLE(0.2, 0.1).fit(observed).predict()
    assert np.array_equal(independent, observed)

    all_zero = np.zeros((1, 4), dtype=np.int8)
    nonempty = NoiseAwareIndependentNonemptyMLE(0.4, 0.4).fit(all_zero).predict()
    assert np.array_equal(nonempty, np.array([[1, 0, 0, 0]], dtype=np.int8))


def test_generator_prior_map_matches_brute_force() -> None:
    tree = generate_tree(6, "balanced", 0)
    observed = np.array([[1, 0, 1, 0, 0, 0]], dtype=np.int8)
    model = GeneratorPriorConnectedMAP(tree, 0.2, 0.2, 0.4).fit(observed)
    log_zero, log_one, _ = node_log_likelihoods(observed, 0.2, 0.2)
    scores = []
    for nodes in enumerate_connected_subtrees(tree):
        selected = np.zeros(6, dtype=bool)
        selected[list(nodes)] = True
        score = (
            log_one[0, selected].sum()
            + log_zero[0, ~selected].sum()
            + np.log(generator_subtree_probability(tree, nodes, 0.4))
        )
        scores.append((float(score), nodes))
    best, expected, _ = _canonical_brute(tree, scores)
    assert np.isclose(model.row_objectives_[0], best)
    assert frozenset(np.flatnonzero(model.predict()[0])) == expected

