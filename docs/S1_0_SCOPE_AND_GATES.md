# S1.0 scope and frozen gates

Search and analysis date: **2026-08-27 (Asia/Shanghai)**. Branch base: `283dfbfa88c9e5e1c2ac3cbcf571859523c41d07`.

This phase audits one claim only: whether incomplete/noisy combinatorial response panels support a scientifically meaningful, order-3-or-higher support-recovery problem with residual beyond classical methods. It does not develop or train a new ML model. The closed A0--S0 lines remain unchanged.

## Frozen before analysis

| Gate quantity | Frozen value | Rationale |
|---|---:|---|
| microbial material effect | 0.10 log10 CFU | about a 26% multiplicative change, in addition to a 95% bootstrap interval excluding zero |
| bootstrap confidence / draws | 95% / 500 | replicate-aware uncertainty at tolerable audit compute |
| estimand support Jaccard | 0.60 median | prompt's suggested meaningful-overlap threshold |
| overlapping-support sign agreement | 0.80 median | prompt's suggested sign-stability threshold |
| classical sufficiency | support F1 0.85 | prompt's suggested saturation threshold |
| material subgroup miss | 15% | prompt's suggested residual threshold |
| yeast published strong negative | `p<0.05` and `tau<-0.08` | Kuzmin et al. published structural rule |

No unmeasured intervention set is treated as a negative. Labels are `STRONG_POSITIVE`, `STRONG_NEGATIVE`, `UNCERTAIN_OR_NULL`, or `UNKNOWN`.

## Five-question result

| Question | Result | Evidence |
|---|---|---|
| Q1 defensible estimand? | PASS | tau-SGA, replicate-aware log-CFU Möbius coefficients, and dose-specific drug DA/emergent contrasts are each domain-defensible. |
| Q2 stable enough? | PASS, narrow | microbial median raw/log Jaccard 0.633 and sign agreement 1.000 pass; 2/7 focal landscapes individually miss Jaccard 0.60. Drug support is not stable as a context-free set label. |
| Q3 two direct real benchmark families? | FAIL | only the seven-strain microbial panel supports clean partial-factorial recovery with observed full truth. Yeast supports noisy score prediction but not direct support recovery for unmeasured triples without external side information; drug-set support is dose-dependent. |
| Q4 enough data after leakage control? | FAIL for the common problem | yeast retains rows under strict splits, but the held-out structural truth for unmeasured triples is absent; microbial has seven dependent 64-cell landscapes; drug has only 182 drug sets over eight identities. |
| Q5 material classical residual? | FAIL as a cross-domain research residual | a large masking residual exists on the small microbial panel, but it is a single-domain retrospective result; yeast's remaining route is already Dango-style side-information prediction and the sparse-Möbius oracle setting is occupied by 2024/2026 work. |

Because Q3--Q5 fail, the exact decision is **S1.0-C — NO-GO: ESTIMAND / IDENTIFIABILITY**. The failure is not that every domain lacks a coefficient; it is that the same directly evaluable structural-learning target does not survive in at least two real domains.
