import inspect

import networkx as nx
import numpy as np

from ahsl.acyclicity import running_intersection_violations
from ahsl.join_tree_estimators import AlternatingTreeIncidenceEstimator
from ahsl.synthetic import generate_alpha_acyclic_hypergraph
from ahsl.trees import generate_tree


def test_alternating_outputs_valid_trees_and_matching_connected_incidences() -> None:
    observed = np.random.default_rng(1).integers(0, 2, size=(12, 6), dtype=np.int8)
    model = AlternatingTreeIncidenceEstimator(0.2, 0.2, max_iterations=3).fit(observed)
    assert nx.is_tree(model.predict_tree())
    for tree, incidence in zip(
        model.decoded_trees_, model.decoded_incidences_, strict=True
    ):
        assert nx.is_tree(tree)
        assert running_intersection_violations(incidence, tree)[
            "num_violating_vertices"
        ] == 0
    assert np.array_equal(model.predict(), model.decoded_incidences_[-1])
    assert sorted(model.predict_tree().edges()) == sorted(model.decoded_trees_[-1].edges())


def test_alternating_unchanged_tree_stop_is_deterministic_on_zero_noise() -> None:
    generating_tree = generate_tree(8, "balanced", seed=3)
    clean = generate_alpha_acyclic_hypergraph(
        100, 8, generating_tree, 0.4, seed=7, simple_hypergraph=True
    )["incidence"]
    first = AlternatingTreeIncidenceEstimator(0.0, 0.0).fit(clean)
    second = AlternatingTreeIncidenceEstimator(0.0, 0.0).fit(clean)
    assert first.converged_
    assert first.num_iterations_ == 0
    assert not first.tree_changed_
    assert np.array_equal(first.predict(), clean)
    assert sorted(first.predict_tree().edges()) == sorted(second.predict_tree().edges())


def test_alternating_maximum_iteration_guard_preserves_final_tree_alignment() -> None:
    observed = np.random.default_rng(1).integers(0, 2, size=(12, 6), dtype=np.int8)
    model = AlternatingTreeIncidenceEstimator(0.2, 0.2, max_iterations=1).fit(observed)
    assert model.max_iteration_reached_
    assert model.num_iterations_ == 1
    assert model.tree_changed_
    assert sorted(model.predict_tree().edges()) == sorted(model.decoded_trees_[-1].edges())
    assert running_intersection_violations(model.predict(), model.predict_tree())[
        "num_violating_vertices"
    ] == 0


def test_alternating_fit_has_no_clean_target_argument() -> None:
    assert list(inspect.signature(AlternatingTreeIncidenceEstimator.fit).parameters) == [
        "self",
        "observed",
    ]
