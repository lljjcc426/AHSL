from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable

from lxml import etree

from .hypergraph_builder import DirectedHypergraph, Hyperedge

BP = "http://www.biopax.org/release/biopax-level3.owl#"
RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
REACTION_TYPES = {"BiochemicalReaction", "Degradation", "TemplateReaction"}
ENTITY_TYPES = {"Protein", "SmallMolecule", "Complex", "PhysicalEntity", "Dna", "Rna"}
STABLE_RE = re.compile(r"R-HSA-\d+")


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _ref(element: etree._Element) -> str | None:
    value = element.get(f"{{{RDF}}}resource")
    return value[1:] if value and value.startswith("#") else value


@dataclass(frozen=True, slots=True)
class PathwayRecord:
    id: str
    name: str
    components: frozenset[str]
    child_pathways: frozenset[str]


@dataclass(slots=True)
class ReactomeSnapshot:
    release: int
    hypergraph: DirectedHypergraph
    pathways: dict[str, PathwayRecord]
    local_to_stable: dict[str, str]

    def reaction_set(self, pathway_id: str) -> frozenset[str]:
        memo: dict[str, frozenset[str]] = {}

        def expand(pid: str, active: frozenset[str]) -> frozenset[str]:
            if pid in memo:
                return memo[pid]
            if pid in active:
                return frozenset()
            pathway = self.pathways[pid]
            reactions = {
                self.local_to_stable.get(component, component)
                for component in pathway.components
                if self.local_to_stable.get(component, component) in self.hypergraph.edges
            }
            for child in pathway.child_pathways:
                if child in self.pathways:
                    reactions.update(expand(child, active | {pid}))
            memo[pid] = frozenset(reactions)
            return memo[pid]

        return expand(pathway_id, frozenset())

    def leaf_pathways(self) -> list[PathwayRecord]:
        return [
            pathway
            for pathway in self.pathways.values()
            if not pathway.child_pathways and self.reaction_set(pathway.id)
        ]

    def top_level_families(self) -> dict[str, str]:
        parents: dict[str, set[str]] = {pid: set() for pid in self.pathways}
        for pid, pathway in self.pathways.items():
            for child in pathway.child_pathways:
                if child in parents:
                    parents[child].add(pid)
        roots = sorted(pid for pid, values in parents.items() if not values)
        root_descendants: dict[str, set[str]] = {root: set() for root in roots}
        for root in roots:
            stack = [root]
            while stack:
                current = stack.pop()
                if current in root_descendants[root]:
                    continue
                root_descendants[root].add(current)
                stack.extend(self.pathways[current].child_pathways)
        result: dict[str, str] = {}
        for pid in self.pathways:
            candidates = [root for root in roots if pid in root_descendants[root]]
            chosen = min(candidates) if candidates else pid
            result[pid] = self.pathways[chosen].name
        return result


