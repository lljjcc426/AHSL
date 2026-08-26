# N1 proposal: CertPath

## Title

**CertPath: Calibrated Reaction-Cost Learning with Exact Directed-Hyperpath Decoding for Pathway Inference**

## Problem

Given a versioned curated reaction network, a source set, a target, and reaction/context features, learn nonnegative reaction costs such that the exact minimum-cost directed hyperpath recovers a biologically curated pathway on unseen pathway families and future database releases. Return the learned solution only when a cost-uncertainty margin certifies that it remains optimal throughout a declared uncertainty set; otherwise abstain to a classical cost.

## Why existing methods are insufficient

Exact Mmunin and heuristic Hhugin solve a supplied weighted directed-hyperpath problem but largely evaluate unit or externally supplied weights. CHESHIRE, Multi-HGNN, DHGNN, and BPP learn reaction/hyperedge representations but do not guarantee source–target feasibility or optimality of a pathway. Simply composing either class is insufficient: N1 requires a decision-focused objective, a leakage-resistant evaluation protocol, and a robust-optimality/abstention certificate.

## Dataset

- Primary: versioned Reactome BioPAX, CC0, with quarterly Zenodo snapshots from release 89 onward.
- Structural protocol: the published Hyperpaths conversion, preserving entity variants, conjunctive tails, products, positive regulators, cycles, and self-loops.
- External historical stress set: NCI-PID via Pathway Commons where terms permit.
- Primary split: group-disjoint by top-level Reactome pathway family.
- Shift split: train/validate on older release(s), test on a later release.
- Primary unit: a reachable source-set/target task with curated reaction membership.
- No random reaction-edge split as primary evidence.

## Theory

Let \(\mathcal P(s,t)\) be feasible directed hyperpaths and let the learner return positive costs \(\hat c\) and coordinate intervals \([\ell_e,u_e]\). Exact decoding returns \(\hat P=\arg\min_{P\in\mathcal P}\sum_{e\in P}\hat c_e\). The proposed certificate verifies a sufficient separation condition between the worst admissible cost of \(\hat P\) and a lower bound for every alternative. If it holds, \(\hat P\) is optimal for all \(c\in\prod_e[\ell_e,u_e]\); otherwise the system abstains. The statistical calibration claim and deterministic robust-optimality claim must be stated separately.

## Learning component

Start with a transparent positive reaction-cost model using reaction type, provenance, compartment, tail/head arity, regulator status, biochemical annotations, and local directed-hypergraph context. Compare linear, gradient-boosted, and one compact directed-hypergraph scorer only after the non-neural models establish residual. Train against reaction membership/ranking first; decision-focused structured training is conditional on the first kill test.

## Algorithmic skeleton

1. Freeze Reactome releases and construct source–target instances.
2. Fit a positive cost/ranking model on training families only.
3. Calibrate cost intervals on a disjoint calibration set.
4. Decode the exact general directed hyperpath with Mmunin-equivalent cutting planes.
5. Compute the robust-optimality separation certificate.
6. If certified, emit the learned path; otherwise emit the classical unit/provenance-cost exact path and mark abstention.
7. Evaluate reaction-set quality separately from conditional exactness.

## Baselines

1. exact unit-weight Mmunin;
2. Hhugin heuristic;
3. exact hand-crafted provenance/rate/atom-conservation weights;
4. reaction-scoring model with unconstrained top-k output;
5. ordinary pairwise graph shortest path;
6. same learned costs + exact decode but no calibration/abstention;
7. CHESHIRE/Multi-HGNN-style prediction where compatible with the data.

## Primary metrics

- primary: reaction-set F1 on held-out pathway families;
- precision and recall separately;
- exact-feasibility rate;
- certificate coverage and F1 conditional on certification;
- fallback rate;
- runtime and memory;
- results stratified by tail arity, cycle status, target reachability, pathway family, and release shift.

## Expected theorem/guarantee

If the selected path's upper interval cost is strictly below a valid lower bound on every competing path's lower interval cost, then the selected directed hyperpath is optimal for every reaction-cost vector in the interval set. With calibrated intervals under explicitly stated sampling assumptions, this yields a corresponding conditional stability statement; it does not certify biological truth.

## First kill test

Use 300--500 reachable Reactome tasks from at least four top-level pathway families. Train on disjoint families from one or more older releases, calibrate separately, and test on a held-out family plus a later release. Fit only linear and gradient-boosted positive cost models. Compare exact learned-cost decoding against exact unit/provenance costs and unconstrained top-k scoring.

## Stop conditions

Stop N1 before a neural model if any occurs:

1. paired held-out F1 improvement over the best classical exact-cost baseline is <2 absolute points and its 95% paired bootstrap interval includes 0;
2. improvement appears on random splits but disappears on both family-disjoint and temporal tests;
3. ordinary pairwise projection matches the native directed-hyperpath decoder without an increase in infeasible/semantically invalid paths;
4. robust certificate coverage is <20% at no positive F1 trade-off over fallback;
5. exact decoding exceeds 500 CPU-hours for the bounded test;
6. refreshed prior-art search finds a work matching the learned cost, exact general directed-hyperpath decoder, uncertainty certificate, and grouped real-data protocol.

## Compute budget

- <=500 CPU-hours total for data construction, exact labels, and decoding;
- <=24 GPU-hours, and zero GPU is acceptable for the first test;
- <=7 elapsed days on normal academic hardware;
- no proprietary data or cloud-scale requirement.

## Likely venue family

Strong fit: RECOMB/ISMB/Bioinformatics. Plausible fit: UAI/AISTATS or CP/AAAI/IJCAI if the guarantee and generality are substantial. General top-ML fit is weak unless the theory transfers beyond this single domain.

## Novelty risks

- a two-stage “predict scores then call Mmunin” contribution is only Level 1;
- uncertainty-set learning and decision-focused optimization are established generically;
- curated pathways are overlapping/incomplete and can make F1 misleading;
- research-use solver terms require a downloader/adapter or independent implementation;
- a new 2026/2027 direct collision may appear.

N1 is not implemented by this document.
