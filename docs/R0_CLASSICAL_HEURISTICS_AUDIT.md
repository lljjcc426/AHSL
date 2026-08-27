# R0 Classical Heuristics Audit

## Baselines

R0 implemented four deterministic dynamic baselines:

- min-fill;
- weighted min-fill using domain-size edge weights;
- min-degree;
- minimum next joined-factor entries from native scopes and domains.

Eight fixed random orders were included only to expose the full danger of poor
strategy choice. They are not a fair classical policy.

## Structural results

Seven UAI representatives cover pairwise grids/DBN/object detection and
higher-order CSP, Promedus, SAT-grid and bit-comparator families. Random orders
were between `1.6e4x` and roughly `5.6e18x` worse in peak entries on several
instances. Thus strategy is not irrelevant.

Among the four serious classical strategies, however:

- six of seven instances had identical peak-entry cost;
- `2bitcomp_5` had only a `2x` classical peak and total-entry ratio;
- total-entry ratios in the other six were between `1.00x` and `1.48x`.

The factor/domain-aware greedy rule did not improve peak cost over min-fill on
any selected instance. It tied or lost slightly in total joined entries.

## Exact execution

Four instances fit the frozen dense peak/total caps. Across three repetitions
per strategy, the slowest/fastest classical runtime ratios were:

| instance | high-order? | ratio |
|---|---:|---:|
| `CSP_12` | yes, max arity 3 | 1.28x |
| `Promedus_24` | yes, 50% factors order >=3 | 1.37x |
| `sat-grid-pbl-0010` | yes, max arity 4 | 2.23x |
| `Grids_12` | no, pairwise control | 1.46x |

No two families reach the preregistered `3x` threshold. The exact partition
value was invariant across all four strategies.

## Interpretation

The data establish a large gap between arbitrary and competent orders, not a
large gap between competent classical heuristics. A learner could easily look
successful against random ordering while adding little beyond min-fill. The
bounded sample is not a universal proof that no residual exists, but it is
sufficient to fail the positive R0 gate; the burden was to establish residual,
not assume it.