def parse_reactome_biopax(path: str | Path, release: int) -> ReactomeSnapshot:
    """Stream a Reactome BioPAX L3 file without importing third-party parser code."""
    xrefs: dict[str, tuple[str, str, str]] = {}
    object_xrefs: dict[str, list[str]] = {}
    entity_local_ids: set[str] = set()
    raw_reactions: dict[str, tuple[str, list[str], list[str], str, list[str]]] = {}
    raw_controls: list[tuple[list[str], list[str], str, str]] = []
    raw_pathways: dict[str, tuple[str, list[str], list[str]]] = {}

    for _, element in etree.iterparse(str(path), events=("end",), huge_tree=True):
        parent = element.getparent()
        if parent is None or _local(parent.tag) != "RDF":
            continue
        kind = _local(element.tag)
        local_id = element.get(f"{{{RDF}}}ID")
        if not local_id:
            element.clear()
            continue
        children = list(element)
        refs = [_ref(child) for child in children if _local(child.tag) == "xref"]
        relevant_refs = [value for value in refs if value]
        if kind == "UnificationXref":
            values = { _local(child.tag): (child.text or "").strip() for child in children }
            xrefs[local_id] = (values.get("db", ""), values.get("id", ""), values.get("idVersion", ""))
        elif kind in REACTION_TYPES:
            object_xrefs[local_id] = relevant_refs
            left = [_ref(child) for child in children if _local(child.tag) in {"left", "template"}]
            right = [_ref(child) for child in children if _local(child.tag) in {"right", "product"}]
            name = next(((child.text or "").strip() for child in children if _local(child.tag) == "displayName"), "")
            direction = next(((child.text or "").strip() for child in children if _local(child.tag) == "conversionDirection"), "LEFT-TO-RIGHT")
            if direction == "RIGHT-TO-LEFT":
                left, right = right, left
            raw_reactions[local_id] = (kind, [v for v in left if v], [v for v in right if v], name, object_xrefs[local_id])
        elif kind in {"Catalysis", "Control", "TemplateReactionRegulation"}:
            controllers = [_ref(child) for child in children if _local(child.tag) == "controller"]
            controlled = [_ref(child) for child in children if _local(child.tag) == "controlled"]
            control_type = next(((child.text or "").strip() for child in children if _local(child.tag) == "controlType"), "ACTIVATION" if kind == "Catalysis" else "")
            raw_controls.append(([v for v in controllers if v], [v for v in controlled if v], control_type, kind))
        elif kind == "Pathway":
            object_xrefs[local_id] = relevant_refs
            components = [_ref(child) for child in children if _local(child.tag) == "pathwayComponent"]
            name = next(((child.text or "").strip() for child in children if _local(child.tag) == "displayName"), "")
            raw_pathways[local_id] = (name, [v for v in components if v], relevant_refs)
        elif kind in ENTITY_TYPES:
            object_xrefs[local_id] = relevant_refs
            entity_local_ids.add(local_id)
        element.clear()
        while element.getprevious() is not None:
            del parent[0]

    def stable(local_id: str, fallback_prefix: str) -> str:
        candidates = []
        for xref_id in object_xrefs.get(local_id, []):
            db, value, _ = xrefs.get(xref_id, ("", "", ""))
            if db == "Reactome" and STABLE_RE.fullmatch(value):
                candidates.append(value)
        return min(candidates) if candidates else f"{fallback_prefix}:{release}:{local_id}"

    local_to_stable: dict[str, str] = {}
    for local_id in set(raw_reactions) | set(raw_pathways) | entity_local_ids:
        prefix = "reaction" if local_id in raw_reactions else "pathway" if local_id in raw_pathways else "entity"
        local_to_stable[local_id] = stable(local_id, prefix)

    positive_regulators: dict[str, set[str]] = {rid: set() for rid in raw_reactions}
    for controllers, controlled, control_type, _ in raw_controls:
        if not (control_type.startswith("ACTIVATION") or control_type == ""):
            continue
        for target in controlled:
            if target in positive_regulators:
                positive_regulators[target].update(controllers)

    edges: list[Hyperedge] = []
    for local_id, (kind, left, right, name, _) in raw_reactions.items():
        tail_local = set(left) | positive_regulators.get(local_id, set())
        if not right or not tail_local:
            continue
        edge_id = local_to_stable[local_id]
        edges.append(Hyperedge(
            id=edge_id,
            tail=frozenset(local_to_stable.get(vertex, f"entity:{release}:{vertex}") for vertex in tail_local),
            head=frozenset(local_to_stable.get(vertex, f"entity:{release}:{vertex}") for vertex in right),
            reaction_type=kind,
            name=name,
        ))

    pathway_local_ids = set(raw_pathways)
    pathways: dict[str, PathwayRecord] = {}
    for local_id, (name, components, _) in raw_pathways.items():
        pathway_id = local_to_stable[local_id]
        pathways[pathway_id] = PathwayRecord(
            id=pathway_id,
            name=name,
            components=frozenset(components),
            child_pathways=frozenset(local_to_stable[c] for c in components if c in pathway_local_ids),
        )
    return ReactomeSnapshot(release, DirectedHypergraph(edges), pathways, local_to_stable)
