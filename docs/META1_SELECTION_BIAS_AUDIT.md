# META1 selection-bias audit

| Item | Development exposure |
|---|---|
| Response scales | 2 per panel: Ishizawa log10/raw; Díaz raw/log1p |
| Practical thresholds | primary plus fixed 0.8 and 1.2 multipliers |
| Support rules | CI95+practical, sign95+practical, bootstrap-sign BH10+practical |
| Uniform method families | 14 |
| Acquisition policies | uniform, row_cosine_v0, d_optimal_rows, hybrid_d25, hybrid_d50, hybrid_d75 |
| Budgets | 4 per panel |
| Development mask seeds | 4: 101, 202, 303, 404 |
| Reserved seeds | 2: 505, 606 |
| Experiment rows retained | 3,200 |
| Tuning-trial evaluations retained | 51,168 |

Post-outcome decisions were: adding the corrected pivoted-row policy after row-cosine failed; searching hybrid fractions 0.25/0.50/0.75; choosing D50; and delimiting the promising claim to Ishizawa budgets 16/24/32 after observing the budget-48 reversal and Díaz failure. The response scales, estimand R1, budget grid, Development seeds, and Confirmation seeds preceded this choice.

The final regime can be stated using panel semantics, dimension, replicate availability, response scale, measurement fraction, and a fixed design rule, without saying where the method won. That makes it confirmable, but not outcome-independent in selection history. Reported Development effect sizes are therefore exploratory and likely optimistic.

All failures and neutral results remain in the experiment and tuning ledgers. The reserve masks for seeds 505 and 606 at every budget have not been used. Confirmation must run the frozen candidate and comparators once, without retuning the policy fraction or moving the regime boundary.
