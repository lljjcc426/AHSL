# S0 theory-interface audit

## Rank 1: sparse combinatorial interaction structure

### Functional interfaces

1. **Möbius/ANOVA identification.** Fixing the response scale and null composition rule gives a unique contrast expansion when the required subsets are observed. With missing subsets, identifiability depends on the design matrix, not on neural expressivity.
2. **Sparse recovery.** Sample complexity can depend on the number `K` of nonzero supports, maximum order `d`, coherence/restricted-eigenvalue properties of the chosen intervention design, and noise—not on `2^p` alone.
3. **Heredity and simplicial structure.** Strong/weak heredity can reduce search but can delete pure high-order effects. The theory should compare downward-closed and non-hereditary support classes rather than assume one.
4. **Active experimental design.** Adaptive measurements can target support identification, top-combination discovery, or prediction. These goals require different acquisition functions and guarantees.
5. **Uncertainty and false discovery.** Selective inference, stability selection, conformal response intervals, and posterior inclusion probabilities can control different errors. Coverage of `y(A)` is not coverage of the support `H*`.
6. **Transfer and invariance.** Cross-condition or cross-organism structure may share supports while effects change. Partial pooling and invariant-support assumptions are falsifiable theory interfaces.

### Identifiability warning

Interactions are coordinate- and scale-dependent. For drugs, Bliss, Loewe, HSA, ZIP, emergent, and hidden-suppression definitions answer different questions. For fitness, multiplicative and additive scales differ. S1 must freeze the estimand before claiming recovery. This is the closest analogue of the CertPath representability failure.

### Hypergraph theory judgment

Hypergraph rank, sparsity, incidence structure, overlap, and order distribution are useful. GHW, FHW, submodular width, join trees, and acyclicity are **decorative at present**: no required downstream computation has been shown to depend on them. They must not be inserted merely to retain continuity with AHSL.

## Rank 2: open-world temporal set-event structure

Functional interfaces include marked/set-valued point processes, exchangeability and permutation invariance, projective consistency across changing node sets, calibrated set prediction, open-set retrieval, anti-monotone search bounds, and event-history generalization. Candidate-space tractability is real; hypertree-width theory is not.

The central theoretical/evaluation problem is that a model can classify easy random negatives while failing to retrieve the next group from the full combinatorial space. Proper set-event scores and search-aware calibration matter more than another message-passing theorem.

## Rejected interfaces

- Dynamics reconstruction has strong identifiability theory, but no trustworthy real structural labels.
- Causal hypergraph discovery has the highest formal ceiling, but observational equivalence and missing interventions currently push evidence back to simulations.
- Factor-scope learning has mature likelihood/complexity theory, but high-order necessity and benchmark relevance are not established.

## Required S1 theorem discipline

A credible first paper needs one bounded statement tied to the real task: identifiability under a declared incomplete factorial design, support-recovery/sample-complexity conditions, or a valid uncertainty/error-control result. A generic HGNN expressivity theorem would not address the scientific bottleneck.
