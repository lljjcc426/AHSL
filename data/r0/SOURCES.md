# R0 Data Sources

R0 uses the public UAI 2014 probability-of-evidence benchmark archive, also
linked by the UAI 2022 competition:

- index: <https://ics.uci.edu/~dechter/softwares/benchmarks/Uai14/>
- archive: `PR_prob.tar.gz`
- task description: <https://uaicompetition.github.io/uci-2022/results/benchmarks/>

Place the archive and extracted `.uai` files under:

```text
data/r0/downloads/PR_prob.tar.gz
data/r0/downloads/uai2014_pr/
```

The download directory is ignored by Git. The UAI page provides public
downloads but does not state one uniform license for all contributed model
families; redistribution is therefore not assumed. Only derived structural and
runtime statistics are committed.

Reproduce the bounded audit with:

```powershell
python experiments/r0_strategy_variance.py `
  --input-dir data/r0/downloads/uai2014_pr `
  --output-dir results/r0/raw `
  --max-strategy-variables 100 `
  --max-per-family 1 `
  --random-orders 4 `
  --exact-per-family 0
```

The checked-in representative run uses a seven-instance subset documented in
`docs/R0_STRATEGY_VARIANCE_AUDIT.md` and prefix `uai2014_selected`.
