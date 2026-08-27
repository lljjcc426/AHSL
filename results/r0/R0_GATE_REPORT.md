# Project R0 Gate Report

## 1. Executive decision

**R0-E — NO-GO: GENERIC SOLVER-LEARNING SATURATION.**

Fixed high-order factor structures and exact/certified computation form a valid
scientific interface. Strategy can matter dramatically, and prediction can be
insulated from correctness. However, the bounded accepted-benchmark audit did
not find a material residual among competent classical VE policies, while the
remaining proposals reduce to learned branching, engine selection, join-cost
prediction or tensor contraction planning. Hypergraph-specific value was not
demonstrated beyond primal/standard solver features on two factor benchmark
families.

Six candidates were screened. Zero satisfy every hard gate, so there are zero
semifinals and zero finalists. No R1 proposal is created and no ML model is
trained.

## 2. Search scope

The search was completed on **2026-08-27**. It screened **63** directly relevant
primary works/resources, deeply reviewed **24**, and deeply reviewed **11**
works from 2024--2026. The scope covered exact PGM inference, CSP/CP, HD/GHD/FHD
theory, FAQ/joins, tensor contraction, algorithm selection and
learning-augmented guarantees without expanding to the entire learned SAT/MIP
literature.

## 3. Exact-inference problem definition

Given a known factor hypergraph and factor/constraint data, the downstream task
is exact partition/probability-of-evidence, marginals, MAP/MPE or exact CSP
solving. A learned component may rank or propose a strategy. Exact algorithm
semantics, a decomposition verifier, an admissible bound or a complete fallback
must remain responsible for correctness.

Learning may change runtime, memory and search. It may not change the returned
mathematical answer.

## 4. High-order structural representation

Native factor scopes are hyperedges. In the local official UAI archive, 85 of
175 models have maximum factor arity at least three and the maximum arity is 14.
The representation is not merely formal: table sizes, domain cardinalities,
nonzero support and deterministic entries are recorded.

A single large hyperedge has GHW one but a clique primal graph. This theoretical
separation is real, yet it does not make a dense large factor cheap. Practical
high-order advantage requires compact or sparse factor representation.

## 5. Classical inference algorithms

The required foundation includes variable and bucket elimination, junction-tree
propagation, recursive conditioning, AND/OR search, knowledge compilation and
constraint propagation plus search. These algorithms are exact under their
declared arithmetic/semiring and differ mainly in decomposition, time-memory
tradeoff and exploitation of determinism/sparsity.

Min-fill, weighted min-fill, min-degree and factor-entry-aware elimination were
implemented as fair R0 baselines. Random orders were diagnostic only.

## 6. Width/decomposition theory

Dense VE is controlled by order-dependent induced width and domain sizes.
GHD/FHD and fractional edge covers can bound sparse/native multiway operations
more sharply. `fhw <= ghw <= hw`; GHW one characterizes alpha-acyclicity.

Recognition and construction are nontrivial. Recent 2024--2026 algorithms give
parallel exact HD search, bounded-intersection GHW approximation, FHW
approximation, LP/branch-and-bound methods and parameterized exact algorithms.
R0 therefore does not treat width optimization as a differentiable or cheap
subroutine. No exact GHW/FHW values are claimed locally.

## 7. Learning-augmented algorithms literature

The relevant contract is consistency under good prediction, robustness under
bad prediction and deterministic fallback. Exact inference supports this cleanly:
a poor complete order is slow but exact; a proposed decomposition can be
verified; a branch score may alter priority while exhaustive search remains
complete.

This contract gives a theory template, not empirical headroom. R0 did not find
two high-order factor families where classical policies leave the required
residual, nor family-disjoint evidence that pre-solve features predict it.

## 8. SAT/CSP collision

XCSP3 provides native high-arity/global constraints, more than 23,000 public
instances and annual exact/certified competitions. Learned branching,
configuration, clause/cut guidance and solver portfolios are already mature
interfaces. A scope-aware branch policy remains generic CP/SAT solver learning
unless a hypergraph decomposition quantity provides independent execution gain.

