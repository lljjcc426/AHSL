# S3.0 Scope and Definition

## Estimand

S3.0 studies an observation model

\[
H^* \longrightarrow O \longrightarrow Y,
\]

where `H*` contains relations of order at least three and the real measurement
process `O` does not directly reveal all hyperedge identities. The task is
structural inference `Y -> H*`, not response prediction alone. Exact recovery is
claimed only when the observation map is injective on a declared model class;
otherwise the target must be a posterior or a scientifically meaningful
equivalence class.

## Inclusion and exclusion

Primary evidence requires natural sensing, aggregation, censoring, projection,
or dynamical response. Projecting or masking a fully observed hypergraph is a
diagnostic only. Temporal next-event forecasting, noisy incidence/join-tree
recovery, static artificial-negative completion, node classification, generic
matrix completion, and new HGNN encoders remain out of scope.

The structural gold must be independent of the input modality. “Known positives
and unknown remainder” is not a complete binary gold set. A method that predicts
`Y` well but returns the wrong `H` does not pass.

## Families screened

1. pairwise/network projection to latent hyperedges;
2. trajectories to higher-order coupling scopes;
3. pooled assays to sparse interaction supports;
4. naturally censored group events to full participant sets;
5. CF-MS/AP-MS/PPI evidence to protein-complex membership sets;
6. released low-order marginals to higher-order dependencies.

No family is carried forward merely because a hypergraph representation is
possible. The final gate asks whether the representation adds an identifiable,
validated residual beyond clique cover, community detection, sparse regression,
system identification, graph clustering, matrix/tensor factorization, and
log-linear inference.
