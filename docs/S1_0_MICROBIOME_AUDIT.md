# S1.0 microbiome audit

## Complete real panel

Ishizawa et al., *PNAS* 2024, DOI `10.1073/pnas.2312396121`, measures every nonempty subset of seven strains: `2^7-1=127` community systems. The public raw CFU table contains 2,377 measurements. For each focal strain, conditioning on its presence gives a complete `2^6=64` set-response landscape over the other six strains, with 5--12 independent flask measurements per cell.

This yields seven landscapes, not 127 iid learning tasks. The panel is a complete real truth/calibration panel; its small `p=6` per focal prevents treating it as a large ML benchmark.

## Exact expansion and labels

The audit applies exact Möbius inversion separately on raw and log10 CFU. Log10 is primary because the source paper finds a log-normal response treatment more appropriate. On log scale there are 294 order>=3 coefficients: 140 strong (74 positive, 66 negative) and 154 uncertain/null under the predeclared replicate bootstrap and magnitude rule.

Full data make the coefficient vector exactly computable from cell means; no learner is needed. Artificial masking is explicitly **retrospective measurement masking**: the hidden response was genuinely measured, and the full-panel coefficient remains evaluation truth.

## Heredity

Among 140 strong order>=3 log-scale effects:

- strong heredity: 22;
- weak-only heredity: 110;
- pure non-hereditary: 8;
- weak heredity satisfied: 132/140 = 94.29%;
- pure-HOI fraction: 8/140 = 5.71%.

The 95% diagnostic is narrowly missed, so pure effects are real but small. They do not support a broad non-hereditary-method claim on their own.

## Retrospective recovery

At budget 48 of 64 cells, averaged over seven focal landscapes and five masks, lasso reaches F1 0.235, AP 0.506, pure recall 0.425, and response RMSE 0.102 log10 CFU. OMP reaches F1 0.047, AP 0.479, pure recall 0.050, RMSE 0.115. A weak-heredity lasso post-filter reaches F1 0.218, AP 0.509, pure recall 0.350, RMSE 0.103. Full exact Möbius recovers the operational label by construction.

This is a genuine classical failure under masking, but evidence comes from one small biological system. It cannot by itself pass the two-domain gate.

## Adjacent compressed-sensing data

Arya et al. (*PNAS* 2023) use an order-weighted Walsh basis and compressed sensing on simulations plus four experimental panels, primarily assessing response recovery. This is close prior art and shows why prediction RMSE cannot substitute for direct support recovery.
