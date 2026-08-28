# Paper extraction and contribution-collision matrix

## Coding

`Y/N/P` means yes/no/partial. “Support known?” records what the practical method requires, not only a local theorem. Severity is 0 background, 1 adjacent, 2 same mechanism, 3 same problem, 4 same problem plus mechanism, 5 near-direct collision.

## Paper-by-paper extraction A: problem and observation model

| ID | Paper | Year | Venue | Problem | Data model | Design/query choice | Target | Support known? | Adaptive? | Noise? | Replicates? | Interaction basis? | High-order? |
|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|
| P1 | Stallrich et al., *Optimal design framework for lasso sign recovery* | 2025 | JRSS-B | SSD design for Lasso sign recovery | Gaussian homoscedastic linear main-effects model | choose +/-1 factor-level design entries; HILS coordinate exchange + exact sieve | exact signed support probability along lambda path | No identities; fixed k/effect magnitude/sign prior | No | iid response Gaussian | No | No, generic main effects | No |
| P2 | Singh & Stufken, *Selection of Two-Level Supersaturated Designs* | 2023 | Technometrics | SSD selection tied to Gauss-Dantzig recovery | two-level main-effects screening | Pareto coordinate exchange under EC/WSC criteria | estimation/sign-consistency conditions over active subsets | No identities; k range and positive-sign case | No | homoscedastic simulations | No | No | No |
| P3 | Weese et al., *Group Orthogonal and Constrained Var(s) Designs* | 2021 | Technometrics | SSD construction with group/sign information | two-level main-effects screening | group-orthogonal / constrained Var(s+) design search | screening, especially common positive signs | group/sign prior | No | homoscedastic simulations | No | No | No |
| P4 | Huang et al., *Optimal designs in sparse linear models* | 2020 | Metrika | design for debiased-Lasso estimation/inference | sparse linear model, quantitative factors | approximate design weights then rounding | asymptotic covariance, MSE and test power | nominal local parameter structure | No | standard regression noise | weights can imply repeated points, not biological replicates | generic regression columns | No |
| P5 | Box & Hunter, *2^(k-p) fractional factorial designs*, Parts I-II | 1961 | Technometrics | regular fractions, confounding and resolution | deterministic two-level factorial | choose defining contrast subgroup/fraction | estimability and alias structure | model hierarchy assumptions | No | classical response model | possible but not central | factorial effects | Yes, through alias chains |
| P6 | Tang & Wu, *Constructing supersaturated designs and optimality* | 1997 | Canadian J. Statistics | SSD construction near orthogonality | two-level main effects | deterministic construction optimizing E(s2)-type geometry | correlation/alias quality | No support model | No | not recovery-noise objective | No | No | No |
| P7 | Jones et al., *Model-robust supersaturated and partially supersaturated designs* | 2009 | JSPI | sparse model estimability under unknown active set | two-level main-effects models | exchange search over model space | estimation capacity/model discrimination | unknown identities; fixed active count/core set | No | standard DOE | No | limited to modeled terms | mainly main effects |
| P8 | Smucker & Drew, *Approximate model spaces for model-robust design* | 2015 | Technometrics | scalable robust design across many models | two-level linear models | sample model space + coordinate exchange + large evaluation sample | estimation capacity and average D-efficiency | unknown identities via model distribution | No | standard DOE | No | can include 2FIs | Pairwise |
| P9 | Wainwright, *Sharp thresholds for noisy sparsity recovery* | 2009 | IEEE TIT | exact Lasso signed-support recovery | deterministic or Gaussian design; additive sub-Gaussian/Gaussian response noise | analyzes fixed/random X; does not construct DOE | exact signed support and phase threshold | unknown vector, theory conditional on true support geometry | No | Yes, response noise | No | generic columns | Generic |
| P10 | Young et al., *Graphical comparison of screening designs* | 2024 | JQT | compare screening designs without tuning-procedure artifacts | two-level main-effects linear model | evaluate fixed designs along recovery-probability path | support/sign recovery curves | scenarios specify k/effects/signs | No | simulation/exact Gaussian criterion | No | No | No |
| P11 | Kang et al., *Learning to Understand: Mobius Transform* | 2024 | NeurIPS | sparse low-degree Mobius recovery | exact set-function samples; robust version has iid Gaussian spectral/bin noise | nonadaptive hashing, group-testing delays, peeling | coefficient and support recovery | unknown random/independent support; K,t specified | No | Yes, spectral/bin noise; known magnitude/SNR | No | Mobius/AND | Yes |
| P12 | Erginbas et al., *Adaptive Sparse Mobius Transforms* | 2026 | arXiv | exact sparse Boolean polynomial learning | exact additive evaluation oracle | FASMT adaptive splitting; PASMT few-round disjunct tests | exact support and coefficients | unknown arbitrary support under non-cancellation; s,d specified | Yes/FASMT; few-round/PASMT | No; noisy oracle open | No | Mobius/AND | Yes |
| P13 | Wendler et al., *Sparse non-orthogonal Fourier set functions* | 2021 | AAAI | exact sparse set-function learning | exact evaluation oracle | adaptive restriction-chain queries | exact Fourier support and coefficients | Unknown under generic/non-cancellation assumptions | Yes | No | No | nonorthogonal bases including AND-related | Yes |
| P14 | Stobbe & Krause, *Learning Fourier Sparse Set Functions* | 2012 | AISTATS | compressed recovery of sparse set functions | exact random set-function observations | uniformly random query sets | exact sparse Fourier coefficients | support contained in known candidate collection | No | No | No | orthogonal Fourier/WHT | Yes |
| P15 | Suzumura et al., *Selective inference for sparse high-order interactions* | 2017 | ICML | valid post-selection inference for huge interaction spaces | observational linear regression with interaction features | data fixed; algorithm characterizes Lasso selection event | significant selected high-order interactions | unknown, selected by Lasso | No | response noise in linear model | No | product interactions | Yes |
| P16 | Chen et al., *Diamond* | 2025 | Nature Machine Intelligence | error-controlled non-additive interaction discovery | iid observational feature-response data + fitted ML model | no experimental row design; model-X knockoffs | interactions with controlled FDR | unknown | No | observational/model perturbation | No | non-additive model interactions | Primarily pairwise |
| P17 | Diaz et al., *Sparse polynomial chaos via compressed sensing and D-optimal design* | 2018 | CMAME | budgeted sparse polynomial approximation | computational model evaluations in polynomial-chaos basis | sequential/adaptive D-opt selection from candidate pool | sparse coefficient/prediction accuracy | estimated support updated from coefficients | Yes | numerical/model setting; not replicate biology | No | polynomial chaos | Yes |

