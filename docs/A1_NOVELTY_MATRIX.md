# A1 Novelty Matrix

`Yes` records substantive coverage, not a keyword match. `Partial` means an
analogue exists but the learned object or data model differs.

| Work | Year | Observed data | Learned object | Hypergraph-native? | Alpha-acyclic? | Latent clean incidence? | Noisy incidence? | Join-tree constraint? | Marginalizes latent structure? | Exact DP? | Outputs certificate? | GHW-related? | Downstream tractability objective? | Main difference from AHSL |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Beeri et al. | 1983 | database schema | characterization | Yes | Yes | No | No | Yes | No | No | Yes | No | Yes | Theory, not statistical learning |
| Berry & Simonet | 2021 | fixed hypergraph | union join graph | Yes | Yes | No | No | Yes | No | No | Yes | No | Partial | Enumerates possible join-tree edges |
| Borgelt & Kruse | 2001 | attribute samples | decomposable graphical model | Partial | Partial | No | Partial | Clique join tree | Partial | Join-tree inference | Yes | No | Yes | Learns cliques/variable graph, not incidence-column tree |
| Karger & Srebro | 2001 | complete samples | bounded-treewidth Markov graph | No | No | No | No | Partial | No | No | Yes | Treewidth | Yes | Pairwise graphical-model likelihood |
| Kumar & Bach | 2013 | complete samples | bounded-treewidth decomposable graph | No | No | No | No | Partial | No | No | Yes | Treewidth | Yes | Convex relaxation over graphical models |
| Chow & Liu | 1968 | complete variable samples | dependence tree | No | No | No | No | No | No | No | Yes | No | Partial | Variables are tree nodes; pairwise decomposable score |
| Choi et al. | 2011 | observed-node samples | latent graphical tree | No | No | No | Partial | No | Partial | No | Yes | No | Yes | Hidden nodes plus information distances |
| Nikolakakis et al. | 2019 | noisy variable samples | Ising/Gaussian tree | No | No | Partial | Yes | No | Noise integrated statistically | No | Yes | No | Partial | Pairwise Markov model, not connected supports |
| Felsenstein | 1981 | aligned character data | phylogenetic tree | No | No | Yes | Partial | No | Yes | Yes | Yes | No | Partial | Evolutionary transition model |
| Kschischang et al. | 2001 | arbitrary factorized evidence | marginals | No | No | Yes | Yes | No | Yes | Yes | No | No | Yes | General algorithm containing the A1 recurrence |
| Chen & Yuille | 2015 | image evidence | connected visible composition | No | No | Partial | Partial | Fixed tree | Max, not sum | Yes | No | No | Yes | Fixed body tree and vision score |
| Friedman | 1998 | incomplete records | Bayesian-network structure | No | No | Yes | Partial | No | Yes | Model-dependent | Yes | No | Yes | General Structural EM framework |
| Koo et al. | 2007 | labeled dependency data | directed spanning-tree distribution | No | No | No | No | No | Yes | Matrix-tree | Yes | No | Partial | Sums over tree outputs, not connected supports on a tree |
| Paulus et al. | 2020 | task data | relaxed combinatorial latent structure | No | No | No | No | No | Approximate | Differentiable relaxation | Yes | No | Partial | Neural/relaxed spanning-tree distributions |
| Cai et al. | 2022 | features, labels, initial hypergraph | soft/pruned incidence | Yes | No | Partial | Yes | No | Approximate | No | No | No | No | Downstream task objective without acyclicity certificate |
| Badalyan et al. | 2024 | hyperedges and node attributes | communities/model parameters | Yes | No | Partial | Partial | No | Yes | No | No | No | No | Community and missing-hyperedge inference |
| Li et al. | 2025 | features and optional hypergraph | soft incidence | Yes | No | Partial | Yes | No | No | No | No | No | No | Self-supervised contrastive objective |
| Wen & Yu | 2025 | observed hypergraph | hypergraph generator | Yes | No | Partial | No | No | Partial | No | No | No | No | Projection and clique-cover reconstruction |
| Gottlob et al. | 2002 | conjunctive-query hypergraph | hypertree decomposition | Yes | Generalizes | No | No | Decomposition tree | No | Yes | Yes | Yes | Yes | Query decomposition, not statistical denoising |
| Grohe & Marx | 2006 | CSP hypergraph | fractional decomposition | Yes | Generalizes | No | No | Decomposition tree | No | No | Yes | Yes | Yes | Width-based tractability theory |
| **AHSL A1 candidate** | 2026 | noisy binary incidence rows | labeled tree prior and clean supports | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | k=1 | Yes | Combination under test; algorithmic ingredients are classical |

## Flagged overlap

No row matches all AHSL columns. However, the apparent uniqueness is composite:
Kschischang et al. cover exact marginalization, Friedman covers latent structure
learning, Nikolakakis et al. cover noisy tree recovery, and Chen and Yuille cover
connected-subtree latent states. The matrix must not be used to claim that each
ingredient is new.

