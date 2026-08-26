# N1.0 CertPath supervision, attainability, leakage and headroom gate

Search/freeze date: 2026-08-26. Decision frozen on branch `project-n1.0-supervision-attainability-gate` from N0 commit `3a7839ce35f8bdf925562cc99fe09ff070d86ba7`.

## 1. Executive decision

**N1.0-C — NO-GO: supervision / representability.** Only 961/1,620 natural candidate tasks (59.32%) are positive-cost attainable, below the predeclared 70% hard gate. In addition, 456/1,620 curated gold sets are infeasible without prohibited internal-source repair. No ML model was trained.

## 2. Refreshed prior art

Eighteen closely relevant primary works were retained and ten deeply inspected. No direct predecessor was found that combines learned reaction/hyperedge costs, exact general directed-hyperpath decoding, and real curated pathway-recovery supervision. The 2026 hyperpath-deletion/inverse-hyperpath work is the closest new theory pressure but lacks biological learning and recovery evaluation. Prior-art gate: PASS.

## 3. Reactome release freeze

Historical V89 (2024-06) and later V97 (2026-06-30) official human BioPAX Level 3 archives were frozen. SHA-256 values are `1570AB7B...E94B` and `EFEDB0F6...A4D7`; full values, URLs, bytes, timestamps, and CC0 terms are in `docs/N1_0_DATA_FREEZE.md`. V97 contains 2,883 parsed curated pathways; V89 contains 2,711.

## 4. Published benchmark reconciliation

The published 5,066 Reactome instances are single-target optimization queries, of which 2,432 are reachable—not supervised pathway-set examples. Mmunin's biological recovery section evaluates ten selected curated pathways; five required manually supplied supplementary/internal sources. N1.0's 1,620 whole-pathway labels are a new deterministic benchmark construction and do not inherit the scale or accuracy claims of the 5,066-target benchmark.

## 5. Directed-hypergraph construction

Physical-entity state/compartment URIs are vertices. Reactants plus direct positive regulators form a reaction tail; products form its head. AND tails, cycles, self-loops, complexes, and multi-product heads remain native. V97 has 26,345 vertices and 15,613 hyperedges; 13,683 are multi-tail. Deviations from the historical Pathway Commons conversion are documented and were not tuned to match counts.

## 6. Natural supervised task universe

V97 yields 1,641 leaf pathways with retained reactions and 1,620 query-valid candidate tasks, one per unique curated pathway. The benchmark creates neither repeated target variants nor solver-selected sublabels.

## 7. Query semantics

A query supplies the full release hypergraph, all global network sources, declared pathway-boundary inputs, and all terminal pathway outputs conjunctively. A future domain user would have to supply these boundary conditions. This is whole-process reconstruction between declared endpoints, not de novo endpoint discovery.

## 8. Gold definition

The gold (P^*) is the complete retained reaction membership of one leaf Reactome pathway. It was not shortened, repaired, or redefined after solver inspection. Gold size has mean 8.45, median 6, p95 25, and maximum 66.

## 9. Source leakage audit

Allowed sources are `GLOBAL_NETWORK_SOURCE` and query-visible `QUERY_VISIBLE_PATHWAY_BOUNDARY`. `GOLD_INTERNAL_REPAIR` is prohibited. No retained primary task uses repair, so the source-leakage gate passes under the explicitly declared reconstruction query. However, 456 natural labels are infeasible without repair or a changed query; excluding them heavily selects against cyclic biology and drives the separate representability failure.

## 10. Gold feasibility

Gold is feasible for 1,164/1,620 tasks (71.85%). The remaining 456 are outside the decoder output class under the frozen source policy and are not counted as model errors or silently repaired.

## 11. Positive-cost attainability theorem

For a finite feasible family and strictly positive additive edge costs, (P^*) can be the unique minimum if and only if it has no feasible proper subset. Necessity follows from strict positivity; sufficiency assigns cost \(\varepsilon<1/|P^*|\) to gold edges and one to all outside edges. The proof is valid under Mmunin's superpath/minimal-hyperpath semantics.

## 12. Attainability empirical results

Exactly 961/1,620 natural candidates are attainable: 59.32% of the required denominator, or 82.56% conditional on feasibility. The former is the frozen hard-gate statistic. Exhaustive validation covered 64 small hypergraphs and 1,847 feasible gold sets with zero decision and zero solver-minimum mismatches.

## 13. Selection-bias analysis

