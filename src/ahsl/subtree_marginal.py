"""Exact marginal likelihood for the anchor-growth connected-subtree model."""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx
import numpy as np
from scipy.special import logsumexp

from ahsl.models.noise_likelihood import node_log_likelihoods
from ahsl.subtree import enumerate_connected_subtrees, subtree_boundary_size
from ahsl.trees import validate_labeled_tree


def _rooted_order(tree: nx.Graph, root: int) -> tuple[list[int], list[int]]:
    m = validate_labeled_tree(tree)
    parent = [-1] * m
    order = [root]
    for node in order:
        for neighbor in sorted(tree.neighbors(node)):
            if neighbor == parent[node]:
                continue
            parent[neighbor] = node
            order.append(neighbor)
    return order, parent


def _log_mix(log_excluded: np.ndarray, log_included: np.ndarray, q: float) -> np.ndarray:
    if q == 0.0:
        return log_excluded
    if q == 1.0:
        return log_included
    return np.logaddexp(
        np.log1p(-q) + log_excluded,
        np.log(q) + log_included,
    )


def _sum_logs(parts: list[np.ndarray], n: int) -> np.ndarray:
    if not parts:
        return np.zeros(n, dtype=float)
    return np.sum(np.stack(parts, axis=0), axis=0)


def _sum_except(parts: list[np.ndarray]) -> list[np.ndarray]:
    """Sum all log factors except one without an ``-inf - -inf`` operation."""
    if len(parts) == 1:
        return [np.zeros_like(parts[0])]
    stacked = np.stack(parts, axis=0)
    negative_infinity = np.isneginf(stacked)
    finite_sum = np.where(negative_infinity, 0.0, stacked).sum(axis=0)
    negative_infinity_count = negative_infinity.sum(axis=0)
    results = []
    for index in range(len(parts)):
        remaining_count = negative_infinity_count - negative_infinity[index]
        result = finite_sum - np.where(negative_infinity[index], 0.0, stacked[index])
        results.append(np.where(remaining_count > 0, -np.inf, result))
    return results


@dataclass(frozen=True)
class MarginalLikelihoodResult:
    row_log_likelihoods: np.ndarray
    anchor_log_weights: np.ndarray

    @property
    def log_likelihood(self) -> float:
        return float(self.row_log_likelihoods.sum())

    def anchor_posterior(self) -> np.ndarray:
        normalizer = logsumexp(self.anchor_log_weights, axis=1, keepdims=True)
        return np.exp(self.anchor_log_weights - normalizer)


def marginal_log_likelihood_from_node_logs(
    tree: nx.Graph,
    log_if_zero: np.ndarray,
    log_if_one: np.ndarray,
    branch_probability: float,
    root: int = 0,
) -> MarginalLikelihoodResult:
    """Compute all row likelihoods by two-pass tree sum-product in ``O(nm)``."""
    m = validate_labeled_tree(tree)
    log_zero = np.asarray(log_if_zero, dtype=float)
    log_one = np.asarray(log_if_one, dtype=float)
    if log_zero.shape != log_one.shape or log_zero.ndim != 2 or log_zero.shape[1] != m:
        raise ValueError("node log likelihoods must both have shape (n, m)")
    if not 0.0 <= branch_probability <= 1.0:
        raise ValueError("branch_probability must lie in [0, 1]")

    n = log_zero.shape[0]
    q = float(branch_probability)
    order, parent = _rooted_order(tree, root)
    log_e: dict[tuple[int, int], np.ndarray] = {}
    log_i: dict[tuple[int, int], np.ndarray] = {}

    for node in reversed(order[1:]):
        target = parent[node]
        children = [neighbor for neighbor in tree.neighbors(node) if neighbor != target]
        log_e[(node, target)] = log_zero[:, node] + _sum_logs(
            [log_e[(child, node)] for child in children], n
        )
        log_i[(node, target)] = log_one[:, node] + _sum_logs(
            [
                _log_mix(log_e[(child, node)], log_i[(child, node)], q)
                for child in children
            ],
            n,
        )

    anchor_log_weights = np.empty((n, m), dtype=float)
    for node in order:
        neighbors = sorted(tree.neighbors(node))
        incoming_e = [log_e[(neighbor, node)] for neighbor in neighbors]
        incoming_mixture = [
            _log_mix(log_e[(neighbor, node)], log_i[(neighbor, node)], q)
            for neighbor in neighbors
        ]
        anchor_log_weights[:, node] = log_one[:, node] + _sum_logs(
            incoming_mixture, n
        )

        excluded_e = _sum_except(incoming_e) if neighbors else []
        excluded_mixture = _sum_except(incoming_mixture) if neighbors else []
        for index, neighbor in enumerate(neighbors):
            if (node, neighbor) in log_e:
                continue
            log_e[(node, neighbor)] = log_zero[:, node] + excluded_e[index]
            log_i[(node, neighbor)] = log_one[:, node] + excluded_mixture[index]

    row_log_likelihoods = logsumexp(anchor_log_weights, axis=1) - np.log(m)
    return MarginalLikelihoodResult(row_log_likelihoods, anchor_log_weights)


