# S3.0 Search Log

## Protocol and counts

- Search date: **2026-08-27**.
- Directly relevant works screened: **50**.
- Deeply reviewed: **22** (`D` below).
- Deeply reviewed works dated 2024--2026: **14** (`D24-26`).
- Candidate families: projection, dynamics, pooled assays, censored events,
  complexes/modules, and low-order marginals.
- Sources: publisher/conference pages, full papers, public repositories and
  dataset/database documentation. Bibliographic fields not confirmed from a
  primary page are intentionally omitted from the bibliography.

## Query families

1. `latent hypergraph from pairwise observations`, `hypergraph reconstruction
   graph projection`, `recover hyperedges pairwise cooccurrence`, `multiplicity`;
2. `higher-order interaction inference time series`, `hypergraph system
   identification`, `simplicial dynamics reconstruction`, `SINDy`;
3. `pooled CRISPR interaction inference`, `group testing interactions`,
   `combinatorial perturbation`;
4. `censored group events`, `partial participant set`, `animal group imperfect
   detection`, `MNAR relational events`;
5. `CF-MS protein complex discovery`, `co-elution complex benchmark`, `CORUM`,
   `overlapping protein complex clustering`;
6. `higher-order interactions from marginals`, `log-linear support`, `maximum
   entropy`, `tensor latent variable moments`;
7. collision searches: `mixed membership SBM`, `overlapping community`, `CP
   uniqueness`, `nonnegative tensor factorization`, `capture recapture`,
   `compressed sensing`, `system identification`.

## Screened works

| # | work/resource | year | depth | role and disposition |
|---:|---|---:|---|---|
| 1 | Young, Petri & Peixoto, *Hypergraph reconstruction from network data* | 2021 | D | natural graph examples; inverse is prior-selected |
| 2 | Wang & Kleinberg, *From Graphs to Hypergraphs: Hypergraph Projection and its Reconstruction* | 2024 | D24-26 | artificial projection plus prior knowledge; kill G2/G8 |
| 3 | *Supervised Hypergraph Reconstruction* (SHyRe) | 2022 | D | supervised projected-known-hypergraph protocol |
| 4 | Bresler et al., COLT poster on random-hypergraph reconstruction thresholds | 2024 | screen | theory under sparse random uniform model |
| 5 | Bresler, Guo, Polyanskiy & Yao, *Partial and Exact Recovery of a Random Hypergraph from its Graph Projection* | 2025 | D24-26 | occupies exact/partial threshold theory |
| 6 | Lee, Lee & Shin, *MARIOH: Multiplicity-Aware Hypergraph Reconstruction* | 2025 | D24-26 | modern classifier/search saturation |
| 7 | reconstruction from uncertain pairwise observations | 2023 | screen | uncertainty extension; no new natural gold |
| 8 | Delabays et al., *Hypergraph reconstruction from dynamics* | 2025 | D24-26 | THIS; natural EEG but no real structural truth |
| 9 | Malizia et al., *Reconstructing higher-order interactions in coupled dynamical systems* | 2024 | D24-26 | numerical structural recovery |
| 10 | Tabar et al., PRX higher-order interaction inference using Kramers--Moyal coefficients | 2024 | D24-26 | modern system identification |
| 11 | Tang, Srikrishnan & Kulik, *Bayes-THIS* | 2026 | D24-26 | posterior uncertainty; structural non-identifiability remains |
| 12 | multiplex higher-order dynamics reconstruction | 2026 | screen | regression extension; numerical truth |
| 13 | higher-order dynamics review, *Nature Reviews Physics* | 2026 | D24-26 | confirms active and broad dynamics field |
| 14 | Brunton, Proctor & Kutz, SINDy | 2016 | D | classical sparse feature-library baseline |
| 15 | ARNI network reconstruction | 2017 | screen | nonlinear network inference collision |
| 16 | reactionet lasso for chemical reaction networks | 2016 | D | sparse reaction support recovery |
| 17 | BioPreDyn-bench | 2015 | D | real-inspired dynamics benchmark; parameters/structures not independent natural gold |
| 18 | survey of chemical-reaction-network inference methods | 2026 | D24-26 | mature system-identification landscape |
| 19 | Giurgiu et al., CORUM 5.0 | 2025 | D24-26 | 7,193 curated complexes; partial positives |
| 20 | *Integrating CORUM and co-fractionation mass spectrometry to create enhanced benchmarks for protein complex predictions* | 2025 | D24-26 | benchmark construction shares CF-MS/CORUM evidence |
| 21 | Fischer et al., hu.MAP 3.0 | 2025 | D24-26 | >25,000 experiments and >15,000 inferred complexes |
| 22 | *Co-fractionation/mass spectrometry to identify protein complexes* | 2021 | D | pair scoring plus graph clustering is standard |
| 23 | scalable multi-cell CF/MS | 2022 | screen | real assay route, no independent complete gold |
| 24 | mCP: FDR-controlled protein-complex prediction | 2024 | D24-26 | mature domain method and uncertainty control |
| 25 | Nepusz et al., ClusterONE | 2012 | D | overlapping graph clusters directly equal set output |
| 26 | Bader & Hogue, MCODE | 2003 | screen | dense graph-module baseline |
| 27 | van Dongen, Markov Cluster Algorithm | 2000 | screen | standard graph clustering baseline |
| 28 | evidence-aware protein complex detection preprint | 2026 | screen | recent saturation signal |
| 29 | Giurgiu et al., original CORUM resource | 2008 | screen | historical gold provenance |
| 30 | Complex Portal update | 2025 | screen | second curated reference, still partial positives |
| 31 | Qin et al., NAIAD | 2025 | D24-26 | combinatorial response prediction/selection, not group recovery |
| 32 | benchmark of genetic-interaction scoring across five dual-CRISPR studies | 2025 | screen | effects derived from same assay |
| 33 | dual-guide combinatorial CRISPR screen | 2025 | screen | primarily pairwise perturbations |
| 34 | Ghosh et al., compressed-sensing pooled RT-PCR testing | 2021 | screen | group-testing/compressed-sensing collision; not structural group recovery |
| 35 | quantitative group testing for interactions | 2026 | screen | active classical inverse line |
| 36 | Farine et al., animal social network methods | 2016 | screen | group-by-individual data and observation bias |
| 37 | association indices under imperfect observation | 2017 | screen | natural censoring, no full-event truth |
| 38 | higher-order animal communication study | 2024 | screen | natural group events, not partial-to-full recovery |
| 39 | capture--recapture/occupancy modeling literature | classical | screen | detection/process separation collision |
| 40 | Airoldi et al., mixed-membership stochastic blockmodel | 2008 | screen | latent-community collision |
| 41 | Yang & Leskovec, BigCLAM | 2013 | screen | overlapping affiliation communities |
| 42 | Anandkumar et al., tensor decompositions for latent-variable models | 2014 | D | moment-to-factor recovery collision |
| 43 | Bhaskara et al., uniqueness of tensor decompositions | 2014 | screen | robust Kruskal theory |
| 44 | overcomplete latent-variable tensor decomposition | 2015 | screen | additional tensor identifiability theory |
| 45 | Kruskal, three-way array uniqueness | 1977 | screen | foundational uniqueness condition |
| 46 | low-order marginal release for differential privacy | 2018 | screen | natural privacy output; full table non-identifiable |
| 47 | CIPHER private marginal release | 2018 | screen | private synthetic-data collision |
| 48 | iterative proportional fitting for synthetic count data | 2022 | screen | classical log-linear/max-entropy representative |
| 49 | hierarchical log-linear model selection | classical | screen | target already native to statistics |
| 50 | maximum-entropy reconstruction from marginals | classical | screen | selects one feasible table; does not identify truth |

