# META1.6 row search

Search operates only on the feasible Boolean rows. Row 0 is mandatory; every proposal exchanges one selected nonzero row with one unselected row. Starts are uniform, D-opt, and `hybrid_d50`; two are used per objective under the frozen compute budget. Each round evaluates 16 deterministic random proposals and stops after two non-improving rounds.

The same engine is used for HILS, DCD, and candidate ablations. Search uses the complete primary Pi and never observes synthetic recovery outcomes or Ishizawa responses. The recorded evaluation counts, accepted swaps, objective values, and runtimes are in `results/meta1_6/raw/tuning_trials.csv`.
