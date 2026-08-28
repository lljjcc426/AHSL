# META1 data audit

## Sources

| Panel | Source | Frozen version | Statistical unit |
|---|---|---|---|
| Ishizawa | PNAS 2024 supplement, DOI `10.1073/pnas.2312396121`, `data1_rawcfu.csv` | `PNAS-2024-supplement` | focal-strain CFU landscape |
| Díaz-Colunga | eLife article DOI `10.7554/eLife.101906.3`, official `full_factorial_design` repository, `data/pseudo.txt` | git `35c150c85df2fc5964523f906ceeb8229f0b1666` | consortium OD600 response |

The Díaz adapter uses the source repository's primary selection `wavelength=600` and `dilution_factor=0.0025`. OD600 is described as a quantitative community-function response, not exact biomass truth.

## Completeness

Ishizawa contains 2,377 raw CFU records and 127 unique nonempty seven-strain systems. Conditioning on each focal strain yields seven complete six-factor landscapes, each with 64 cells. Six landscapes contain 341 records and DW147 contains 331. Replicate counts are 5--12 per cell except DW147, which has 5--9. No `(strain, system, replicate)` duplicate key was found.

Díaz-Colunga contains one complete eight-factor landscape: 256 cells, exactly three biological replicates per cell, and 768 records. No `(community, replicate)` duplicate key was found.

| Panel/landscape | dimension | expected/observed cells | missing | replicates/cell |
|---|---:|---:|---:|---:|
| Ishizawa DW039, DW067, DW100, DW102, DW145, DW155 | 6 | 64/64 each | 0 | 5--12 |
| Ishizawa DW147 | 6 | 64/64 | 0 | 5--9 |
| Díaz-Colunga OD600 | 8 | 256/256 | 0 | 3 |

The adapters normalize only community bitmask, replicate identifier, response, and panel metadata. Panels are not concatenated and no common response normalization or noise model is imposed. Machine-readable audit tables are in `results/meta1/raw/data_audit.csv`, `panel_replicates.csv`, and `replicate_statistics.csv`.
