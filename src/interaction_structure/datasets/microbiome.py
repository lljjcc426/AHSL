from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from ..estimands.mobius import Subset, powerset

STRAINS = ("DW039", "DW067", "DW100", "DW102", "DW145", "DW147", "DW155")
SYSTEM_POSITION = ("DW100", "DW102", "DW039", "DW145", "DW155", "DW067", "DW147")


def decode_system(system: str) -> frozenset[str]:
    return frozenset(SYSTEM_POSITION[int(digit) - 1] for digit in system[1:] if digit != "0")


def load_raw_cfu(path: str | Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    frame["members"] = frame["system"].map(decode_system)
    return frame


def focal_replicate_landscapes(frame: pd.DataFrame, *, scale: str = "log10") -> dict[str, dict[Subset, np.ndarray]]:
    transform = np.log10 if scale == "log10" else np.asarray
    landscapes: dict[str, dict[Subset, np.ndarray]] = {}
    for focal in STRAINS:
        universe = tuple(strain for strain in STRAINS if strain != focal)
        rows = frame[frame["strain"].eq(focal)]
        landscape: dict[Subset, np.ndarray] = {}
        for members, group in rows.groupby("members"):
            subset = frozenset(members - {focal})
            landscape[subset] = np.asarray(transform(group["cfu"].to_numpy(dtype=float)), dtype=float)
        expected = set(powerset(universe))
        if set(landscape) != expected:
            raise ValueError(f"{focal} does not contain the complete 2^6 factorial")
        landscapes[focal] = landscape
    return landscapes
