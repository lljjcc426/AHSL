# S0 search log

Exact search date: **2026-08-27 (Asia/Shanghai)**.

## Sources and procedure

Search used publisher/venue pages and scholarly indexes: OpenAlex API, Crossref metadata API, PMLR, OpenReview, AAAI proceedings, ACM/IEEE metadata, PubMed/PMC, Nature/PNAS/Science publisher pages, arXiv, DBLP, GitHub repositories, Dryad, Zenodo, Mendeley Data, and official benchmark pages. Metadata was not inferred from filenames; decision-critical citations were checked against a publisher, proceedings, DOI registry, or official repository.

Counts: **92 unique scholarly works/resources screened; 34 substantive reviews; 17 substantive reviews dated 2024–2026.** The ledger contains 84 primary method/empirical works and 8 survey, protocol, benchmark, or data-resource works. `D` means substantive review; `S` means title/abstract/method-position screening. A star marks a 2024–2026 substantive review.

## Exact query families

- `factor graph structure learning higher order interactions`, `factor-scope discovery`, `hierarchical log-linear model selection`, `bounded treewidth Bayesian network structure learning`;
- `probabilistic circuits structure learning 2024`, `tractable probabilistic generative models review`;
- `hyperedge prediction`, `prediction is not classification hyperedge`, `unconstrained hyperedge search`, `hard negative hyperedge prediction`;
- `temporal hypergraph prediction`, `set-valued event forecasting`, `temporal point process higher-order interaction`, `directed temporal hyperedge`;
- `hypergraph reconstruction from network data`, `hypergraph reconstruction from dynamics`, `higher-order interaction inference time series`, `directed acyclic hypergraph topology identification`;
- `latent hypergraph discovery`, `higher-order stochastic block model`, `hypergraph mesoscale structure`;
- `protein complex discovery graph neural network CORUM`, `CYC2008 complex prediction`, `AP-MS protein complex detection`;
- `higher-order genetic interaction prediction`, `trigenic interaction data`, `combinatorial CRISPR active learning`, `higher-order epistasis`;
- `microbial community higher-order interactions all combinations`, `higher-order drug combinations factorial`, `sparse set function Möbius interaction recovery`;
- `higher-order causal structure learning`, `causal hypergraph discovery`, `hypergraph interference causal effects`;
- `n-ary relation extraction`, `hyper-relational knowledge graph completion`, `WikiPeople JF17K high arity`.

## Screening ledger

