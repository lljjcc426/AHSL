# N1.0 exact-solver reproducibility

## Implementation

`src/certpath/solver_adapter.py` is an independent SciPy/HiGHS MILP cut-generation implementation of the Mmunin superpath characterization. It does not copy or vendor Mmunin/Hhugin code. Source-to-target cut inequalities are added until the selected edge set is feasible; positive weights then imply a minimal optimum.

The exact attainability decision used monotone one-edge deletion inside each gold set. This is not a heuristic shortcut: a feasible proper subset exists if and only if at least one one-edge deletion remains feasible. A full minimum-cardinality call is retained for examples and theorem validation.

## Commands

From repository root with the package installed:

```powershell
python -m certpath.experiments.n1_0_build_tasks --v89 data/n1_0/downloads/v89/Homo_sapiens.owl --v97 data/n1_0/downloads/v97/Homo_sapiens.owl --output results/n1_0/raw
python -m certpath.experiments.n1_0_run_baselines --biopax data/n1_0/downloads/v97/Homo_sapiens.owl --release 97 --snapshot-cache data/n1_0/downloads/v97/snapshot.pkl --output results/n1_0/raw/task_audit_v97.csv
python -m certpath.experiments.n1_0_validate_theory --output results/n1_0/raw/attainability_bruteforce.csv
python -m certpath.experiments.n1_0_analyze --audit results/n1_0/raw/task_audit_v97.csv --temporal results/n1_0/raw/temporal_task_status.csv --snapshot-cache data/n1_0/downloads/v97/snapshot.pkl
pytest
```

The analysis command uses only applicable upstream-gate results. Pairwise and classical-baseline fields remain blank because the 59.32% representability result mandated an early stop.

## External artifact handling and license boundary

Mmunin commit `3bb5f17` and pathway-connectivity commit `62de73b` were shallow-cloned under ignored `data/n1_0/external/` only to inspect published artifacts and source semantics. They are not distributed in this branch. The current Mmunin GitHub repository exposes GPL-3.0 while the project website states older noncommercial/no-redistribution terms; the independent implementation avoids relying on that ambiguity. Hhugin was not executed because the upstream gate failed.

## Scope of runtime evidence

A 5-edge example (`R-HSA-110312`) solved in 0.043 s with seven added cuts. A 20-edge multi-target example (`R-HSA-1059683`) hit a 10 s exploratory limit after 191 cuts. These are diagnostic examples, not a runtime distribution. Median/p95/max runtime is therefore **not evaluated**, and no solver-feasibility PASS is claimed.