## Paper-by-paper extraction B: recovery, evidence, and collision

| ID | Sign recovery? | FDR? | Theory? | Real data? | Algorithm | Public code | Closest overlap with META1 | Remaining difference | Severity |
|---|---|---|---|---|---|---|---|---|---:|
| P1 | Yes, exact | No | KKT probability, symmetric relaxation | No | HILS | supplementary artifacts; no independent repository located | design objective is signed support recovery with unknown support identities | free SSD entries; main effects; homoscedastic; no fixed Boolean rows/order target | 4 |
| P2 | Weak sign consistency | No | recovery-condition motivated | No | DCD Pareto exchange | not located | support-aware design under unknown active subsets | Dantzig/main effects; no AND/replicates | 4 |
| P3 | Positive-sign screening | No | criterion/construction results | No | constrained Var(s) and group construction | not located | sign information changes optimal correlations | prior group/sign structure; main effects | 3 |
| P4 | No exact sign target | No; test power | equivalence/local optimality | No | iterative approximate design + rounding | not located | sparse-estimator-aware design, inference objective | approximate design; not fixed-row support recovery | 3 |
| P5 | No | No | algebraic DOE theory | No | regular fraction construction | classical tables/software | limited runs and exact aliases among interactions | no sparse estimator or noisy support objective | 3 |
| P6 | No | No | construction/optimality | No | combinatorial SSD construction | not located | correlation and near-orthogonality heuristics | main effects, not recovery-specific | 2 |
| P7 | No | No | estimability/model-discrimination results | No | model-robust exchange | not located | robustness over unknown sparse active set | estimability, not signed Lasso; main effects | 3 |
| P8 | No | No | empirical algorithm study | No | sampled-model coordinate exchange | supplementary code reported | scalable averaging over enormous unknown-support model spaces | D-efficiency, mostly main/2FI; no Mobius noise | 3 |
| P9 | Yes | No | sharp sufficient/necessary thresholds | No | Lasso analysis | not applicable | noisy response signed-support recovery and incoherence | no row-selection algorithm, replicates, or AND constraint | 3 |
| P10 | Yes | No | exact/simulation probability evaluation | No | graphical recovery-path comparator | supplementary code | evaluates designs by support/sign probability | comparison, not fixed-row construction; main effects | 3 |
| P11 | coefficients include signs | No | sample/time complexity and robust asymptotics | ML model examples | nonadaptive SMT | no verified official repository | noisy sparse high-order Mobius query recovery | spectral rather than raw response noise; random support; no replicate/FDR estimand | 4 |
| P12 | coefficients include signs | No | near-optimal query bounds | hypergraphs from real circuit/metabolic topology, exact oracle | FASMT/PASMT | no repository located | direct AND-basis query selection and exact support recovery | exact oracle/non-cancellation; no biological outcomes | 4 |
| P13 | coefficients include signs | No | exact-query bounds | auctions/facility/sensor set functions | SSFT variants | no verified official repository | adaptive sparse nonorthogonal/AND-related set-function recovery | exact oracle; no noise/design inference | 3 |
| P14 | coefficient recovery | No | random-sampling exact-recovery theorem | graph/surrogate tasks | compressed recovery | article artifacts | sparse set-function sampling under known candidate support universe | orthogonal basis, exact observations | 2 |
| P15 | selected coefficient inference | selective p-values, not global FDR design | selective-inference validity | HIV drug response | interaction-tree pruning/selection-event characterization | author GitHub linked by PMLR | sparse high-order interaction target and inferential reliability | observational X; no acquisition design/Mobius factorial rows | 3 |
| P16 | sign not primary | Yes | model-X knockoff control | biomedical datasets | Diamond knockoff + distillation | article code/data links | FDR-controlled interaction discovery | fitted-model pairwise interactions; no factorial acquisition | 3 |
| P17 | coefficient recovery, sign incidental | No | design/compressed-sensing analysis | physical computational models | sequential DSP | article implementation not independently verified | adaptive D-opt sampling for sparse polynomial coefficients | different basis and prediction/approximation goal | 3 |

