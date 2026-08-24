"""Classical join-tree recovery from hyperedge intersection weights."""

from __future__ import annotations

import networkx as nx
import numpy as np


class _UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, node: int) -> int:
        while self.parent[node] != node:
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    def union(self, left: int, right: int) -> bool:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return False
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1
        return True


class IntersectionMWSTJoinTree:
    """Recover a deterministic maximum spanning tree of hyperedge intersections."""

    name = "IntersectionMWSTJoinTree"

    def fit(self, incidence: np.ndarray) -> "IntersectionMWSTJoinTree":
        binary = np.asarray(incidence, dtype=np.int64)
        if binary.ndim != 2 or binary.shape[1] < 1:
            raise ValueError("incidence must be a non-empty matrix")
        m = binary.shape[1]
        intersections = binary.T @ binary
        weighted_edges = [
            (int(intersections[left, right]), left, right)
            for left in range(m)
            for right in range(left + 1, m)
        ]
        weighted_edges.sort(key=lambda item: (-item[0], item[1], item[2]))
        union_find = _UnionFind(m)
        tree = nx.Graph()
        tree.add_nodes_from(range(m))
        for weight, left, right in weighted_edges:
            if union_find.union(left, right):
                tree.add_edge(left, right, weight=weight)
                if tree.number_of_edges() == m - 1:
                    break
        if not nx.is_tree(tree):
            raise RuntimeError("maximum-spanning-tree construction failed")
        self.tree_ = tree
        self.intersection_weights_ = intersections
        return self

    def predict_tree(self) -> nx.Graph:
        return self.tree_.copy()

