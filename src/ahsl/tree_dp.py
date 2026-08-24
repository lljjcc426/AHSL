"""Exact dynamic programs for connected subsets of a labeled tree."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from typing import Callable, Iterable

import networkx as nx
import numpy as np

from ahsl.trees import validate_labeled_tree


TIE_BREAK = "min_size_then_lexicographic"
_ABSOLUTE_TOLERANCE = 1e-12
_RELATIVE_TOLERANCE = 1e-12


def _scores_equal(left: float, right: float) -> bool:
    return isclose(
        left,
        right,
        rel_tol=_RELATIVE_TOLERANCE,
        abs_tol=_ABSOLUTE_TOLERANCE,
    )


def _rooted_tree(tree: nx.Graph, root: int = 0) -> tuple[list[int], list[list[int]]]:
    m = validate_labeled_tree(tree)
    parent = [-1] * m
    children: list[list[int]] = [[] for _ in range(m)]
    order = [root]
    for node in order:
        for neighbor in sorted(tree.neighbors(node)):
            if neighbor == parent[node]:
                continue
            parent[neighbor] = node
            children[node].append(neighbor)
            order.append(neighbor)
    return order, children


def maximum_weight_connected_subtree(
    tree: nx.Graph,
    node_weights: Iterable[float],
    tie_break: str = TIE_BREAK,
) -> dict[str, object]:
    """Return an exact maximum-weight non-empty connected node set.

    The score recurrence is linear in the number of tree nodes. Exact
    lexicographic comparison materializes only globally tied canonical
    candidates and can add quadratic work in a deliberately tie-heavy case.
    """
    if tie_break != TIE_BREAK:
        raise ValueError(f"unsupported tie policy: {tie_break}")
    m = validate_labeled_tree(tree)
    weights = np.asarray(list(node_weights), dtype=float)
    if weights.shape != (m,):
        raise ValueError("node_weights must contain one value per labeled tree node")
    if np.isnan(weights).any() or np.isposinf(weights).any():
        raise ValueError("node weights may be finite or negative infinity, but not NaN/+inf")
    if np.isneginf(weights).all():
        raise ValueError("no non-empty feasible connected subset exists")

    order, children = _rooted_tree(tree)
    scores = weights.copy()
    sizes = np.ones(m, dtype=int)
    include_child: dict[tuple[int, int], bool] = {}
    contains_objective_tie = np.zeros(m, dtype=bool)

    for node in reversed(order):
        for child in children[node]:
            child_score = float(scores[child])
            if child_score > 0.0 and not _scores_equal(child_score, 0.0):
                scores[node] += child_score
                sizes[node] += sizes[child]
                include_child[(node, child)] = True
                contains_objective_tie[node] |= contains_objective_tie[child]
            else:
                include_child[(node, child)] = False
                if _scores_equal(child_score, 0.0):
                    contains_objective_tie[node] = True

    best_score = float(np.max(scores))
    score_tied_roots = [
        node for node in range(m) if _scores_equal(float(scores[node]), best_score)
    ]
    minimum_size = min(int(sizes[node]) for node in score_tied_roots)
    canonical_roots = [
        node for node in score_tied_roots if int(sizes[node]) == minimum_size
    ]

    def reconstruct(highest_node: int) -> tuple[int, ...]:
        selected: list[int] = []
        stack = [highest_node]
        while stack:
            node = stack.pop()
            selected.append(node)
            for child in reversed(children[node]):
                if include_child[(node, child)]:
                    stack.append(child)
        return tuple(sorted(selected))

    candidates = [(reconstruct(root), root) for root in canonical_roots]
    selected_tuple, selected_root = min(candidates, key=lambda item: item[0])
    has_tie = len(score_tied_roots) > 1 or bool(
        contains_objective_tie[selected_root]
    )
    return {
        "selected_nodes": frozenset(selected_tuple),
        "objective": best_score,
        "size": len(selected_tuple),
        "has_tie": has_tie,
        "num_optima_capped": 2 if has_tie else 1,
    }


@dataclass(frozen=True)
class _SizeState:
    score: float
    nodes: tuple[int, ...]
    num_optima_capped: int = 1


def _better_size_state(candidate: _SizeState, incumbent: _SizeState) -> _SizeState:
    if candidate.score > incumbent.score and not _scores_equal(
        candidate.score, incumbent.score
    ):
        return candidate
    if incumbent.score > candidate.score and not _scores_equal(
        candidate.score, incumbent.score
    ):
        return incumbent
    count = min(2, candidate.num_optima_capped + incumbent.num_optima_capped)
    canonical = candidate if candidate.nodes < incumbent.nodes else incumbent
    return _SizeState(canonical.score, canonical.nodes, count)


def maximum_weight_connected_subtree_by_size(
    tree: nx.Graph,
    node_weights: Iterable[float],
    size_bonus: Callable[[int], float],
    tie_break: str = TIE_BREAK,
) -> dict[str, object]:
    """Solve a connected-subtree problem with a non-additive size bonus.

    A tree-knapsack state stores the best additive score for each exact selected
    size. State convolution is `O(m^2)`; canonical tuple storage is intended for
    the moderate-size generator-prior oracle rather than the scaling runs.
    """
    if tie_break != TIE_BREAK:
        raise ValueError(f"unsupported tie policy: {tie_break}")
    m = validate_labeled_tree(tree)
    weights = np.asarray(list(node_weights), dtype=float)
    if weights.shape != (m,) or not np.isfinite(weights).all():
        raise ValueError("size-aware DP requires one finite weight per tree node")

    order, children = _rooted_tree(tree)
    states: list[dict[int, _SizeState]] = [{} for _ in range(m)]
    for node in reversed(order):
        current = {1: _SizeState(float(weights[node]), (node,))}
        for child in children[node]:
            combined = dict(current)
            for left_size, left_state in current.items():
                for right_size, right_state in states[child].items():
                    total_size = left_size + right_size
                    candidate = _SizeState(
                        left_state.score + right_state.score,
                        tuple(sorted((*left_state.nodes, *right_state.nodes))),
                        min(
                            2,
                            left_state.num_optima_capped
                            * right_state.num_optima_capped,
                        ),
                    )
                    if total_size in combined:
                        combined[total_size] = _better_size_state(
                            candidate, combined[total_size]
                        )
                    else:
                        combined[total_size] = candidate
            current = combined
        states[node] = current

    best_total = -np.inf
    optimal_states: list[_SizeState] = []
    for node in range(m):
        for size, state in states[node].items():
            total = state.score + float(size_bonus(size))
            adjusted = _SizeState(total, state.nodes, state.num_optima_capped)
            if total > best_total and not _scores_equal(total, best_total):
                best_total = total
                optimal_states = [adjusted]
            elif _scores_equal(total, best_total):
                optimal_states.append(adjusted)

    minimum_size = min(len(state.nodes) for state in optimal_states)
    size_tied = [state for state in optimal_states if len(state.nodes) == minimum_size]
    canonical = min(size_tied, key=lambda state: state.nodes)
    total_optima = min(
        2, sum(state.num_optima_capped for state in optimal_states)
    )
    return {
        "selected_nodes": frozenset(canonical.nodes),
        "objective": best_total,
        "size": len(canonical.nodes),
        "has_tie": total_optima > 1,
        "num_optima_capped": total_optima,
    }


def subtree_boundary_size(tree: nx.Graph, selected_nodes: Iterable[int]) -> int:
    """Count tree edges with exactly one selected endpoint."""
    selected = set(selected_nodes)
    return sum((left in selected) != (right in selected) for left, right in tree.edges)


def generator_subtree_probability(
    tree: nx.Graph,
    selected_nodes: Iterable[int],
    branch_probability: float,
) -> float:
    """Return the exact untruncated anchor-growth probability of a connected set."""
    m = validate_labeled_tree(tree)
    selected = frozenset(selected_nodes)
    if not selected or not nx.is_connected(tree.subgraph(selected)):
        return 0.0
    if branch_probability == 0.0:
        return 1.0 / m if len(selected) == 1 else 0.0
    if branch_probability == 1.0:
        return 1.0 if len(selected) == m else 0.0
    if not 0.0 < branch_probability < 1.0:
        raise ValueError("branch_probability must lie in [0, 1]")
    boundary = subtree_boundary_size(tree, selected)
    return float(
        (len(selected) / m)
        * branch_probability ** (len(selected) - 1)
        * (1.0 - branch_probability) ** boundary
    )
