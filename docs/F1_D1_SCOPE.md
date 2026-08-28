# F1-D1 scope

F1-D1 studies fully verified repair of real fuzz-found C/C++ vulnerabilities. A successful patch must reach V4: it applies/builds, stops the original crash, survives benchmark fuzzing, and passes behavioral differential verification. Build success or crash stopping alone is not success.

The primary benchmark is AutoPatchBench-Lite. Development uses a project-disjoint pool; untouched instances cannot be evaluated. Same-backbone, equal-budget paired comparisons are mandatory before any mechanism claim. Ground-truth patches and fixed-program states are evaluator-only.

The present branch completes artifact freeze, environment audit, split construction, protocol implementation, and leakage tests. It does not contain a scientific baseline because the current host cannot run the required containers. F1 therefore remains at F1-D1-C rather than being falsely stopped or promoted.
