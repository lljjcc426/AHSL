# META1 conditional regime definition

The proposed Confirmation regime is defined without reference to candidate wins:

1. focal-response microbial factorial landscapes of the Ishizawa type;
2. six binary companion factors, hence 64 possible communities per landscape;
3. at least five biological replicates for every complete-panel cell;
4. log10 CFU as the primary response scale;
5. a distinct-community measurement fraction no greater than 0.50, corresponding to budgets 16, 24, and 32;
6. all replicates revealed when a community is selected;
7. a fixed hybrid acquisition mask with half the budget selected by greedy pivoting on the column-scaled AND design and half sampled uniformly;
8. Elastic Net tuned using revealed responses only.

The regime is scientifically and operationally definable independently of outcomes. However, its selection was outcome-adaptive: the D50 fraction, Ishizawa panel, and `<=0.50` boundary were chosen after inspecting Development results. It must therefore be treated as a frozen hypothesis for Confirmation, not as confirmed evidence.

Within this regime, 84 paired Development conditions (7 landscapes × 3 budgets × 4 seeds) give mean F1 0.2509 versus 0.2001 for uniform Elastic Net, a +0.0508 gain. Mean precision increases 0.0217, recall 0.0955, AP 0.0135, FDR decreases 0.0217, seed stability increases 0.0653, and response RMSE worsens only 0.00151 (0.76%). Pure-HOI recall is unchanged.

The mean F1 gain is positive for all four Development seeds, 6 of 7 landscapes, and all three budgets. It is positive in 50 of 84 individual mask pairs and at least +0.05 in 42. At budget 48 the advantage reverses, and on Díaz the same policy decreases F1 by 0.0257 and worsens response RMSE by 0.0186. These boundaries are part of the regime, not discarded exceptions.
