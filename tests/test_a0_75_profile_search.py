import inspect

import networkx as nx
import numpy as np

from ahsl.join_tree_estimators import ProfileLikelihoodTreeSearch


def test_profile_search_is_deterministic_and_non_decreasing() -> None:
    observed = np.random.default_rng(8).integers(0, 2, size=(20, 7), dtype=np.int8)
    first = ProfileLikelihoodTreeSearch(
        0.2, 0.2, max_iterations=3, max_candidates_per_iteration=8
    ).fit(observed)
    second = ProfileLikelihoodTreeSearch(
        0.2, 0.2, max_iterations=3, max_candidates_per_iteration=8
    ).fit(observed)
    assert nx.is_tree(first.predict_tree())
    assert first.profile_objective_ >= first.initial_profile_objective_ - 1e-12
    assert sorted(first.predict_tree().edges()) == sorted(second.predict_tree().edges())
    assert np.array_equal(first.predict(), second.predict())


def test_profile_search_fit_uses_only_observations() -> None:
    assert list(inspect.signature(ProfileLikelihoodTreeSearch.fit).parameters) == [
        "self",
        "observed",
    ]
