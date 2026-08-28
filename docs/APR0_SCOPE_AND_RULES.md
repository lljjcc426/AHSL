# AP-R0 scope and rules

Search date: 2026-08-27--28. Frozen base:
`fe9d56c830332c395f69fe86e2f4e1f29496e9c7`. This phase preserves P0-B,
AP0-A and AP1.0-C and implements no new research method.

## Decision rule

A parent direction requires a current public implementation, a reproducible
primary and independent secondary workload, a material residual reproduced
against the current practical baseline, a realistic mechanism and an open
nontrivial intervention. Scores never override G1--G14. The materiality default
was frozen before execution as at least 2x latency/memory/wasted work, at least
20 percentage points of objective correctness, or a comparable systematic
failure/timeout rate.

Artifact access, benchmark usability, executable residual and recent-prior-art
collision are evaluated before mechanism or method ideation. A benchmark-only
run is not residual evidence. An environment failure is not a research residual
when a standard setup or configuration removes it.

## Budgets and exclusions

- Pre-gate: at most 2 CPU-hours and 0.5 GPU-hours per candidate.
- Semifinal: at most 10 CPU-hours and 5 GPU-hours per candidate; at most three.
- Total: at most 30 CPU-hours and 10 GPU-hours.
- Actual AP-R0 execution: under 0.05 CPU-hours and 0 GPU-hours.
- No new model, scheduler, optimizer, repair algorithm, index, compiler pass or
  system architecture was created.
- AP0's failed recursive direction was not reopened through new datasets,
  Feldera/Linux work, distributed execution, GPU, ML scheduling or scale-up.

Permanent methodology rule: **literature-reported bottleneck is not a current
actionable residual**. Method development starts only after a current executable
residual survives fair configuration.
