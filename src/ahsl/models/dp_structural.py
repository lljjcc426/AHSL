"""Decision-aligned connected-subtree estimators solved by tree DP."""

from __future__ import annotations

from math import isclose

import networkx as nx
import numpy as np

from ahsl.models.common import repeated_observations
from ahsl.models.noise_likelihood import node_log_likelihoods
from ahsl.tree_dp import (
    maximum_weight_connected_subtree,
    maximum_weight_connected_subtree_by_size,
)
from ahsl.trees import validate_labeled_tree


def _same_score(left: float, right: float) -> bool:
    return isclose(left, right, rel_tol=1e-12, abs_tol=1e-12)


def _branch_containing(
    tree: nx.Graph,
    start: int,
    parent: int,
    blocked: set[int],
    weights: np.ndarray,
) -> tuple[float, frozenset[int], bool]:
    order = [start]
    parents = {start: parent}
    children: dict[int, list[int]] = {}
    for node in order:
        children[node] = []
        for neighbor in sorted(tree.neighbors(node)):
            if neighbor == parents[node] or neighbor in blocked:
                continue
            parents[neighbor] = node
            children[node].append(neighbor)
            order.append(neighbor)

    scores: dict[int, float] = {}
    selected: dict[int, frozenset[int]] = {}
    ties: dict[int, bool] = {}
    for node in reversed(order):
        score = float(weights[node])
        nodes = {node}
        tie = False
        for child in children[node]:
            child_score = scores[child]
            if child_score > 0.0 and not _same_score(child_score, 0.0):
                score += child_score
                nodes.update(selected[child])
                tie |= ties[child]
            elif _same_score(child_score, 0.0):
                tie = True
        scores[node] = score
        selected[node] = frozenset(nodes)
        ties[node] = tie
    return scores[start], selected[start], ties[start]


def _connected_log_likelihood_solution(
    tree: nx.Graph,
    log_if_zero: np.ndarray,
    log_if_one: np.ndarray,
) -> dict[str, object]:
    mandatory = set(np.flatnonzero(np.isneginf(log_if_zero)))
    forbidden = set(np.flatnonzero(np.isneginf(log_if_one)))
    finite = np.isfinite(log_if_zero) & np.isfinite(log_if_one)
    weights = np.zeros_like(log_if_zero, dtype=float)
    weights[finite] = log_if_one[finite] - log_if_zero[finite]

    if not mandatory:
        weights[list(forbidden)] = -np.inf
        result = maximum_weight_connected_subtree(tree, weights)
        selected = set(result["selected_nodes"])
    else:
        first = min(mandatory)
        connector = {first}
        for required in sorted(mandatory - {first}):
            connector.update(nx.shortest_path(tree, first, required))
        if connector & forbidden:
            raise ValueError("no positive-likelihood connected row exists")
        selected = set(connector)
        has_tie = False
        blocked = connector | forbidden
        for connector_node in sorted(connector):
            for neighbor in sorted(tree.neighbors(connector_node)):
                if neighbor in blocked:
                    continue
                score, branch_nodes, branch_tie = _branch_containing(
                    tree, neighbor, connector_node, blocked, weights
                )
                blocked.update(branch_nodes)
                if score > 0.0 and not _same_score(score, 0.0):
                    selected.update(branch_nodes)
                    has_tie |= branch_tie
                elif _same_score(score, 0.0):
                    has_tie = True
        result = {
            "selected_nodes": frozenset(selected),
            "has_tie": has_tie,
            "size": len(selected),
        }

    selected_mask = np.zeros(len(log_if_zero), dtype=bool)
    selected_mask[list(selected)] = True
    objective = float(
        log_if_one[selected_mask].sum() + log_if_zero[~selected_mask].sum()
    )
    return {**result, "objective": objective}


class DPNearestConnectedSubtree:
    """Exact Hamming projection using one linear tree DP per incidence row."""

    name = "DPNearestConnectedSubtree"

    def __init__(self, tree: nx.Graph) -> None:
        self.tree = tree.copy()
        validate_labeled_tree(self.tree)

    def fit(self, observed: np.ndarray) -> "DPNearestConnectedSubtree":
        observations = repeated_observations(observed).astype(np.int8)
        repetitions, n, m = observations.shape
        weights = 2 * observations.sum(axis=0) - repetitions
        prediction = np.zeros((n, m), dtype=np.int8)
        objectives = np.empty(n, dtype=float)
        ties = np.zeros(n, dtype=bool)
        sizes = np.empty(n, dtype=int)
        for row in range(n):
            result = maximum_weight_connected_subtree(self.tree, weights[row])
            prediction[row, list(result["selected_nodes"])] = 1
            objectives[row] = float(result["objective"])
            ties[row] = bool(result["has_tie"])
            sizes[row] = int(result["size"])
        mismatch = np.not_equal(prediction[None, :, :], observations).sum()
        self.prediction_ = prediction
        self.row_objectives_ = objectives
        self.row_ties_ = ties
        self.selected_sizes_ = sizes
        self.optimal_tie_fraction_ = float(ties.mean())
        self.train_loss_ = float(mismatch / observations.size)
        return self

    def predict(self) -> np.ndarray:
        return self.prediction_.copy()

    def predict_proba(self) -> np.ndarray:
        return self.prediction_.astype(float)


