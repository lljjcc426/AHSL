# A1.5 Literature Review

Search date: 2026-08-26

## Scope and gate conclusion

The focused review covers Bayes actions, Viterbi/MAP versus posterior decoding,
constrained minimum Bayes risk, exact posterior marginals, connected-subset
optimization, and posterior calibration under model mismatch.

The release gate is **GO**. A1.5 addresses a real decision-theory mismatch in
A1, and the proposed correction is mathematically valid and computationally
bounded. The gate does not imply novelty: posterior marginals followed by an
exact feasible-structure optimizer is established constrained-MBR/centroid
methodology.

## A. MAP, posterior decoding, and minimum Bayes risk

A Bayes action depends on its loss. MAP over a complete structure minimizes
posterior probability of choosing the wrong complete structure. Additive
Hamming loss instead separates by coordinates, so the unconstrained Bayes
action is a posterior coordinate median. Rabiner's classical HMM account and
the risk analysis of Lember and Koloydenko distinguish Viterbi path decoding
from positionwise minimum-error decoding. The distinction exactly matches
A1's MAP-support versus Hamming endpoint mismatch.

## B. Valid structured actions

Coordinatewise posterior decoding can violate a grammar or structural
constraint. Kall et al. optimize posterior label accuracy; Fariselli et al.
compute posterior state probabilities and then use a Viterbi-style step to
obtain a legal path. Holmes and Durbin similarly construct expected-accuracy
alignments by dynamic programming. These works show that legality should be
imposed in the Bayes-action optimization, not repaired afterward.

## C. Centroid and maximum-expected-accuracy estimators

Carvalho and Lawrence give the most direct theoretical precedent: under binary
Hamming distance, a centroid is determined by posterior component marginals,
subject to the predictive space. Ding et al. show why an ensemble centroid can
outperform the single minimum-energy/mode-like structure. Hamada et al. derive
generalized centroid estimators whose expected gain is an additive function of
posterior base-pair probabilities and optimize it over valid RNA structures by
DP. A1.5 is the connected-subtree instance of this construction.

## D. Exact posterior marginals

Kschischang, Frey, and Loeliger establish exact sum-product on cycle-free factor
graphs. McCaskill computes a partition function and all base-pair marginals by
paired forward/backward recursions. Darwiche shows the more general arithmetic-
circuit view: partial derivatives of a partition polynomial provide posterior
queries, and all derivatives can be obtained by reverse traversal. Therefore
reverse differentiation of A1's `O(m)` scorer is a classical, clean way to get
all node marginals in `O(m)` per row.

## E. Connected Bayes action

For Hamming risk, selecting node `j` changes expected loss by `1-2*pi_j`.
Minimizing risk over nonempty connected supports is thus a maximum additive-
weight connected-subtree problem with weight `2*pi_j-1`. Additive subtree
optimization on an input tree is a standard linear-time DP special case; A1's
frozen canonical DP already solves it.

## F. Calibration and likelihood/task mismatch

Stoyanov, Ropson, and Eisner explicitly analyze the full graphical-model
pipeline and show that likelihood, approximate inference, decoder, and task
loss may be misaligned. Gneiting and Raftery separate probabilistic forecast
quality from the loss-specific point action. Kleijn and van der Vaart show that
under misspecification a posterior concentrates near a KL projection, which
need not minimize a downstream task loss. These results explain why A1 could
improve noisy-data likelihood without improving clean Hamming.

## Loss selection for AHSL

Hamming remains appropriate for the current synthetic question because each
incidence error has equal declared cost and partial recovery is scientifically
credited. Exact-support loss would discard partial correctness. A real
application could instead require asymmetric false-positive/false-negative
costs, F-score-like utilities, or downstream query/inference loss; each would
have a different Bayes action. A1.5 does not change the preregistered loss.

## Novelty and stop assessment

No direct paper was found for noisy AHSL incidence rows with connected-support
posterior risk. Nonetheless, the abstract decoder is substantially covered by
centroid, MEA, posterior-decoding, and sum-product literature. A1.5 should be
reported as a decision-aligned empirical audit, not as a new decoder family.
