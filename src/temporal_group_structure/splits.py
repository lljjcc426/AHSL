from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from temporal_group_structure.event_identity import TemporalEvent


@dataclass(frozen=True)
class ChronologicalSplit:
    train: tuple[TemporalEvent, ...]
    validation: tuple[TemporalEvent, ...]
    test: tuple[TemporalEvent, ...]


def _next_timestamp_boundary(events: Sequence[TemporalEvent], target: int) -> int:
    if target <= 0 or target >= len(events):
        return max(0, min(target, len(events)))
    timestamp = events[target - 1].timestamp
    boundary = target
    while boundary < len(events) and events[boundary].timestamp == timestamp:
        boundary += 1
    return boundary


def chronological_split(
    events: Sequence[TemporalEvent],
    *,
    train_fraction: float = 0.70,
    validation_fraction: float = 0.15,
) -> ChronologicalSplit:
    """Split a sorted stream without cutting an identical-timestamp batch."""

    ordered = tuple(sorted(events, key=lambda event: (event.timestamp, event.event_id)))
    n_events = len(ordered)
    train_end = _next_timestamp_boundary(ordered, round(train_fraction * n_events))
    validation_end = _next_timestamp_boundary(
        ordered, round((train_fraction + validation_fraction) * n_events)
    )
    validation_end = max(train_end, validation_end)
    return ChronologicalSplit(
        train=ordered[:train_end],
        validation=ordered[train_end:validation_end],
        test=ordered[validation_end:],
    )


def has_future_leakage(split: ChronologicalSplit) -> bool:
    """Timestamp leakage check for the three chronological partitions."""

    if split.train and split.validation and split.train[-1].timestamp >= split.validation[0].timestamp:
        return True
    if split.validation and split.test and split.validation[-1].timestamp >= split.test[0].timestamp:
        return True
    return False