| ID | Year | Work/resource | Family | Depth |
|---|---:|---|---|:---:|
| S001 | 2003 | *Maximum Likelihood Bounded Tree-width Markov Networks* | factor/tractability | D |
| S002 | 2013 | *Exact Learning of Bounded Tree-width Bayesian Networks* | factor/tractability | D |
| S003 | 2014 | *Learning Optimal Bounded Treewidth Bayesian Networks* | factor/tractability | D |
| S004 | 2024 | *Building Expressive and Tractable Probabilistic Generative Models: A Review* | probabilistic circuits | D* |
| S005 | 2024 | *Soft Learning Probabilistic Circuits* | probabilistic circuits | D* |
| S006 | 2020 | *Hyper-SAGNN: a Self-Attention Based Graph Neural Network for Hypergraphs* | static hyperedge | D |
| S007 | 2023 | *Dynamic Representation Learning with Temporal Point Processes for Higher-Order Interaction Forecasting* | temporal event | D |
| S008 | 2023 | *CAt-Walk: Inductive Hypergraph Learning via Set Walks* | temporal event | D |
| S009 | 2024 | *Prediction Is NOT Classification: On Formulation and Evaluation of Hyperedge Prediction* | static/open-world evaluation | D* |
| S010 | 2025 | *Fast and Accurate Temporal Hypergraph Representation for Hyperedge Prediction* | temporal event | D* |
| S011 | 2025 | *HyperSearch: Prediction of New Hyperedges Through Unconstrained yet Efficient Search* | open-world hyperedge | D* |
| S012 | 2025 | *Neural Temporal Point Processes for Forecasting Directional Relations in Evolving Hypergraphs* | directed temporal event | D* |
| S013 | 2026 | *Self-Supervised Hypergraph Learning with Substructure Awareness for Hyperedge Prediction* | static hyperedge | D* |
| S014 | 2018 | *Simplicial Closure and Higher-Order Link Prediction* | higher-order prediction | D |
| S015 | 2021 | *Hypergraph Reconstruction from Network Data* | projected reconstruction | D |
| S016 | 2025 | *Hypergraph Reconstruction from Dynamics* | dynamical reconstruction | D* |
| S017 | 2024 | *Revealing Higher-Order Interactions in High-Dimensional Complex Systems: A Data-Driven Approach* | dynamical reconstruction | D* |
| S018 | 2018 | *Neural Relational Inference for Interacting Systems* | latent dynamics | D |
| S019 | 2022 | *Learning Causal Effects on Hypergraphs* | causal effects | D |
| S020 | 2025 | *Higher-Order Causal Structure Learning with Additive Models* | causal structure | D* |
| S021 | 2026 | *Dynamic Higher-Order Causality Discovery via Reinforcement Learning for Mild Cognitive Impairment Analysis* | causal structure | D* |
| S022 | 2018 | *Systematic Analysis of Complex Genetic Interactions* | combinatorial genetics | D |
| S023 | 2026 | *Dango: Predicting Higher-Order Genetic Interactions* | combinatorial genetics | D* |
| S024 | 2025 | *Active Learning for Efficient Discovery of Optimal Combinatorial Perturbations* | combinatorial genetics | D* |
| S025 | 2023 | *Sparsity of Higher-Order Landscape Interactions Enables Learning and Prediction for Microbiomes* | microbial combinations | D |
| S026 | 2024 | *Learning Beyond-Pairwise Interactions Enables the Bottom-Up Prediction of Microbial Community Structure* | microbial combinations | D* |
| S027 | 2021 | *Hidden Suppressive Interactions Are Common in Higher-Order Drug Combinations* | drug combinations | D |
| S028 | 2021 | *Machine Learning Approach for Higher-Order Interactions Detection to Ecological Communities Management* | ecological combinations | D |
| S029 | 2024 | *MoCHI: Neural Networks to Fit Interpretable Models and Quantify Energies, Energetic Couplings, Epistasis, and Allostery from Deep Mutational Scanning Data* | mutational interactions | D* |
| S030 | 2024 | *Learning to Understand: Identifying Interactions via the Möbius Transform* | sparse set functions | D* |
| S031 | 2021 | *Learning Set Functions that are Sparse in Non-Orthogonal Fourier Bases* | sparse set functions | D |
| S032 | 2013 | *A Lasso for Hierarchical Interactions* | statistics | D |
| S033 | 2015 | *Learning Interactions via Hierarchical Group-Lasso Regularization* | statistics | D |
| S034 | 2025 | *HODDI: A Dataset of High-Order Drug-Drug Interactions for Computational Pharmacovigilance* | polypharmacy data | D* |
| S035 | 2024 | *Polynomial Semantics of Tractable Probabilistic Circuits* | probabilistic circuits | S |
| S036 | 2019 | *On Structure Priors for Learning Bayesian Networks* | factor structure | S |
| S037 | 2023 | *Revisiting Bayesian Network Learning with Small Vertex Cover* | tractability | S |
| S038 | 2017 | *Information-Theoretic Limits of Bayesian Network Structure Learning* | factor structure | S |
| S039 | 2018 | *Beyond Link Prediction: Predicting Hyperlinks in Adjacency Space* | static hyperedge | S |
| S040 | 2020 | *How Much and When Do We Need Higher-Order Information in Hypergraphs? A Case Study on Hyperedge Prediction* | static hyperedge | S |
| S041 | 2020 | *HPRA: Hyperedge Prediction Using Resource Allocation* | static hyperedge | S |
| S042 | 2021 | *Principled Hyperedge Prediction with Structural Spectral Features and Neural Networks* | static hyperedge | S |
| S043 | 2022 | *AHP: Learning to Negative Sample for Hyperedge Prediction* | static hyperedge | S |
| S044 | 2023 | *Hyperedge Prediction and the Statistical Mechanisms of Higher-Order and Lower-Order Interactions in Complex Networks* | static hyperedge | S |
| S045 | 2024 | *Expressive Higher-Order Link Prediction through Hypergraph Symmetry Breaking* | static hyperedge | S |
| S046 | 2024 | *Dual-View Desynchronization Hypergraph Learning for Dynamic Hyperedge Prediction* | temporal hyperedge | S |
| S047 | 2024 | *Physics-Guided Hypergraph Contrastive Learning for Dynamic Hyperedge Prediction* | temporal hyperedge | S |
| S048 | 2024 | *Hypergraph Contrastive Attention Networks for Hyperedge Prediction with Negative Samples Evaluation* | static hyperedge | S |
| S049 | 2025 | *Hard Negative Sampling in Hyperedge Prediction* | static hyperedge | S |
| S050 | 2025 | *Enhancing Hyperedge Prediction with Context-Aware Self-Supervised Learning* | static hyperedge | S |
| S051 | 2025 | *Unveiling the Role of Higher-Order Interactions via Stepwise Reduction* | higher-order necessity | S |
| S052 | 2026 | *DHG-Bench: A Comprehensive Benchmark for Deep Hypergraph Learning* | benchmark | S |
| S053 | 2024 | *Dynamic Hypergraph Structure Learning for Multivariate Time Series Forecasting* | downstream HSL | S |
| S054 | 2023 | *Dynamic Hypergraph Structure Learning for Traffic Flow Forecasting* | downstream HSL | S |
| S055 | 2024 | *Reconstructing Higher-Order Interactions in Coupled Dynamical Systems* | dynamical reconstruction | S |
| S056 | 2024 | *Collective Relational Inference for Learning Heterogeneous Interactions* | latent dynamics | S |
| S057 | 2016 | *Discovering Governing Equations from Data by Sparse Identification of Nonlinear Dynamical Systems* | system identification | S |
| S058 | 2019 | *Model-Free Inference of Direct Network Interactions from Nonlinear Collective Dynamics* | system identification | S |
| S059 | 2022 | *Supervised Hypergraph Reconstruction* | dynamical reconstruction | S |
| S060 | 2026 | *Bayesian Hypergraph Inference from Scarce and Noisy Dynamical Observations* | dynamical reconstruction | S |
| S061 | 2026 | *Reconstructing Multiplex Networks with Higher-Order Interactions from Dynamics* | dynamical reconstruction | S |
| S062 | 2026 | *Directed Acyclic Hypergraphs: Topology Identification from Nodal Data* | causal/dynamical topology | S |
| S063 | 2025 | *Causal Discovery on Higher-Order Interactions* | causal structure | S |
| S064 | 2023 | *Causal Effect Estimation under Interference on Hypergraphs* | causal effects | S |
| S065 | 2022 | *On the Definition and Computation of Causal Treewidth* | causal tractability | S |
| S066 | 2023 | *Generalized Inference of Mesoscale Structures in Higher-Order Networks* | latent groups | S |
| S067 | 2026 | *Broad Spectrum Structure Discovery in Large-Scale Higher-Order Networks* | latent groups | S |
| S068 | 2021 | *Generative Hypergraph Clustering: From Blockmodels to Modularity* | latent groups | S |
| S069 | 2024 | *Structure and Inference in Hypergraphs with Node Attributes* | latent groups | S |
| S070 | 2022 | *Higher-Order Motif Analysis in Hypergraphs* | interaction statistics | S |
| S071 | 2003 | *An Automated Method for Finding Molecular Complexes in Large Protein Interaction Networks* (MCODE) | protein complexes | S |
| S072 | 2000 | *Graph Clustering by Flow Simulation* (MCL) | protein complexes | S |
| S073 | 2012 | *Detecting Overlapping Protein Complexes in Protein-Protein Interaction Networks* (ClusterONE) | protein complexes | S |
| S074 | 2023 | *PCGAN: A Generative Approach for Protein Complex Identification from Protein Interaction Networks* | protein complexes | S |
| S075 | 2023 | *HPC-Atlas: Computationally Constructing a Comprehensive Atlas of Human Protein Complexes* | protein complexes | S |
| S076 | 2025 | *CORUM in 2024: Protein Complexes as Drug Targets* | protein-complex resource | S |
| S077 | 2025 | *A Multi-Objective Evolutionary Algorithm for Detecting Protein Complexes in PPI Networks Using Gene Ontology* | protein complexes | S |
| S078 | 2022 | *τ-SGA: Synthetic Genetic Array Analysis for Systematically Screening and Quantifying Trigenic Interactions in Yeast* | experimental protocol | S |
| S079 | 2022 | *Higher-Order Interactions Shape Microbial Interactions as Microbial Community Complexity Increases* | microbial combinations | S |
| S080 | 2017 | *Higher-Order Interactions Capture Unexplained Complexity in Diverse Communities* | ecology | S |
| S081 | 2016 | *The Contribution of High-Order Metabolic Interactions to the Global Activity of a Four-Species Microbial Community* | microbial combinations | S |
| S082 | 2017 | *Combinatorial CRISPR-Cas9 Screens for De Novo Mapping of Genetic Interactions* | combinatorial genetics | S |
| S083 | 2019 | *GEMINI: A Variational Bayesian Approach to Identify Genetic Interactions from Combinatorial CRISPR Screens* | combinatorial genetics | S |
| S084 | 2025 | *Benchmarking Genetic Interaction Scoring Methods for Identifying Synthetic Lethality from Combinatorial CRISPR Screens* | genetic-interaction benchmark | S |
| S085 | 2023 | *A General Framework for Identifying Hierarchical Interactions and Its Application to Genomics Data* | statistics | S |
| S086 | 2018 | *Detecting Statistical Interactions from Neural Network Weights* | ML interaction discovery | S |
| S087 | 2024 | *Assessing the Limitations of Relief-Based Algorithms in Detecting Higher-Order Interactions* | interaction benchmark | S |
| S088 | 2024 | *Proving Sparsity of Interaction Primitives* | interaction theory | S |
| S089 | 2020 | *Message Passing for Hyper-Relational Knowledge Graphs* (StarE) | n-ary relations | S |
| S090 | 2021 | *Link Prediction on N-ary Relational Facts: A Graph-Based Approach* | n-ary relations | S |
| S091 | 2023 | *HAHE: Hierarchical Attention for Hyper-Relational Knowledge Graphs in Global and Local Level* | n-ary relations | S |
| S092 | 2024 | *HyperMono: A Monotonicity-Aware Approach to Hyper-Relational Knowledge Representation* | n-ary relations | S |

