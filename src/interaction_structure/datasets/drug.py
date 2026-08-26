from __future__ import annotations

from pathlib import Path
import re

import numpy as np
import pandas as pd


def _split_agent(value: str) -> tuple[str, int]:
    match = re.fullmatch(r"(.+?)(\d+)", str(value))
    if match is None:
        raise ValueError(f"unrecognized drug-dose code: {value}")
    return match.group(1), int(match.group(2))


def _is_supported_label(values: pd.Series) -> pd.Series:
    """Preserve source uncertainty: inconclusive is neither support nor negative."""
    return ~values.isin(["Additive", "Inconclusive"])


def load_processed_tables(directory: str | Path, orders: tuple[int, ...] = (3, 4, 5)) -> pd.DataFrame:
    directory = Path(directory)
    outputs = []
    for order in orders:
        filename = {3: "3Drug.xlsx", 4: "4Drugs.xlsx", 5: "5Drug.xlsx"}[order]
        frame = pd.read_excel(directory / filename)
        columns = [f"Drug-{letter}" for letter in "ABCDE"[:order]]
        parsed = frame[columns].map(_split_agent)
        frame["drug_set"] = [tuple(sorted(item[0] for item in row)) for row in parsed.itertuples(index=False, name=None)]
        frame["dose_context"] = [tuple(sorted(row)) for row in parsed.itertuples(index=False, name=None)]
        frame["order"] = order
        # The source labels "Inconclusive" separately; it is uncertainty, not support.
        frame["net_support"] = _is_supported_label(frame["DA-interaction"])
        frame["net_suppressive"] = frame["DA-interaction"].str.contains("Suppression", na=False)
        frame["emergent_support"] = _is_supported_label(frame[f"E{order}-interaction"])
        outputs.append(frame)
    return pd.concat(outputs, ignore_index=True)


def context_stability(frame: pd.DataFrame) -> pd.DataFrame:
    records = []
    for (order, drug_set), group in frame.groupby(["order", "drug_set"]):
        net_labels = group["DA-interaction"].astype(str)
        emergent_labels = group[f"E{order}-interaction"].astype(str)
        net_sign = np.sign(group["DA"].to_numpy(dtype=float))
        emergent_sign = np.sign(group[f"E{order}"].to_numpy(dtype=float))
        records.append(
            {
                "order": order,
                "drug_set": "+".join(drug_set),
                "contexts": len(group),
                "net_support_fraction": float(group["net_support"].mean()),
                "emergent_support_fraction": float(group["emergent_support"].mean()),
                "net_modal_fraction": float(net_labels.value_counts(normalize=True).iloc[0]),
                "emergent_modal_fraction": float(emergent_labels.value_counts(normalize=True).iloc[0]),
                "net_sign_flip": bool(len(set(net_sign)) > 1),
                "emergent_sign_flip": bool(len(set(emergent_sign)) > 1),
            }
        )
    return pd.DataFrame(records)
