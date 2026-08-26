from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from temporal_group_structure.event_identity import TemporalEvent


def _edge_sort_key(edge_id: str) -> tuple[int, int | str]:
    try:
        return 0, int(edge_id)
    except ValueError:
        return 1, edge_id


def load_hif_events(path: str | Path, *, minimum_size: int = 1) -> list[TemporalEvent]:
    """Load undirected HIF JSON while preserving each timestamped event."""

    with Path(path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if payload.get("network-type") != "undirected":
        raise ValueError("this loader expects an undirected HIF event stream")

    members: dict[str, set[str]] = defaultdict(set)
    for incidence in payload["incidences"]:
        members[str(incidence["edge"])].add(str(incidence["node"]))

    events = []
    for item in payload["edges"]:
        edge_id = str(item["edge"])
        nodes = frozenset(members[edge_id])
        if len(nodes) >= minimum_size:
            timestamp = str(item.get("attrs", {}).get("timestamp", ""))
            events.append(TemporalEvent(timestamp=timestamp, nodes=nodes, event_id=edge_id))
    events.sort(key=lambda event: (event.timestamp, _edge_sort_key(event.event_id)))
    return events
