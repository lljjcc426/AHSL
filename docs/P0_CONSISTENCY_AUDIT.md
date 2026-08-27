# P0 consistency and reproducibility audit

## Documentation findings

1. **A1 neural kill-rule label:** `kill_neural_rule_met=False` is numerically
   consistent with the preregistered rule because the marginal estimator did
   not make the residual small. It does not mean neural work was authorized.
   The independent continuation condition failed because marginal likelihood
   did not improve downstream recovery and real covariates were absent. No
   historical correction is required.
2. **A1.5 Decision B:** the code is internally consistent: tree-identity
   learning stops while posterior-decision modeling retains a positive signal.
   B0 then closes implementation due to the real-task gate.
3. **S1.0 label:** the primary failure is estimand/identifiability and
   cross-domain truth, not Dango reproducibility. Missing Dango inputs are an
   engineering issue but do not control the decision.
4. **S2.0 label:** prior-art saturation is supported by HyperSearch; local zero
   novel recall alone cannot establish model inferiority because candidate
   recall is below 1%.
5. **S3.0 label:** classical/latent-model saturation is narrower and more
   accurate than claiming all natural observation mechanisms are artificial.
6. **R0 width terminology:** locally reported induced widths are heuristic
   upper bounds. No exact GHW/FHW is claimed. This is consistent.
7. **Candidate counts:** S1.0 has four scored candidates and zero finalists;
   S2.0 five and zero survivors; S3.0 six and zero semifinalists/finalists; R0
   six and zero semifinalists/finalists. Reports are internally consistent.

## Git/reproducibility findings

- Every frozen phase in the required history map has a local and remote branch.
- Downloaded/external N1.0, S2.0 and R0 data are ignored by Git; source ledgers
  are tracked where supplied.
- A0--A1.5, N1.0, S1.0, S2.0 and R0 include executable code/tests appropriate to
  their phase. Documentation-only gates correctly avoid inventing experiments.
- The repository has no `.github` workflow. All reported tests are local; no
  report should imply GitHub Actions or external CI success.
- P0 adds documentation only and does not rerun expensive historical studies.

## Corrections made

No frozen historical report was edited. P0 resolves apparent ambiguity by
recording narrower interpretations in new documents. There is no concrete
documented error strong enough to rewrite a prior scientific decision.
