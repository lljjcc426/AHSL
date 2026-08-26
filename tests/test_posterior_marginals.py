import networkx as nx
import numpy as np
from scipy.special import logsumexp

from ahsl.models.noise_likelihood import node_log_likelihoods
from ahsl.posterior_marginals import posterior_node_marginals
from ahsl.subtree import enumerate_connected_subtrees, generator_subtree_probability
from ahsl.trees import generate_tree


def _enumerated_posterior(tree, observed, false_negative, false_positive, q):
    log_zero, log_one, _ = node_log_likelihoods(
        observed, false_negative, false_positive
    )
    supports = []
    scores = []
    for support in enumerate_connected_subtrees(tree):
        prior = generator_subtree_probability(tree, support, q)
        if prior == 0.0:
            continue
        mask = np.zeros(tree.number_of_nodes(), dtype=bool)
        mask[list(support)] = True
        supports.append(mask)
        scores.append(
            np.log(prior)
            + log_one[:, mask].sum(axis=1)
            + log_zero[:, ~mask].sum(axis=1)
        )
    score_matrix = np.stack(scores, axis=1)
    probabilities = np.exp(score_matrix - logsumexp(score_matrix, axis=1, keepdims=True))
    return probabilities @ np.stack(supports), logsumexp(score_matrix, axis=1)


def test_all_node_marginals_match_enumeration_and_are_root_invariant():
    tree = nx.Graph([(0, 1), (1, 2), (1, 3), (3, 4), (3, 5)])
    observed = np.random.default_rng(8).integers(0, 2, size=(17, 6), dtype=np.int8)
    reference, log_evidence = _enumerated_posterior(tree, observed, 0.2, 0.3, 0.4)
    results = [posterior_node_marginals(tree, observed, 0.2, 0.3, 0.4, root=root) for root in range(6)]
    for result in results:
        np.testing.assert_allclose(result.node_marginals, reference, atol=2e-12)
        np.testing.assert_allclose(result.row_log_likelihoods, log_evidence, atol=2e-12)
    for result in results[1:]:
        np.testing.assert_allclose(result.node_marginals, results[0].node_marginals, atol=2e-12)


def test_marginals_cover_q_and_noise_boundaries():
    tree = nx.path_graph(5)
    clean = np.array([[1, 1, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 1, 0]], dtype=np.int8)
    cases = [
        (clean, 0.0, 0.0, 0.4),
        (clean, 0.0, 0.25, 0.4),
        (clean, 0.25, 0.0, 0.4),
        (clean, 0.2, 0.3, 0.0),
        (clean, 0.2, 0.3, 1.0),
    ]
    for observed, false_negative, false_positive, q in cases:
        reference, _ = _enumerated_posterior(
            tree, observed, false_negative, false_positive, q
        )
        result = posterior_node_marginals(
            tree, observed, false_negative, false_positive, q
        )
        np.testing.assert_allclose(result.node_marginals, reference, atol=2e-12)


def test_repeated_observations_match_enumeration_and_stay_in_unit_interval():
    tree = nx.star_graph(4)
    repeated = np.array(
        [
            [[1, 1, 0, 0, 0], [0, 1, 0, 1, 0]],
            [[1, 0, 0, 0, 0], [0, 1, 1, 1, 0]],
            [[1, 1, 0, 0, 0], [0, 1, 0, 1, 1]],
        ],
        dtype=np.int8,
    )
    reference, _ = _enumerated_posterior(tree, repeated, 0.2, 0.1, 0.6)
    result = posterior_node_marginals(tree, repeated, 0.2, 0.1, 0.6)
    np.testing.assert_allclose(result.node_marginals, reference, atol=2e-12)
    assert np.all((result.node_marginals >= 0.0) & (result.node_marginals <= 1.0))


def test_medium_random_tree_is_root_invariant():
    tree = generate_tree(64, "random", seed=91)
    observed = np.random.default_rng(92).integers(0, 2, size=(5, 64), dtype=np.int8)
    reference = posterior_node_marginals(tree, observed, 0.2, 0.2, 0.4, root=0)
    for root in [7, 31, 63]:
        result = posterior_node_marginals(tree, observed, 0.2, 0.2, 0.4, root=root)
        np.testing.assert_allclose(result.node_marginals, reference.node_marginals, atol=3e-12)