def marginal_log_likelihood(
    tree: nx.Graph,
    observed: np.ndarray,
    p_false_negative: float,
    p_false_positive: float,
    branch_probability: float,
) -> MarginalLikelihoodResult:
    """Score noisy incidence observations under the matched subtree model."""
    log_zero, log_one, _ = node_log_likelihoods(
        observed, p_false_negative, p_false_positive
    )
    return marginal_log_likelihood_from_node_logs(
        tree, log_zero, log_one, branch_probability
    )


def brute_force_marginal_log_likelihood(
    tree: nx.Graph,
    observed: np.ndarray,
    p_false_negative: float,
    p_false_positive: float,
    branch_probability: float,
) -> np.ndarray:
    """Reference enumeration for small-tree verification only."""
    m = validate_labeled_tree(tree)
    if not 0.0 < branch_probability < 1.0:
        raise ValueError("brute-force reference requires 0 < q < 1")
    log_zero, log_one, _ = node_log_likelihoods(
        observed, p_false_negative, p_false_positive
    )
    q = float(branch_probability)
    support_scores = []
    for support in enumerate_connected_subtrees(tree):
        selected = np.zeros(m, dtype=bool)
        selected[list(support)] = True
        log_prior = (
            np.log(len(support))
            - np.log(m)
            + (len(support) - 1) * np.log(q)
            + subtree_boundary_size(tree, support) * np.log1p(-q)
        )
        support_scores.append(
            log_prior
            + log_one[:, selected].sum(axis=1)
            + log_zero[:, ~selected].sum(axis=1)
        )
    return logsumexp(np.stack(support_scores, axis=1), axis=1)


class SubtreeMarginalLikelihood:
    """Small estimator-style wrapper around the exact row scorer."""

    def __init__(
        self,
        tree: nx.Graph,
        p_false_negative: float,
        p_false_positive: float,
        branch_probability: float,
    ) -> None:
        self.tree = tree.copy()
        validate_labeled_tree(self.tree)
        self.p_false_negative = p_false_negative
        self.p_false_positive = p_false_positive
        self.branch_probability = branch_probability

    def fit(self, observed: np.ndarray) -> "SubtreeMarginalLikelihood":
        result = marginal_log_likelihood(
            self.tree,
            observed,
            self.p_false_negative,
            self.p_false_positive,
            self.branch_probability,
        )
        self.row_log_likelihoods_ = result.row_log_likelihoods
        self.anchor_log_weights_ = result.anchor_log_weights
        self.log_likelihood_ = result.log_likelihood
        return self

    def anchor_posterior(self) -> np.ndarray:
        return MarginalLikelihoodResult(
            self.row_log_likelihoods_, self.anchor_log_weights_
        ).anchor_posterior()
