# F1-D1 ContraFix collision audit

ContraFix (2026) is the strongest direct novelty threat. It mutates PoCs around a failure boundary, compares crashing and non-crashing runtime state, compiles the divergence into a repair specification, and reuses mutation/repair skills across instances. Its reported benchmark route is SEC-Bench/PatchEval rather than AutoPatchBench.

No official runnable repository was located in the bounded artifact search, so no unofficial implementation or performance number is used. The following are already occupied and cannot become F1 contributions: crash/non-crash variant generation, generic differential runtime evidence, repair-specification prompting, or reusable repair memories.

A full 8–15 work targeted audit is intentionally deferred. The protocol requires real AutoPatchBench failure concentration first; current evidence is exclusively F9 infrastructure. No intervention is promoted, so there is no candidate-specific novelty claim to audit.
