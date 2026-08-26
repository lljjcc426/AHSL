"""Bayes actions under exact-support and nodewise Hamming losses."""

from __future__ import annotations

import networkx as nx
import numpy as np

from ahsl.models import GeneratorPriorConnectedMAP
from ahsl.models.noise_likelihood import node_log_likelihoods
from ahsl.subtree import enumerate_connected_subtrees, generator_subtree_probability
from ahsl.subtree_marginal import _sum_except
from ahsl.tree_dp import maximum_weight_connected_subtree
from ahsl.trees import validate_labeled_tree


def posterior_hamming_risk(
    prediction: np.ndarray, node_marginals: np.ndarray
) -> np.ndarray:
    """Posterior expected nodewise Hamming loss, normalized by row width."""
    action = np.asarray(prediction, dtype=np.int8)
    marginals = np.asarray(node_marginals, dtype=float)
    if action.shape != marginals.shape:
        raise ValueError("prediction and node_marginals must have the same shape")
    losses = np.where(action == 1, 1.0 - marginals, marginals)
    return losses.mean(axis=1)


class PosteriorMedianUnconstrained:
    """Coordinatewise posterior median; ties at one half are set to zero."""

    name = "PosteriorMedianUnconstrained"

    def fit(self, node_marginals: np.ndarray) -> "PosteriorMedianUnconstrained":
        marginals = np.asarray(node_marginals, dtype=float)
        if marginals.ndim != 2:
            raise ValueError("node_marginals must have shape (n, m)")
        self.node_marginals_ = marginals.copy()
        self.prediction_ = (marginals > 0.5).astype(np.int8)
        self.row_ties_ = np.any(np.isclose(marginals, 0.5, atol=1e-12, rtol=1e-12), axis=1)
        self.row_posterior_risk_ = posterior_hamming_risk(self.prediction_, marginals)
        return self

    def predict(self) -> np.ndarray:
        return self.prediction_.copy()


class ConnectedBayesHamming:
    """Exact non-empty connected Bayes action for nodewise Hamming loss."""

    name = "ConnectedBayesHamming"

    def __init__(self, tree: nx.Graph) -> None:
        self.tree = tree.copy()
        self.m = validate_labeled_tree(self.tree)

    def fit(self, node_marginals: np.ndarray) -> "ConnectedBayesHamming":
        marginals = np.asarray(node_marginals, dtype=float)
        if marginals.ndim != 2 or marginals.shape[1] != self.m:
            raise ValueError("node_marginals must have shape (n, m)")
        n = marginals.shape[0]
        prediction = np.zeros((n, self.m), dtype=np.int8)
        objectives = np.empty(n, dtype=float)
        ties = np.zeros(n, dtype=bool)
        for row in range(n):
            result = maximum_weight_connected_subtree(
                self.tree, 2.0 * marginals[row] - 1.0
            )
            prediction[row, list(result["selected_nodes"])] = 1
            objectives[row] = float(result["objective"])
            ties[row] = bool(result["has_tie"])
        self.node_marginals_ = marginals.copy()
        self.prediction_ = prediction
        self.row_objectives_ = objectives
        self.row_ties_ = ties
        self.row_posterior_risk_ = posterior_hamming_risk(prediction, marginals)
        return self

    def predict(self) -> np.ndarray:
        return self.prediction_.copy()


class PosteriorMAPConnected:
    """Posterior MAP connected support, including the q=0 and q=1 limits."""

    name = "PosteriorMAPConnected"

    def __init__(
        self,
        tree: nx.Graph,
        p_false_negative: float,
        p_false_positive: float,
        branch_probability: float,
    ) -> None:
        self.tree = tree.copy()
        self.m = validate_labeled_tree(self.tree)
        if not 0.0 <= branch_probability <= 1.0:
            raise ValueError("branch_probability must lie in [0, 1]")
        self.p_false_negative = p_false_negative
        self.p_false_positive = p_false_positive
        self.branch_probability = float(branch_probability)

    def fit(self, observed: np.ndarray) -> "PosteriorMAPConnected":
        q = self.branch_probability
        log_zero, log_one, _ = node_log_likelihoods(
            observed, self.p_false_negative, self.p_false_positive
        )
        n = log_zero.shape[0]
        if q == 1.0:
            self.prediction_ = np.ones((n, self.m), dtype=np.int8)
            self.row_ties_ = np.zeros(n, dtype=bool)
            self.row_objectives_ = log_one.sum(axis=1)
            return self
        if q == 0.0:
            excluded_zero = _sum_except([log_zero[:, node] for node in range(self.m)])
            scores = np.stack(
                [
                    -np.log(self.m) + log_one[:, node] + excluded_zero[node]
                    for node in range(self.m)
                ],
                axis=1,
            )
            prediction = np.zeros((n, self.m), dtype=np.int8)
            ties = np.zeros(n, dtype=bool)
            for row in range(n):
                best = np.max(scores[row])
                candidates = np.flatnonzero(
                    np.isclose(scores[row], best, atol=1e-12, rtol=1e-12)
                )
                prediction[row, int(candidates[0])] = 1
                ties[row] = len(candidates) > 1
            self.prediction_ = prediction
            self.row_ties_ = ties
            self.row_objectives_ = scores.max(axis=1)
            return self
        if 0.0 < q < 1.0 and np.isfinite(log_zero).all() and np.isfinite(log_one).all():
            delegate = GeneratorPriorConnectedMAP(
                self.tree,
                self.p_false_negative,
                self.p_false_positive,
                q,
            ).fit(observed)
            self.prediction_ = delegate.predict()
            self.row_ties_ = delegate.row_ties_.copy()
            self.row_objectives_ = delegate.row_objectives_.copy()
            return self

        # Boundary q or deterministic noise creates exact zero likelihoods.
        # Enumeration is only the small-tree reference path; the primary
        # interior-noise experiment always uses the polynomial DP above.
        supports = []
        for support in enumerate_connected_subtrees(self.tree):
            prior = generator_subtree_probability(self.tree, support, q)
            if prior > 0.0:
                supports.append((tuple(sorted(support)), np.log(prior)))
        prediction = np.zeros((n, self.m), dtype=np.int8)
        objectives = np.empty(n, dtype=float)
        ties = np.zeros(n, dtype=bool)
        scores = np.empty((n, len(supports)), dtype=float)
        for index, (support, log_prior) in enumerate(supports):
            mask = np.zeros(self.m, dtype=bool)
            mask[list(support)] = True
            scores[:, index] = (
                log_prior
                + log_one[:, mask].sum(axis=1)
                + log_zero[:, ~mask].sum(axis=1)
            )
        for row in range(n):
            best = np.max(scores[row])
            candidates = [
                index
                for index, score in enumerate(scores[row])
                if np.isclose(score, best, atol=1e-12, rtol=1e-12)
            ]
            chosen = min(candidates, key=lambda index: (len(supports[index][0]), supports[index][0]))
            prediction[row, list(supports[chosen][0])] = 1
            objectives[row] = best
            ties[row] = len(candidates) > 1
        self.prediction_ = prediction
        self.row_ties_ = ties
        self.row_objectives_ = objectives
        return self

    def predict(self) -> np.ndarray:
        return self.prediction_.copy()
