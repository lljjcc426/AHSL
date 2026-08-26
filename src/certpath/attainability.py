from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping

from .hypergraph_builder import DirectedHypergraph
from .solver_adapter import ExactSolveResult, solve_shortest_superpath


@dataclass(frozen=True, slots=True)
class AttainabilityResult:
    feasible: bool
    attainable: bool | None
    gold_size: int
    minimum_size: int | None
    solve: ExactSolveResult


def check_positive_cost_attainability(
    graph: DirectedHypergraph,
    sources: frozenset[str],
    targets: frozenset[str],
    gold_reactions: frozenset[str],
    time_limit: float = 120.0,
    compute_minimum: bool = True,
) -> AttainabilityResult:
    feasible = graph.is_feasible(sources, targets, gold_reactions)
    if not feasible:
        empty = ExactSolveResult("INFEASIBLE_GOLD", frozenset(), math.inf, 0.0, 0)
        return AttainabilityResult(False, False, len(gold_reactions), None, empty)
    if not compute_minimum:
        for edge_id in sorted(gold_reactions):
            proper_subset = gold_reactions - {edge_id}
            if graph.is_feasible(sources, targets, proper_subset):
                witness = ExactSolveResult(
                    "PROPER_SUBSET_WITNESS", proper_subset, float(len(proper_subset)), 0.0, 0
                )
                return AttainabilityResult(True, False, len(gold_reactions), None, witness)
        witness = ExactSolveResult(
            "INCLUSION_MINIMAL", gold_reactions, float(len(gold_reactions)), 0.0, 0
        )
        return AttainabilityResult(True, True, len(gold_reactions), len(gold_reactions), witness)
    solve = solve_shortest_superpath(
        graph,
        sources,
        targets,
        allowed_edges=gold_reactions,
        time_limit=time_limit,
    )
    minimum = len(solve.edge_ids) if solve.status == "OPTIMAL" else None
    return AttainabilityResult(
        True,
        minimum == len(gold_reactions) if minimum is not None else None,
        len(gold_reactions),
        minimum,
        solve,
    )


def robust_optimality_margin(
    graph: DirectedHypergraph,
    sources: frozenset[str],
    targets: frozenset[str],
    selected: frozenset[str],
    lower_cost: Mapping[str, float],
    upper_cost: Mapping[str, float],
    time_limit: float = 120.0,
) -> tuple[float, ExactSolveResult]:
    modified = {
        edge_id: upper_cost[edge_id] if edge_id in selected else lower_cost[edge_id]
        for edge_id in graph.edges
    }
    competitor = solve_shortest_superpath(
        graph,
        sources,
        targets,
        costs=modified,
        omit_at_least_one_of=selected,
        time_limit=time_limit,
    )
    if competitor.status == "INFEASIBLE":
        return math.inf, competitor
    if competitor.status != "OPTIMAL":
        return math.nan, competitor
    margin = competitor.objective - sum(upper_cost[e] for e in selected)
    return margin, competitor
