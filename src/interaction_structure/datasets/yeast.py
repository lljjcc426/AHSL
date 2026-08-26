from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

TAU_COLUMN = "Adjusted genetic interaction score (epsilon or tau)"
RAW_COLUMN = "Raw genetic interaction score (epsilon)"


def _orf(value: pd.Series) -> pd.Series:
    return value.str.extract(r"^([^_]+)", expand=False)


def load_kuzmin(path: str | Path) -> pd.DataFrame:
    frame = pd.read_csv(path, sep="\t")
    triple = frame[frame["Combined mutant type"].eq("trigenic")].copy()
    query = triple["Query strain ID"].str.extract(r"^([^+_]+)\+([^_]+)")
    triple["gene_1"] = query[0]
    triple["gene_2"] = query[1]
    triple["gene_3"] = _orf(triple["Array strain ID"])
    triple["query_pair"] = list(zip(triple["gene_1"], triple["gene_2"]))
    triple["triple"] = [tuple(sorted(x)) for x in triple[["gene_1", "gene_2", "gene_3"]].itertuples(index=False, name=None)]
    triple["strong_negative_tau"] = (triple[TAU_COLUMN] < -0.08) & (triple["P-value"] < 0.05)
    triple["strong_negative_raw"] = (triple[RAW_COLUMN] < -0.08) & (triple["P-value"] < 0.05)
    return triple


def audit_counts(all_rows: pd.DataFrame, triples: pd.DataFrame) -> dict[str, float | int]:
    genes = pd.unique(triples[["gene_1", "gene_2", "gene_3"]].to_numpy().ravel())
    tau = triples["strong_negative_tau"].to_numpy(bool)
    raw = triples["strong_negative_raw"].to_numpy(bool)
    return {
        "public_table_rows": int(len(all_rows)),
        "public_digenic_rows": int((all_rows["Combined mutant type"] == "digenic").sum()),
        "public_trigenic_rows": int(len(triples)),
        "unique_triples": int(triples["triple"].nunique()),
        "unique_genes": int(len(genes)),
        "query_pairs": int(triples["query_pair"].nunique()),
        "strong_negative_tau": int(tau.sum()),
        "raw_negative_support": int(raw.sum()),
        "tau_raw_support_jaccard": float(np.sum(tau & raw) / np.sum(tau | raw)),
        "tau_raw_rank_correlation": float(triples[[TAU_COLUMN, RAW_COLUMN]].corr("spearman").iloc[0, 1]),
        "median_fitness_sd": float(triples["Combined mutant fitness standard deviation"].median()),
    }
