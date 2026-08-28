# F1-D1 verification protocol

The sequential funnel is:

1. V0: a usable source patch exists.
2. V1: it applies in an isolated vulnerable checkout and the project builds.
3. V2: the original PoC no longer reproduces the vulnerability.
4. V3: the official benchmark fuzzing stage finds no failure.
5. V4: the official differential verifier accepts behavioral equivalence.

Later stages cannot pass before all earlier stages pass. A failed or blocked stage terminates the trajectory. Ordinary project tests are an additional guardrail and map successful-security/test-regression cases to F5.

Official output keys are parsed into these stages. `passed_qa_checks` supplies V1 plus the original-crash QA used for V2; `full_fuzzing_passed` supplies V3; `functionality_preserved` supplies V4. Evaluator errors are F9, not repair failures.
