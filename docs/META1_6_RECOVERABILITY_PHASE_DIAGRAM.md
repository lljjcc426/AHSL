# META1.6 recoverability phase diagram

The synthetic grid crosses budgets 16/24/32, `k_H={2,4,8,12}`, `k_L={0,4,8,12}`, SNR `{0.5,1,2}`, and four representative designs. Each singular support contributes zero rather than disappearing from the denominator.

The complete table is `results/meta1_6/aggregated/phase_diagram.csv`; budget-specific heatmaps are in `results/meta1_6/figures/phase_diagram_b*.png`. The observed phase is not monotone in the proposed KKT objective: D-opt is often stronger than both fixed-row HILS and the modified candidate, and exact target-sign recovery is rare. These results support a bounded negative conclusion rather than a uniform recovery claim.
