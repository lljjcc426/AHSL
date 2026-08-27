# S3.0 Reality and Gold Audit

## Gold classes

- **A:** direct independent structural measurements.
- **B:** partial high-precision structural positives with assay-disjoint origin.
- **C:** indirect functional or downstream validation.
- **D:** synthetic planted structure.
- **E:** no structural validation.

## Findings

Projection papers often use real hypergraphs, but the partial observation is
manufactured by computing their graph projection. Their original hyperedges are
A-quality labels for a simulation of information loss, not evidence that the
real application supplies only `Y`.

Dynamics papers have genuinely natural `Y`. THIS explicitly notes that ground
truth is unavailable for its real EEG analysis; exact support recovery is shown
on synthetic dynamics. Biological plausibility of prefrontal hyperedges and
variance explained are C-quality, not structural gold.

CF-MS is genuinely indirect: proteins co-migrate in fractions and the complex
identity is not directly exposed. CORUM is high-precision manual literature
curation and excludes unvalidated high-throughput complexes, so it can be B
under a strict assay/publication-disjoint protocol. Current pipelines commonly
use CORUM-derived pairs for classifier training, thresholding, benchmark
refinement, or parameter tuning before evaluating complexes against CORUM.
Without provenance-level exclusions, independence is not established. Moreover,
unknown complexes are not negatives.

Pooled CRISPR measurements are natural, but guide assignments are decoded and
known; the latent object is an effect coefficient supported by the same assay.
External paralog/BioGRID positives are partial and predominantly pairwise.

Censored group and privacy-marginal settings have strong naturality but no
public paired full truth. A private/full dataset used to simulate censoring does
not turn the public observation mechanism into an independently validated
benchmark.

The minimum gold gate fails project-wide.
