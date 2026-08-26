# S1.0 publication feasibility

## General cross-domain paper

Not currently feasible. A defensible abstract would need two real domains with direct order>=3 truth, strict splits, and a residual beyond exact contrasts plus tuned sparse recovery. Only the microbial panel supplies clean full truth for incomplete-measurement calibration, and it contains seven dependent `p=6` landscapes.

## Domain-specific options

- Yeast: a computational-biology paper would need new experimental validation or a statistically explicit latent-label model. Without that, an additional PPI/embedding predictor is too close to Dango.
- Microbiome: the 127-system panel can support a careful methods note or benchmark audit, but its size and the Arya compressed-sensing collision limit a standalone general ML claim.
- Drug: context-dependent interaction analysis is scientifically important, but eight drugs and 182 sets are too small for a broadly learned shared-support claim. A larger prospective multi-dose panel could change this.

## Theory ceiling

Potential theorem classes—FDR control for noisy factorial contrasts, support identifiability with missing lower subsets, or context-shared support consistency—are nontrivial. The current data do not provide the necessary two-domain evaluation interface. Theory possibility alone is not a reason to proceed to model development.

## Compute and reproducibility

The completed audits are CPU-light. Dango's code is public and the local GPU could run a reduced one-process setup, but the exact preprocessing path references two absent inputs. Substituting reconstructed features would no longer be exact reproduction. Compute is therefore not the decisive no-go reason.
