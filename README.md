# AHSL Phase A0

This repository is a reproducible prototype for testing whether a known
alpha-acyclic structural constraint can denoise corrupted hypergraph incidence
observations.

## Scientific hypothesis

Let `B` be an `n x m` incidence matrix and let the `m` labeled hyperedges be the
nodes of a fixed tree `T`. For each original vertex `i`, define

```text
S_i = {j : B[i, j] = 1}.
```

The running-intersection property requires every `S_i` to induce a connected
subgraph of `T`. The classical join-tree characterization then makes the
hypergraph alpha-acyclic. Phase A0 asks whether restricting estimates to this
hypothesis class improves recovery of a clean incidence matrix after independent
false-positive and false-negative flips.

The representation itself is classical and is not claimed as novel.

## Exact A0 representation

The synthetic generator chooses an anchor separately for every original vertex
and traverses outward from that anchor. A frontier branch is explored only when
its connecting node is accepted. This represents connected subtrees without the
artificial restriction caused by a single global descendant orientation.

For learning, every non-empty bit mask over tree nodes is inspected and retained
exactly when its induced subgraph is connected. If `S(T)` is the resulting
candidate set, FixedTreeAHSL learns one categorical distribution per incidence
row:

```text
q_i(S) = softmax(logits_i)[S]
P[i, j] = sum_S q_i(S) 1[j in S].
```

Training probabilities lie in the convex hull of connected-subtree incidence
vectors. Inference takes `argmax_S q_i(S)`, so every discrete prediction is a
connected, non-empty subtree by construction. No soft acyclicity loss and no
post-hoc repair are used.

Enumeration costs `O(2^m m)` time. A path has `m(m+1)/2` candidates, while a
star has `2^(m-1) + m - 1`. The runner prints the search-space size, a candidate
upper bound, and an estimated logits footprint before fitting any model. It
stops explicitly if configured enumeration limits are exceeded.

## Models and baselines

- `Observed`: raw observation for `R=1`, or entrywise majority for repeated observations.
- `Unconstrained`: independent free logits trained by Bernoulli reconstruction. For one binary observation this can simply memorize noise.
- `SparseUnconstrained`: the same logits plus `lambda_s * mean(P)`. The default pilot retains all five requested lambda values; plots use the preregistered `lambda_s=0.01` line rather than clean-label oracle selection.
- `NearestConnectedSubtree`: exact minimum-Hamming projection for every row.
- `NoiseAwareMAPSubtree`: exact maximum likelihood over connected candidates with a uniform candidate prior and known `p_+`, `p_-`.
- `FixedTreeAHSL`: learnable categorical distributions over the complete connected-subtree candidate set.

The exact projection and known-noise likelihood estimators are central scientific
baselines. Matching or losing to them is evidence that a neural estimator is not
needed in the known-tree setting.

## Synthetic data and evaluation

Supported tree topologies are `random`, `path`, `star`, and `balanced`. Random
trees use uniformly sampled Pruefer sequences. Incidences are independently
corrupted by false-negative and false-positive rates; observations are never
repaired to be acyclic.

The default controlled pilot covers:

- four tree topologies;
- symmetric noise `0.0, 0.1, 0.2, 0.3`;
- false-positive-only and false-negative-only noise at `0.2`;
- one and three repeated observations;
- five paired seeds;
- all requested sparse penalties.

Every raw row records incidence precision/recall/F1, Hamming error, exact row
recovery, mean row symmetric difference, RIV, density, noisy reconstruction BCE,
hyperedge Jaccard/F1/exact recovery, runtime, and candidate count. Aggregation is
mean and standard deviation over seeds. Paired bootstrap intervals and Wilcoxon
tests are generated without treating a few-seed p-value as decisive evidence.

## Installation and commands

Python 3.11 or newer is required.

```powershell
python -m pip install -e .
python -m pytest -q
python experiments/exp_a0_fixed_tree.py `
  --config experiments/configs/a0_default.yaml `
  --dry-run
python experiments/exp_a0_fixed_tree.py `
  --config experiments/configs/a0_default.yaml
```

Use `--max-runs N` to cap the number of paired dataset cases after the full plan
has been printed. The dry run executes the complete output pipeline on tiny data;
it is an integration check, not scientific evidence.

## Result locations

```text
results/raw/a0_results.csv
results/aggregated/a0_summary.csv
results/aggregated/a0_statistical_tests.csv
results/plots/a0_clean_f1_vs_noise.png
results/plots/a0_exact_recovery_vs_noise.png
results/plots/a0_symmetric_difference_vs_noise.png
results/plots/a0_riv_vs_noise.png
results/plots/a0_reconstruction_bce_vs_clean_f1.png
results/plots/a0_performance_vs_candidates.png
results/plots/a0_runtime_vs_m.png
results/logs/a0_run.log
results/A0_RESEARCH_REPORT.md
```

Raw per-seed results are always retained; aggregated means are not the only
saved evidence.

## Scope and limitations

Phase A0 assumes the true join tree is known. It tests structural projection and
denoising from direct noisy incidence observations. It does not establish
statistical consistency, usefulness for general hypergraph structure learning,
or neural superiority. Empty hyperedges can occur in the synthetic sampler, but
each original vertex belongs to at least one hyperedge as required.

This phase does not implement GYO verification, learned join trees, generalized
hypertree width, GNNs, directed hypergraphs, causal discovery, real datasets, or
large-scale GPU optimization. Those are separate theoretical and empirical
questions for later phases, and should not be conflated with alpha-acyclicity.

