# P0 failure taxonomy

## Classification rule

`F1` is reserved for a genuine engineering blocker that, once repaired, would
leave the scientific claim intact. No main project line stopped primarily for
F1. Missing Dango inputs and incomplete reproduction are real hygiene issues,
but S1.0 would still fail its cross-domain truth gate if they were repaired.

| Line or formulation | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9 | Controlling interpretation |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A0 learned categorical estimator |  |  |  | yes |  |  | yes |  | yes | exact projection/MAP dominated and the BCE/argmax decision was misaligned |
| A1 latent join-tree estimation |  | yes |  | yes |  |  |  |  | yes | synthetic identifiable model lacked real observable signal; likelihood gain did not transfer to downstream loss |
| A1.5 tree-identity learning |  | yes |  | yes |  |  | yes |  | yes | decision-aligned tree gain failed while classical posterior decoding retained value |
| B0 shared subtree prior |  | yes | yes |  |  | yes | yes |  | yes | no public task jointly matched output, tree, covariates and loss |
| N1.0 CertPath |  | yes | yes |  |  |  |  |  | yes | the positive-cost decoder could not represent a sufficiently large natural label universe |
| S1.0 interaction support |  | yes | yes |  | yes | yes |  |  | yes | one direct small panel was insufficient for a general recoverable support task |
| S2.0 temporal complete-set prediction |  |  |  |  | yes | yes |  |  |  | HyperSearch occupies the correct protocol; the remaining local failure is search rather than isolated structure learning |
| S3.0 partial-observation recovery |  | yes | yes | yes | yes | yes |  |  | yes | natural observation, independent gold, identifiability and residual never coincide |
| R0 learned exact-inference strategy |  | yes |  | yes | yes | yes | yes | yes |  | competent heuristics, generic adjacent fields and label economics eliminate the current learning case |

## What transfers

- **F2 transfers conditionally.** A missing benchmark in one domain does not
  prove another domain lacks data. Repetition across unrelated domains does,
  however, raise the required evidence standard.
- **F3 transfers strongly to latent targets.** A learned prior can select a
  solution but cannot make a non-injective observation operator identifiable.
- **F4 transfers strongly when the same exact/classical anchor applies.** It
  does not transfer to a genuinely different objective with measured headroom.
- **F5 transfers at the interface level.** An architecture change does not
  reopen a formulation already occupied at task/protocol level.
- **F6 transfers broadly.** If graph, matrix, tensor, set or generic-solver
  objects preserve the estimand, calling the result a hypergraph does not create
  strong coupling.
- **F7 transfers from AHSL and R0.** Mathematical structure can be essential to
  correctness while ML remains unnecessary.
- **F8 is specific to strategy learning.** It applies when oracle labels cost
  multiple expensive solves and no repeated workload amortizes them.
- **F9 transfers at the assumption level, not as a universal ban.** A new
  dataset or theorem can change it; a new model alone cannot.

## Level of negative evidence

| Evidence | Level 1 formulation | Level 2 interface | Level 3 parent program |
|---|---:|---:|---:|
| A0 estimator loss mismatch | strong | weak | weak |
| AHSL A1--B0 sequence | strong | strong for connected-subtree structure learning | moderate |
| CertPath attainability | strong | moderate for constrained decoding from curated pathway sets | weak-to-moderate |
| S1 direct-truth scarcity | strong | strong for cross-domain latent interaction support | moderate |
| S2 HyperSearch collision | strong | strong for open seen-node temporal set retrieval | moderate |
| S3 identifiability/reduction | strong | near-fatal for current latent-recovery interfaces | strong |
| R0 generic solver-learning result | strong | strong for learned known-structure exploitation | strong |

The combined Level-3 evidence is substantial because S1/S3 and R0 fail for
different reasons. It is still evidence about investment priority, not a proof
that no future hypergraph-theory/ML problem can exist.
