from __future__ import annotations

from itertools import combinations

import numpy as np
import pytest

from temporal_group_structure.audits import (
    cardinality_summary,
    classify_event,
    prequential_classes,
    audit_test_events,
)
from temporal_group_structure.event_identity import TemporalEvent, event_identity
from temporal_group_structure.candidate_search import candidate_recall, cns_candidates, history_statistics
from temporal_group_structure.metrics import exact_set_metrics, member_metrics
from temporal_group_structure.negative_sampling import one_member_corruption, random_same_cardinality
from temporal_group_structure.recurrence import score_edge
from temporal_group_structure.splits import chronological_split, has_future_leakage


def event(timestamp: str, nodes: str, event_id: str) -> TemporalEvent:
    return TemporalEvent(timestamp, frozenset(nodes), event_id)


def test_exact_undirected_identity_is_permutation_invariant() -> None:
    assert event_identity(["a", "b", "c"]) == event_identity(["c", "a", "b"])


def test_directed_identity_preserves_tail_and_head_roles() -> None:
    forward = event_identity(["a", "b"], head_nodes=["c"])
    reverse = event_identity(["c"], head_nodes=["a", "b"])
    assert forward != reverse


def test_empty_event_is_rejected() -> None:
    with pytest.raises(ValueError):
        TemporalEvent("1", frozenset(), "0")


def test_chronological_split_keeps_timestamp_batches_together() -> None:
    events = [event(str(i // 2), chr(97 + i), str(i)) for i in range(10)]
    split = chronological_split(events, train_fraction=0.55, validation_fraction=0.20)
    assert split.train[-1].timestamp != split.validation[0].timestamp
    assert split.validation[-1].timestamp != split.test[0].timestamp


def test_chronological_split_has_no_future_leakage() -> None:
    events = [event(f"{i:02d}", "ab", str(i)) for i in range(20)]
    assert not has_future_leakage(chronological_split(events))


@pytest.mark.parametrize(
    ("nodes", "expected"),
    [
        (frozenset("abc"), "EXACT_REPEAT"),
        (frozenset("abd"), "PARTIAL_REPEAT"),
        (frozenset("de"), "NOVEL_COMBINATION"),
        (frozenset("ax"), "CONTAINS_NEW_NODE"),
        (frozenset("xy"), "ALL_NEW_TOGETHER"),
    ],
)
def test_repeat_and_churn_classification(nodes: frozenset[str], expected: str) -> None:
    assert classify_event(nodes, {frozenset("abc")}, set("abcde")) == expected


def test_equal_time_events_do_not_leak_into_each_other() -> None:
    history = [event("0", "ab", "0")]
    test = [event("1", "cd", "1"), event("1", "cd", "2"), event("2", "cd", "3")]
    assert prequential_classes(history, test) == [
        "ALL_NEW_TOGETHER",
        "ALL_NEW_TOGETHER",
        "EXACT_REPEAT",
    ]


def test_cardinality_statistics() -> None:
    events = [event("0", "ab", "0"), event("1", "abc", "1"), event("2", "abcd", "2")]
    stats = cardinality_summary(events)
    assert stats["median_size"] == 3
    assert stats["size_ge3_fraction"] == pytest.approx(2 / 3)
    assert stats["size_ge4_fraction"] == pytest.approx(1 / 3)


def test_initial_history_repeat_rate_is_separate_from_prequential_rate() -> None:
    history = [event("0", "ab", "0")]
    test = [event("1", "cd", "1"), event("2", "cd", "2")]
    audit = audit_test_events(history, test)
    assert audit["exact_repeat_rate"] == pytest.approx(0.5)
    assert audit["exact_in_initial_history_rate"] == 0


def test_initial_history_and_prequential_node_churn_are_separate() -> None:
    history = [event("0", "ab", "0")]
    test = [event("1", "cd", "1"), event("2", "ce", "2")]
    audit = audit_test_events(history, test)
    assert audit["new_node_event_rate"] == 1
    assert audit["all_new_event_rate"] == pytest.approx(0.5)
    assert audit["initial_history_all_new_event_rate"] == 1


def test_toy_full_set_universe_has_expected_size() -> None:
    nodes = "abcd"
    universe = {frozenset(group) for size in (2, 3) for group in combinations(nodes, size)}
    assert len(universe) == 10


def test_candidate_generation_contains_expected_one_member_replacement() -> None:
    history = [event("0", "abc", "0"), event("1", "abd", "1"), event("2", "acd", "2")]
    candidates = cns_candidates(history, source_limit=10, replacements_per_slot=5)
    assert frozenset("bcd") in candidates


def test_candidate_recall_counts_only_exact_sets() -> None:
    truth = [event("0", "abc", "0"), event("1", "abd", "1")]
    assert candidate_recall(truth, {frozenset("abc")}) == 0.5


def test_negative_samplers_preserve_cardinality_and_avoid_forbidden() -> None:
    rng = np.random.default_rng(7)
    positive = frozenset("abc")
    forbidden = {positive}
    for sampler in (random_same_cardinality, one_member_corruption):
        negative = sampler(positive, list("abcdef"), forbidden, rng)
        assert len(negative) == len(positive)
        assert negative not in forbidden


def test_exact_set_metrics_do_not_award_partial_overlap() -> None:
    truth = [event("0", "abc", "0")]
    metrics = exact_set_metrics(truth, [frozenset("abd"), frozenset("abc")])
    assert metrics["hit_at_1"] == 0
    assert metrics["mrr"] == 0.5


def test_member_level_metrics_are_secondary_partial_credit() -> None:
    metrics = member_metrics(frozenset("abc"), frozenset("abd"))
    assert metrics["jaccard"] == 0.5
    assert metrics["member_f1"] == pytest.approx(2 / 3)


def test_pairwise_projection_cannot_distinguish_equal_pair_sums() -> None:
    history = [event("0", "abc", "0"), event("1", "abd", "1")]
    stats = history_statistics(history)
    assert score_edge(frozenset("acd"), stats, "pair_sum") == score_edge(
        frozenset("bcd"), stats, "pair_sum"
    )


def test_recurrence_scores_are_deterministic() -> None:
    history = [event("0", "ab", "0"), event("1", "ab", "1"), event("2", "ac", "2")]
    stats = history_statistics(history)
    assert score_edge(frozenset("ab"), stats, "exact_frequency") == 2
    assert score_edge(frozenset("ac"), stats, "most_recent") > score_edge(
        frozenset("ab"), stats, "most_recent"
    )


def test_candidate_preprocessing_is_deterministic() -> None:
    history = [event("0", "abc", "0"), event("1", "abd", "1"), event("2", "acd", "2")]
    assert cns_candidates(history) == cns_candidates(history)
