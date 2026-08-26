from __future__ import annotations

from collections import Counter
from itertools import combinations

import numpy as np
import pandas as pd


def random_split(size: int, *, test_fraction: float = 0.2, seed: int = 20260827) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    order = rng.permutation(size)
    cut = int(round(size * (1 - test_fraction)))
    return np.sort(order[:cut]), np.sort(order[cut:])


def gene_disjoint_split(triples: pd.DataFrame, *, test_fraction: float = 0.2, seed: int = 20260827) -> tuple[np.ndarray, np.ndarray, set[str]]:
    genes = np.unique(triples[["gene_1", "gene_2", "gene_3"]].to_numpy().ravel())
    rng = np.random.default_rng(seed)
    held = set(rng.choice(genes, size=max(1, int(round(len(genes) * test_fraction))), replace=False))
    membership = triples[["gene_1", "gene_2", "gene_3"]].isin(held).sum(axis=1)
    train = np.flatnonzero(membership.eq(0).to_numpy())
    test = np.flatnonzero(membership.gt(0).to_numpy())
    return train, test, held


def query_pair_disjoint_split(triples: pd.DataFrame, *, test_fraction: float = 0.2, seed: int = 20260827) -> tuple[np.ndarray, np.ndarray]:
    pairs = triples["query_pair"].drop_duplicates().to_numpy()
    rng = np.random.default_rng(seed)
    held = set(rng.choice(pairs, size=max(1, int(round(len(pairs) * test_fraction))), replace=False))
    is_test = triples["query_pair"].isin(held).to_numpy()
    return np.flatnonzero(~is_test), np.flatnonzero(is_test)


def overlap_audit(triples: pd.DataFrame, train_index: np.ndarray, test_index: np.ndarray) -> dict[str, float | int]:
    train = triples.iloc[train_index]
    test = triples.iloc[test_index]
    train_genes = set(train[["gene_1", "gene_2", "gene_3"]].to_numpy().ravel())
    train_pairs = Counter(
        pair
        for row in train[["gene_1", "gene_2", "gene_3"]].itertuples(index=False, name=None)
        for pair in combinations(sorted(row), 2)
    )
    test_rows = list(test[["gene_1", "gene_2", "gene_3"]].itertuples(index=False, name=None))
    gene_overlap = [sum(gene in train_genes for gene in row) for row in test_rows]
    pair_overlap = [sum(tuple(sorted(pair)) in train_pairs for pair in combinations(row, 2)) for row in test_rows]
    return {
        "train": len(train),
        "test": len(test),
        "test_strong_prevalence": float(test["strong_negative_tau"].mean()),
        "test_with_any_gene_overlap": float(np.mean(np.asarray(gene_overlap) > 0)),
        "test_with_all_gene_overlap": float(np.mean(np.asarray(gene_overlap) == 3)),
        "test_with_any_pair_overlap": float(np.mean(np.asarray(pair_overlap) > 0)),
        "test_with_all_pair_overlap": float(np.mean(np.asarray(pair_overlap) == 3)),
        "query_pair_overlap": int(len(set(train["query_pair"]) & set(test["query_pair"]))),
    }
