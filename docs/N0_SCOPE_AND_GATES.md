# Project N0 scope and gates

## Decision question

Project N0 asks a narrow question: **which real machine-learning or learned-systems problem intrinsically needs a hypergraph/high-order object and a functional theoretical guarantee?** It is an independent topic-discovery gate, not AHSL Phase B1 and not an application of the A0--A1.5 estimator.

Search date: 2026-08-26. Literature horizon: through 2026-08-26.

## Frozen provenance

- N0 branch: `project-n0-topic-discovery-gate`
- branch point: B0 frozen SHA `674d712debe1b29d262159b13f6e3bda0bc252a9`
- A1.5 reference SHA (not the branch point): `930ebc003cbc35a5704e3eb76200b15d0c7a17d3`
- N0 is search and decision only. No neural model, optimizer, decomposition learner, or scientific experiment was implemented.

## In scope

The mandatory families A--K were screened, with two additional families found during search:

1. learned database query optimization;
2. learned exact inference in high-order factor graphs;
3. tensor-network contraction;
4. CSP/SAT/WMC;
5. relational and factorized ML;
6. structured prediction with high-order factors;
7. scientific ML with native high-order constraints;
8. HNN expressivity versus computational width;
9. causal/probabilistic computation;
10. neural combinatorial optimization with certificates;
11. learned hypergraph partitioning/decomposition;
12. directed-hypergraph pathway inference (discovered family);
13. learning-augmented exact metabolic factories/robust pathways (discovered family).

## Out of scope

- another synthetic alpha-acyclic recovery task;
- an HNN/GNN application whose high-order object is only a representation choice;
- decomposition-quality prediction without a downstream or solver-level effect;
- proprietary-only workloads;
- a one-shot combinatorial solver with no cross-instance learning problem;
- implementation of N1.

## Hard gates

| Gate | Pass condition | Operational test used in N0 |
|---|---|---|
| G1 real problem | recognized scientific/systems problem | peer-reviewed task and active benchmark/community |
| G2 public reproducibility | usable public workload | downloadable data, documented schema, usable license or research-use terms |
| G3 native high-order | graph reduction loses semantics or algorithmic property | explicit graph-reduction audit |
| G4 real ML | statistically meaningful cross-instance target | repeated queries/pathways/instances with grouped split |
| G5 necessary theory | guarantee affects output or computation | exactness, certificate, bound, fallback, or tractability |
| G6 residual | classical and learned baselines leave room | strongest-baseline and oracle-gap audit |
| G7 measurable | decisive primary metric exists | runtime, memory, F1, exactness, calibration, or cost |
| G8 novelty | more than a neural score on an old solver | exact-keyword collision search and one-sentence contribution test |
| G9 feasible | normal academic compute | bounded data and CPU/GPU estimate |
| G10 falsifiable | bounded failure is interpretable | predeclared kill test and stop rule |

Hard-gate failure overrides the /60 score.

## Finalist threshold

A finalist must pass G1--G10, score at least 42/60, have no fatal closest-prior-art collision, have a usable benchmark now, state a paper-level contribution, and admit a bounded first kill test. Six candidates reached the semifinal; only one met the finalist rule.

## Exact decision vocabulary

- N0-A: GO; recommend one project for N1 feasibility testing.
- N0-B: CONDITIONAL HOLD; an external benchmark/data/software dependency blocks immediate work.
- N0-C: NO-GO within width-based hypergraph ML.
- N0-D: NO-GO for the current hypergraph-theory × ML theme.

The decision reached in N0 is **N0-A** for one narrow directed-hypergraph pathway project. This does not validate width-centered learned decomposition as the primary project.
