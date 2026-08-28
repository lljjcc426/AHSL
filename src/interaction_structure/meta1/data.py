from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from ..datasets.microbiome import STRAINS, focal_replicate_landscapes, load_raw_cfu


@dataclass(frozen=True)
class Landscape:
    panel_id: str
    landscape_id: str
    universe: tuple[str, ...]
    replicates: dict[int, np.ndarray]
    response_type: str
    source_metadata: dict[str, Any]

    @property
    def dimension(self) -> int:
        return len(self.universe)

    @property
    def n_cells(self) -> int:
        return 1 << self.dimension

    def transformed_replicates(self, scale: str) -> dict[int, np.ndarray]:
        if scale == "raw":
            return {mask: values.astype(float, copy=True) for mask, values in self.replicates.items()}
        if scale == "log10":
            return {mask: np.log10(values.astype(float)) for mask, values in self.replicates.items()}
        if scale == "log1p":
            return {mask: np.log1p(values.astype(float)) for mask, values in self.replicates.items()}
        raise ValueError(f"unsupported response scale: {scale}")


@dataclass(frozen=True)
class CompletePanel:
    panel_id: str
    landscapes: tuple[Landscape, ...]
    source_version: str


def _subset_mask(members: frozenset[str], universe: tuple[str, ...]) -> int:
    return sum(1 << index for index, item in enumerate(universe) if item in members)


def load_ishizawa(path: str | Path) -> CompletePanel:
    source = Path(path)
    frame = load_raw_cfu(source)
    raw_landscapes = focal_replicate_landscapes(frame, scale="raw")
    landscapes: list[Landscape] = []
    for focal in STRAINS:
        universe = tuple(strain for strain in STRAINS if strain != focal)
        replicates = {
            _subset_mask(subset, universe): np.asarray(values, dtype=float)
            for subset, values in raw_landscapes[focal].items()
        }
        landscapes.append(
            Landscape(
                panel_id="ishizawa",
                landscape_id=f"ishizawa_{focal}",
                universe=universe,
                replicates=replicates,
                response_type="focal_strain_cfu",
                source_metadata={
                    "focal_strain": focal,
                    "doi": "10.1073/pnas.2312396121",
                    "source_file": source.name,
                },
            )
        )
    return CompletePanel("ishizawa", tuple(landscapes), "PNAS-2024-supplement")


def load_diaz_colunga(path: str | Path) -> CompletePanel:
    source = Path(path)
    frame = pd.read_csv(source, sep="\t", dtype={"community": str})
    selected = frame[(frame["wavelength"] == 600) & np.isclose(frame["dilution_factor"], 0.0025)].copy()
    replicates = {
        int(community, 2): group.sort_values("replicate")["absorbance"].to_numpy(dtype=float)
        for community, group in selected.groupby("community", sort=False)
    }
    landscape = Landscape(
        panel_id="diaz_colunga",
        landscape_id="diaz_colunga_od600",
        universe=tuple(f"strain_{index}" for index in range(1, 9)),
        replicates=replicates,
        response_type="od600_community_function",
        source_metadata={
            "wavelength_nm": 600,
            "dilution_factor": 0.0025,
            "doi": "10.7554/eLife.101906.3",
            "source_file": source.name,
        },
    )
    return CompletePanel("diaz_colunga", (landscape,), "35c150c85df2fc5964523f906ceeb8229f0b1666")


def normalized_replicate_frame(panels: tuple[CompletePanel, ...]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for panel in panels:
        for landscape in panel.landscapes:
            width = landscape.dimension
            for mask, values in sorted(landscape.replicates.items()):
                for replicate_index, response in enumerate(values, start=1):
                    rows.append(
                        {
                            "panel_id": panel.panel_id,
                            "landscape_id": landscape.landscape_id,
                            "community_bitmask": format(mask, f"0{width}b"),
                            "strain_count": int(mask.bit_count()),
                            "replicate_id": replicate_index,
                            "response": float(response),
                            "response_type": landscape.response_type,
                            "source_metadata": str(landscape.source_metadata),
                        }
                    )
    return pd.DataFrame(rows)
