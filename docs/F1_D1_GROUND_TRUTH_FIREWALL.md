# F1-D1 ground-truth firewall

Generation code may read vulnerable source, public metadata, original PoC/crash report, harness, compiler output, sanitizer output, public tests, and candidate-version traces. It may not read `*-patch.json`, human/fixed diffs, fixed source, fixed-container state, differential labels, or final evaluator labels.

The adapter projects raw AutoPatchBench metadata onto project, fuzzer, sanitizer, crash type, severity, patch-size descriptors, and stack-trace availability. Fields including `fix` and `fix_commit` are discarded and cannot enter agent context. Generation-path checks reject patch/fixed/ground-truth paths.

Instance 10445 was used while auditing the raw metadata schema and is marked ANALYSIS-EXPOSED. It cannot later re-enter unbiased Development. The actual ground-truth patch content was not read.