## Datasets and repositories inspected

- projection reconstruction: the dataset collections and code routes attached
  to ICLR 2024, SHyRe and MARIOH;
- dynamics: THIS code/data route, its 218 resting-state EEG time series, and the
  synthetic Kuramoto/Lorenz/oscillator controls used across recent methods;
- complexes: CORUM 5.0, hu.MAP3.0 downloads, CF-MS studies and standard
  ClusterONE/MCODE pipelines;
- pooled perturbations: five dual-CRISPR studies consolidated by the 2025
  scoring benchmark, NAIAD and Tapestry;
- censored events: animal group-by-individual examples and imperfect-detection
  methodology;
- marginals: privacy-release and synthetic-tabular workflows.

## Negative searches and kill reasons

- No naturally pairwise-only dataset with independently measured complete event
  sets at benchmark scale was found. Projection family killed by G2/G3/G5/G8.
- No real trajectory dataset with independent higher-order coupling support was
  found. Dynamics killed by G3/G4/G6/G7/G9.
- No pooled assay whose unknown is a physical group set, rather than sparse
  coefficients/effects, was found. Pooled family killed by G3/G7/G11.
- No public large paired partial/full group-event dataset with a calibrated
  censoring mechanism was found. Censoring killed by G3/G4/G5/G10.
- Protein complexes supplied the best natural route, but no clean
  assay-disjoint complete structural gold or residual beyond overlapping graph
  clustering/integrative methods was found. Family E killed by G3/G5/G7/G8.
- Privacy marginals supplied genuine natural aggregation, but the unreleased
  high-order truth is non-identifiable and unavailable for public scoring.
  Family F killed by G3/G5/G7.

## Count reconciliation

Rows marked `D` or `D24-26` total 22. Rows marked `D24-26` total 14. The search
therefore exceeds all requested scale minima without padding the semifinal set.
