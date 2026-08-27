"""Small, engine-independent pieces of the AP1.0 measurement protocol."""

from __future__ import annotations

from dataclasses import dataclass
import math
import random
import re
from typing import Iterable, Sequence


@dataclass(frozen=True)
class UpdateBatch:
    """One atomic set-valued input update."""

    inserts: tuple[tuple[str, ...], ...]
    deletes: tuple[tuple[str, ...], ...]


def deterministic_edge_stream(
    edges: Iterable[tuple[int, int]],
    *,
    batches: int,
    insert_count: int,
    delete_count: int,
    seed: int,
) -> list[UpdateBatch]:
    """Construct repeatable valid edge updates without duplicate set entries."""

    rng = random.Random(seed)
    current = set(edges)
    next_node = 1 + max((max(edge) for edge in current), default=0)
    stream: list[UpdateBatch] = []
    for _ in range(batches):
        deletable = sorted(current)
        chosen_deletes = rng.sample(deletable, min(delete_count, len(deletable)))
        for edge in chosen_deletes:
            current.remove(edge)

        chosen_inserts: list[tuple[int, int]] = []
        while len(chosen_inserts) < insert_count:
            if current:
                src = rng.choice(sorted(current))[1]
            else:
                src = max(0, next_node - 1)
            edge = (src, next_node)
            next_node += 1
            if edge not in current:
                current.add(edge)
                chosen_inserts.append(edge)

        stream.append(
            UpdateBatch(
                inserts=tuple((str(a), str(b)) for a, b in chosen_inserts),
                deletes=tuple((str(a), str(b)) for a, b in chosen_deletes),
            )
        )
    return stream


def apply_batch(
    state: set[tuple[str, ...]], batch: UpdateBatch
) -> set[tuple[str, ...]]:
    """Apply a valid set-valued batch and return a fresh state."""

    updated = set(state)
    updated.difference_update(batch.deletes)
    updated.update(batch.inserts)
    return updated


def normalize_rows(rows: Iterable[Sequence[object]]) -> tuple[tuple[str, ...], ...]:
    """Canonicalize a relation snapshot for exact set comparison."""

    return tuple(sorted({tuple(str(value).strip() for value in row) for row in rows}))


def apply_delta_rows(
    state: set[tuple[str, ...]], rows: Iterable[Sequence[object]]
) -> set[tuple[str, ...]]:
    """Apply FlowLog incremental output rows whose last column is a signed diff."""

    result = set(state)
    for raw in rows:
        row = tuple(str(value).strip() for value in raw)
        if len(row) < 2:
            raise ValueError("incremental row must contain data and a diff")
        values, diff_text = row[:-1], row[-1]
        diff = int(diff_text)
        if diff > 0:
            result.add(values)
        elif diff < 0:
            result.discard(values)
    return result


_DURATION_RE = re.compile(
    r"(?:(?P<h>\d+):)?(?:(?P<m>\d+):)?(?P<s>\d+)(?:\.(?P<f>\d+))?"
)


def parse_rust_duration(text: str) -> float:
    """Parse Rust Debug durations such as ``12.4ms`` or ``1.02s`` to ms."""

    value = text.strip()
    match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)(.+)", value)
    if match:
        number, unit = float(match.group(1)), match.group(2)
        if unit == "ns":
            return number * 1e-6
        if unit == "ms":
            return number
        if unit == "s":
            return number * 1e3
        if unit == "us" or (len(unit) <= 2 and unit.endswith("s")):
            return number * 1e-3
    raise ValueError(f"unsupported duration: {text}")


def parse_committed_durations(log_text: str) -> list[float]:
    """Extract per-commit FlowLog wall times from shell output."""

    marker = ":\tCommitted & executed"
    values = []
    for line in log_text.splitlines():
        if marker in line:
            values.append(parse_rust_duration(line.split(marker, 1)[0].strip()))
    return values


def percentile(values: Sequence[float], q: float) -> float:
    """Linear-interpolated percentile with explicit finite-input semantics."""

    if not values:
        raise ValueError("percentile requires at least one value")
    if not 0 <= q <= 1:
        raise ValueError("q must be in [0, 1]")
    ordered = sorted(float(value) for value in values)
    position = (len(ordered) - 1) * q
    low = math.floor(position)
    high = math.ceil(position)
    if low == high:
        return ordered[low]
    weight = position - low
    return ordered[low] * (1 - weight) + ordered[high] * weight


def summarize_rss(samples: Sequence[int]) -> tuple[float, float]:
    """Return first and peak working-set samples in MiB."""

    if not samples:
        raise ValueError("RSS sample list is empty")
    mib = 1024.0 * 1024.0
    return samples[0] / mib, max(samples) / mib
