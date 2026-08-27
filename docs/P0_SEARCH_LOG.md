# P0 narrow search log

Search date: **2026-08-27 (Asia/Shanghai)**. P0 was synthesis-first. The search
covered **15 primary works**, below the budget of 20; **12 were deeply
inspected**. Nine titles were not already explicitly indexed in repository
reports/references, although some address interfaces already covered by prior
phases. Search-engine snippets were used only for discovery; conclusions use
primary paper/proceedings pages or arXiv records.

## Question 1: does native hypergraph width now control ML generalization?

- Exact query: `site:arxiv.org hypergraph width generalization bound machine learning 2024 2025 2026`
- Source: arXiv and primary paper pages.
- Why necessary: I9 was not directly implemented in previous phases and could
  have been a surviving Q1 interface.
- Result: Wang, Arce and Tong (2025) derive PAC-Bayes bounds for HGNN classes
  using model norms and hypergraph structural/spectral terms. The work does not
  establish GHD/FHD, fractional-cover or acyclicity necessity and does not
  supply a two-route classical residual.
- Change to prior evidence: **no reopening; moves I9 from unexamined to Q3**.

## Question 2: is there a direct certified learning-augmented GHD/FHD result?

- Exact queries:
  - `site:arxiv.org learning-augmented hypertree decomposition generalized hypertree width prediction 2024 2025 2026`
  - `site:arxiv.org "learning-augmented" "hypertree" OR "hypergraph decomposition"`
  - `site:proceedings.mlr.press OR site:drops.dagstuhl.de learning augmented set cover predictions hypergraph robust 2024 2025`
- Source: PMLR, Dagstuhl/LIPIcs, arXiv and ACM primary records.
- Why necessary: I7 was the closest formal strong-coupling route after R0.
- Result: no direct prediction-augmented GHD/FHD result with real paired
  benchmarks was found. Generic robust online packing/covering and
  prediction-aided graph/set-cover approximation are active. In parallel,
  purely classical GHD/FHD approximation, exact FPT, LP, rerootability and
  parallel algorithms advanced substantially.
- Change to prior evidence: **strengthens P0-B and R0 transfer; does not reopen
  R0**.

## Question 3: is adaptive/query learning a genuine untested Q1 interface?

- Exact queries:
  - `site:proceedings.mlr.press hypergraph active learning query complexity reconstruction 2024 2025`
  - `site:arxiv.org "hypergraph" "query complexity" learning reconstruction 2024 2025 2026`
  - `site:drops.dagstuhl.de hypergraph query algorithm adaptive learning 2024 2025`
- Source: PMLR and arXiv primary records.
- Why necessary: I11 was explicitly named as a possible surviving interface.
- Result: SP-query hypertree learning, CUT-query connectivity and adaptive
  Möbius/edge-detecting algorithms expose real hypergraph-specific query
  phenomena. Their positive component is exact/randomized algorithms and
  information theory, not trained ML; real paired acquisition benchmarks are
  absent.
- Change to prior evidence: **creates a Q2 theory neighbor, not Q1**.

## Question 4: can a theory-only decomposition program sustain 2--3 projects?

- Exact queries:
  - `2026 rerootable hypertree decompositions paper`
  - `2024 2025 dynamic generalized hypertree decomposition hypergraph updates algorithm`
  - `HyperBench 2025 generalized hypertree width benchmark decomposition algorithms`
  - `2025 exact generalized fractional hypertree width FPT open problems`
- Source: arXiv, ACM, Oxford repository and HyperBench primary records.
- Why necessary: P0-B requires positive program depth, not merely failure of ML.
- Result: recent exact/FPT, approximation, parallel, incremental and
  rerootability work plus HyperBench supports a coherent program around
  verifiable, reusable and dynamic decompositions.
- Change to prior evidence: **positive support for P0-B**.

## Work ledger

`D` means deeply inspected in P0; `S` means screened. `Prior` records whether
the exact work was already present in repository evidence.

| # | Work | Year | Depth | Prior | Interface result |
|---:|---|---:|---|---|---|
| 1 | Wang, Arce & Tong, *Generalization Performance of Hypergraph Neural Networks* | 2025 | D | new | structural/spectral HGNN bound, not native width necessity |
| 2 | Grigorescu, Lin & Song, *Learning-Augmented Algorithms for Online Concave Packing and Convex Covering Problems* | 2025 | D | new | generic robust-advice collision |
| 3 | Aamand et al., *Improved Approximations for Hard Graph Problems using Predictions* | 2025 | D | new | graph/set-cover prediction collision |
| 4 | Bresler et al., *Partial and Exact Recovery of a Random Hypergraph from its Graph Projection* | 2025 | D | prior | random-model theorem does not supply natural gold |
| 5 | Bresler, Guo & Polyanskiy, *Thresholds for Reconstruction of Random Hypergraphs From Graph Projections* | 2024 | S | prior family | reinforces conditional identifiability only |
| 6 | Korchemna et al., *Efficient Approximation of Fractional Hypertree Width* | 2024 | D | prior | strong classical Q2 progress |
| 7 | Lanzinger, Razgon & Unterberger, *FPT Parameterisations of Fractional and Generalised Hypertree Width* | 2025 | D | prior | exact FPT Q2 progress |
| 8 | Jiang et al., *Rerootable Hypertree Decompositions* | 2026 | D | prior | representation/reuse program depth |
| 9 | Gottlob et al., *Fast Parallel Hypertree Decompositions in Logarithmic Recursion Depth* | 2024 | D | prior | practical exact decomposition baseline |
| 10 | Fallat et al., *Learning Hypertrees From Shortest Path Queries* | 2024 | D | prior | native query complexity, ML not necessary |
| 11 | Fallat et al., *Distance-based Learning of Hypertrees* | 2025 | D | new | extends Q2 query-theory depth |
| 12 | Chakrabarty & Liao, *Query Complexity of Hypergraph Connectivity and Learnability using CUT Oracles* | 2026 | D | new | native identifiability/query result, no ML requirement |
| 13 | Erginbas et al., *Adaptive Sparse Möbius Transforms for Learning Polynomials* | 2026 | D | prior family | near-optimal adaptive sparse recovery; S1 collision |
| 14 | Chien, Zhou & Li, *HS2: Active Learning over Hypergraphs with Pointwise and Pairwise Queries* | 2019 | S | new to ledger | active labeling exists, but native theory/benchmark depth is limited |
| 15 | Pham & Ta, *A Fast Hierarchical Splitting Approach for Non-Adaptive Learning of Random Hypergraphs* | 2026 | S | new | random-model query algorithm, not real ML coupling |

No search exceeded the declared boundary and no broad query for “hypergraph
machine learning” was used.

## Exact primary sources

1. https://arxiv.org/abs/2501.12554
2. https://proceedings.mlr.press/v258/grigorescu25a.html
3. https://proceedings.mlr.press/v267/aamand25c.html
4. https://proceedings.mlr.press/v291/bresler25a.html
5. https://proceedings.mlr.press/v247/bresler24a.html
6. https://arxiv.org/abs/2409.20172
7. https://arxiv.org/abs/2507.11080
8. https://arxiv.org/abs/2608.17853
9. https://doi.org/10.1145/3638758
10. https://proceedings.mlr.press/v237/fallat24a.html
11. https://arxiv.org/abs/2511.22014
12. https://arxiv.org/abs/2607.01216
13. https://arxiv.org/abs/2602.06246
14. https://proceedings.mlr.press/v89/chien19a.html
15. https://arxiv.org/abs/2605.09970
