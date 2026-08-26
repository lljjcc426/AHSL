# S0 scope and definition

Search date: **2026-08-27**. Frozen parent: `4f45a6bbf6c594b217f18b87ea7ede0900d24ebb`.

## Objective

S0 selects one durable subfield inside machine learning → structure learning → high-order/hypergraph structure learning. It does not select a model, dataset, or final paper.

Structure learning requires that the learned target contain a relation of arity at least three, a set-valued relation, a factor scope, a latent group, or a time-varying collection of such objects. Merely running a hypergraph neural network on fixed hyperedges does not qualify.

## Frozen exclusions

- alpha-acyclic incidence denoising, join-tree identity learning, and neural join-tree learning;
- learned positive reaction costs plus exact shortest directed-hyperpath pathway reconstruction;
- fixed-hypergraph node/graph classification, generic representation learning, ordinary graph link prediction;
- decomposition-only learning, query optimization, tensor contraction, solver heuristics, partitioning, and generic HGNN design.

No S0 model was trained. The work is a literature, benchmark, and theory-interface audit.

## Structural objects used in the audit

| Code | Unknown object |
|---|---|
| U1 | factor scopes `E` in a product distribution |
| U2 | tractability-constrained graphical/factor structure |
| U3 | missing or future hyperedge sets |
| U4 | time, membership, cardinality, direction, and roles of group events |
| U5 | latent hyperedges behind pairwise projections |
| U6 | supports and weights of nonpairwise dynamical couplings |
| U7 | latent groups/blocks and group-to-group interaction tensors |
| U8 | overlapping protein-complex membership sets |
| U9 | supports, signs, and strengths of non-additive combinatorial effects |
| U10 | directed causal mechanism scopes |
| U11 | n-ary facts/events and their argument roles |

## Selected subfield

**Sparse high-order combinatorial interaction structure learning from intervention–response data.**

Let `N={1,...,p}` be possible perturbations and let `y(A)` be a measured response for a jointly applied subset `A⊆N`. Under an explicitly declared effect scale and null composition rule, write a set-function expansion

`y(A) = sum_{S⊆A} beta_S + epsilon_A`.

The structural target is

`H* = {S⊆N : |S|≥3 and beta_S≠0}`,

together with signed/quantitative effects and uncertainty where estimable. `H*` is a hypergraph of irreducible intervention sets. The definition does not assume downward closure: a three-way effect need not imply a pairwise effect.

This object is distinct from a black-box response predictor. A valid evaluation must assess the recovered supports/effects or their value for prospectively selecting unseen combinations, not only random-split response error.

## Boundary conditions

- Real, public, experimentally measured combination responses are the main evidence.
- Order at least three is mandatory in the primary evaluation.
- A study must state the response scale, null composition model, and interaction contrast. “Synergy” is not scale invariant.
- Random tuple splits alone are inadequate because shared genes/drugs/species can make interpolation look like structure recovery.
- GHW/FHW/acyclicity are not presumed relevant. Sparsity, interaction order, heredity, set-function transforms, and experimental design are the operative structural controls.

## Decision

The gate decision is **S0-A (GO)** for the selected subfield, subject to a first S1 gate on target identifiability and benchmark split validity.
