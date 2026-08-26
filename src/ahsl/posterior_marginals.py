"""Exact node marginals for the anchor-growth connected-subtree posterior."""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx
import numpy as np
from scipy.special import logsumexp

from ahsl.models.noise_likelihood import node_log_likelihoods
from ahsl.subtree_marginal import _log_mix, _rooted_order, _sum_except, _sum_logs
from ahsl.trees import validate_labeled_tree


@dataclass(frozen=True)
class PosteriorMarginalResult:
    """Posterior summaries for each independently observed incidence row."""

    node_marginals: np.ndarray
    row_log_likelihoods: np.ndarray
    anchor_log_weights: np.ndarray

    def anchor_posterior(self) -> np.ndarray:
        normalizer = logsumexp(self.anchor_log_weights, axis=1, keepdims=True)
        return np.exp(self.anchor_log_weights - normalizer)


def _mix_responsibilities(
    log_excluded: np.ndarray,
    log_included: np.ndarray,
    q: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Derivative of log((1-q)e^E + q e^I) with stable boundary cases."""
    if q == 0.0:
        return np.ones_like(log_excluded), np.zeros_like(log_included)
    if q == 1.0:
        return np.zeros_like(log_excluded), np.ones_like(log_included)
    denominator = _log_mix(log_excluded, log_included, q)
    excluded = np.zeros_like(denominator)
    included = np.zeros_like(denominator)
    finite = np.isfinite(denominator)
    excluded[finite] = np.exp(
        np.log1p(-q) + log_excluded[finite] - denominator[finite]
    )
    included[finite] = np.exp(
        np.log(q) + log_included[finite] - denominator[finite]
    )
    return excluded, included


def posterior_marginals_from_node_logs(
    tree: nx.Graph,
    log_if_zero: np.ndarray,
    log_if_one: np.ndarray,
    branch_probability: float,
    root: int = 0,
) -> PosteriorMarginalResult:
    """Return all ``P(X_j=1 | Y)`` values in ``O(nm)`` time.

    The forward pass is the A1 two-pass likelihood circuit.  The reverse pass
    differentiates its row log-normalizer with respect to every ``log_if_one``
    input.  This derivative is exactly the corresponding posterior marginal.
    """
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

    # Forward postorder: messages from children toward the arbitrary root.
    for node in reversed(order[1:]):
        target = parent[node]
        children = [neighbor for neighbor in tree.neighbors(node) if neighbor != target]
        log_e[(node, target)] = log_zero[:, node] + _sum_logs(
            [log_e[(child, node)] for child in children], n
        )
        log_i[(node, target)] = log_one[:, node] + _sum_logs(
            [_log_mix(log_e[(child, node)], log_i[(child, node)], q) for child in children],
            n,
        )

    # Forward preorder: anchors and the remaining directed messages.
    anchor_log_weights = np.empty((n, m), dtype=float)
    children_by_node: list[list[int]] = [[] for _ in range(m)]
    for node in order:
        neighbors = sorted(tree.neighbors(node))
        children_by_node[node] = [neighbor for neighbor in neighbors if parent[neighbor] == node]
        incoming_e = [log_e[(neighbor, node)] for neighbor in neighbors]
        incoming_mix = [
            _log_mix(log_e[(neighbor, node)], log_i[(neighbor, node)], q)
            for neighbor in neighbors
        ]
        anchor_log_weights[:, node] = log_one[:, node] + _sum_logs(incoming_mix, n)
        excluded_e = _sum_except(incoming_e) if neighbors else []
        excluded_mix = _sum_except(incoming_mix) if neighbors else []
        for index, neighbor in enumerate(neighbors):
            if (node, neighbor) not in log_e:
                log_e[(node, neighbor)] = log_zero[:, node] + excluded_e[index]
                log_i[(node, neighbor)] = log_one[:, node] + excluded_mix[index]

    row_log_likelihoods = logsumexp(anchor_log_weights, axis=1) - np.log(m)
    if not np.isfinite(row_log_likelihoods).all():
        raise ValueError("posterior is undefined for a row with zero model likelihood")
    anchor_adjoint = np.exp(
        anchor_log_weights - logsumexp(anchor_log_weights, axis=1, keepdims=True)
    )
    adj_e = {edge: np.zeros(n, dtype=float) for edge in log_e}
    adj_i = {edge: np.zeros(n, dtype=float) for edge in log_i}
    adj_zero = np.zeros((n, m), dtype=float)
    adj_one = np.zeros((n, m), dtype=float)

    # Reverse the preorder circuit.  A child is processed before its parent,
    # so all adjoints of parent-to-child messages are already available.
    for node in reversed(order):
        children = children_by_node[node]
        total_e = sum((adj_e[(node, child)] for child in children), np.zeros(n))
        total_i = sum((adj_i[(node, child)] for child in children), np.zeros(n))
        adj_zero[:, node] += total_e
        adj_one[:, node] += anchor_adjoint[:, node] + total_i
        for neighbor in tree.neighbors(node):
            direct_e = total_e.copy()
            mix_adjoint = anchor_adjoint[:, node] + total_i
            if neighbor in children:
                direct_e -= adj_e[(node, neighbor)]
                mix_adjoint = mix_adjoint - adj_i[(node, neighbor)]
            excluded_resp, included_resp = _mix_responsibilities(
                log_e[(neighbor, node)], log_i[(neighbor, node)], q
            )
            adj_e[(neighbor, node)] += direct_e + mix_adjoint * excluded_resp
            adj_i[(neighbor, node)] += mix_adjoint * included_resp

    # Reverse the original postorder messages, from the root outward.
    for node in order[1:]:
        target = parent[node]
        message_adj_e = adj_e[(node, target)]
        message_adj_i = adj_i[(node, target)]
        adj_zero[:, node] += message_adj_e
        adj_one[:, node] += message_adj_i
        for child in children_by_node[node]:
            adj_e[(child, node)] += message_adj_e
            excluded_resp, included_resp = _mix_responsibilities(
                log_e[(child, node)], log_i[(child, node)], q
            )
            adj_e[(child, node)] += message_adj_i * excluded_resp
            adj_i[(child, node)] += message_adj_i * included_resp

    return PosteriorMarginalResult(
        node_marginals=adj_one,
        row_log_likelihoods=row_log_likelihoods,
        anchor_log_weights=anchor_log_weights,
    )


def posterior_node_marginals(
    tree: nx.Graph,
    observed: np.ndarray,
    p_false_negative: float,
    p_false_positive: float,
    branch_probability: float,
    root: int = 0,
) -> PosteriorMarginalResult:
    """Compute exact posterior node marginals under the A1 matched model."""
    log_zero, log_one, _ = node_log_likelihoods(
        observed, p_false_negative, p_false_positive
    )
    return posterior_marginals_from_node_logs(
        tree, log_zero, log_one, branch_probability, root=root
    )
