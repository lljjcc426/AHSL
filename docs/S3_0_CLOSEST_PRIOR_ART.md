# S3.0 Closest Prior Art

`Y` denotes what is observed and `H*` the proposed latent high-order object.
“Natural” refers to the real measurement process, not to whether the source
dataset itself is real.

| work | problem and output | Y -> H* | natural primary evidence | structural gold | identifiability / assumptions | strongest collision | code/data | exact overlap with S3.0 |
|---|---|---|---:|---|---|---|---|---|
| Young, Petri & Peixoto (2021), *Hypergraph reconstruction from network data* | Bayesian reconstruction and model selection | simple graph -> latent hyperedges | yes for selected graph case studies; structural tests also project known hypergraphs | case-study interpretation or artificially projected labels | prior-selected representative of a non-injective inverse | Bayesian/MDL clique cover | data and implementation routes reported | nearly exact family A, but not independent natural event-set recovery |
| Wang & Kleinberg (ICLR 2024), *From Graphs to Hypergraphs: Hypergraph Projection and its Reconstruction* | supervised hyperedge reconstruction | clique projection plus prior examples -> hyperedges | no: benchmark projections are computed from known hypergraphs | original hyperedges | extra domain prior is explicitly needed after combinatorial impossibility | supervised set reconstruction | public paper; repository linked by authors | exact artificial-projection formulation |
| Bresler et al. (COLT 2025), *Partial and Exact Recovery of a Random Hypergraph from its Graph Projection* | exact/partial recovery thresholds | weighted or unweighted projection -> random uniform hypergraph | no | planted random structure | sparse random `d`-uniform model and density thresholds | information-theoretic inverse problem | paper | occupies the cleanest family-A theory interface |
| Lee, Lee & Shin (2025), *MARIOH: Multiplicity-Aware Hypergraph Reconstruction* | multiplicity-aware hyperedge reconstruction | multigraph projection -> hyperedges | no: ten known hypergraphs are projected | original hyperedges | bounded candidate structure, multiplicity, learned labels | classifier plus combinatorial search | public repository | saturates practical reconstruction under richer projections |
| Malizia et al. (2024), *Reconstructing higher-order interactions in coupled dynamical systems* | algebraic recovery of interaction order/support | trajectories -> coupling terms | trajectories are natural in principle; reported structural experiments are numerical | planted support | correct dynamics class, observation quality and excitation | nonlinear system identification | paper/data route | exact family-B formulation without real structural gold |
| Tabar et al. (PRX 2024), Kramers--Moyal inference of higher-order interactions | infer coupling tensors from stochastic dynamics | sampled trajectories -> coefficients | natural in principle | chiefly synthetic/controlled | Markov diffusion model, sampling and basis assumptions | moment/system identification | paper | exact family-B inverse method |
| Delabays et al. (2025), *Hypergraph reconstruction from dynamics* (THIS) | sparse regression of directed weighted higher-order topology | time series -> 2/3/4-order terms | yes; includes resting-state EEG | real EEG has no structural ground truth | nondecomposable coupling, state sufficiency, excitation and sparse library | SINDy-style sparse regression | code/data route reported | closest end-to-end family-B method; explicitly exposes the real-gold gap |
| Brunton, Proctor & Kutz (2016), SINDy | sparse governing-equation discovery | trajectories -> active nonlinear terms | yes | equation truth only in controlled/synthetic settings | sparse representation in a chosen function library | classical sparse regression | public ecosystem | higher-order hyperedges are multivariate feature supports |
| Drew et al. (2021), CF-MS computational pipeline | score pairs and cluster complexes | elution profiles -> overlapping protein sets | yes | curated known complexes, commonly used during learning | co-elution, extraction and context assumptions | supervised pair scoring plus graph clustering | review/protocol resources | shows family E's standard solution already outputs sets |
| Nepusz, Yu & Paccanaro (2012), ClusterONE | detect overlapping complexes | weighted PPI graph -> overlapping groups | yes | curated complexes | dense subgraph/cohesiveness objective | overlapping graph communities | Cytoscape/plugin code | directly returns the proposed latent high-order objects |
| Giurgiu et al. (2025), CORUM 5.0 | curated mammalian complex reference | literature evidence -> curated complexes | yes | partial high-precision positives | curation inclusion rules; absence is not a negative | reference database, not inference | downloadable database | best gold route, but incomplete and potentially non-independent |
| Fischer et al. (2025), hu.MAP 3.0 | integrated human complex atlas | >25,000 proteomic experiments -> >15,000 complexes | yes | mixed curated and orthogonal evidence | integration/model assumptions and source overlap | mature ensemble/integrative latent model | downloadable resource | saturates family E at atlas scale |
| Qin et al. (ICML 2025), NAIAD | predict and select combinatorial perturbations | measured combinations -> interaction effects | yes | same-assay effects and partial biological positives | learned response surface; no latent membership recovery | regression/active experiment design | paper/code route | family C is effect learning, not hidden hyperedge recovery |
| Anandkumar et al. (JMLR 2014), tensor methods for latent-variable models | recover latent components from low-order moments | moments -> mixture/topic/HMM components | yes in applications | model-defined components | rank, multi-view and nondegeneracy assumptions | tensor decomposition | algorithms described | occupies moment-to-latent-factor theory; factors are not independently verified hyperedges |
| Airoldi et al. (JMLR 2008), mixed-membership SBM | infer overlapping memberships | dyadic network -> node memberships | yes | latent/model-based | exchangeability and block-model assumptions | mixed-membership latent groups | software lineage | family A/E collapses to community inference when event identity is absent |

## Consequence

The closest work is not a single paper that kills every family. The decisive
pattern is a conjunction:

1. projection and dynamics have direct recent methods and theory but evaluate
   exact structure mainly after constructing observations from known truth;
2. protein complexes have a natural measurement process and partial curated
   truth, but overlapping graph clustering and integrated latent models already
   solve the meaningful set-output task;
3. pooled and marginal settings reduce to classical sparse regression, group
   testing, log-linear inference or tensor decomposition.

Therefore no isolated S3.1 learning residual remains after the reality,
identifiability and collision gates are applied together.
