# R0 Strategy-Variance Audit

## Protocol

The official UAI 2014 probability-of-evidence archive contains 175 models.
Every model was profiled for variables, factors, arity, domains, table entries,
nonzero fraction and primal edges. Seven representatives were selected before
execution to span high-order and pairwise controls:

`CSP_12`, `Promedus_24`, `sat-grid-pbl-0010`, `2bitcomp_5`, `Grids_12`,
`DBN_11`, and `ObjectDetection_74`.

Strategies were dynamic min-fill, weighted min-fill, min-degree,
minimum-next-factor-entries, and eight deterministic random orders. Structural
costs were peak joined entries and total joined entries. Dense exact execution
was limited to strategies whose symbolic peak was at most 1,048,576 and total
joined entries at most 50,000,000; three repetitions were used.

## Arbitrary-strategy variance

Random ordering was catastrophically worse on several instances:

| instance | best peak entries | worst sampled peak entries | ratio |
|---|---:|---:|---:|
| `CSP_12` | 524,288 | 34,359,738,368 | 65,536x |
| `Promedus_24` | 32 | 524,288 | 16,384x |
| `sat-grid-pbl-0010` | 4,096 | 274,877,906,944 | 67,108,864x |
| `Grids_12` | 16,384 | 1,099,511,627,776 | 67,108,864x |
| `2bitcomp_5` | 137,438,953,472 | 590,295,810,358,705,651,712 | 4,294,967,296x |

This establishes that strategy can affect cost while exactness remains fixed.
It does not establish a learnable residual over competent heuristics.

## Classical residual

For six of seven models all four classical strategies had identical peak cost.
The remaining `2bitcomp_5` ratio was 2x. Classical total-entry ratios were at
most 2.01x. Exact slowest/fastest runtime ratios were 1.28x, 1.37x, 2.23x and
1.46x on CSP, Promedus, SAT-grid and grid respectively.

The preregistered threshold requires at least 3x median feasible-strategy
runtime or a 20-point timeout gap on two families. No tested family reaches 3x;
no timeout gap occurs. G3/G6 fail for learned VE ordering.

## Limits

The runtime subset is intentionally small and dense. It does not prove that no
UAI model has a classical gap. Conversely, R0-A requires positive evidence on
two families; failure to find that evidence is a valid gate failure. The audit
does not use random order as the classical comparator and does not extrapolate
symbolic peak ratios into measured runtime claims.
