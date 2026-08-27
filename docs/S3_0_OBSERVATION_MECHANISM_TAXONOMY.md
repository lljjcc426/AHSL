# S3.0 Observation-Mechanism Taxonomy

| family | actual observation `Y` | mechanism | naturality | information naturally missing | latent type |
|---|---|---|---|---|---|
| projected networks | reliable dyadic adjacency or multiplicity | D: natural low-order projection in some domains | plausible in social/PPI data; published recovery benchmarks usually project known hypergraphs artificially | which clique edges originated in one joint event | A/B hyperedge identities/weights |
| dynamics | multivariate trajectories or snapshots | E: natural dynamical response | strong | coupling scopes, directions and functions | B/C/E weighted, signed or directed interactions |
| pooled screens | aggregate abundance/read-count response for a known pool/design | B: natural aggregation | strong as an experimental economy | sparse response coefficients; usually not latent group membership | C interaction support, not necessarily hyperedges |
| censored group events | partial detections of group membership | A/C: sensor limitation or censoring | strong in wildlife/privacy settings | undetected individuals and entire unobserved groups | A/D event sets or latent groups |
| protein complexes | co-elution profiles, bait-prey evidence, pairwise associations | A/B/D: assay limitation and aggregation | strong | which pairwise signals cohere into the same physical assembly | D latent complexes |
| privacy marginals | released low-order contingency marginals | B/D: aggregation and privacy projection | strong | higher-order cells and interaction parameters | C/F dependency supports or factor scopes |

Artificial type F occurs in the dominant supervised projection benchmark:
authors start with known hyperedges, compute the clique projection, and use the
original sets as labels. That is useful for method comparison but does not
establish that a real instrument supplied only the projection.

For natural censoring, missingness is generally detection-dependent or MNAR:
large, visible, collared, abundant, or bait-compatible entities are more likely
to be observed. Treating an unrecorded membership as a negative is invalid
without calibrated detection probabilities.
