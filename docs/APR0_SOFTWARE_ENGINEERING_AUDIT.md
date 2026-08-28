# AP-R0 software-engineering audit

The family is attractive because correctness is executable and workloads are
real repositories. Current resources screened in depth included SWE-bench and
its live variants, SAGA, TestGenEval, Vero, RepoExec, Nemotron-CORTEXA and
AutoPatchBench.

## Candidate C1: repository-level test generation

Problem: generated patches/tests can execute yet miss the intended behavior.
Current systems/benchmarks: SAGA, TestGenEval and Vero. The measurable target is
test validity plus fault detection or repository test outcomes, not code-token
accuracy. Current inference requires a model/API and often repository containers;
no current strong baseline was run here. Therefore G5 is not established.

## Candidate C2: incremental program analysis

Problem: repository-scale changes can force expensive recomputation or lose
precision. Public systems exist, but the audit did not identify a 2025--2026
accepted benchmark exposing a material current same-system residual plus an
independent workload. Caching/demand-driven/incremental analyses are extensive
prior art. This route fails G3/G5/G9 before implementation.

## Security boundary

Fuzz-found repair was moved to optional family F because its benchmark contract
includes crash reproduction, fuzzing and behavioral differential verification.
It is stronger than ordinary pass/fail repair but has a larger container and
model burden.
