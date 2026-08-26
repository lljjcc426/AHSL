import itertools

import networkx as nx
import numpy as np

from ahsl.models.noise_likelihood import node_log_likelihoods
from ahsl.posterior_decoders import (
    ConnectedBayesHamming,
    PosteriorMAPConnected,
    PosteriorMedianUnconstrained,
    posterior_hamming_risk,
)
from ahsl.posterior_marginals import posterior_node_marginals
from ahsl.subtree import enumerate_connected_subtrees, generator_subtree_probability


def _binary_actions(m):
    return [np.asarray(bits, dtype=np.int8) for bits in itertools.product([0, 1], repeat=m)]


def _connected_actions(tree):
    return [
        action
        for action in _binary_actions(tree.number_of_nodes())
        if action.any() and nx.is_connected(tree.subgraph(np.flatnonzero(action)))
    ]


def test_posterior_median_and_connected_mbr_match_exhaustive_risk():
    tree = nx.Graph([(0, 1), (1, 2), (1, 3), (3, 4)])
    marginals = np.array(
        [
            [0.9, 0.8, 0.2, 0.7, 0.1],
            [0.6, 0.4, 0.7, 0.3, 0.8],
            [0.5, 0.5, 0.1, 0.1, 0.1],
        ]
    )
    median = PosteriorMedianUnconstrained().fit(marginals)
    connected = ConnectedBayesHamming(tree).fit(marginals)
    all_actions = _binary_actions(5)
    connected_actions = _connected_actions(tree)
    for row in range(len(marginals)):
        all_risks = [posterior_hamming_risk(action[None, :], marginals[row : row + 1])[0] for action in all_actions]
        connected_risks = [posterior_hamming_risk(action[None, :], marginals[row : row + 1])[0] for action in connected_actions]
        assert np.isclose(median.row_posterior_risk_[row], min(all_risks))
        assert np.isclose(connected.row_posterior_risk_[row], min(connected_risks))
    np.testing.assert_array_equal(median.predict()[2], np.zeros(5, dtype=np.int8))


def test_posterior_map_matches_exhaustive_posterior_mode_including_boundaries():
    tree = nx.path_graph(5)
    observed = np.array([[1, 1, 0, 0, 0], [0, 1, 1, 1, 0]], dtype=np.int8)
    for q, false_negative, false_positive in [
        (0.0, 0.2, 0.3),
        (0.4, 0.2, 0.3),
        (1.0, 0.2, 0.3),
        (0.4, 0.0, 0.0),
    ]:
        decoded = PosteriorMAPConnected(
            tree, false_negative, false_positive, q
        ).fit(observed)
        log_zero, log_one, _ = node_log_likelihoods(
            observed, false_negative, false_positive
        )
        support_scores = []
        support_masks = []
        for support in enumerate_connected_subtrees(tree):
            prior = generator_subtree_probability(tree, support, q)
            if prior == 0.0:
                continue
            mask = np.zeros(5, dtype=np.int8)
            mask[list(support)] = 1
            selected = mask.astype(bool)
            support_masks.append(mask)
            support_scores.append(
                np.log(prior)
                + log_one[:, selected].sum(axis=1)
                + log_zero[:, ~selected].sum(axis=1)
            )
        scores = np.stack(support_scores, axis=1)
        masks = np.stack(support_masks)
        for row, prediction in enumerate(decoded.predict()):
            selected_score = scores[row, np.equal(masks, prediction).all(axis=1)][0]
            assert np.isclose(selected_score, scores[row].max())
        assert all(
            nx.is_connected(tree.subgraph(np.flatnonzero(row)))
            for row in decoded.predict()
        )


def test_risk_ties_and_decoder_outputs_are_deterministic():
    tree = nx.path_graph(4)
    marginals = np.full((2, 4), 0.5)
    median = PosteriorMedianUnconstrained().fit(marginals)
    first = ConnectedBayesHamming(tree).fit(marginals)
    second = ConnectedBayesHamming(tree).fit(marginals)
    np.testing.assert_array_equal(median.predict(), np.zeros((2, 4), dtype=np.int8))
    np.testing.assert_array_equal(first.predict(), second.predict())
    np.testing.assert_array_equal(first.predict()[:, 0], np.ones(2, dtype=np.int8))
    assert first.row_ties_.all()
    np.testing.assert_allclose(
        posterior_hamming_risk(np.array([[1, 0]], dtype=np.int8), np.array([[0.8, 0.3]])),
        np.array([0.25]),
    )
