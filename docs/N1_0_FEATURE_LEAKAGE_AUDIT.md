# N1.0 feature leakage audit

No feature model was trained. This audit fixes what could and could not be used if a future phase were authorized.

| Candidate feature | Status | Reason |
|---|---|---|
| reaction/event type available in the historical release | SAFE | graph-local and known at prediction time |
| tail/head arity; direct positive-regulator flag | SAFE | native historical incidence |
| compartment and physical-entity state | SAFE | preserved release-specific BioPAX attributes |
| local degree/connectivity computed on historical release | SAFE | allowed only with split-time graph isolation |
| biochemical class already present in historical release | SAFE | no later annotation required |
| broad provenance/evidence counts | RISKY | annotation effort may proxy pathway/family membership |
| pathway hierarchy or pathway name as a reaction feature | TARGET_LEAKAGE | directly reveals label/group annotation |
| stable reaction ID embedding or per-ID free parameter | TARGET_LEAKAGE | memorizes recurring reactions across tasks |
| gold pathway membership or gold-derived internal source | TARGET_LEAKAGE | contains the answer |
| V97 attributes/features for a V89 example | TEMPORAL_LEAKAGE | violates historical availability |
| free text, gene/protein embeddings, external omics | UNVERIFIED | release timing, entity overlap, and provenance not audited |

Family names are permitted only to define a holdout group. Query-visible boundary sources and targets are inputs by task definition, not hidden features; using internal gold nodes beyond those declared endpoints is prohibited.

Historical isolation tests verify that task construction is deterministic and V89 objects are built only from the V89 snapshot. The later V97 snapshot is used solely for the NEW/MODIFIED/UNCHANGED comparison.
