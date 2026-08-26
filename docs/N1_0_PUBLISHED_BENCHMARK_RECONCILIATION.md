# N1.0 published benchmark reconciliation

## Three different counting units

The Mmunin paper's 5,066 Reactome instances are optimization queries: a global source construction paired with individual candidate targets. Of these, 2,432 were reachable. They are not 5,066 curated pathway-reaction labels.

The paper's known-pathway recovery experiment instead selected ten pathways from 22 cyclic targets that mapped uniquely to one Reactome pathway. Only those ten experiments had a curated pathway edge set used for precision/recall. The reconstruction source set combined pathway-boundary sources with a supplementary source list; five of the ten cases required manually supplied internal sources to make the cyclic gold process recoverable. Thus the historical supervised recovery evidence is ten case studies, five with source repair—not thousands of independent labeled examples.

N1.0 constructs a new benchmark extension: one whole-reaction-set task for each V97 leaf pathway satisfying deterministic query-construction rules. It yields 1,620 candidate gold-labeled tasks, of which 712 pass feasibility, attainability, and size filters. This extension is legitimate as a benchmark construction because it keeps one task per curated pathway and freezes endpoint rules before decoding. It does not inherit validation from the 5,066-target benchmark.

## Published graph counts

| Statistic | Published Reactome/PC12 | Checked Mmunin artifact | N1.0 official V97 BioPAX |
|---|---:|---:|---:|
| vertices | 20,458 | 20,477 under independent incidence deduplication | 26,345 |
| hyperedges | 11,802 | 53,581 context rows; 11,834 unique reaction IDs; 11,816 unique tail/head incidences | 15,613 |
| self-loops | 433 | 433 context rows; 93 unique incidences | 99 |
| mean / max tail | 2.4 / 26 | 2.381 / 26 | 2.384 / 31 |
| mean / max head | 1.6 / 28 | 1.603 / 28 | 1.590 / 61 |

The row-level 433 self-loops and repeated pathway contexts explain why naive row counts cannot be treated as unique reactions. Remaining count differences follow from the historical Pathway Commons PC12 conversion and its filtering versus current direct official Reactome BioPAX and the documented N1.0 exclusions. Preprocessing was not tuned to make counts match.

## Source and target differences

The 5,066 benchmark uses a global supersource and one target at a time. The ten recovery cases use pathway-specific sources/targets and supplementary sources. N1.0 uses global network sources plus query-visible pathway boundary inputs and requires all terminal pathway outputs conjunctively. Therefore published runtime/accuracy figures are contextual baselines, not directly transferable N1.0 results.
