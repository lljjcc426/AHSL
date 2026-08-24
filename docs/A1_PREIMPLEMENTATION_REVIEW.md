# A1 Pre-implementation Review

Date: 2026-08-25

## Literature Gate decision

**Literature Gate MODIFY**

Proceed with the classical kill-test, but narrow the contribution claim. The
anchor-growth prior is a size-biased Bernoulli bond-percolation cluster, and the
proposed recurrence is an instance of exact sum-product on a tree. Marginal
likelihood structure search and latent-variable structure learning are also
classical ideas. The defensible open question is therefore empirical and
problem-specific:

> Does a correctly specified connected-support likelihood select a useful tree
> over labeled hyperedge columns from noisy incidence rows, and does it close
> the held-out A0.75 recovery gap?

No screened paper was found that performs the complete AHSL mapping

```text
noisy binary incidence rows
  -> latent nonempty connected supports on a tree of hyperedge columns
  -> exact support marginalization
  -> likelihood-based selection of that labeled tree
  -> alpha-acyclic certificate by construction.
```

This absence is not a proof of novelty. It is sufficient to run a bounded
classical experiment, not to claim a new general inference algorithm.

## Required questions

### 1. What remains unsolved after A0.75?

A0.75 used a uniform connected-support decoder and profile likelihood. It left
a held-out-style motivation, but not a valid generalization experiment. The
remaining question is whether the A0.75 residual is caused by a misspecified
subtree prior and profile maximization, or by genuine tree-selection error.

### 2. Is "join-tree recovery" the correct phrase?

Not as the primary phrase. A sampled alpha-acyclic hypergraph can have multiple
join trees, and the generating tree need not minimize downstream loss under a
misspecified decoder. A1 will use "tree-structured connected-support prior
selection" or "latent tree selection". Generating-tree edge recovery remains a
secondary diagnostic.

### 3. Is the anchor-growth subtree prior already known?

Its probabilistic object is known: sample independent open/closed states for the
edges of a fixed tree and return the open cluster containing a uniformly chosen
vertex. Marginalizing the anchor size-biases each percolation cluster by its
number of vertices. The exact AHSL parameterization is useful, but it is not a
new family of random connected subsets.

### 4. Is exact marginalization over connected subtrees already known?

The general mechanism is known. It is tree sum-product / belief propagation;
connected-subgraph generating functions and application-specific connected-
subtree dynamic programs also predate AHSL. A1 may derive and validate the
specialized two-message recurrence, but must not claim a new DP paradigm.

### 5. Is marginal-likelihood tree search covered by Structural EM?

It lies within the classical latent-variable structure-learning setting, but a
literal Structural EM update is unattractive here. The latent support space
depends on the candidate tree. A support connected in the current tree can be
disconnected in a proposed tree, making a naive expected complete-data score
equal to negative infinity. Direct observed-data likelihood search gives exact
scores and a monotone accepted-move criterion without this changing-support
problem.

### 6. What are the five closest prior works?

1. Borgelt and Kruse (2001): likelihood-guided learning of bounded-clique
   hypertree graphical models for tractable propagation.
2. Friedman (1998): Bayesian Structural EM for structure learning with missing
   or hidden data.
3. Choi et al. (2011): consistent latent-tree graphical-model recovery from
   observed variables using information distances and MST-guided grouping.
4. Nikolakakis et al. (2019): recovery of tree-structured Ising/Gaussian models
   from noisy samples.
5. Chen and Yuille (2015): an explicit connected-subtree latent visibility
   constraint with efficient exact tree inference.

Kschischang, Frey, and Loeliger (2001) is the strongest algorithmic prior for
the message computation itself.

### 7. What is the current novelty risk?

High for algorithmic claims, moderate for the combined statistical formulation,
and unresolved for practical scientific value. The project must describe the
work as a problem-specific classical synthesis unless a later exhaustive review
establishes a stronger contribution.

### 8. Is there a stronger classical model to test?

The proposed observed-data marginal likelihood with known noise and both oracle
and estimated `q` is the strongest proportionate first test. A richer
degree-dependent or feature-conditioned subtree prior may fit better, but adding
it before testing the matched one would confound the kill-test.

### 9. Is neural A1 justified now?

No. Exact classical inference is available, the proposed model has one scalar
prior parameter, and A0.75 did not test a matched marginal likelihood. Neural
work remains blocked by the A1 kill rules.

### 10. Should the project stop before implementation?

No. No screened work substantially subsumes the full problem, and the matched
model makes a falsifiable prediction about the A0.75 residual and star anomaly.
Implementation is justified under the modified, non-novel-DP framing.

## Bounded execution plan

1. Verify the specialized log-space sum-product score against exhaustive
   connected-subtree enumeration.
2. Implement deterministic full-neighborhood observed-likelihood tree search
   if measured feasible at `m=16`.
3. Estimate `q` using noisy train/validation rows only.
4. Validate local search against all labeled trees for small `m`.
5. Run the preregistered 30-seed held-out experiment and apply the kill rules.

