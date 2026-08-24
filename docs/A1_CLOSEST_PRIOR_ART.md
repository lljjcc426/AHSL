# A1 Closest Prior Art

## 1. Borgelt and Kruse (2001)

- **Problem:** learn a graphical model whose later evidence propagation remains
  tractable.
- **Observed data:** complete or partially complete sample cases over domain
  attributes.
- **Latent variables:** none in the primary probabilistic experiment; missing
  values occur in the possibilistic data.
- **Structure class:** undirected decomposable graphs whose maximal cliques have
  the running-intersection property; clique size is bounded.
- **Objective:** probabilistic log likelihood, optionally penalized by model
  size; a possibilistic quality measure in the second experiment.
- **Inference algorithm:** join-tree evidence propagation after learning.
- **Structure search:** simulated annealing with specialized random generation
  and modification of hypertree structures.
- **Complexity:** controlled through a maximum clique-size restriction; the
  paper does not give a polynomial global optimization guarantee.
- **Guarantees:** generated/modified candidates retain hypertree structure;
  simulated annealing is heuristic.
- **Experiments:** Danish Jersey cattle network; probabilistic train/test pairs
  and a partially observed possibilistic dataset. The probabilistic annealing
  result was worse than several baselines.
- **Relationship to AHSL:** both learn under a running-intersection/tractability
  constraint and evaluate held-out likelihood.
- **Overlap risk:** high for a broad "learn hypertree structure for tractable
  inference" claim.
- **Remaining difference:** their variables are graph nodes and join-tree nodes
  are learned maximal cliques. AHSL tree nodes are fixed labeled hyperedge
  columns, while each original vertex supplies a noisy row with a latent
  connected support.

## 2. Friedman (1998), Bayesian Structural EM

- **Problem:** Bayesian structure selection with missing or hidden data.
- **Observed data:** incomplete sample records.
- **Latent variables:** missing values and hidden variables in probabilistic
  models.
- **Structure class:** Bayesian networks and related model families.
- **Objective:** Bayesian model score; the earlier Structural EM version also
  covers penalized likelihood/MDL-style scores.
- **Inference algorithm:** posterior expected sufficient statistics under the
  current model.
- **Structure search:** structural improvements inside EM using the expected
  complete-data score.
- **Complexity:** inherits inference and complete-data structure-search costs;
  tractability depends on the model family and search restrictions.
- **Guarantees:** monotone/convergent model-selection EM updates under the
  stated score construction.
- **Experiments:** missing-data and hidden-variable belief-network learning in
  the Structural EM line.
- **Relationship to AHSL:** establishes the general framework of alternating
  latent inference and structure search.
- **Overlap risk:** high for any claim that optimizing a tree with latent clean
  rows is a new structure-learning principle.
- **Remaining difference:** AHSL has a tree-dependent feasible support set and
  can score observed likelihood exactly; the usual expected-statistic structural
  step does not reduce to an established AHSL tree update.

## 3. Choi et al. (2011)

- **Problem:** recover a minimal latent tree graphical model when only a subset
  of node variables is observed.
- **Observed data:** iid samples of observed variables.
- **Latent variables:** unobserved internal tree nodes.
- **Structure class:** minimal latent trees, including discrete and Gaussian
  families under information-distance assumptions.
- **Objective:** structure recovery from additive information distances; also
  regularized latent-tree approximation.
- **Inference algorithm:** moment/information-distance calculations rather than
  per-row connected-support marginalization.
- **Structure search:** recursive grouping and CLGrouping, initialized by an
  MST over observed variables.
- **Complexity:** polynomial and scalable under bounded degree/effective depth;
  the paper gives sample and computational guarantees.
- **Guarantees:** consistency and sample-complexity results under model
  assumptions.
- **Experiments:** synthetic latent trees, stock returns, and binary word data.
- **Relationship to AHSL:** both infer a tree from iid observations and use an
  MST as a global structural tool.
- **Overlap risk:** high for generic "latent tree structure learning" or
  "MST-initialized hidden tree recovery" claims.
- **Remaining difference:** their tree nodes are stochastic variables and some
  nodes are hidden; AHSL observes noisy coordinates at every labeled tree node
  and the hidden object is a connected support per row.

## 4. Nikolakakis, Kalogerias, and Sarwate (2019)

- **Problem:** learn Ising and Gaussian tree structures from noisy data.
- **Observed data:** iid samples passed through additive/discrete noise models.
- **Latent variables:** clean samples before observation noise.
- **Structure class:** tree-structured pairwise graphical models.
- **Objective:** recover the conditional-dependence tree using noisy-data
  analogues of Chow-Liu statistics.
- **Inference algorithm:** estimate noisy pairwise statistics/information
  distances.
- **Structure search:** maximum spanning tree.
- **Complexity:** polynomial; pairwise statistics plus MST.
- **Guarantees:** exact recovery/sample-complexity characterizations under
  Ising and Gaussian assumptions.
- **Experiments:** synthetic noisy tree recovery across noise/sample regimes.
- **Relationship to AHSL:** both estimate a labeled tree from noisy binary-like
  samples and compare against an MST baseline.
- **Overlap risk:** decisive against any "first noisy tree recovery" claim.
- **Remaining difference:** AHSL rows are not Markov samples on `T`; their
  latent one-sets are connected percolation clusters, producing higher-order,
  non-pairwise row distributions.

## 5. Chen and Yuille (2015)

- **Problem:** parse human pose under large occlusions.
- **Observed data:** image evidence for locations, pairwise relations, and
  occlusion cues.
- **Latent variables:** visible body-part composition and part locations.
- **Structure class:** every connected subtree of a fixed tree-like body model.
- **Objective:** maximum-score pose/composition inference.
- **Inference algorithm:** dynamic programming sharing computations across all
  connected subtrees; about twice the base-model computation.
- **Structure search:** the body tree is fixed; it is not learned.
- **Complexity:** efficient exact max inference despite exponentially many
  possible connected compositions.
- **Guarantees:** exactness for the specified tree model; no general tree-
  structure recovery guarantee.
- **Experiments:** the We Are Family occlusion benchmark and diagnostics showing
  that visible parts are usually connected.
- **Relationship to AHSL:** the closest located prior for a latent variable that
  is explicitly restricted to a connected subtree.
- **Overlap risk:** high for novelty of connected-subtree state spaces or
  efficient shared tree inference.
- **Remaining difference:** AHSL sums rather than maximizes support likelihoods,
  uses a percolation prior and bit-flip emissions, and searches over the labeled
  tree itself.

## Algorithmic reference: Kschischang et al. (2001)

The two-message AHSL scorer is a direct specialization of cycle-free
sum-product. This paper is not one of the five closest problem formulations,
but it is the strongest prior-art constraint on algorithmic novelty.

