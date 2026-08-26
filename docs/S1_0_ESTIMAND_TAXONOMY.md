# S1.0 estimand taxonomy

An interaction coefficient is a contrast defined by a response scale and a null. It is not invariant biological ground truth.

## Formal set-function baseline

For `f:2^N -> R`, on a declared additive response scale,

`beta_S = sum_{T subseteq S} (-1)^(|S|-|T|) f(T)`.

The inverse is `f(A)=sum_{S subseteq A} beta_S`. These two triangular transforms have unit diagonal when subsets are ordered by inclusion, so a complete noiseless `2^p` table is exactly invertible and needs no ML. Missing subset rows remove equations and create an inverse problem; replicate noise turns the equations into estimation; a sparse coefficient vector supplies the assumption used by lasso/compressed sensing. The implementation and exact inversion tests are in `src/interaction_structure/estimands/mobius.py`.

## Domain taxonomy

| Domain / estimand | Scale | Null | Lower-order data | Identification here | Sign / zero meaning | Monotone invariant? | Acceptance and limitation |
|---|---|---|---|---|---|---|---|
| yeast raw epsilon | colony fitness | multiplicative single-mutant fitness | singles and triple | noisy | negative is worse than multiplicative null; zero is null-relative | no | standard SGA precursor, but leaves digenic effects in a trigenic score |
| yeast adjusted tau-SGA | colony fitness | multiplicative expectation with two digenic effects subtracted and scaled by third-gene fitness | triple, singles, matching doubles | identifiable with noise for measured triples | negative is aggravating trigenic effect | no | accepted target in Kuzmin; two-replicate reliability is limited |
| microbial Möbius, raw CFU | CFU | additive finite difference | every subset of six companions for each focal | direct with replicate noise | sign is raw-abundance contrast | no | mathematically exact but heteroscedastic and biologically less natural |
| microbial Möbius, log10 CFU | log10 CFU | additive on log scale, hence multiplicative on CFU scale | same complete `2^6` panel | direct with replicate noise | sign is multiplicative abundance contrast | no | preferred because the source study supports log-normal response; still scale-specific |
| Walsh--Hadamard landscape coefficient | normalized/relative abundance | orthogonal parity basis, often order-weighted | broad factorial coverage | identifiable on complete panel | sign depends on coding and weighting | no | established in compressed-sensing microbiome work; not numerically identical to Möbius support |
| ANOVA interaction | transformed response | orthogonal decomposition relative to design distribution | balanced cells or explicit weighting | direct on complete balanced panel | deviation from lower-order ANOVA components | no | distribution/design dependent |
| drug DA / net interaction | growth | source paper's dose-additivity comparison | focal dose combination and relevant constituent/lower combinations | direct per dose context | synergy/antagonism/suppression relative to null | no | domain-accepted in this dataset; fixed drug-set sign is not stable |
| drug emergent `E_k` | growth | highest-order effect versus all relevant lower-order combinations | complete lower-order dose-matched lattice | direct per dose context | hidden/emergent suppression has explicit mechanistic comparison | no | scientifically useful and distinct from only comparing singles |
| Bliss independence | relative viability/growth | product of single-agent effects | matched singles | direct if matched | sign is deviation from independent action | no | common; assumes probabilistic independence |
| Loewe additivity | dose-response | dose equivalence / isobole | single-drug dose curves | model-dependent | synergy/antagonism relative to dose equivalence | no | difficult for drugs with dissimilar mechanisms or poor curve fit |
| Highest Single Agent | viability/growth | best single-agent effect | matched singles | direct | incremental benefit over best single | no | simple but ignores lower-order combinations and hidden suppression |
| ZIP | response surface | zero-interaction potency | fitted single and combination dose curves | model-dependent | deviation from fitted potency surface | no | useful for dose matrices, not a unique set-level coefficient |

## Future structural outputs actually implied by the audit

- Yeast: a probability or posterior for latent strong negative tau status of a *measured* triple, or score prediction for unmeasured triples using explicit PPI/feature assumptions. These are not the same task.
- Microbiome: signed, weighted, uncertainty-bearing support over companion-species subsets for each focal strain.
- Drug: `support(S,c)` plus `beta_S(c)`; a context-free `support(S)` is contradicted by the observed dose behavior.
