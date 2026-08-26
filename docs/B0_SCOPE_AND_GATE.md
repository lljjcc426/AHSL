# Phase B0 Scope and Feasibility Gate

## 1. Phase boundary

Phase B0 starts from the frozen A1.5 commit
`930ebc003cbc35a5704e3eb76200b15d0c7a17d3`.

The following A-series conclusions are fixed inputs, not questions to reopen:

- fixed-tree exact dynamic programming is infrastructure;
- exact subtree marginalization and posterior marginals are infrastructure;
- Bayes-Hamming decoding gives a small, stable decision-alignment gain;
- learning join-tree identity has no stable material value and is stopped;
- no neural tree learner, new edge scorer, tree-search heuristic, A1.6, or
  generalized-hypertree-width expansion is authorized;
- no further synthetic estimator development is part of B0.

B0 contains no model implementation or experiment. It is a feasibility study
of real tasks, real data, observable covariates, structural validity, and the
need for tractable exact inference.

## 2. Translation from the A-series object to a real task

For a candidate application, one prediction instance must have the form

```text
observable covariates X_i  ->  unknown support S_i on a declared scaffold T.
```

The repeated instances must share a statistical law so that learning
`P_theta(S_i | X_i, T)` can generalize to unseen instances. The mapping must
also specify what the support elements mean in the domain, why the support is
the prediction target, and what real decision or evaluation loss uses it.

A visually tree-like domain is insufficient. A candidate is relevant only if
the *label support*, rather than merely the input geometry, is well represented
by the allowed output family.

## 3. Hard feasibility gates

A candidate receives GO only if every gate below passes.

| Gate | Required evidence | Failure condition |
| --- | --- | --- |
| G1 Real target | A repeated supervised or decision problem with real labels and a named loss or operational use | The target is invented for the method or is available only from a simulator |
| G2 Observable `X_i` | Covariates are available at prediction time, before the target is known | Features leak the answer, require unavailable annotations, or exist only retrospectively |
| G3 Shared law | Multiple instances support estimation of a transferable conditional prior | Each instance has a unique incomparable scaffold or no repeated statistical population |
| G4 Domain-valid support | Connected or low-width support is scientifically justified, including empty and multi-component cases | Connectivity is imposed only for convenience, or common valid outcomes lie outside the output class |
| G5 Exact-inference need | Exact or calibrated structured inference addresses an evidenced accuracy, uncertainty, latency, or decision requirement not already trivialized by the task | The output is a singleton, the constraint is vacuous, or mature task-specific inference already solves a different formulation |

## 4. Data gate

Passing the conceptual gates is not enough. Before implementation there must be
a usable dataset containing, for the same instances:

1. real covariates available at prediction time;
2. real target labels at the required structural resolution;
3. the scaffold, or an explicit and scientifically valid canonical mapping;
4. enough independent instances to separate train, validation, and test data;
5. terms that permit the intended academic analysis.

Synthetic inputs can validate software but cannot substitute for this gate.
Real covariates combined with simulated faults or simulated labels also do not
constitute a real supervised target.

## 5. Structural-uncertainty gate

A1.5 showed near calibration with the generating tree but systematic
overconfidence when an estimated tree was treated as fixed. Therefore each B0
candidate must be classified as one of:

- **known fixed scaffold**: `T` is available at prediction time and its meaning
  is stable across instances;
- **known instance-specific scaffold**: each `T_i` is observed and instances
  have a defensible common coordinate system or equivariant parameterization;
- **uncertain scaffold**: the graph/tree is estimated, incomplete, changing, or
  itself the target.

The last category cannot be passed into the frozen posterior as if it were
known. If scaffold uncertainty is central to the application, it is a new
scientific problem and not a justification for reviving tree-identity learning.

## 6. Decision rule

- **GO**: all five scientific gates and the data gate pass.
- **CONDITIONAL HOLD**: the task is scientifically aligned but one concrete,
  externally resolvable data item is missing. No model implementation is
  allowed during the hold.
- **NO-GO**: at least one core task or structural premise fails.

The B0 project-level decision is GO only if at least one candidate receives
GO. A collection of partial matches does not add up to a pass.

## 7. B0 result

No surveyed candidate passes all gates. The project-level decision is:

```text
B0 = NO-GO for a Phase B1 model implementation.
```

The current AHSL machine-learning line therefore stops after B0. The exact
inference code remains valid research infrastructure, but there is no evidence
base for attaching a feature-conditioned model to it now.