There are 712 qualified feasible, attainable tasks with at least three reactions. Qualified versus excluded mean sizes are 8.28 versus 8.59, but cycle rates are 5.90% versus 58.26%. Thus the survivor set suppresses cyclic pathways drastically; reporting only it would make the domain look more compatible with the method than it is.

## 14. High-order semantic activity

At least one multi-tail reaction appears in 98.52% of natural gold sets; the mean within-gold multi-tail fraction is 87.72%. This is strong evidence that the annotations themselves are higher-order. It is not evidence that exact and projected decoders disagree.

## 15. Pairwise graph reduction audit

NOT EVALUATED after the upstream representability hard stop. The implementation includes a simple projection and tests showing how AND prerequisites can be violated, but no benchmark-wide semantic-invalid rate, output-disagreement rate, F1, or runtime was produced. Hypergraph-necessity gate therefore has no PASS evidence.

## 16. Pathway-overlap audit

Among 1,311,390 candidate-pathway pairs, 438 have nonzero reaction overlap, one is an exact duplicate, and 22 are strict subset pairs. Most pairs are disjoint, but stable reaction identities still cross the family split and may not be used as lookup features.

## 17. Family-disjoint split

A deterministic four-family test holdout gives 591 train and 121 test tasks. It has 25 shared reaction IDs, equal to 2.28% of test reaction IDs; entity overlap is 288/2,202 (13.08%). Hierarchy overlap is zero. All 29 families occur among the qualified universe.

## 18. Reaction-disjoint stress split

Shared-reaction connected components yield a zero-reaction-overlap split of 570 train and 142 test tasks; the largest component has 29 tasks. The test side is below 300, so this split is a useful stress test but infeasible as the primary scale claim.

## 19. Temporal split

V89→V97 classification yields 104 NEW, 71 MODIFIED, and 1,445 UNCHANGED V97 tasks. Temporal evidence is WEAK: only 175 tasks are changed/new, though historical feature isolation is technically possible. Unchanged tasks are not called temporal OOD.

## 20. Feature leakage audit

Historical reaction type, arity, compartment/state, and graph-local features are safe. Pathway membership/hierarchy as reaction features, reaction-ID parameters, and internal gold repair are target leakage. Current-release annotations on historical tasks are temporal leakage. Text/external embeddings remain unverified. No feature model was fitted.

## 21. Classical exact baseline

NOT EVALUATED after the mandated early stop. Published Mmunin results are not substituted because their source-target task differs from N1.0. No unit-cost or handcrafted-cost N1.0 F1 was generated.

## 22. Hhugin

NOT RUN. Consequently Hhugin biological F1 and exact-objective agreement are unavailable rather than zero.

## 23. Baseline headroom

NOT EVALUATED after upstream failure. Mean/median classical F1, fraction with F1 at most 0.95, and theoretical F1 headroom are unavailable. The headroom gate is recorded FAIL—not established, not as an empirical saturation finding.

## 24. Baseline failure taxonomy

Upstream structural categories are 456 `GOLD_NOT_FEASIBLE`, 203 feasible-but-`POSITIVE_COST_UNATTAINABLE`, and 249 attainable tasks with fewer than three gold reactions. Decoder-specific crosstalk, tie, alternative-branch, and timeout categories were not measured systematically.

## 25. Solver runtime

No production runtime distribution was run. A 5-edge diagnostic solved in 0.043 s with seven cuts; a 20-edge multi-target diagnostic hit 10 s after 191 cuts. These examples do not support median/p95/max claims. Solver-feasibility gate was not reached.

## 26. Robust certificate theory

For intervals \([\ell_e,u_e]\), the worst competitor gap against (P) is obtained with weight (u_e) on (P) and \(\ell_e\) outside. A positive minimum gap certifies that (P) remains uniquely optimal throughout the box. The theorem is proved algebraically.

## 27. Cost-uncertainty semantics

The robust margin reduces to a second exact solve with \(\sum_{e\in P}x_e\le |P|-1\), excluding all supersets of (P). A simple exact-vector no-good cut is insufficient under superpath variables. Deterministic interval certification is distinct from statistical calibration; marginal cost coverage does not imply joint-vector coverage.

## 28. Evidence FOR CertPath

There are 712 nontrivial qualified tasks across 29 families; 98.52% of natural labels include multi-tail reactions; exact attainability classification has zero mismatches in 1,847 enumerated cases; and no fatal direct prior-art collision was found.

## 29. Evidence AGAINST CertPath