The local candidate did not establish that necessity. Thus XCSP is a valid
benchmark source but not evidence of a distinct R0 learning problem.

## 9. DB/join collision

FAQ expresses semiring aggregation through variable elimination; fractional
edge covers and FAQ-width control multiway joins. Learned intermediate-factor
cost is cardinality estimation, and factor ordering is join ordering.

JoinInfer is both the strongest positive evidence and the closest collision. It
uses GHDs and worst-case optimal joins for exact PGM marginals, reports up to
630x speedup over other exact engines on some networks, and includes a
data-driven per-bag/engine hybrid. Some benchmark sparsity was induced. No later
artifact was found that establishes a new family-disjoint strategy learner
beyond this interface.

## 10. Tensor contraction collision

Dense sum-product VE is tensor contraction. Contraction order controls FLOPs
and peak tensor memory. cotengra already combines path heuristics,
hyperparameter search, slicing and simulated annealing; RL-TNCO directly learns
contraction order. A learned VE order evaluated only by peak entries/FLOPs is
therefore not distinctive.

Sparse factors, mixed semirings, evidence and deterministic constraints could
distinguish PGM/CSP execution, but no measured residual isolated those features.

## 11. Benchmark inventory

- **UAI 2014/2022:** public factor tables for PR/MAR/MPE/MMAP; 175 PR models
  locally audited across 21 filename families.
- **XCSP3:** high-order/global constraint models and annual exact-solver traces;
  source/model licenses vary.
- **HyperBench:** 3,648 CQ/CSP hypergraphs with decomposition experiments; the
  Zenodo artifact is CC BY 4.0.
- **JoinInfer testbed:** 52 UAI'06/PIC/BN Learns networks with exact marginal
  engine comparisons.
- **PACE/treewidth:** useful graph/decomposition controls, not primary
  high-order inference evidence.

No two sources provide the same factor-strategy learning problem with full
tables, certified decompositions, plan costs and a repeated workload.

## 12. Real high-order evidence

Of 175 UAI PR models, 85 have order-three-or-higher factors. High-order families
include CSP, Promedus, pedigree/linkage, circuits, BN and relational models. The
smallest high-order model has 67 variables; many have hundreds or thousands.

This passes the representation gate but not the necessity gate. `Promedus_24`
has 200 binary variables, half its factors are order at least three, yet all four
classical policies yield the same peak of 32 entries. High-order structure can
be present without creating a strategy-learning problem.

## 13. Factor representation audit

Across the 175 UAI models, median model-level median table size is four entries,
the largest single input table has 16,384 entries, and median model-level median
nonzero fraction is 0.879. Domain sizes, not arity alone, matter:
`ObjectDetection_74` has induced-width upper bound six but median domain 11 and
a 19,487,171-entry dense intermediate peak.

UAI stores explicit tables. XCSP may use extensional, intensional or specialized
global constraints. HyperBench has scopes only and cannot support a factor-cost
claim.

## 14. Strategy-variance measurements

Seven representative UAI models were evaluated with four classical policies
and eight deterministic random orders. Random orders could be 16,384x to more
than `10^18x` worse in peak entries. Strategy choice can therefore matter in
principle without affecting exactness.

Among classical policies, six of seven instances had identical peak cost; the
remaining ratio was 2x. Four bounded exact runs produced slowest/fastest
classical runtime ratios of 1.28x, 1.46x, 1.37x and 2.23x. No two families reach
the frozen 3x threshold and no timeout-rate gap occurs.

## 15. Classical heuristic performance

Min-fill or weighted min-fill attained the lowest total joined entries on
`2bitcomp_5`, `Grids_12` and `ObjectDetection_74`; all four tied on DBN,
Promedus and SAT-grid peak cost. The native factor-entry greedy policy never
improved peak cost over min-fill in the selected sample.

The empirical result is not “all orders are equal”. It is “competent classical
orders absorb most of the easily demonstrated opportunity”. This fails the
classical-residual gate for candidate A.

