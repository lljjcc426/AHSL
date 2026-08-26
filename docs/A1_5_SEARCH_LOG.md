# A1.5 Focused Literature Search Log

## Search record

- **Search date:** 2026-08-26
- **Cutoff:** current search date
- **Sources used:** primary publisher/proceedings pages, DOI records, JMLR,
  PMLR, Oxford Academic, PNAS/PMC, Wiley, ACM, AAAI, and author manuscripts.
- **Research skills:** not used, per project instruction.
- **Primary works screened:** 18
- **Works read in substantive detail:** 8
- **Closest concepts analyzed field-by-field:** 3

Substantive reading means the loss, posterior quantity, feasible output class,
decoder, complexity, and empirical role were inspected rather than only the
title and abstract.

## Query families

```text
minimum Bayes risk decoding Hamming loss structured prediction
posterior decoding versus Viterbi MAP HMM
constrained posterior decoding maximum expected accuracy
centroid estimator posterior marginals structured output
RNA gamma centroid estimator base pair probabilities dynamic programming
sum product node marginals reverse mode partition function derivative
maximum weight connected subtree node weights tree
posterior risk calibration Bayesian model misspecification
likelihood versus decision loss graphical models
```

## Screened primary works

| # | Cluster | Work | Depth | Relevance decision |
|---:|---|---|---|---|
| 1 | A | Berger, *Statistical Decision Theory and Bayesian Analysis* (1985) | Screened | General Bayes-action foundation; retained as book-level reference |
| 2 | B | Rabiner, *A Tutorial on Hidden Markov Models...* (1989) | Detailed | Forward-backward and Viterbi distinction; retained |
| 3 | B/C | Holmes & Durbin, *Dynamic Programming Alignment Accuracy* (1998) | Detailed | Expected-accuracy structured decoder; retained |
| 4 | B/C | Kall et al., *An HMM Posterior Decoder...* (2005) | Detailed | Optimal-accuracy posterior label decoding; retained |
| 5 | B/C | Fariselli et al., *A New Decoding Algorithm for HMMs...* (2005) | Detailed | Posterior probabilities followed by legal-path DP; retained |
| 6 | B/C | Lember & Koloydenko, *Bridging Viterbi and Posterior Decoding* (2014) | Detailed | Generalized risk framework for admissible HMM paths; retained |
| 7 | C | Carvalho & Lawrence, *Centroid Estimation in Discrete High-Dimensional Spaces* (2008) | Detailed | Direct Hamming/centroid analogue; closest prior |
| 8 | C | Ding et al., *RNA Secondary Structure Prediction by Centroids...* (2005) | Screened | Ensemble centroid rather than MFE/MAP; retained |
| 9 | C | Do et al., *CONTRAfold* (2006) | Screened | Probabilistic RNA model with expected-accuracy decoding context; retained |
| 10 | C | Hamada et al., *Prediction of RNA Secondary Structure Using Generalized Centroid Estimators* (2009) | Detailed | Marginals plus constrained DP; closest prior |
| 11 | C | Hamada et al., *Generalized Centroid Estimators in Bioinformatics* (2011) | Screened | General framework and feasibility conditions; retained |
| 12 | D | McCaskill, *The Equilibrium Partition Function and Base Pair Binding Probabilities...* (1990) | Detailed | Exact ensemble marginals by inside/outside-style recursion; retained |
| 13 | D | Kschischang et al., *Factor Graphs and the Sum-Product Algorithm* (2001) | Screened | Classical exact tree marginals; retained |
| 14 | D | Darwiche, *A Differential Approach to Inference in Bayesian Networks* (2003) | Screened | Partition derivatives and all marginals; retained |
| 15 | E | Carlson & Eppstein, *The Weighted Maximum-Mean Subtree...* (2005) | Screened | Additive maximum subtree on a tree is linear; retained |
| 16 | F | Stoyanov et al., *Empirical Risk Minimization of Graphical Model Parameters...* (2011) | Detailed | Likelihood/inference/decision mismatch; retained |
| 17 | F | Kleijn & van der Vaart, *Misspecification in Infinite-Dimensional Bayesian Statistics* (2006) | Screened | Posterior may target a KL projection under misspecification; retained |
| 18 | F | Gneiting & Raftery, *Strictly Proper Scoring Rules, Prediction, and Estimation* (2007) | Screened | Calibration and loss-dependent point decisions; retained |

## Rejected or secondary-only items

- General neural MBR work for machine translation: modern but unnecessary for
  an exact finite structured posterior.
- Differentiable optimization and neural structured prediction: relevant only
  to future training, explicitly outside A1.5.
- Generic Bayesian-decision summaries and blogs: rejected in favor of primary
  papers and standard references.
- General-graph prize-collecting Steiner approximations: the input here is
  already a tree, where the additive problem is elementary and exact.

## Search conclusion

The proposed decoder is a direct constrained centroid/maximum-expected-accuracy
construction. No located paper studies AHSL's exact connected-support posterior,
but the decision-theoretic and algorithmic pattern is established prior art.
