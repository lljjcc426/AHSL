# S3.0 Identifiability Audit

## Pairwise projection

For an undirected hypergraph `H`, let `P(H)` contain pair `{u,v}` iff some
hyperedge contains both nodes. This map is non-injective. Exhaustive enumeration
gives:

| nodes | allowed orders | hypergraphs | graph projections | uniquely represented projection classes | ambiguous classes | maximum preimages |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 2–3 | 16 | 8 | 7 | 1 | 9 |
| 4 | 2–4 | 2,048 | 64 | 41 | 23 | 1,569 |
| 5 | 2–3 | 1,048,576 | 1,024 | 388 | 636 | 608,273 |

The maximum occurs for the complete projected graph. Thus a single size-3/4/5
hyperedge, its constituent pair edges, and many mixtures are observationally
equivalent. Exact recovery is class D without assumptions. Recent random-uniform
theory obtains class B only below density thresholds; learned methods use
labeled hyperedges, multiplicities, or application priors.

## Dynamics

For `dx_i/dt = F_i(x)`, a triadic term is distinguishable through nonzero mixed
derivatives only if its coupling function is not decomposable into pairwise
terms and data explore a nonlinear region. Pairwise and higher-order structures
are equivalent for decomposable coupling and under local linearization. Exact
support recovery additionally requires measured state sufficiency, persistent
excitation, a suitable feature library, sparsity, derivative quality, and no
latent confounding. These conditions are class B in controlled systems and D/E
for current EEG/ecological data.

Bayes-THIS adds posterior uncertainty but reports a Taylor-structure failure in
which isolated higher-order interactions induce spurious lower-order terms that
cannot be distinguished statistically. A Bayesian prior does not repair the
observation map.

## Protein complexes

Co-elution satisfies neither exclusivity nor injectivity. Two complexes may
co-elute; one protein may moonlight in several complexes; subcomplexes and
assembly states overlap; extraction can dissociate weak complexes; unrelated
proteins may share an elution profile. Complex identity is class C/D unless
multiple orthogonal assays and anchor/separability assumptions are available.
CORUM positives constrain possibilities but do not define all negatives.

## Pooled designs and marginals

Known linear pools identify a sparse coefficient vector only under disjunctness,
restricted-eigenvalue/incoherence and a correct additive/noise model. Higher-
order interaction terms require a much larger design and remain aliased when
the design columns coincide. This is classical class B, not a new hypergraph
identifiability result.

Low-order marginals leave the kernel of the marginalization operator
unobserved. Higher-order log-linear terms vary along that kernel. Maximum
entropy selects one representative but does not identify the generating table;
the class is D unless higher-order terms are assumed zero or a parametric model
is externally justified.

## Censoring

Unknown MNAR membership censoring permits many combinations of event frequency,
group composition, and detection propensity to generate the same observations.
With calibrated individual/group detection and repeated independent sightings,
partial identification may be possible. No qualifying public paired benchmark
was found to test those assumptions.
