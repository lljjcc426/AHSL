# N1.0 directed-hypergraph construction

## Object mapping

The parser streams the official human BioPAX Level 3 OWL. Each state- and compartment-specific `PhysicalEntity` URI is a vertex. Each retained reaction-like event is one directed hyperedge:

\[
T(e)=\text{reactants}(e)\cup\text{direct positive regulators}(e),
\qquad H(e)=\text{products}(e).
\]

Retained event classes are `BiochemicalReaction`, `Degradation`, and `TemplateReaction`. Direct `Catalysis`, `Control`, and `TemplateReactionRegulation` records with positive control type add their controller to the controlled reaction's tail. Multiple tail members remain conjunctive. Complexes are preserved as BioPAX physical entities rather than expanded into pairwise components. Cycles and self-loops are retained.

## Deliberate exclusions and deviations

- Empty-head and empty-effective-tail events are excluded because the solver semantics require nonempty tail/head hyperedges.
- Negative regulators are not treated as positive prerequisites.
- A direct control with absent `controlType` is retained as activation-compatible; explicitly inhibitory controls are excluded.
- Higher-order controls of controls and pathway pseudoedges are not synthesized.
- Complexes are not recursively flattened; their distinct state/compartment URIs remain vertices.
- A vertex whose only incoming reactions are self-loops is treated as a global source, because a self-loop cannot seed forward closure. This is more feasibility-favorable than the literal empty-backward-star construction used in the historical artifact.
- The source is official Reactome BioPAX, not Pathway Commons PC12. Consequently URI identity, control materialization, duplicate pathway contexts, and counts differ from the published artifact.
- No preprocessing parameter was tuned to force agreement with published counts.

## Release counts

| Statistic | V89 | V97 |
|---|---:|---:|
| vertices | 24,610 | 26,345 |
| hyperedges | 14,538 | 15,613 |
| global sources | 9,666 | 10,358 |
| self-loop hyperedges | 95 | 99 |
| multi-tail hyperedges | 12,709 | 13,683 |
| mean / max tail size | 2.371 / 31 | 2.384 / 31 |
| mean / max head size | 1.583 / 61 | 1.591 / 61 |

These figures establish that the native object is high-order; they do not by themselves prove that high-order semantics alter the selected solutions. That empirical comparison was not reached after the upstream representability hard stop.

Implementation: `src/certpath/reactome_adapter.py`, `src/certpath/hypergraph_builder.py`.
