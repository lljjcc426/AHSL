# META1.6 HILS baseline

The baseline follows the sign-recovery logic of Stallrich et al. (2025): for every Pi scenario and lambda on the frozen path, it evaluates the active-sign and inactive-exclusion KKT events under iid Gaussian response noise. It uses the full signed model event, averages probabilities over Pi, and searches feasible Boolean rows by multi-start exchange.

The unavoidable adaptation is the search space: published HILS changes entries of a two-level supersaturated design, whereas META1.6 must choose whole rows from a fixed AND dictionary. The KKT event, support/sign averaging, homoscedastic noise model, and singular-support loss are retained. Search settings are two starts, 16 proposals per round, and patience two, with the complete 36-scenario Pi.
