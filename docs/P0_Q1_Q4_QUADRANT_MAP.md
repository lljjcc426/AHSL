# P0 Q1--Q4 quadrant map

## Necessity tests

Hypergraph theory is necessary only when removing native concepts such as
acyclicity, GHD/GHW, FHD/FHW, fractional covers, hypergraph cuts/transversals or
hypertree structure changes the theorem, target or complexity. ML is necessary
only when exact algorithms, optimization, Bayesian inference, sparse recovery
or classical statistics leave a measured residual.

| Quadrant | Interfaces | Count | Interpretation |
|---|---|---:|---|
| Q1: hypergraph theory necessary, ML necessary | none | 0 | no interface passes both necessity tests |
| Q2: hypergraph theory necessary, ML not necessary | I11 adaptive/query algorithms; I13 canonical/reusable/dynamic decompositions | 2 | supports a theory/algorithms pivot |
| Q3: ML may be necessary, hypergraph theory not necessary | I1, I2, I3, I4, I5, I6, I7, I9, I10, I12 | 10 | valid adjacent ML work may exist, but not the intended strong coupling |
| Q4: neither strongly necessary | I8 generic hypergraph regularization/inductive bias | 1 | use only as a secondary representation choice |

## Closest rejected Q1 candidates

### Parameter-aware statistical generalization

The 2025 HGNN generalization work establishes PAC-Bayes bounds using model
norms and hypergraph structural/spectral quantities. It does not establish that
GHD/FHD, fractional covers or acyclicity control a real learning residual beyond
incidence/spectral descriptions. Removing native decomposition theory leaves
the classification problem essentially unchanged. Result: **Q3, not Q1**.

### Robust learning-augmented GHD/FHD algorithms

Robust advice and exact fallback are coherent, and hypergraph decompositions are
native. However, R0 found neither a two-family classical gap nor affordable,
family-disjoint prediction labels. Removing ML leaves an active exact and
approximation theory program; removing hypergraph theory leaves generic
learning-augmented optimization. Result: **Q3 as formulated; Q2 after removing
ML**.

### Adaptive/query algorithms

Shortest-path, CUT and edge-count queries reveal genuine hypergraph-specific
identifiability and query-complexity phenomena. Yet current positive results are
algorithmic and information-theoretic; learned predictors are unnecessary.
Result: **Q2**.

## P0-A hard gates

Because Q1 is empty, there is no surviving candidate to which G1--G12 can all
be assigned PASS. The strongest attempted candidate, robust
learning-augmented GHD/FHD search, has:

| Gate | Status | Reason |
|---|---|---|
| G1 ML necessary | FAIL | no measured residual/predictability |
| G2 native hypergraph theory necessary | PASS | decomposition validity and width are native |
| G3 real accepted benchmark | PASS | HyperBench/CQ/CSP structure exists |
| G4 second validation route | FAIL | no second paired factor-execution/prediction route |
| G5 identifiable/evaluable target | PASS for decomposition certificate | validity and width can be checked; optimal labels remain costly |
| G6 material classical residual | FAIL | R0 threshold not met and decomposition-only downstream residual unmeasured |
| G7 prior-art residual | FAIL | active exact/approximation/LP/FPT decomposition literature narrows the gap |
| G8 not generic learning | FAIL | advice/ranking component remains generic algorithm selection |
| G9 feasible first project | PASS as theory, not as ML experiment | bounded HyperBench work is feasible |
| G10 2--3 project sequence | PASS only after removing ML | theory sequence is coherent |
| G11 transferred evidence not strong | FAIL | R0 transfers strongly |
| G12 no artificial reopening | PASS | can start a theory program without reopening R0 |