## 16. Width versus runtime

Equal induced width did not imply perfectly equal runtime, but the residual was
small. `Grids_12` has width upper bound 13 and peak 16,384 for all classical
orders while total entries vary 1.48x and runtime 1.46x. `CSP_12` similarly has
width upper bound 11, identical peak 524,288 and runtime ratio 1.28x.

Structural width is therefore incomplete, but no evidence shows that a learned
cost model adds enough beyond table/domain-aware analytic quantities.

## 17. Hypergraph versus primal-graph features

The factor-entry-aware native order tied or underperformed min-fill in peak
entries on all seven selected models. No local empirical advantage over primal
fill structure was observed.

JoinInfer shows that high factor arity and sparse listing representation can
favor GHD/WCOJ execution. However, that result depends on support/table
properties and partially induced sparsity; it does not establish a family-
disjoint learned strategy problem. HyperBench's structural separation lacks
downstream factors. G8 therefore fails.

## 18. Exactness/certificate architecture

- VE: any complete order; correctness by distributivity.
- GHD/FHD: verify coverage, connectedness, guards/covers and width before use.
- Portfolio: allow only exact engines compatible with the requested task.
- Branching: retain complete search.
- Pruning: require an independent admissible bound; learning may rank only.

Local tests confirm that different UAI orders return the same partition value.
G9 passes cleanly.

## 19. Oracle-label cost

Full labels require running many orders, decompositions or engines per instance.
The most informative high-order UAI models are also larger, so dense oracle
sweeps quickly become infeasible or censored by timeouts. HyperBench supplies
decomposition runtimes but not factor execution; solver traces supply one policy
trajectory rather than a plan oracle.

Pairwise preferences and bounded probes could reduce label cost, but their
learnability is not established. G12 fails on current artifacts.

## 20. Amortization analysis

Learning could amortize for repeated evidence/query updates on a stable factor
family, repeated industrial CSP models, or deployed inference services. UAI,
XCSP and HyperBench are heterogeneous research archives rather than documented
repeated workloads. A one-off exact solve cannot justify multiple expensive
oracle solves plus training.

No concrete current benchmark supplies the necessary repeated workload and
future-instance distribution.

## 21. Distribution-shift analysis

UAI's high-order property is strongly family-linked: all Promedus and linkage
models are high-order, while local DBN, grids and object-detection models are
pairwise. A random instance split would let a predictor recognize family and
memorize a strategy.

Any future evaluation must hold out whole model/generator families and report
size, arity, domain and evidence-density extrapolation. No published closest
method was found satisfying this full split contract.

## 22. Candidate problems

1. learned VE/factor order;
2. verified GHD/FHD separator/decomposition search;
3. local separator/bucket move ranking;
4. hypergraph-aware exact-engine portfolio;
5. plan execution-cost prediction;
6. safe learned proposal plus exact fallback.

Candidate D scores highest diagnostically because engine variance and exactness
are real. It nevertheless fails learnability, novelty/interface and amortization
gates; its remaining form is generic algorithm selection.

## 23. Semifinals

**None.** VE fails the frozen classical-residual threshold. GHD/FHD search lacks
a factor-bearing downstream benchmark. Local decisions, portfolios and cost
models fail the generic-solver/DB/tensor collision. The fallback architecture
has no independent problem residual.

## 24. Finalists

**None.** Accordingly no Rank-1 problem, paper claim or R1 bounded experiment is
authorized.

## 25. Candidate scores

| candidate | score /75 | fatal gates |
|---|---:|---|
| VE/factor ordering | 39 | G3/G6/G7/G8 |
| verified GHD/FHD search | 49 | G3/G4/G5/G7/G12 |
| local separator/bucket ranking | 41 | G6/G7/G8/G11 |
| exact-engine portfolio | 51 | G7/G10/G11/G12 |
| execution-cost model | 47 | G6/G7/G11/G12 |
| safe proposal + fallback | 41 | G3/G6/G7/G11 |

