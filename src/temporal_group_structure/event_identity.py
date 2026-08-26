from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Iterable

Node = Hashable
UndirectedIdentity = frozenset[Node]
DirectedIdentity = tuple[frozenset[Node], frozenset[Node]]


@dataclass(frozen=True)
class TemporalEvent:
    """A timestamped undirected group event with a stable source identifier."""

    timestamp: str
    nodes: frozenset[Node]
    event_id: str

    def __post_init__(self) -> None:
        if not self.nodes:
            raise ValueError("an event must contain at least one node")


def event_identity(
    nodes: Iterable[Node],
    *,
    head_nodes: Iterable[Node] | None = None,
) -> UndirectedIdentity | DirectedIdentity:
    """Return exact set identity; directed events preserve tail/head roles."""

    tail = frozenset(nodes)
    if head_nodes is None:
        return tail
    return tail, frozenset(head_nodes)
