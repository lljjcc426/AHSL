from __future__ import annotations

from dataclasses import dataclass
import math
import time
from typing import Iterable, Mapping

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

from .hypergraph_builder import DirectedHypergraph


@dataclass(frozen=True, slots=True)
class ExactSolveResult:
    status: str
    edge_ids: frozenset[str]
    objective: float
    runtime_seconds: float
    cuts_added: int


def solve_shortest_superpath(
    graph: DirectedHypergraph,
    sources: Iterable[str],
    targets: Iterable[str],
    costs: Mapping[str, float] | None = None,
    allowed_edges: Iterable[str] | None = None,
    omit_at_least_one_of: Iterable[str] | None = None,
    time_limit: float = 120.0,
) -> ExactSolveResult:
    """Independent Mmunin-equivalent cut generation over superpaths.

    A cut C is crossed by e when tail(e) is contained in C and head(e) is
    not. Repeatedly adding the violated reachable-set cut is exact because an
    edge set reaches the targets iff it crosses every source-target cut.
    """
    start = time.perf_counter()
    edge_ids = sorted(graph.edges if allowed_edges is None else set(allowed_edges))
    if not edge_ids:
        return ExactSolveResult("INFEASIBLE", frozenset(), math.inf, time.perf_counter() - start, 0)
    index = {edge_id: position for position, edge_id in enumerate(edge_ids)}
    objective = np.array([1.0 if costs is None else float(costs[edge_id]) for edge_id in edge_ids])
    if np.any(objective <= 0):
        raise ValueError("Exact CertPath solves require strictly positive reaction costs")
    rows: list[dict[int, float]] = []
    lower: list[float] = []
    upper: list[float] = []
    omitted = set(omit_at_least_one_of or ()) & set(edge_ids)
    if omitted:
        rows.append({index[edge_id]: 1.0 for edge_id in omitted})
        lower.append(-math.inf)
        upper.append(float(len(omitted) - 1))

    source_set = frozenset(sources)
    target_set = frozenset(targets)
    cut_count = 0
    while True:
        elapsed = time.perf_counter() - start
        if elapsed >= time_limit:
            return ExactSolveResult("TIMEOUT", frozenset(), math.inf, elapsed, cut_count)
        constraints = None
        if rows:
            rr: list[int] = []
            cc: list[int] = []
            vv: list[float] = []
            for row_index, row in enumerate(rows):
                for column, value in row.items():
                    rr.append(row_index)
                    cc.append(column)
                    vv.append(value)
            matrix = coo_matrix((vv, (rr, cc)), shape=(len(rows), len(edge_ids))).tocsr()
            constraints = LinearConstraint(matrix, np.array(lower), np.array(upper))
        result = milp(
            c=objective,
            integrality=np.ones(len(edge_ids)),
            bounds=Bounds(np.zeros(len(edge_ids)), np.ones(len(edge_ids))),
            constraints=constraints,
            options={"time_limit": max(0.01, time_limit - elapsed), "mip_rel_gap": 0.0},
        )
        if result.x is None:
            status = "TIMEOUT" if result.status == 1 else "INFEASIBLE"
            return ExactSolveResult(status, frozenset(), math.inf, time.perf_counter() - start, cut_count)
        selected = frozenset(edge_ids[i] for i, value in enumerate(result.x) if value > 0.5)
        reached = graph.closure(source_set, selected)
        missing_targets = target_set - reached
        if not missing_targets:
            return ExactSolveResult(
                "OPTIMAL",
                selected,
                float(sum(objective[index[e]] for e in selected)),
                time.perf_counter() - start,
                cut_count,
            )
        crossing = {
            index[edge_id]: 1.0
            for edge_id in edge_ids
            if graph.edges[edge_id].tail <= reached
            and not graph.edges[edge_id].head <= reached
        }
        if not crossing:
            return ExactSolveResult("INFEASIBLE", frozenset(), math.inf, time.perf_counter() - start, cut_count)
        rows.append(crossing)
        lower.append(1.0)
        upper.append(math.inf)
        cut_count += 1
