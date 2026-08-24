# A1 Structured Literature Search Log

## Search record

- **Date:** 2026-08-25
- **Cutoff:** current search date
- **Search method:** general web search routed to primary sources and verified
  against publisher/proceedings pages, DOI records, DBLP, arXiv, PMLR, JMLR,
  CVF Open Access, and author manuscripts.
- **Research skills:** not used, per project instruction.
- **Screened primary works:** 38
- **Read in substantive detail:** 14
- **Closest works analyzed field-by-field:** 5

"Detailed" means that the problem formulation, model/structure class,
algorithm, guarantees or complexity, and experiments were inspected rather than
only the title/abstract.

## Major query families

```text
alpha-acyclic hypergraphs join trees running intersection
union join graph maximum spanning tree weighted line graph
learning graphical models hypertree structure Borgelt Kruse
bounded treewidth decomposable graph structure learning likelihood
latent tree graphical model structure recovery noisy samples
Chow-Liu with noise hidden tree maximum likelihood
random connected subtree fixed tree probability distribution
bond percolation cluster uniformly chosen vertex finite tree
connected subtree partition function tree dynamic programming
sum-product connected subtree factor graph
structural EM hidden variables structure learning
structured prediction spanning tree matrix-tree differentiable MST
hypergraph structure learning 2024 2025 2026
generalized hypertree width fractional hypertree width computation
```

## Screened works

| # | Cluster | Work | Depth | Decision and relevance |
| ---: | --- | --- | --- | --- |
| 1 | A | Yannakakis, *Algorithms for Acyclic Database Schemes* (1981) | Screened | Foundational acyclic-scheme algorithms; retained |
| 2 | A | Beeri et al., *On the Desirability of Acyclic Database Schemes* (1983) | Detailed | Core alpha-acyclic equivalences; retained |
| 3 | A | Fagin, *Degrees of Acyclicity...* (1983) | Screened | Distinguishes alpha/beta/gamma acyclicity; retained |
| 4 | A | Tarjan & Yannakakis, *Simple Linear-Time Algorithms...* (1984) | Screened | Recognition/reduction foundation; retained |
| 5 | A | Berry & Simonet, *Computing the Atom Graph...* (2021 journal version) | Detailed | Union join graph and nonuniqueness; retained |
| 6 | A | Leitert, *Computing the Union Join and Subset Graph...* (2021) | Screened | Modern complexity/algorithms; retained |
| 7 | B | Karger & Srebro, *Learning Markov Networks: Maximum Bounded Tree-Width Graphs* (2001) | Screened | Likelihood under tractability constraints; retained |
| 8 | B | Borgelt & Kruse, *Learning Graphical Models With Hypertree Structure...* (2001) | Detailed | Mandatory closest prior; retained |
| 9 | B | Thomas & Green, *Enumerating the Junction Trees of a Decomposable Graph* (2009) | Screened | Junction-tree nonuniqueness; retained |
| 10 | B | Kumar & Bach, *Convex Relaxations for Learning Bounded-Treewidth Decomposable Graphs* (2013) | Detailed | Modern bounded-width ML; retained |
| 11 | B | Nie et al., *Learning Bayesian Networks with Bounded Tree-width via Guided Search* (2016) | Screened | Score-based guided structure search; retained |
| 12 | C | Chow & Liu, *Approximating Discrete Probability Distributions with Dependence Trees* (1968) | Detailed | Classical ML tree/MWST; retained |
| 13 | C | Felsenstein, *Evolutionary Trees from DNA Sequences* (1981) | Detailed | Exact likelihood and topology search; retained |
| 14 | C | Choi et al., *Learning Latent Tree Graphical Models* (2011) | Detailed | Closest latent-tree recovery line; retained |
| 15 | C | Zwiernik, *An Asymptotic Behaviour of the Marginal Likelihood for General Markov Models* (2011) | Screened | Hidden-tree marginal-likelihood singularity; retained |
| 16 | C | Nikolakakis et al., *Learning Tree Structures from Noisy Data* (2019) | Detailed | Closest noisy-tree recovery line; retained |
| 17 | C | Huang et al., *Guaranteed Scalable Learning of Latent Tree Models* (2020) | Screened | Modern guarantees and scale; retained |
| 18 | D | Moon, *On the Number of Induced Subgraphs of Trees* (1997) | Screened | Connected induced-subtree enumeration; retained |
| 19 | D | Fredes & Marckert, *Models of Random Subtrees of a Graph* (2021) | Detailed | Random-subtree model survey; retained |
| 20 | E | Kschischang et al., *Factor Graphs and the Sum-Product Algorithm* (2001) | Detailed | Subsumes message-passing mechanism; retained |
| 21 | E | Tittmann et al., *The Enumeration of Vertex Induced Subgraphs...* (2011) | Screened | Connected-component partition functions; retained |
| 22 | E | Chen & Yuille, *Parsing Occluded People by Flexible Compositions* (2015) | Detailed | Explicit connected-subtree latent state and exact DP; retained |
| 23 | F | Friedman, *Learning Belief Networks in the Presence of Missing Values and Hidden Variables* (1997) | Detailed | Original Structural EM line; retained |
| 24 | F | Friedman, *The Bayesian Structural EM Algorithm* (1998) | Detailed | Bayesian model-selection extension; retained |
| 25 | F/G | Meila & Jaakkola, *Tractable Bayesian Learning of Tree Belief Networks* (2000) | Screened | Priors/integration over tree structures; retained |
| 26 | G | Koo et al., *Structured Prediction Models via the Matrix-Tree Theorem* (2007) | Detailed | Exact tree partition functions; retained |
| 27 | G | Kim et al., *Structured Attention Networks* (2017) | Screened | Differentiable structured marginals; retained as future context |
| 28 | G | Corro & Titov, *Learning Latent Trees with Stochastic Perturbations...* (2019) | Screened | Differentiable latent tree learning; retained as future context |
| 29 | G | Paulus et al., *Gradient Estimation with Stochastic Softmax Tricks* (2020) | Screened | Spanning-tree relaxation; retained as future context |
| 30 | H | Cai et al., *Hypergraph Structure Learning for Hypergraph Neural Networks* (2022) | Detailed | Task-driven noisy-incidence refinement; retained |
| 31 | H | Badalyan et al., *Structure and Inference in Hypergraphs with Node Attributes* (2024) | Detailed | Probabilistic modern hypergraph inference; retained |
| 32 | H | Fallat et al., *Learning Hypertrees From Shortest Path Queries* (2024) | Screened | Genuine hypertree learning but query model differs; retained for terminology |
| 33 | H | Li et al., *Self-supervised Hypergraph Structure Learning* (2025) | Detailed | Current soft structure learning; retained |
| 34 | H | Wen & Yu, *HyperPLR* (2025) | Screened | Current hypergraph generation; retained |
| 35 | I | Gottlob et al., *Hypertree Decompositions and Tractable Queries* (2002) | Detailed | GHW foundation; retained |
| 36 | I | Grohe & Marx, *Constraint Solving via Fractional Edge Covers* (2006) | Screened | FHW foundation; retained |
| 37 | I | Marx, *Tractable Hypergraph Properties...* (2013) | Screened | Submodular-width boundary; retained |
| 38 | I | Gottlob et al., *Fast Parallel Hypertree Decompositions...* (2024) | Detailed | Current GHW computation; retained |