The strongest evidence is structural: only 59.32% of the natural universe is positive-cost attainable, while 28.15% is infeasible without internal repair. Filtering to survivors reduces the cycle rate from 35.25% overall to 5.90%, so the apparent benchmark would be strongly method-selected.

## 30. Hard-gate evaluation

| Gate | Status | Evidence |
|---|---|---|
| G1 prior art | PASS | no direct essential-combination collision |
| G2 coherent supervised query | PASS, narrow | declared boundary-to-terminal whole-pathway reconstruction |
| G3 no primary internal repair | PASS | 456 candidates are rejected, never repaired; retained tasks use declared boundaries only |
| G4 attainability at least 70% | FAIL | 59.32% |
| G5 at least 300 qualified | PASS | 712 |
| G6 at least four families | PASS | 29 |
| G7 material multi-tail annotations | PASS as annotation activity | 98.52%; decoder necessity not reached |
| G8 graph projection not equivalent | NOT REACHED | stopped after G4 |
| G9 leakage-resistant split | PARTIAL | family split feasible; reaction-disjoint test only 142 |
| G10 classical headroom | NOT REACHED | stopped after G4 |
| G11 exact solve practicality | NOT REACHED | no distribution |
| G12 no post-hoc target rescue | PASS | one frozen natural definition |

One hard-gate failure is sufficient. G4 fails decisively, with G3 adding an independent supervision warning.

## 31. Final decision

**Decision N1.0-C — NO-GO: supervision / representability**

> CertPath is stopped because the available curated supervision is too small, leaky, structurally infeasible, or frequently unattainable under positive additive shortest-hyperpath decoding.

This branch does not update `docs/N1_PROPOSAL.md`, create an N1 learning branch, or train any model.

## 32. Exact next action

Freeze and review this negative result. Close CertPath. Do not immediately search for another biological hypergraph application; return to project-level topic selection only after user review.

### A--AT frozen handoff

| Field | Result |
|---|---|
| A | branch `project-n1.0-supervision-attainability-gate`; final SHA is Git metadata reported on delivery |
| B | 2026-08-26 |
| C | 18 closely relevant / 10 deeply reviewed |
| D | NO direct collision found |
| E | Reactome V89 and V97 |
| F | V97: 2,883 parsed curated pathways; 1,641 leaf pathways with retained reactions |
| G | 1,620 raw candidate queries |
| H | 5,066 optimization targets, 2,432 reachable; only ten curated recovery cases, five with added sources |
| I | 1,620 actual pathway-set gold tasks constructed |
| J | 456 require internal repair or a changed query to become feasible |
| K | 1,164 / 71.85% gold feasible |
| L | 961 / 59.32% natural-universe attainable; 82.56% among feasible |
| M | PROVED under finite Mmunin semantics |
| N | 1,847 feasible gold sets / 0 mismatches |
| O | 712 qualified tasks |
| P | 712 unique qualified pathways |
| Q | 29 top-level families |
| R | mean 8.45; median 6; p95 25; max 66 |
| S | 98.52% of tasks contain a multi-tail reaction; mean gold multi-tail fraction 87.72% |
| T | NOT EVALUATED—upstream stop |
| U | NOT EVALUATED—upstream stop |
| V | family split 591 train / 121 test |
| W | 25 reaction IDs; 2.28% of test IDs |
| X | zero-overlap 570/142 exists, but test <300; infeasible as primary evidence |
| Y | 104 NEW / 71 MODIFIED / 1,445 UNCHANGED |
| Z | NOT EVALUATED—upstream stop |
| AA | NOT EVALUATED—upstream stop |
| AB | NOT EVALUATED—upstream stop |
| AC | NOT EVALUATED—upstream stop |
| AD | NOT RUN |
| AE | NOT RUN |
| AF | 456 infeasible; 203 feasible but unattainable; 249 attainable but <3 reactions |
| AG | NOT EVALUATED; two diagnostics only |
| AH | PROVED |
| AI | YES, with superset exclusion in the second exact solve |
| AJ | 712 tasks, 29 families, 98.52% multi-tail prevalence |
| AK | 59.32% attainability and 456 repair-dependent/infeasible labels |
| AL | PASS |
| AM | FAIL |
| AN | PASS; no retained task is repaired and boundary inputs are query-visible |
| AO | FAIL—not established because benchmark audit was stopped upstream |
| AP | FAIL—not established because baseline audit was stopped upstream |
| AQ | PASS |
| AR | **N1.0-C** |
| AS | **NO** |
| AT | freeze N1.0-C, close CertPath, await review, then return to project-level topic selection |
