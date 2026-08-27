# P0 transferability matrix

Scale: `N` none, `W` weak, `M` moderate, `S` strong, `NF` near-fatal. A rating
means the old result raises the burden of proof for the future interface; it is
not a theorem of impossibility.

| Prior failure | I1 structure | I2 interactions | I3 future events | I4 partial recovery | I5 solver/decomp | I6 cost surrogate | I7 certified LA | I8 regularization | I9 generalization | I10 fixed HGNN | I11 adaptive/query | I12 causal | I13 dynamic/canonical decomposition |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AHSL: exact projection beats learning | NF | M | W | S | M | W | M | S | W | W | M | M | M |
| AHSL/B0: no matching real task | NF | M | W | S | W | W | W | M | W | W | M | M | N |
| N1.0: decoder excludes natural labels | M | M | M | S | W | W | M | M | W | W | M | S | N |
| S1.0: direct interaction truth absent across domains | M | NF | W | S | N | W | W | M | M | W | S | S | N |
| S2.0: artificial negatives and same-protocol collision | W | W | NF | M | W | M | M | W | W | M | M | W | N |
| S3.0: non-identifiability and graph/matrix/tensor reduction | S | NF | M | NF | W | M | M | S | S | S | S | NF | W |
| R0: competent classical policies and generic solver collision | M | W | M | M | NF | NF | NF | M | M | M | M | W | M |

## Reading the strongest transfers

- **I1/I4:** AHSL and S3 jointly make another passive latent-structure task
  nearly indefensible without a new observation theorem and real gold.
- **I2/I12:** S1 and S3 show that coefficient support, causal mechanism and
  biological truth cannot be interchanged. The remaining learning problems are
  usually sparse regression/system identification rather than native
  hypergraph theory.
- **I3:** S2 transfers almost exactly because it tested the correct open-world
  complete-set protocol and found a direct prior-art collision.
- **I5--I7:** R0 transfers almost exactly. A future proposal must exhibit a
  hypergraph-specific residual, not merely add guarantees to generic algorithm
  selection.
- **I8--I10:** fixed-hypergraph prediction remains a valid ML area, but previous
  evidence strongly threatens the claim that alpha-acyclicity, GHW/FHW or
  related native theory is materially necessary.
- **I11/I13:** negative transfer is weaker for pure query/decomposition theory.
  These interfaces change the scientific objective and do not need ML, which is
  why they support a P0-B pivot rather than P0-A.

## Correlation audit

AHSL/B0 and parts of S1/S3 share benchmark scarcity and are **partially
correlated**. S1 and S3 share identifiability concerns but use different
observation mechanisms, so they are **partially correlated** rather than
duplicates. S2's protocol/prior-art failure and R0's classical/generic-solver
failure are **largely independent** of the biology and latent-gold problems.
Taken together, the parent-program update is therefore stronger than a count of
many biology failures but weaker than a formal impossibility result.