## Benchmarks/resources inspected

- Dryad `10.5061/dryad.tt367` and the Dango repository for yeast trigenic scores;
- complete seven-strain microbial combinations and four experimental microbiome landscapes reported in the PNAS works;
- higher-order antibiotic combination supplements/Mendeley Data;
- HODDI GitHub and its documented negative-sample construction;
- Benson/AHORN group-event repositories, CAT-Walk data route, directed-HyperTPP datasets;
- CORUM, CYC2008/MIPS usage in protein-complex papers;
- JF17K, WikiPeople, WD50K/HAHE data routes;
- THIS code/data and PhysioNet EEG route.

## Negative and collision searches

Searches for `higher-order interaction support recovery gene held out`, `trigenic active learning`, `order extrapolation combinatorial perturbation`, `calibrated higher-order interaction discovery`, and `cross-domain combinatorial interaction benchmark` did not reveal a single work combining the full selected S0 boundary. This is a bounded non-collision result, not proof of novelty.

Searches for `temporal hyperedge full candidate retrieval`, `open-world temporal hyperedge prediction`, and `unconstrained temporal hyperedge search` found direct components but no settled joint benchmark; they also revealed high collision density. Searches for real ground-truth causal/dynamical hyperedges found applications without accepted structural truth, causing the G7/G8 kills.

## Kill reasons

- factor/tractability: G4/G5/G6/G7;
- static hyperedge prediction: G3/G6/G7;
- projected reconstruction: G7/G8;
- dynamics reconstruction: G2/G7/G8;
- latent groups: G4/G7;
- protein complexes: G5/G7;
- causal mechanisms: G2/G7/G8;
- n-ary completion/extraction: G3/G6.