## Rejected or background-only search hits

| Work/search hit | Reason for rejection from the core comparison |
| --- | --- |
| *Hypergraph Augmentation via Latent Hyperedge Induction* (online 2026; issue dated 2027) | Soft task-driven augmentation; publication timing and object differ; background only |
| *Self-Supervised Hypergraph Learning with Substructure Awareness for Hyperedge Prediction* (2026) | Predicts missing hyperedges; no acyclicity or tree prior |
| *Hypergraph-Enhanced Contrastive Learning* (2025) | Representation-learning application, not structure identification |
| *Learning Hyperspectral Noisy Label with Hypergraph Laplacian Energy* (2025) | Noisy labels, not noisy incidence or latent tree |
| *Beyond Convolution: Hypergraph U-Nets* (2026) | Pooling/reconstruction architecture, not statistical tree selection |
| *Finding Induced Trees* (2009) | Combinatorial feasibility problem, not a probability model |
| *On the Probability that a Random Subtree is Spanning* (2021) | Uniform graph-subtree statistic; not the anchor-growth law |
| *Root and Community Inference on the Latent Growth Process of a Network* (2024) | Network arrival histories and spanning subtrees; observation model differs |
| Random recursive-tree percolation papers | Primarily asymptotics for random host trees; AHSL has a fixed finite host tree |
| Hypergraph motif/representation papers | Learn embeddings, not certified alpha-acyclic incidence |

## Closest-prior conclusion

No exact end-to-end match was found. The highest overlap is distributed across
separate literatures, so A1 proceeds only under the narrowed `MODIFY` framing.
The complete field-by-field comparison is in `A1_CLOSEST_PRIOR_ART.md` and the
cross-paper feature comparison is in `A1_NOVELTY_MATRIX.md`.

