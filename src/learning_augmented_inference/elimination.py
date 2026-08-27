"""Classical elimination strategies and exact dense execution for R0."""

from __future__ import annotations

from dataclasses import dataclass
from math import prod
from time import perf_counter

import networkx as nx
import numpy as np

from learning_augmented_inference.structure import primal_graph
from learning_augmented_inference.uai import UAIFactor, UAIModel


@dataclass(frozen=True)
class EliminationCost:
    order: tuple[int, ...]
    induced_width: int
    max_union_arity: int
    peak_entries: int
    total_join_entries: int


@dataclass(frozen=True)
class ExactResult:
    value: float
    seconds: float
    peak_entries: int
    total_join_entries: int


def _step_scopes(
    scopes: list[frozenset[int]], variable: int
) -> tuple[list[frozenset[int]], frozenset[int]]:
    incident = [scope for scope in scopes if variable in scope]
    union = frozenset().union(*incident) if incident else frozenset({variable})
    remaining = [scope for scope in scopes if variable not in scope]
    new_scope = union - {variable}
    if new_scope:
        remaining.append(new_scope)
    return remaining, union


def _entry_count(scope: frozenset[int], domains: tuple[int, ...]) -> int:
    return prod(domains[variable] for variable in scope)


def simulate_elimination(
    scopes: tuple[tuple[int, ...], ...],
    domains: tuple[int, ...],
    order: tuple[int, ...] | list[int],
) -> EliminationCost:
    active = list({frozenset(scope) for scope in scopes})
    peak_entries = 1
    total_entries = 0
    max_arity = 0
    induced_width = 0
    for variable in order:
        active, union = _step_scopes(active, variable)
        entries = _entry_count(union, domains)
        peak_entries = max(peak_entries, entries)
        total_entries += entries
        max_arity = max(max_arity, len(union))
        induced_width = max(induced_width, max(0, len(union) - 1))
    return EliminationCost(
        tuple(order), induced_width, max_arity, peak_entries, total_entries
    )


def heuristic_order(
    scopes: tuple[tuple[int, ...], ...],
    domains: tuple[int, ...],
    strategy: str,
) -> tuple[int, ...]:
    """Construct a deterministic dynamic greedy elimination order."""

    active = list({frozenset(scope) for scope in scopes})
    remaining = set(range(len(domains)))
    order: list[int] = []
    while remaining:
        graph = primal_graph(active, len(domains))

        def score(variable: int) -> tuple[int, int]:
            neighbors = sorted(set(graph.neighbors(variable)) & remaining)
            missing = [
                (left, right)
                for index, left in enumerate(neighbors)
                for right in neighbors[index + 1 :]
                if not graph.has_edge(left, right)
            ]
            if strategy == "min_degree":
                primary = len(neighbors)
            elif strategy == "min_fill":
                primary = len(missing)
            elif strategy == "weighted_min_fill":
                primary = sum(domains[left] * domains[right] for left, right in missing)
            elif strategy == "min_factor_entries":
                union = frozenset({variable})
                for scope in active:
                    if variable in scope:
                        union |= scope
                primary = _entry_count(union, domains)
            else:
                raise ValueError(f"unknown strategy: {strategy}")
            return primary, variable

        chosen = min(remaining, key=score)
        order.append(chosen)
        active, _ = _step_scopes(active, chosen)
        remaining.remove(chosen)
    return tuple(order)


def _align_factor(
    factor: UAIFactor,
    union: tuple[int, ...],
    domains: tuple[int, ...],
) -> np.ndarray:
    if factor.values is None:
        raise ValueError("exact elimination requires factor values")
    present = [variable for variable in union if variable in factor.scope]
    permutation = [factor.scope.index(variable) for variable in present]
    values = factor.values
    if permutation != list(range(len(permutation))):
        values = np.transpose(values, permutation)
    shape = [domains[variable] if variable in factor.scope else 1 for variable in union]
    return values.reshape(shape)


def run_exact_elimination(model: UAIModel, order: tuple[int, ...]) -> ExactResult:
    """Compute the partition function; the order changes cost, never the answer."""

    factors = list(model.factors)
    peak_entries = 1
    total_entries = 0
    start = perf_counter()
    for variable in order:
        incident = [factor for factor in factors if variable in factor.scope]
        if not incident:
            continue
        union = tuple(sorted(set().union(*(factor.scope for factor in incident))))
        entries = prod(model.domain_sizes[item] for item in union)
        peak_entries = max(peak_entries, entries)
        total_entries += entries
        product_values = np.ones(
            tuple(model.domain_sizes[item] for item in union), dtype=np.float64
        )
        for factor in incident:
            product_values *= _align_factor(factor, union, model.domain_sizes)
        reduced_values = product_values.sum(axis=union.index(variable))
        reduced_scope = tuple(item for item in union if item != variable)
        factors = [factor for factor in factors if variable not in factor.scope]
        factors.append(
            UAIFactor(
                scope=reduced_scope,
                table_size=int(reduced_values.size),
                nonzero_count=int(np.count_nonzero(reduced_values)),
                values=np.asarray(reduced_values),
            )
        )
    value = 1.0
    for factor in factors:
        if factor.values is None:
            raise ValueError("exact elimination requires factor values")
        value *= float(np.asarray(factor.values).sum())
    return ExactResult(value, perf_counter() - start, peak_entries, total_entries)
