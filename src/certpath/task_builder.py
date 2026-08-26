from __future__ import annotations

from dataclasses import dataclass

from .reactome_adapter import ReactomeSnapshot


@dataclass(frozen=True, slots=True)
class CertPathTask:
    pathway_id: str
    pathway_name: str
    family: str
    sources: frozenset[str]
    targets: frozenset[str]
    gold_reactions: frozenset[str]
    boundary_sources: frozenset[str]


def build_natural_tasks(snapshot: ReactomeSnapshot) -> list[CertPathTask]:
    """Build one grouped task per reaction-level (leaf) curated pathway.

    The query reveals the pathway boundary: all external inputs are sources and
    all terminal outputs are conjunctive targets. No internal entity is added
    after observing reachability or an optimizer result.
    """
    graph = snapshot.hypergraph
    global_sources = graph.global_sources()
    families = snapshot.top_level_families()
    tasks: list[CertPathTask] = []
    for pathway in snapshot.leaf_pathways():
        gold = snapshot.reaction_set(pathway.id)
        tails = set().union(*(graph.edges[e].tail for e in gold))
        heads = set().union(*(graph.edges[e].head for e in gold))
        boundary_sources = frozenset(tails - heads)
        targets = frozenset(heads - tails)
        if not boundary_sources or not targets:
            continue
        tasks.append(CertPathTask(
            pathway_id=pathway.id,
            pathway_name=pathway.name,
            family=families[pathway.id],
            sources=frozenset(global_sources | boundary_sources),
            targets=targets,
            gold_reactions=gold,
            boundary_sources=boundary_sources,
        ))
    return sorted(tasks, key=lambda task: task.pathway_id)
