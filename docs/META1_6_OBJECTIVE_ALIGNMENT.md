# META1.6 objective alignment

For each budget, 24 uniformly sampled feasible designs form a random-design cloud. Every design is scored by the frozen robust KKT objective, six frozen synthetic scenarios, and the seven-landscape Ishizawa macro F1 using seed 101.

Across 72 designs, Spearman correlation is -0.077 with synthetic signed F1 and 0.195 with real macro F1 (real p=0.101). At budget 32 the synthetic correlation is significantly negative. These results show objective/recovery mismatch, not successful surrogate validation. Full data and correlations are in `results/meta1_6/raw/random_design_cloud.csv` and `results/meta1_6/aggregated/objective_alignment.csv`.
