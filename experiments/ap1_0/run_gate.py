"""Run the bounded AP1.0 FlowLog incremental-versus-scratch gate.

This is an experiment adapter, not a query optimizer.  It freezes inputs,
compiles the same Datalog program in FlowLog's incremental and batch modes,
checks every incremental epoch against a fresh same-engine recomputation, and
records per-batch latency and Windows working-set samples.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime
import json
import os
from pathlib import Path
import queue
import random
import shutil
import statistics
import subprocess
import threading
import time
from typing import Iterable

import psutil

from ap1_0.protocol import UpdateBatch, apply_batch, apply_delta_rows, percentile


SEED = 20260827
FLOWLOG_COMMIT = "6c111b729e4bf8bffb5037b85b894031786140cc"
FELDERA_COMMIT = "718320cf1deb49c51f8528f2469fbfc7aac995db"
FLOWLOG_BENCH_COMMIT = "2db7c2eab9f64852242a1691b51707f3fb3454ff"
POLONIUS_COMMIT = "d099f36b2c2d8ca531f994fbc2b555732962cbd6"
LDBC_EXAMPLE_COMMIT = "647eed01859e2115cb06e2a4bda98235943a308f"
RAW_FIELDS = [
    "system", "commit", "workload", "workload_class", "evidence_route",
    "scale", "update_regime", "batch_size", "insert_count", "delete_count",
    "workers", "repeat", "batch", "measured", "correct", "compile_ms",
    "initial_load_ms", "initial_fixpoint_ms", "initial_ms", "update_ms",
    "p50_ms", "p95_ms", "p99_ms", "mean_ms", "throughput",
    "rss_load_peak_mb", "rss_steady_mb", "rss_update_peak_mb", "rss_post_mb",
    "engine_state_mb", "derived_changes", "retractions", "rederivations",
    "observed_output_changes", "observed_output_retractions",
    "iterations", "worker_utilization", "cpu_ms", "timeout", "oom", "notes",
]


@dataclass(frozen=True)
class Workload:
    name: str
    workload_class: str
    evidence_route: str
    program: str
    relations: tuple[str, ...]
    outputs: tuple[str, ...]


WORKLOADS = {
    "reachability": Workload(
        "reachability", "reachability", "A_FLOWLOG_SUITE", "reachability.dl",
        ("Source", "Arc"), ("Reach",),
    ),
    "sssp": Workload(
        "sssp", "weighted_recursive_aggregate", "A_FLOWLOG_SUITE", "sssp.dl",
        ("Source", "Arc"), ("Distance",),
    ),
    "connected_components": Workload(
        "connected_components", "recursive_aggregate", "A_FLOWLOG_SUITE",
        "connected_components.dl", ("Arc",), ("Component",),
    ),
    "polonius_subset": Workload(
        "polonius_subset", "program_analysis", "A_FLOWLOG_SUITE",
        "polonius_subset.dl",
        ("subset_base", "cfg_edge", "loan_issued_at", "loan_invalidated_at", "universal_region"),
        ("subset", "loan_live_at", "errors"),
    ),
    "ldbc_reachability": Workload(
        "ldbc_reachability", "reachability", "B_LDBC_OFFICIAL_EXAMPLE",
        "ldbc_reachability.dl", ("Knows",), ("Reach",),
    ),
}


def write_relation(path: Path, rows: Iterable[tuple[str, ...]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerows(sorted(set(rows)))


def read_relation(path: Path, *, incremental: bool = False) -> list[tuple[str, ...]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [tuple(row) for row in csv.reader(handle, delimiter="\t") if row]


def graph_edges(n: int, extra_per_node: int, seed: int) -> set[tuple[str, ...]]:
    rng = random.Random(seed)
    edges = {(str(i), str(i + 1)) for i in range(n - 1)}
    for src in range(n):
        for _ in range(extra_per_node):
            dst = rng.randrange(n)
            if src != dst:
                edges.add((str(src), str(dst)))
    return edges


def graph_batches(
    base: set[tuple[str, ...]], *, count: int, inserts: int, deletes: int, seed: int,
    weighted: bool = False,
) -> list[UpdateBatch]:
    rng = random.Random(seed)
    current = set(base)
    max_node = max(int(row[1]) for row in current)
    batches: list[UpdateBatch] = []
    for batch_index in range(count):
        chosen_deletes = rng.sample(sorted(current), min(deletes, len(current)))
        for row in chosen_deletes:
            current.remove(row)
        chosen_inserts: list[tuple[str, ...]] = []
        for offset in range(inserts):
            src = rng.randrange(max_node + 1)
            dst = rng.randrange(max_node + 1)
            if src == dst:
                dst = (dst + 1) % (max_node + 1)
            if weighted:
                row = (str(src), str(dst), str(1 + ((batch_index + offset) % 9)))
            else:
                row = (str(src), str(dst))
            while row in current:
                dst = (dst + 1) % (max_node + 1)
                row = (str(src), str(dst), row[-1]) if weighted else (str(src), str(dst))
            current.add(row)
            chosen_inserts.append(row)
        batches.append(UpdateBatch(tuple(chosen_inserts), tuple(chosen_deletes)))
    return batches


def prepare_graph_case(workload: Workload, scale: str, regime: str) -> tuple[dict[str, set[tuple[str, ...]]], list[UpdateBatch], str]:
    n = 400 if scale == "small" else 1500
    base_edges = graph_edges(n, 2, SEED + n)
    if workload.name == "sssp":
        weighted = {(a, b, str(1 + (int(a) * 7 + int(b)) % 9)) for a, b in base_edges}
        base = {"Source": {("0",)}, "Arc": weighted}
        batches = graph_batches(
            weighted, count=6, inserts=8 if scale == "small" else 30,
            deletes=(8 if regime == "realistic_mixed" else 35),
            seed=SEED + 11, weighted=True,
        )
    else:
        base = {"Arc": base_edges}
        if workload.name == "reachability":
            base["Source"] = {("0",)}
        batches = graph_batches(
            base_edges, count=6,
            inserts=(8 if regime == "realistic_mixed" else 0),
            deletes=(8 if regime == "realistic_mixed" else 35),
            seed=SEED + (17 if workload.name == "reachability" else 23),
        )
    note = "deterministic sparse graph; realistic_mixed uses sub-1% balanced churn"
    if regime == "delete_heavy_stress":
        note = "deterministic sparse graph; deletion-only stress intervention"
    return base, batches, note


def facts_rows(path: Path) -> set[tuple[str, ...]]:
    rows: set[tuple[str, ...]] = set()
    if not path.exists():
        return rows
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.rstrip("\r\n")
            if line:
                rows.add(tuple(line.split("\t")))
    return rows


def prepare_polonius_case(polonius_root: Path) -> tuple[dict[str, set[tuple[str, ...]]], list[UpdateBatch], str]:
    source = polonius_root / "inputs" / "vec-push-ref" / "nll-facts" / "foo1"
    mapping = {
        "subset_base": "subset_base.facts",
        "cfg_edge": "cfg_edge.facts",
        "loan_issued_at": "loan_issued_at.facts",
        "loan_invalidated_at": "loan_invalidated_at.facts",
        "universal_region": "universal_region.facts",
    }
    base = {relation: facts_rows(source / filename) for relation, filename in mapping.items()}
    cfg_rows = sorted(base["cfg_edge"])
    batches = []
    for i in range(6):
        deleted = (cfg_rows[(i * 7) % len(cfg_rows)],)
        inserted = ((deleted[0][1], deleted[0][0]),)
        batches.append(UpdateBatch(inserted, deleted))
        base["cfg_edge"].remove(deleted[0])
        base["cfg_edge"].add(inserted[0])
    # Rewind to the pre-stream state.
    for batch in reversed(batches):
        base["cfg_edge"].discard(batch.inserts[0])
        base["cfg_edge"].add(batch.deletes[0])
    return base, batches, "real rust-lang/polonius vec-push-ref/foo1 facts; synthesized local CFG deltas"


def prepare_ldbc_case(ldbc_root: Path) -> tuple[dict[str, set[tuple[str, ...]]], list[UpdateBatch], str]:
    edge_file = ldbc_root / "data" / "raw" / "dynamic" / "Person_knows_Person.csv"
    person_file = ldbc_root / "data" / "raw" / "dynamic" / "Person.csv"
    with edge_file.open(newline="", encoding="utf-8") as handle:
        edges = list(csv.DictReader(handle, delimiter="|"))
    with person_file.open(newline="", encoding="utf-8") as handle:
        persons = list(csv.DictReader(handle, delimiter="|"))
    years = range(2010, 2016)
    state: set[tuple[str, ...]] = set()
    batches: list[UpdateBatch] = []
    deleted_people: set[str] = set()
    for year in years:
        inserted = {
            (row["Person1.id"], row["Person2.id"])
            for row in edges
            if int(row["creationDate"][:4]) == year
        }
        newly_deleted_people = {
            row["id"] for row in persons
            if row["explicitlyDeleted"] == "true" and int(row["deletionDate"][:4]) == year
        }
        deleted_people.update(newly_deleted_people)
        explicit_edges = {
            (row["Person1.id"], row["Person2.id"])
            for row in edges
            if row["explicitlyDeleted"] == "true" and int(row["deletionDate"][:4]) == year
        }
        cascaded = {edge for edge in state if any(node in deleted_people for node in edge)}
        deleted = explicit_edges | cascaded
        state.difference_update(deleted)
        state.update(inserted)
        batches.append(UpdateBatch(tuple(sorted(inserted)), tuple(sorted(deleted))))
    return {"Knows": set()}, batches, "official LDBC SNB temporal example; person delete cascades to incident knows edges"


def make_case(
    workload: Workload, scale: str, regime: str, polonius_root: Path, ldbc_root: Path,
) -> tuple[dict[str, set[tuple[str, ...]]], list[UpdateBatch], str]:
    if workload.name == "polonius_subset":
        return prepare_polonius_case(polonius_root)
    if workload.name == "ldbc_reachability":
        return prepare_ldbc_case(ldbc_root)
    return prepare_graph_case(workload, scale, regime)


def parse_runtime_phases(log: str) -> tuple[float | None, float | None, float | None]:
    load_ms = 0.0
    assembled = None
    for line in log.splitlines():
        if ":\tData loaded for " in line:
            load_ms += parse_duration(line.split(":\t", 1)[0])
        elif ":\tDataflow assembled" in line:
            assembled = parse_duration(line.split(":\t", 1)[0])
            break
    if assembled is None:
        return (load_ms or None, None, None)
    return load_ms, max(0.0, assembled - load_ms), assembled


def parse_duration(text: str) -> float:
    value = text.strip()
    import re

    match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)(.+)", value)
    if match:
        number, unit = float(match.group(1)), match.group(2)
        if unit == "ns":
            return number * 1e-6
        if unit == "ms":
            return number
        if unit == "s":
            return number * 1000.0
        if unit == "us" or (len(unit) <= 2 and unit.endswith("s")):
            return number * 1e-3
    raise ValueError(value)


def rss_mb(process: psutil.Process) -> float:
    return process.memory_info().rss / (1024.0 * 1024.0)


def compile_program(
    compiler: Path, program: Path, facts: Path, out: Path, binary: Path, mode: str,
    env: dict[str, str],
) -> tuple[float, str]:
    binary.parent.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    command = [
        str(compiler), str(program), "-F", str(facts), "-D", str(out),
        "-o", str(binary), "--mode", mode, "-P",
    ]
    started = time.perf_counter()
    result = subprocess.run(command, text=True, capture_output=True, env=env, timeout=900)
    elapsed = (time.perf_counter() - started) * 1000.0
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    binary.with_suffix(binary.suffix + ".compile.json").write_text(
        json.dumps({"compile_ms": elapsed, "command": command}, indent=2),
        encoding="utf-8",
    )
    return elapsed, result.stdout + result.stderr


def prior_compile_ms(binary: Path) -> float | str:
    metadata = binary.with_suffix(binary.suffix + ".compile.json")
    if not metadata.exists():
        return "NA"
    return float(json.loads(metadata.read_text(encoding="utf-8"))["compile_ms"])


def _reader(pipe, messages: queue.Queue[str], transcript: list[str]) -> None:
    for line in iter(pipe.readline, ""):
        transcript.append(line)
        messages.put(line)


def run_incremental(
    binary: Path, workdir: Path, output_dir: Path, facts_dir: Path,
    workload: Workload, batches: list[UpdateBatch], workers: int,
    relation_for_updates: str,
) -> tuple[list[dict[str, object]], dict[str, set[tuple[str, ...]]], str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    for old_output in output_dir.glob("*"):
        if old_output.is_file():
            old_output.unlink()
    process = subprocess.Popen(
        [str(binary), "-w", str(workers)], cwd=workdir, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,
    )
    ps_process = psutil.Process(process.pid)
    messages: queue.Queue[str] = queue.Queue()
    transcript: list[str] = []
    reader = threading.Thread(target=_reader, args=(process.stdout, messages, transcript), daemon=True)
    reader.start()
    load_samples: list[float] = []
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        try:
            load_samples.append(rss_mb(ps_process))
        except psutil.Error:
            pass
        try:
            line = messages.get(timeout=0.005)
        except queue.Empty:
            continue
        if "Dataflow assembled" in line:
            break
    else:
        process.kill()
        raise TimeoutError("incremental initialization did not finish")
    time.sleep(0.02)
    steady = rss_mb(ps_process)
    snapshots: dict[str, set[tuple[str, ...]]] = {name: set() for name in workload.outputs}
    for output in workload.outputs:
        for row in read_relation(output_dir / f"{output}_t1.csv", incremental=True):
            snapshots[output] = apply_delta_rows(snapshots[output], [row])

    records: list[dict[str, object]] = []
    for batch_index, batch in enumerate(batches):
        insert_path = workdir / f"batch_{batch_index}_insert.csv"
        delete_path = workdir / f"batch_{batch_index}_delete.csv"
        write_relation(insert_path, batch.inserts)
        write_relation(delete_path, batch.deletes)
        commands = ["begin"]
        if batch.deletes:
            commands.append(f'file {relation_for_updates} "{delete_path}" -1')
        if batch.inserts:
            commands.append(f'file {relation_for_updates} "{insert_path}" +1')
        commands.append("commit")
        process.stdin.write("\n".join(commands) + "\n")
        process.stdin.flush()
        samples: list[float] = []
        duration = None
        deadline = time.monotonic() + 120
        while time.monotonic() < deadline:
            try:
                samples.append(rss_mb(ps_process))
            except psutil.Error:
                pass
            try:
                line = messages.get(timeout=0.003)
            except queue.Empty:
                continue
            if ":\tCommitted & executed" in line:
                duration = parse_duration(line.split(":\t", 1)[0].split(">>")[-1].strip())
                break
        if duration is None:
            process.kill()
            raise TimeoutError(f"incremental batch {batch_index} did not finish")
        time.sleep(0.01)
        post = rss_mb(ps_process)
        observed_output_changes = 0
        observed_output_retractions = 0
        for output in workload.outputs:
            delta_path = output_dir / f"{output}_t{batch_index + 2}.csv"
            delta_rows = read_relation(delta_path, incremental=True)
            snapshots[output] = apply_delta_rows(snapshots[output], delta_rows)
            observed_output_changes += sum(abs(int(row[-1])) for row in delta_rows)
            observed_output_retractions += sum(
                abs(int(row[-1])) for row in delta_rows if int(row[-1]) < 0
            )
        records.append({
            "batch": batch_index, "update_ms": duration,
            "rss_load_peak_mb": max(load_samples) if load_samples else "NA",
            "rss_steady_mb": steady,
            "rss_update_peak_mb": max([post, *samples]),
            "rss_post_mb": post,
            "observed_output_changes": observed_output_changes,
            "observed_output_retractions": observed_output_retractions,
        })
    process.stdin.write("quit\n")
    process.stdin.flush()
    process.wait(timeout=30)
    return records, snapshots, "".join(transcript)


def run_scratch(
    binary: Path, workdir: Path, output_dir: Path, workload: Workload, workers: int,
) -> tuple[float, list[float], dict[str, set[tuple[str, ...]]], str]:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    started = time.perf_counter()
    process = subprocess.Popen(
        [str(binary), "-w", str(workers)], cwd=workdir,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    ps_process = psutil.Process(process.pid)
    samples: list[float] = []
    while process.poll() is None:
        try:
            samples.append(rss_mb(ps_process))
        except psutil.Error:
            pass
        time.sleep(0.002)
    transcript = process.stdout.read()
    elapsed = (time.perf_counter() - started) * 1000.0
    if process.returncode:
        raise RuntimeError(transcript)
    snapshots = {
        output: set(read_relation(output_dir / f"{output}.csv"))
        for output in workload.outputs
    }
    return elapsed, samples, snapshots, transcript


def base_row(
    workload: Workload, scale: str, regime: str, workers: int, repeat: int,
    batch_index: int, batch: UpdateBatch, method: str, compile_ms: float | str,
) -> dict[str, object]:
    row = {field: "NA" for field in RAW_FIELDS}
    row.update({
        "system": f"FlowLog_{method}", "commit": FLOWLOG_COMMIT,
        "workload": workload.name, "workload_class": workload.workload_class,
        "evidence_route": workload.evidence_route, "scale": scale,
        "update_regime": regime, "batch_size": len(batch.inserts) + len(batch.deletes),
        "insert_count": len(batch.inserts), "delete_count": len(batch.deletes),
        "workers": workers, "repeat": repeat, "batch": batch_index,
        "measured": batch_index > 0,
        "compile_ms": round(compile_ms, 3) if isinstance(compile_ms, float) else compile_ms,
        "timeout": False, "oom": False,
    })
    return row


def execute_case(
    workload: Workload, scale: str, regime: str, workers: int, repeats: int,
    compiler: Path, workload_dir: Path, run_root: Path, external_root: Path,
    env: dict[str, str],
    compile_cache: dict[
        str, tuple[Path, Path, Path, Path, float | str, float | str]
    ],
) -> list[dict[str, object]]:
    facts_dir = run_root / "facts" / workload.name
    output_base = run_root / "engine_output" / workload.name
    facts_dir.mkdir(parents=True, exist_ok=True)
    base, batches, case_note = make_case(
        workload, scale, regime, external_root / "polonius",
        external_root / "ldbc_snb_example_data",
    )
    for relation, rows in base.items():
        write_relation(facts_dir / f"{relation}.csv", rows)

    if workload.name not in compile_cache:
        binaries = run_root / "bin"
        inc = binaries / f"{workload.name}_inc.exe"
        batch = binaries / f"{workload.name}_batch.exe"
        fixed_inc_out = output_base / "incremental"
        fixed_batch_out = output_base / "recompute"
        if inc.exists() and batch.exists():
            inc_compile = prior_compile_ms(inc)
            batch_compile = prior_compile_ms(batch)
        else:
            inc_compile, _ = compile_program(
                compiler, workload_dir / workload.program, facts_dir,
                fixed_inc_out, inc, "datalog-inc", env,
            )
            batch_compile, _ = compile_program(
                compiler, workload_dir / workload.program, facts_dir,
                fixed_batch_out, batch, "datalog-batch", env,
            )
        compile_cache[workload.name] = (
            inc, batch, fixed_inc_out, fixed_batch_out, inc_compile, batch_compile,
        )
    (
        inc_binary, batch_binary, fixed_inc_out, fixed_batch_out,
        inc_compile_ms, batch_compile_ms,
    ) = compile_cache[workload.name]

    rows: list[dict[str, object]] = []
    update_relation = "cfg_edge" if workload.name == "polonius_subset" else (
        "Knows" if workload.name == "ldbc_reachability" else "Arc"
    )
    for repeat in range(repeats):
        current = {relation: set(values) for relation, values in base.items()}
        for relation, values in current.items():
            write_relation(facts_dir / f"{relation}.csv", values)
        inc_work = run_root / "work" / f"{workload.name}_{scale}_{regime}_w{workers}_r{repeat}_inc"
        inc_out = fixed_inc_out
        inc_work.mkdir(parents=True, exist_ok=True)
        inc_records, _, inc_log = run_incremental(
            inc_binary, inc_work, inc_out, facts_dir, workload, batches, workers,
            update_relation,
        )
        load_ms, fixpoint_ms, initial_ms = parse_runtime_phases(inc_log)
        for batch_index, batch_delta in enumerate(batches):
            current[update_relation] = apply_batch(current[update_relation], batch_delta)
            write_relation(facts_dir / f"{update_relation}.csv", current[update_relation])
            scratch_work = run_root / "work" / f"{workload.name}_{scale}_{regime}_w{workers}_r{repeat}_b{batch_index}_scratch"
            scratch_out = fixed_batch_out
            scratch_work.mkdir(parents=True, exist_ok=True)
            scratch_ms, scratch_samples, scratch_snapshot, scratch_log = run_scratch(
                batch_binary, scratch_work, scratch_out, workload, workers,
            )
            s_load, s_fixpoint, s_initial = parse_runtime_phases(scratch_log)
            # Reconstruct the incremental snapshot from epoch deltas up to this batch.
            inc_snapshot: dict[str, set[tuple[str, ...]]] = {name: set() for name in workload.outputs}
            for output in workload.outputs:
                for epoch in range(1, batch_index + 3):
                    inc_snapshot[output] = apply_delta_rows(
                        inc_snapshot[output],
                        read_relation(inc_out / f"{output}_t{epoch}.csv", incremental=True),
                    )
            correct = all(inc_snapshot[name] == scratch_snapshot[name] for name in workload.outputs)

            inc_row = base_row(
                workload, scale, regime, workers, repeat, batch_index, batch_delta,
                "incremental", inc_compile_ms,
            )
            inc_row.update(inc_records[batch_index])
            inc_row.update({
                "correct": correct, "initial_load_ms": round(load_ms, 3) if load_ms is not None else "NA",
                "initial_fixpoint_ms": round(fixpoint_ms, 3) if fixpoint_ms is not None else "NA",
                "initial_ms": round(initial_ms, 3) if initial_ms is not None else "NA",
                "throughput": round((len(batch_delta.inserts) + len(batch_delta.deletes)) / (inc_records[batch_index]["update_ms"] / 1000), 3) if inc_records[batch_index]["update_ms"] else "NA",
                "notes": case_note,
            })
            scratch_row = base_row(
                workload, scale, regime, workers, repeat, batch_index, batch_delta,
                "recompute", batch_compile_ms,
            )
            scratch_row.update({
                "correct": correct, "initial_load_ms": round(s_load, 3) if s_load is not None else "NA",
                "initial_fixpoint_ms": round(s_fixpoint, 3) if s_fixpoint is not None else "NA",
                "initial_ms": round(s_initial, 3) if s_initial is not None else "NA",
                "update_ms": round(scratch_ms, 3),
                "throughput": round((len(batch_delta.inserts) + len(batch_delta.deletes)) / (scratch_ms / 1000), 3) if scratch_ms else "NA",
                "rss_load_peak_mb": round(max(scratch_samples), 3) if scratch_samples else "NA",
                "rss_update_peak_mb": round(max(scratch_samples), 3) if scratch_samples else "NA",
                "rss_post_mb": round(scratch_samples[-1], 3) if scratch_samples else "NA",
                "observed_output_changes": "NA",
                "observed_output_retractions": "NA",
                "notes": case_note + "; scratch post RSS is last pre-exit sample",
            })
            rows.extend((inc_row, scratch_row))
    return rows


def add_group_summaries(rows: list[dict[str, object]]) -> None:
    groups: dict[tuple[object, ...], list[dict[str, object]]] = {}
    keys = ("system", "workload", "scale", "update_regime", "workers")
    for row in rows:
        if row["measured"] is True:
            groups.setdefault(tuple(row[key] for key in keys), []).append(row)
    for group_rows in groups.values():
        values = [float(row["update_ms"]) for row in group_rows]
        summary = {
            "p50_ms": round(percentile(values, 0.50), 3),
            "p95_ms": round(percentile(values, 0.95), 3),
            "p99_ms": round(percentile(values, 0.99), 3),
            "mean_ms": round(statistics.fmean(values), 3),
        }
        for row in group_rows:
            row.update(summary)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--flowlog-compiler", type=Path, required=True)
    parser.add_argument("--external-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, default=Path("results/ap1_0"))
    parser.add_argument("--matrix", choices=("pilot", "gate"), default="gate")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    workload_dir = Path(__file__).resolve().parent / "workloads"
    output_root = (repo_root / args.output_root).resolve() if not args.output_root.is_absolute() else args.output_root
    run_root = output_root / "runtime"
    env = os.environ.copy()
    winlibs = args.external_root / "winlibs" / "mingw64" / "bin"
    cargo = args.external_root / "cargo" / "bin"
    env["PATH"] = os.pathsep.join((str(winlibs), str(cargo), env.get("PATH", "")))
    env["RUSTUP_HOME"] = str(args.external_root / "rustup")
    env["CARGO_HOME"] = str(args.external_root / "cargo")

    matrix = [
        ("reachability", "small", "realistic_mixed", 1, 3),
        ("sssp", "small", "realistic_mixed", 1, 1),
        ("connected_components", "small", "realistic_mixed", 1, 3),
        ("polonius_subset", "real", "realistic_mixed", 1, 3),
        ("ldbc_reachability", "official_toy", "native_temporal", 1, 3),
    ]
    if args.matrix == "gate":
        matrix += [
            ("reachability", "medium", "realistic_mixed", 1, 3),
            ("connected_components", "medium", "realistic_mixed", 1, 3),
            ("reachability", "small", "delete_heavy_stress", 1, 1),
            ("connected_components", "small", "delete_heavy_stress", 1, 1),
            ("reachability", "small", "realistic_mixed", 4, 1),
            ("connected_components", "small", "realistic_mixed", 4, 1),
        ]

    all_rows: list[dict[str, object]] = []
    compile_cache: dict[
        str, tuple[Path, Path, Path, Path, float | str, float | str]
    ] = {}
    started = time.perf_counter()
    for name, scale, regime, workers, repeats in matrix:
        print(f"[AP1.0] {name} scale={scale} regime={regime} workers={workers} repeats={repeats}", flush=True)
        all_rows.extend(execute_case(
            WORKLOADS[name], scale, regime, workers, repeats,
            args.flowlog_compiler.resolve(), workload_dir, run_root,
            args.external_root.resolve(), env, compile_cache,
        ))
    add_group_summaries(all_rows)
    raw_dir = output_root / "raw"
    write_csv(raw_dir / "raw_runs.csv", RAW_FIELDS, all_rows)
    metadata_detail = {
        "reachability": (
            "FlowLog public-suite query route", FLOWLOG_BENCH_COMMIT, "Apache-2.0",
            "semantics retained; deterministic sparse directed graph generated locally",
            "small n=400; medium n=1500",
            "6 batches; balanced sub-1% mixed or concentrated delete stress", "synthesized",
        ),
        "sssp": (
            "FlowLog public-suite query route", FLOWLOG_BENCH_COMMIT, "Apache-2.0",
            "semantics retained; deterministic positive integer weights", "small n=400",
            "6 balanced sub-1% mixed batches", "synthesized",
        ),
        "connected_components": (
            "FlowLog public-suite query route", FLOWLOG_BENCH_COMMIT, "Apache-2.0",
            "semantics retained; deterministic sparse graph generated locally",
            "small n=400; medium n=1500",
            "6 batches; balanced sub-1% mixed or concentrated delete stress", "synthesized",
        ),
        "polonius_subset": (
            "Rust Polonius official input fixture", POLONIUS_COMMIT, "Apache-2.0 OR MIT",
            "selected inputs/vec-push-ref/nll-facts/foo1; tab facts converted to relation CSV; rules unchanged",
            "real official fixture", "6 deterministic local CFG/subset deltas",
            "synthesized_over_real_fixture",
        ),
        "ldbc_reachability": (
            "LDBC SNB official example data", LDBC_EXAMPLE_COMMIT, "Apache-2.0",
            "Person_knows_Person.csv temporal edges; minimal undirected recursive reachability translation",
            "official toy 5 persons", "6 annual temporal batches 2010-2015 including person-delete cascade",
            "native_temporal_extracted",
        ),
    }
    workload_rows = []
    for name, workload in WORKLOADS.items():
        source, version, license_name, preprocessing, scale_note, updates, origin = metadata_detail[name]
        workload_rows.append({
            "workload": name, "class": workload.workload_class,
            "evidence_route": workload.evidence_route, "program": workload.program,
            "source": source, "source_version": version, "license": license_name,
            "preprocessing": preprocessing, "scale": scale_note,
            "update_generation": updates, "update_origin": origin,
            "relations": ";".join(workload.relations), "outputs": ";".join(workload.outputs),
            "seed": SEED,
        })
    write_csv(
        raw_dir / "workload_metadata.csv",
        [
            "workload", "class", "evidence_route", "program", "source", "source_version",
            "license", "preprocessing", "scale", "update_generation", "update_origin",
            "relations", "outputs", "seed",
        ],
        workload_rows,
    )
    machine = "Intel Core i9-13900H; 14 cores; 20 logical; 31.64 GiB RAM"
    os_freeze = "Windows 11 Home Chinese 10.0.26200 x64"
    run_date = datetime.now().astimezone().isoformat()
    system_rows = [
        {
            "system": "FlowLog", "repository": "https://github.com/flowlog-rs/flowlog.git",
            "version_tag": "flowlog-compiler-v0.5.0; flowlog-runtime-v0.3.0; flowlog-build-v0.4.0",
            "commit": FLOWLOG_COMMIT, "build_status": "SUCCESS",
            "build_command": "cargo +1.89.0 build --release --locked; flowlog-compiler PROGRAM -F FACTS -D OUTPUT -o BINARY --mode datalog-inc|datalog-batch -P",
            "compiler_runtime": "rustc 1.89.0 (29483883e 2025-08-04); GCC 16.2.0 MinGW-w64 UCRT",
            "engine_dependencies": "differential-dataflow 0.25.1; timely 0.31.0",
            "feature_and_optimization_flags": "release; locked; profiling enabled; workers 1 or 4",
            "hardware": machine, "os": os_freeze, "run_date": run_date,
            "notes": "Executed same-engine datalog-inc and datalog-batch controls",
        },
        {
            "system": "Feldera_DBSP", "repository": "https://github.com/feldera/feldera.git",
            "version_tag": "v0.338.0", "commit": FELDERA_COMMIT,
            "build_status": "BLOCKED_NATIVE_WINDOWS",
            "build_command": "cargo +1.93.1 build --release --locked -p dbsp --tests (CFLAGS=-std=gnu11; modern MinGW first on PATH)",
            "compiler_runtime": "rustc 1.93.1 (01f6ddf75 2026-02-11); GCC 16.2.0 MinGW-w64 UCRT",
            "engine_dependencies": "pinned Cargo.lock",
            "feature_and_optimization_flags": "release; locked; default dbsp features",
            "hardware": machine, "os": os_freeze, "run_date": run_date,
            "notes": "feldera-samply imports nix clock_gettime/getpid unavailable on native Windows; WSL service unavailable; audit only",
        },
    ]
    write_csv(
        raw_dir / "system_metadata.csv",
        [
            "system", "repository", "version_tag", "commit", "build_status", "build_command",
            "compiler_runtime", "engine_dependencies", "feature_and_optimization_flags",
            "hardware", "os", "run_date", "notes",
        ],
        system_rows,
    )
    manifest = {
        "seed": SEED, "matrix": matrix, "elapsed_seconds": time.perf_counter() - started,
        "raw_rows": len(all_rows), "all_correct": all(row["correct"] is True for row in all_rows),
    }
    (raw_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
