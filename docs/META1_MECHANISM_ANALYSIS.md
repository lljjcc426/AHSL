# META1 mechanism analysis

## M1: replicate noise

Noise weighting improves on Lasso but not on tuned Elastic Net. Across conditions, the P1 gain is uncorrelated with replicate SNR (Spearman rho 0.002, p=0.987). M1 is therefore not isolated as the causal development lever.

## M2: support instability and error control

Strict stability filtering produces low empirical FDR by selecting almost nothing. Its equal-panel macro F1 is approximately 0.0003 at the strict threshold; the 0.6 threshold remains only about 0.0102. This is an abstention frontier, not reliable recovery.

## M3: non-hereditary structure

Only 7 of 137 Ishizawa primary effects are pure HOIs and Díaz has none. Order-aware penalties do not beat Elastic Net in Ishizawa and improve Díaz only marginally while FDR remains about 0.94. The reference does not contain enough pure-HOI mass for this mechanism to explain the candidate gain.

## M4: AND-design coherence and exact aliases

The usual maximum column correlation is saturated at 1 and is not discriminative. The useful structural diagnostic is the fraction of exact column aliases under the selected rows. Hybrid D50 eliminates observed exact aliases in the candidate regime, increases signed recall by 0.0955 and seed Jaccard by 0.0653, and raises F1 by 0.0508. Precision also rises by 0.0217, so the gain is not produced only by uncontrolled discoveries.

This is mechanistically coherent but still associational: the policy was selected during Development, and alias elimination alone does not prove it caused every landscape-level gain. The Díaz failure shows that improving design geometry is insufficient when the response/support geometry differs.
