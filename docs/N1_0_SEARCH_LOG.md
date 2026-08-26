# N1.0 search log

Search date: 2026-08-26 (Asia/Shanghai). Searches covered publisher/proceedings pages, official project pages, primary papers, official Reactome documentation, and source repositories. Secondary indexes were used only to locate primary records.

## Query log

| Family | Representative literal queries | Decisive sources |
|---|---|---|
| directed hyperpaths | `shortest hyperpath reaction pathways`; `Mmunin Hhugin hyperpaths`; `cyclic directed hyperpath pathway inference`; `Reactome hyperpath pathway reconstruction` | Ritz et al.; Hhugin; Mmunin |
| learned costs | `learn reaction weights pathway inference`; `metabolic pathway cost learning`; `learning shortest path costs`; `inverse shortest path`; `inverse optimization shortest path` | Ahuja--Orlin; Burton--Toint; CHESHIRE; Multi-HGNN |
| decision-focused optimization | `predict then optimize shortest path`; `SPO+ shortest path`; `decision-focused learning combinatorial optimization` | Elmachtoub--Grigas; Wilder et al. |
| robust paths | `robust shortest path interval costs`; `interval shortest path optimality`; `inverse shortest path robustness`; `robust hyperpath` | Montemanni--Gambardella; Aissi et al.; Hassanpour--Aman |
| biological supervision | `Reactome pathway reconstruction benchmark`; `pathway completion Reactome`; `reaction pathway recovery curated pathways`; `pathway crosstalk Reactome` | Mmunin recovery section; CHESHIRE; Reactome documentation |
| temporal/generalization | `Reactome versions pathway changes`; `Reactome release history`; `Reactome stable identifiers`; `pathway split leakage reaction prediction` | official release/download/stable-ID pages; Reactome 2026 |
| direct collision | `learned reaction costs exact directed hyperpath Reactome`; `inverse optimization directed hyperpath pathway`; `decision-focused shortest hyperpath biological pathway`; `learned hyperedge cost exact hyperpath recovery` | no direct predecessor found; 2026 inverse-hyperpath paper was closest |

## Dataset and artifact pages

- Reactome downloads: `https://reactome.org/download-data`
- Reactome license: `https://reactome.org/license`
- Reactome release calendar: `https://reactome.org/about/release-calendar`
- versioned archive roots: `https://download.reactome.org/89/`, `https://download.reactome.org/97/`
- Mmunin: `https://mmunin.cs.arizona.edu/`
- Hhugin: `https://hhugin.cs.arizona.edu/`
- Mmunin source inspected at Git commit `3bb5f17` (ignored local clone)
- pathway-connectivity source inspected at Git commit `62de73b` (ignored local clone)

## Collision conclusion and limitation

The retained set contains 18 closely relevant primary works; ten received method/data-level deep inspection. No learned-cost + exact-directed-hyperpath + real pathway-supervised recovery collision was found. Search-engine absence is not a mathematical guarantee; this is the result of the logged falsification procedure as of the stated date.
