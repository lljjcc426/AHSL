import networkx as nx
import numpy as np
import pytest

from ahsl.corruption import corrupt_incidence
from ahsl.subtree import enumerate_connected_subtrees, generator_subtree_probability
from ahsl.subtree_marginal import (
    SubtreeMarginalLikelihood,
    brute_force_marginal_log_likelihood,
    marginal_log_likelihood,
    marginal_log_likelihood_from_node_logs,
)
from ahsl.models.noise_likelihood import node_log_likelihoods
from ahsl.synthetic import generate_alpha_acyclic_hypergraph
from ahsl.trees import generate_tree


@pytest.mark.parametrize("topology", ["path", "star", "balanced", "random"])
@pytest.mark.parametrize("q", [0.2, 0.4, 0.6, 0.8])
@pytest.mark.parametrize(
    ("p_false_negative", "p_false_positive"),
    [(0.0, 0.0), (0.2, 0.2), (0.3, 0.1)],
)
@pytest.mark.parametrize("repetitions", [1, 3])
def test_message_passing_matches_brute_force(
    topology: str,
    q: float,
    p_false_negative: float,
    p_false_positive: float,
    repetitions: int,
) -> None:
    m = 7
    seed = 1000 + repetitions + int(10 * q)
    tree = generate_tree(m, topology, seed)
    clean = generate_alpha_acyclic_hypergraph(
        n=5,
        m=m,
        tree=tree,
        branch_probability=q,
        seed=seed + 1,
    )["incidence"]
    draws = [
        corrupt_incidence(
            clean,
            p_false_negative=p_false_negative,
            p_false_positive=p_false_positive,
            seed=seed + 2 + repetition,
        )["corrupted_incidence"]
        for repetition in range(repetitions)
    ]
    observed = draws[0] if repetitions == 1 else np.stack(draws)
    exact = marginal_log_likelihood(
        tree, observed, p_false_negative, p_false_positive, q
    ).row_log_likelihoods
    reference = brute_force_marginal_log_likelihood(
        tree, observed, p_false_negative, p_false_positive, q
    )
    assert np.allclose(exact, reference, rtol=1e-12, atol=1e-12)


@pytest.mark.parametrize("topology", ["path", "star", "balanced", "random"])
@pytest.mark.parametrize("q", [0.02, 0.4, 0.98])
def test_anchor_growth_prior_normalizes(topology: str, q: float) -> None:
    tree = generate_tree(8, topology, seed=41)
    total = sum(
        generator_subtree_probability(tree, support, q)
        for support in enumerate_connected_subtrees(tree)
    )
    assert total == pytest.approx(1.0, abs=1e-12)


def test_anchor_posterior_normalizes_and_is_root_invariant() -> None:
    tree = nx.from_prufer_sequence([4, 0, 4, 2, 1])
    observed = np.random.default_rng(7).integers(0, 2, size=(9, 7), dtype=np.int8)
    first = SubtreeMarginalLikelihood(tree, 0.2, 0.1, 0.4).fit(observed)
    relabeled = nx.relabel_nodes(tree, {node: (node + 3) % 7 for node in tree.nodes})
    permuted = observed[:, np.argsort([(node + 3) % 7 for node in range(7)])]
    second = SubtreeMarginalLikelihood(relabeled, 0.2, 0.1, 0.4).fit(permuted)
    assert np.allclose(first.anchor_posterior().sum(axis=1), 1.0)
    assert first.log_likelihood_ == pytest.approx(second.log_likelihood_, abs=1e-12)

    log_zero, log_one, _ = node_log_likelihoods(observed, 0.2, 0.1)
    root_scores = [
        marginal_log_likelihood_from_node_logs(
            tree, log_zero, log_one, 0.4, root=root
        ).log_likelihood
        for root in range(7)
    ]
    assert np.allclose(root_scores, root_scores[0], rtol=1e-12, atol=1e-12)


@pytest.mark.parametrize("q", [0.0, 1.0])
def test_boundary_branch_probabilities_normalize(q: float) -> None:
    tree = generate_tree(7, "random", seed=92)
    total = sum(
        generator_subtree_probability(tree, support, q)
        for support in enumerate_connected_subtrees(tree)
    )
    assert total == pytest.approx(1.0, abs=1e-12)