Hard gates override scores. Full fifteen-axis scoring is in
`docs/R0_CANDIDATE_MATRIX.md`.

## 26. Publication feasibility

A credible paper would need one of: a verified learned GHD search tied to
factor execution, a hypergraph-essential exact-engine selector, or a robust
prediction-assisted theorem with a concrete factor strategy. Current evidence
supports only an audit/negative result.

Adding a GNN/RL policy to min-fill, branching or join ordering is architecture-
only novelty and is not publication-feasible as a distinct high-order program.

## 27. Strongest evidence FOR

The task has a clean exactness contract; 85 official UAI models are genuinely
high-order; random orders and published cross-engine comparisons show enormous
cost variation; JoinInfer demonstrates that sparse high-arity factors can make
hypergraph-native multiway execution practically important; GHD/FHD theory is
active and supplies meaningful certificates.

## 28. Strongest evidence AGAINST

Competent VE heuristics stayed below the 3x residual threshold; the native
factor-entry heuristic did not beat primal min-fill; HyperBench lacks factors;
UAI lacks certified GHD/FHD plan traces and repeated workloads; oracle labels
are costly; and the remaining branch/plan/portfolio choices are already generic
CP/SAT, database or tensor-network learning problems.

## 29. Hard-gate table

| gate | status | evidence |
|---|---|---|
| G1 exact/certified | PASS | VE and selected engine semantics are exact |
| G2 genuinely high-order | PASS | 85/175 UAI PR models have max arity >=3 |
| G3 material strategy effect | PASS | random orders and JoinInfer engine comparisons show large effects; classical residual is addressed by G6 |
| G4 accepted public benchmark | PASS | UAI, XCSP and HyperBench are public accepted routes |
| G5 second family for same problem | FAIL | XCSP/HyperBench do not reproduce UAI factor-plan learning with the same task/artifacts |
| G6 classical residual | FAIL | four exact family ratios 1.28--2.23x; classical structural peak ratio <=2x |
| G7 learnably predictable | FAIL | no family-disjoint prediction evidence; no model trained |
| G8 hypergraph beyond primal | FAIL | native factor greedy did not beat min-fill; positive JoinInfer evidence is limited/sparsity-dependent |
| G9 correctness independent | PASS | order/proposal/portfolio can be verified or exact by construction |
| G10 recent prior art unsaturated | FAIL | surviving portfolio/branch/plan interfaces are occupied by JoinInfer and generic solver-learning literature |
| G11 DB/tensor/SAT novelty | FAIL | direct join, contraction and CP/SAT analogues exist |
| G12 label cost amortizes | FAIL | heterogeneous archives lack repeated workload; oracle sweeps are expensive |
| G13 ordinary compute | PASS | bounded structural/exact audit used CPU only |

No single candidate passes all relevant gates.

## 30. Final decision

**R0-E — NO-GO: GENERIC SOLVER-LEARNING SATURATION.**

R0-C is too broad because arbitrary orders and engine choices can have large
effects. R0-D is also incomplete because hypergraph-native sparse execution can
matter in JoinInfer-like regimes. R0-F is too strong because no recent paper
satisfies every desired learning/certificate/split condition. R0-G identifies a
secondary benchmark/amortization problem. The primary surviving proposal is
generic solver/plan/branch selection whose high-order framing is not
indispensable, so R0-E is the narrowest supported outcome.

## 31. Exact next action

Freeze R0. Do not create `docs/R1_SUBFIELD_PROPOSAL.md`, do not train a model and
do not expand into generic learning-augmented algorithms. Return to project
review. Reopen only if new external evidence provides:

1. two factor-bearing exact benchmark families with repeated workloads;
2. at least a 3x classical-oracle gap or 20-point timeout gap on both;
3. family-disjoint predictability from pre-solve features;
4. measurable improvement from native hypergraph features over primal and
   generic solver features;
5. affordable/censored-label-aware amortization and deterministic exactness.
