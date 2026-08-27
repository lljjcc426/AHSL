from __future__ import annotations

import numpy as np

from learning_augmented_inference.elimination import (
    heuristic_order,
    run_exact_elimination,
    simulate_elimination,
)
from learning_augmented_inference.structure import is_alpha_acyclic, primal_graph
from learning_augmented_inference.uai import UAIFactor, UAIModel, read_uai


def _factor(scope: tuple[int, ...], values: list[float], domains=(2, 2, 2)) -> UAIFactor:
    array = np.asarray(values, dtype=float).reshape(tuple(domains[v] for v in scope))
    return UAIFactor(scope, array.size, int(np.count_nonzero(array)), array)


def test_factor_scopes_and_primal_graph_preserve_high_order_identity() -> None:
    graph = primal_graph(((0, 1, 2),), 3)
    assert set(graph.edges()) == {(0, 1), (0, 2), (1, 2)}
    assert (0, 1, 2) != tuple(edge for edge in graph.edges())


def test_elimination_induced_scope_and_strategy_cost_differ() -> None:
    scopes = ((0, 1), (0, 2), (0, 3))
    domains = (2, 2, 2, 2)
    center_first = simulate_elimination(scopes, domains, (0, 1, 2, 3))
    center_last = simulate_elimination(scopes, domains, (1, 2, 3, 0))
    assert center_first.total_join_entries != center_last.total_join_entries
    assert center_first.order == (0, 1, 2, 3)


def test_exact_answer_is_independent_of_elimination_order() -> None:
    model = UAIModel(
        "MARKOV",
        (2, 2, 2),
        (
            _factor((0, 1), [1, 2, 3, 4]),
            _factor((1, 2), [2, 1, 4, 3]),
            _factor((0, 1, 2), list(range(1, 9))),
        ),
    )
    first = run_exact_elimination(model, (0, 1, 2))
    second = run_exact_elimination(model, (2, 1, 0))
    assert np.isclose(first.value, second.value)
    assert first.value > 0


def test_alpha_acyclicity_and_large_hyperedge_graph_distinction() -> None:
    assert is_alpha_acyclic(((0, 1, 2), (1, 2, 3), (2, 3, 4)))
    assert not is_alpha_acyclic(((0, 1), (1, 2), (0, 2)))
    scope = (tuple(range(7)),)
    graph = primal_graph(scope, 7)
    assert graph.number_of_edges() == 21
    assert is_alpha_acyclic(scope)


def test_classical_orders_are_deterministic() -> None:
    scopes = ((0, 1, 2), (2, 3), (3, 4))
    domains = (2, 3, 2, 4, 2)
    for strategy in ("min_fill", "weighted_min_fill", "min_degree", "min_factor_entries"):
        assert heuristic_order(scopes, domains, strategy) == heuristic_order(
            scopes, domains, strategy
        )


def test_uai_reader_preserves_scopes_tables_and_sparsity(tmp_path) -> None:
    path = tmp_path / "toy.uai"
    path.write_text(
        "MARKOV\n3\n2 2 2\n2\n2 0 1\n3 0 1 2\n"
        "4\n1 0 2 3\n8\n1 2 3 4 5 6 7 8\n",
        encoding="utf-8",
    )
    model = read_uai(path, load_values=True)
    assert model.scopes == ((0, 1), (0, 1, 2))
    assert model.factors[0].nonzero_count == 3
    assert model.factors[1].values is not None
    assert model.factors[1].values.shape == (2, 2, 2)
