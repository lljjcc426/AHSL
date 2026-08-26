# A1.5 Closest Prior Art

## 1. Carvalho and Lawrence (2008): centroid estimation

- **Problem:** choose a representative point in a large discrete posterior
  space rather than its mode.
- **Posterior object:** a distribution on high-dimensional binary structures.
- **Loss/action:** centroid under Hamming-type distance; coordinate consensus is
  the unconstrained solution, with feasibility results for important constraint
  families.
- **Algorithm:** compute component marginals and construct a feasible centroid.
- **Relationship to A1.5:** this is the closest decision-theory analogue. AHSL's
  `2*pi-1` weights are exactly the binary centroid/Hamming algebra.
- **Difference:** AHSL's feasible family is all nonempty connected subsets of a
  fixed tree, for which coordinate thresholding need not remain feasible.
- **Overlap risk:** decisive against novelty claims for posterior centroid or
  marginal-based Hamming decisions.

## 2. Hamada et al. (2009): generalized centroid RNA decoding

- **Problem:** predict a valid RNA secondary structure from a posterior ensemble.
- **Posterior object:** base-pairing marginals computed from a probabilistic or
  thermodynamic structure distribution.
- **Loss/action:** maximize expected weighted accuracy (`gamma`-centroid).
- **Algorithm:** transform posterior marginals into additive local scores and
  run a dynamic program over the legal RNA structure space.
- **Relationship to A1.5:** same construction at the abstract level: posterior
  marginals, additive expected gain, then exact constrained DP.
- **Difference:** RNA feasibility is noncrossing base-pair structure; AHSL
  feasibility is a nonempty connected node set of a given tree.
- **Overlap risk:** high. The connected-tree DP is a different feasible-set
  solver, not a new MBR principle.

## 3. Lember and Koloydenko (2014): risk-based HMM decoding

- **Problem:** distinguish and interpolate Viterbi/MAP path decoding and
  symbolwise posterior decoding while retaining admissible HMM paths.
- **Posterior object:** hidden-path and positionwise posterior probabilities.
- **Loss/action:** generalized posterior risks that include pathwise and
  symbolwise error.
- **Algorithm:** forward-backward posterior computation plus dynamic programs
  over admissible paths.
- **Relationship to A1.5:** establishes that MAP-path and minimum-symbol-error
  decisions answer different losses, and that constrained risk minimization is
  the correct way to preserve output validity.
- **Difference:** admissible sequences are HMM paths; AHSL outputs are connected
  supports on a fixed undirected tree.
- **Overlap risk:** high for any claim that valid structured posterior decoding
  under Hamming-like risk is new.

## Supporting algorithmic references

- Kschischang et al. (2001): sum-product on trees supplies exact marginals.
- Darwiche (2003): derivatives of an arithmetic circuit/partition polynomial
  supply posterior queries by reverse differentiation.
- Carlson and Eppstein (2005): additive maximum-subtree optimization on a tree
  is a standard linear-time special case.

## Novelty assessment

A1.5 is an internal scientific correction and kill-test. Its defensible value
is empirical: determining whether A1's negative tree-selection result was an
artifact of using a MAP action with a Hamming endpoint. It is not a novel MBR
method.
