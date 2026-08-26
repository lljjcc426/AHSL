# N1.0 baseline and headroom audit

## Early-stop status

The representability hard gate failed before baseline evaluation: 961/1,620 natural tasks (59.32%) are positive-cost attainable, below the frozen 70% threshold. The protocol requires CertPath to stop at this point. Consequently, the following were deliberately **not evaluated**:

- exact unit-cost pathway-recovery F1;
- supported handcrafted cost variants;
- Hhugin biological F1 and exact-objective agreement;
- ordinary pairwise projection outputs;
- exact-set recovery distribution;
- solver runtime distribution;
- average F1 headroom and the fraction with F1 at most 0.95.

No zeros, placeholders, or published numbers are substituted for unrun N1.0 experiments. Mmunin's published source-target runtimes and ten recovery case studies concern different query/source constructions and cannot serve as this benchmark's baseline.

## Failure categories established upstream

| Category | Count | Meaning |
|---|---:|---|
| `GOLD_NOT_FEASIBLE` | 456 | terminal targets cannot be generated from permitted sources using the complete gold set |
| `POSITIVE_COST_UNATTAINABLE` | 203 | gold is feasible but contains a feasible proper subset |
| attainable but smaller than 3 reactions | 249 | structurally representable but too small for the nontrivial benchmark |

These categories already justify N1.0-C. Baseline-specific categories such as crosstalk, alternative branch, tie, and solver timeout were not measured systematically.

## Headroom and high-order gates

Headroom gate: **NOT EVALUATED—upstream hard stop**. Hypergraph-necessity gate: **NOT EVALUATED—upstream hard stop**. Although 98.52% of gold sets contain a multi-tail reaction, this does not establish pairwise-decoder disagreement and is not mislabeled as a PASS.