class DPNoiseAwareConnectedMLE:
    """Exact connected MLE under known independent incidence-noise rates."""

    name = "DPNoiseAwareConnectedMLE"

    def __init__(
        self,
        tree: nx.Graph,
        p_false_negative: float,
        p_false_positive: float,
    ) -> None:
        self.tree = tree.copy()
        validate_labeled_tree(self.tree)
        self.p_false_negative = p_false_negative
        self.p_false_positive = p_false_positive

    def fit(self, observed: np.ndarray) -> "DPNoiseAwareConnectedMLE":
        log_zero, log_one, repetitions = node_log_likelihoods(
            observed, self.p_false_negative, self.p_false_positive
        )
        n, m = log_zero.shape
        prediction = np.zeros((n, m), dtype=np.int8)
        objectives = np.empty(n, dtype=float)
        ties = np.zeros(n, dtype=bool)
        sizes = np.empty(n, dtype=int)
        for row in range(n):
            result = _connected_log_likelihood_solution(
                self.tree, log_zero[row], log_one[row]
            )
            prediction[row, list(result["selected_nodes"])] = 1
            objectives[row] = float(result["objective"])
            ties[row] = bool(result["has_tie"])
            sizes[row] = int(result["size"])
        self.prediction_ = prediction
        self.row_objectives_ = objectives
        self.row_ties_ = ties
        self.selected_sizes_ = sizes
        self.optimal_tie_fraction_ = float(ties.mean())
        self.train_loss_ = float(-objectives.mean() / (repetitions * m))
        return self

    def predict(self) -> np.ndarray:
        return self.prediction_.copy()

    def predict_proba(self) -> np.ndarray:
        return self.prediction_.astype(float)


class GeneratorPriorConnectedMAP:
    """Oracle connected MAP using the true untruncated anchor-growth prior."""

    name = "GeneratorPriorConnectedMAP"

    def __init__(
        self,
        tree: nx.Graph,
        p_false_negative: float,
        p_false_positive: float,
        branch_probability: float,
    ) -> None:
        self.tree = tree.copy()
        self.m = validate_labeled_tree(self.tree)
        if not 0.0 < branch_probability < 1.0:
            raise ValueError("generator-prior oracle requires 0 < branch_probability < 1")
        self.p_false_negative = p_false_negative
        self.p_false_positive = p_false_positive
        self.branch_probability = branch_probability

    def fit(self, observed: np.ndarray) -> "GeneratorPriorConnectedMAP":
        log_zero, log_one, repetitions = node_log_likelihoods(
            observed, self.p_false_negative, self.p_false_positive
        )
        if not np.isfinite(log_zero).all() or not np.isfinite(log_one).all():
            raise ValueError("generator-prior oracle currently requires interior noise rates")
        q = self.branch_probability
        log_q = np.log(q)
        log_one_minus_q = np.log1p(-q)
        prior_node_weight = np.array(
            [
                log_q + (self.tree.degree(node) - 2) * log_one_minus_q
                for node in range(self.m)
            ]
        )

        def size_bonus(size: int) -> float:
            return float(
                np.log(size)
                - np.log(self.m)
                - log_q
                + 2.0 * log_one_minus_q
            )

        n = log_zero.shape[0]
        prediction = np.zeros_like(log_zero, dtype=np.int8)
        objectives = np.empty(n, dtype=float)
        ties = np.zeros(n, dtype=bool)
        sizes = np.empty(n, dtype=int)
        for row in range(n):
            weights = log_one[row] - log_zero[row] + prior_node_weight
            result = maximum_weight_connected_subtree_by_size(
                self.tree, weights, size_bonus
            )
            prediction[row, list(result["selected_nodes"])] = 1
            objectives[row] = float(log_zero[row].sum() + result["objective"])
            ties[row] = bool(result["has_tie"])
            sizes[row] = int(result["size"])
        self.prediction_ = prediction
        self.row_objectives_ = objectives
        self.row_ties_ = ties
        self.selected_sizes_ = sizes
        self.optimal_tie_fraction_ = float(ties.mean())
        self.train_loss_ = float(-objectives.mean() / (repetitions * self.m))
        return self

    def predict(self) -> np.ndarray:
        return self.prediction_.copy()

    def predict_proba(self) -> np.ndarray:
        return self.prediction_.astype(float)

