# N1.0 supervision definition

## Frozen task

For each human leaf pathway with at least one retained reaction, define a single whole-pathway reconstruction task ((H,S,U,P^*)):

- (H): the full release-specific directed reaction hypergraph;
- (P^*): the set of retained reactions directly annotated to that leaf pathway;
- (S=S_{global}\cup S_{boundary}), where (S_{global}) contains full-network vertices with empty backward star and (S_{boundary}) contains gold-pathway reactants/regulators not produced by another gold reaction;
- (U): all gold products not consumed by another gold reaction, required conjunctively through a synthetic sink.

One pathway yields at most one task. No multiple easy targets are mined from the same pathway. The rule was frozen before baseline evaluation and never altered after observing attainability.

## Scientific interpretation

The query is: “given a declared set of pathway inputs and terminal outputs, reconstruct the curated whole reaction process in the current reaction network.” At deployment, a domain analyst or assay specification must supply those declared boundary entities. The benchmark exposes (S) and (U) as query data; it does not ask the decoder to infer them.

This is deliberately favorable to pathway reconstruction, yet it remains coherent: boundary conditions are observable query variables. It is not a generic unknown-pathway discovery task. If a future application cannot supply boundary inputs and outputs independently of the hidden pathway, this supervision definition does not transfer.

## Source categories

| Category | Meaning | Primary use |
|---|---|---|
| `GLOBAL_NETWORK_SOURCE` | no incoming retained reaction in the release graph | yes |
| `QUERY_VISIBLE_PATHWAY_BOUNDARY` | declared pathway input not generated inside the gold set | yes, exposed in query |
| `GOLD_INTERNAL_REPAIR` | internal gold entity inserted only to break a cyclic dependency | prohibited |
| `OTHER` | any source not justified above | prohibited unless separately specified |

No primary task inserts internal repair vertices. Under the frozen rule, 456/1,620 candidates are gold-infeasible and would require internal repair or a changed task definition; they remain visible as failures and are not silently repaired.

## Prediction-time versus label-only information

Prediction-time information is (H,S,U), the release identifier, and any features derivable from the appropriate historical graph without pathway-membership annotations. Label-only information is (P^*), pathway name, membership, and hierarchy. Family labels may define group splits but may not be reaction-scoring features.

The boundary and terminal sets are derived deterministically from curated annotation when constructing the benchmark, then exposed as the query. This is acceptable only for the stated reconstruction task; it would be leakage if presented as de novo pathway discovery.

## Whole pathway versus query-conditioned subset

The gold is the complete retained reaction set of the leaf pathway. It is not shortened after solver inspection, stripped of redundant branches, or replaced by the decoder's minimum path. No alternative target definition was introduced to rescue the gate.