## Contribution decomposition C1-C10

Components:

- C1 real replicated factorial benchmark formulation
- C2 signed order>=3 support estimand
- C3 partial measurement protocol
- C4 design-aware row/community selection
- C5 unknown-support design
- C6 noise/replicate awareness
- C7 support/FDR awareness
- C8 high-order AND/Mobius structure
- C9 algorithm/theory
- C10 real microbial evaluation

| Work | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 Stallrich 2025 | N | P | Y | Y | Y | P | support Y/FDR N | N | Y | N |
| P2 Singh-Stufken 2023 | N | P | Y | Y | Y | P | support Y/FDR N | N | Y | N |
| P3 Weese 2021 | N | P | Y | Y | P | P | P | N | Y | N |
| P4 Huang 2020 | N | N | Y | Y | P | P | inference P | N | Y | N |
| P5 Box-Hunter 1961 | N | N | Y | Y | N | P | N | P | Y | N |
| P6 Tang-Wu 1997 | N | N | Y | Y | N | N | N | N | Y | N |
| P7 Jones 2009 | N | N | Y | Y | Y | P | P | N | Y | N |
| P8 Smucker-Drew 2015 | N | N | Y | Y | Y | P | P | P | Y | N |
| P9 Wainwright 2009 | N | Y | N | N | P | response noise Y/replicate N | support Y/FDR N | N | Y | N |
| P10 Young 2024 | N | P | Y | evaluator only | P | P | support Y/FDR N | N | Y | N |
| P11 Kang 2024 | N | P | Y | Y | Y | spectral noise Y/replicate N | support Y/FDR N | Y | Y | model-only |
| P12 Erginbas 2026 | N | P | Y | Y | Y | N | support Y/FDR N | Y | Y | topology-only |
| P13 Wendler 2021 | N | P | Y | Y | Y | N | support Y/FDR N | P | Y | N |
| P14 Stobbe-Krause 2012 | N | P | Y | random | P | N | support Y/FDR N | N | Y | N |
| P15 Suzumura 2017 | N | Y | N | N | Y | response noise P | inference Y | product HOI | Y | biomedical, not microbial factorial |
| P16 Chen 2025 | N | N | N | N | Y | perturbation P | FDR Y | interaction P | Y | microbial observational example P |
| P17 Diaz 2018 | N | P | Y | Y | adaptive | numerical noise P | support P | polynomial | Y | N |
| META1 frozen | Y | Y | Y | Y | empirical only | replicates observed, mechanism unsupported | scored, no control | Y | heuristic only | Y |

## Matrix conclusion

No prior paper occupies all C1-C10. That fact alone does not establish novelty. C3-C5 and C7-C9 are already heavily occupied; C8 is occupied by SMT/ASMT; C1/C10 are mostly application components. A viable contribution must therefore arise from a nontrivial coupling of fixed Boolean row feasibility, order-targeted signed support, and unknown-support robustness—not from adding microbial data to HILS or adding Gaussian noise to ASMT.
