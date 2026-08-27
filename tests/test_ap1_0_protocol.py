from __future__ import annotations

from pathlib import Path

from ap1_0.protocol import (
    UpdateBatch,
    apply_batch,
    apply_delta_rows,
    deterministic_edge_stream,
    normalize_rows,
    parse_committed_durations,
    parse_rust_duration,
    percentile,
    summarize_rss,
)


def test_update_stream_is_seed_deterministic() -> None:
    edges = {(0, 1), (1, 2), (2, 3)}
    first = deterministic_edge_stream(
        edges, batches=5, insert_count=2, delete_count=1, seed=20260827
    )
    second = deterministic_edge_stream(
        edges, batches=5, insert_count=2, delete_count=1, seed=20260827
    )
    assert first == second


def test_batch_construction_and_application() -> None:
    state = {("1", "2"), ("2", "3")}
    batch = UpdateBatch(inserts=(("3", "4"),), deletes=(("1", "2"),))
    assert apply_batch(state, batch) == {("2", "3"), ("3", "4")}


def test_snapshot_normalization_has_set_semantics() -> None:
    assert normalize_rows([(2, " a "), (1, "b"), (2, "a")]) == (
        ("1", "b"),
        ("2", "a"),
    )


def test_incremental_delta_reconstructs_exact_snapshot() -> None:
    initial = {("1",), ("2",)}
    assert apply_delta_rows(initial, [("2", "-1"), ("3", "+1")]) == {
        ("1",),
        ("3",),
    }


def test_toy_reachability_incremental_equals_exact_scratch() -> None:
    def closure(edges: set[tuple[str, str]]) -> set[tuple[str, str]]:
        reachable = set(edges)
        while True:
            expanded = reachable | {
                (left, right)
                for left, middle in reachable
                for middle2, right in edges
                if middle == middle2
            }
            if expanded == reachable:
                return reachable
            reachable = expanded

    before_edges = {("0", "1"), ("1", "2"), ("2", "3")}
    batch = UpdateBatch(inserts=(("1", "3"),), deletes=(("1", "2"),))
    after_edges = apply_batch(before_edges, batch)
    exact_after = closure(after_edges)
    before_result = closure(before_edges)
    delta = [(row + ("-1",)) for row in sorted(before_result - exact_after)]
    delta += [(row + ("+1",)) for row in sorted(exact_after - before_result)]
    assert apply_delta_rows(before_result, delta) == exact_after


def test_metric_parser_handles_flowlog_units() -> None:
    assert parse_rust_duration("2.5ms") == 2.5
    assert parse_rust_duration("750µs") == 0.75
    assert parse_rust_duration("750μs") == 0.75
    assert parse_rust_duration("1.2s") == 1200.0
    log = "1.0ms:\tCommitted & executed\n2s:\tCommitted & executed"
    assert parse_committed_durations(log) == [1.0, 2000.0]


def test_rss_parser_reports_first_and_peak() -> None:
    assert summarize_rss([1048576, 3145728, 2097152]) == (1.0, 3.0)


def test_percentile_parser() -> None:
    assert percentile([1, 2, 3, 4, 5], 0.5) == 3
    assert percentile([1, 2, 3, 4, 5], 0.99) == 4.96


def test_metadata_seed_is_frozen() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    workload_dir = repo_root / "experiments" / "ap1_0" / "workloads"
    assert {path.name for path in workload_dir.glob("*.dl")} == {
        "connected_components.dl",
        "ldbc_reachability.dl",
        "polonius_subset.dl",
        "reachability.dl",
        "sssp.dl",
    }
    assert (repo_root / "results" / "ap1_0" / "raw" / "run_manifest.json").read_text(
        encoding="utf-8"
    ).find('"seed": 20260827') >= 0
