# N1.0 refreshed prior art

Search date: 2026-08-26. Scope: directed hyperpaths, biological pathway reconstruction, learned/inverse costs, predict-then-optimize, interval robustness, and versioned Reactome supervision. Eighteen closely relevant primary works were retained; ten were inspected in depth.

## Kill-gate result

**PASS: no fatal direct collision found.** The search did not find a method combining all three essential elements:

1. learned reaction or hyperedge costs from real pathway supervision;
2. exact general directed-hyperpath decoding; and
3. supervised recovery of real curated pathway reaction sets.

This is a bounded negative-search result, not proof of global nonexistence.

The closest new pressure is Hassanpour and Aman (2026): hyperpath deletion is used for (K)-shortest and inverse shortest-hyperpath applications. It is genuinely adjacent theory, but it does not learn costs from curated biological pathways or evaluate exact Reactome pathway recovery. It therefore does not trigger the collision gate.

## Closest works

| Work | Depth | Relevant contribution | Why it does not subsume CertPath |
|---|---|---|---|
| Gallo et al. (1993) | deep | foundational directed-hypergraph algorithms and hyperpath semantics | no learning or biological supervision |
| Ritz, Avent & Murali (2017) | deep | signaling hypergraphs; exact acyclic B-hyperpath MILP; graph comparison | acyclic restriction, unit/handcrafted costs, no cost learning |
| Krieger & Kececioglu (2021/2022), Hhugin | deep | efficient general hyperpath heuristic; cycles; Reactome/NCI-PID benchmark | heuristic, no learned costs, optimization targets mostly lack pathway-set gold |
| Krieger & Kececioglu (2023), Mmunin | deep | first practical exact general shortest-hyperpath cut-plane algorithm | exact decoder but no learned costs; only ten curated recovery case studies |
| Hassanpour & Aman (2026) | deep | hyperpath deletion; inverse shortest hyperpath under bottleneck Hamming distance | no biological data, learned predictor, or supervised recovery |
| Chen, Liao & Liu (2023), CHESHIRE | deep | hypergraph learning for missing metabolic reactions | link/gap prediction, not exact directed-hyperpath decoding |
| Huang et al. (2025), Multi-HGNN | inspected | multimodal high-order missing-reaction prediction | same mismatch: reaction prediction without exact path decision |
| Ma, Zhao & Yang (2024), DHGNN | inspected | directed-hypergraph representation learning/link prediction | generic link prediction, not pathway recovery or cost learning |
| Ahuja & Orlin (2001) | deep | general inverse optimization including inverse shortest path | ordinary networks/general inverse optimization, no directed-hyperpath biology |
| Burton & Toint (1992) | inspected | inverse shortest-path formulation | ordinary graph paths only |
| Elmachtoub & Grigas (2022), SPO+ | deep | decision-aware objective-coefficient learning; shortest-path experiments | general predict-then-optimize, no directed hyperpaths or Reactome labels |
| Wilder, Dilkina & Tambe (2019) | inspected | decision-focused combinatorial optimization | generic relaxation framework, not this decoder/task |
| Montemanni & Gambardella (2004) | deep | robust shortest path with interval data | ordinary graph; robust optimization rather than learned biological costs |
| Aissi, Bazgan & Vanderpooten (2009) | inspected | min-max/min-max-regret survey | generic robust combinatorial optimization |
| Franzese et al. (2019) | inspected | graded hypergraph connectivity on Reactome | connectivity analysis, not exact cost learning |
| Ragueneau et al. (2026) | inspected | current Reactome knowledgebase/version facts | data resource, not an inference method |
| Demir et al. (2013) | inspected | BioPAX/Paxtools pathway exchange and processing | data representation/tooling only |

## Falsification searches

Exact collision queries combined the phrases `learned reaction costs`, `inverse shortest hyperpath`, `exact directed hyperpath`, `Reactome pathway recovery`, `decision-focused hypergraph shortest path`, and `pathway-supervised hyperedge weights`. Citation chaining was run from Mmunin, Hhugin, signaling hypergraphs, CHESHIRE, Multi-HGNN, SPO+, inverse optimization, and the 2026 hyperpath-deletion paper.

No paper found through this procedure made the proposed combination redundant. Nevertheless, this novelty gate is not the reason CertPath stops: the empirical supervision/representability gate fails independently.
