# AP-R0 artifact audit

The raw ledger is `results/ap_r0/raw/artifact_metadata.csv`. Exact downloaded
commits were CP-Bench `92ba7dc197669e102dd8afa391da8abaa192f786`, TorchBench
`bee93389f6bb8c5222429117a1c901b633f32801`, and Hybrid-ANNS-Experiment
`ea97ba1c95a6c605abe798a5f5a8fdb30c690d7e`.

## Successfully installed/run

- PyTorch 2.13.0 official Windows wheel imported, but `torch.compile` failed
  first under default GBK decoding and then, with UTF-8 enabled, because `cl`
  was absent. The first failure is removable configuration; the second is a
  documented toolchain prerequisite, not evidence of an algorithmic gap.
- CP-Bench ground-truth CPMpy programs ran on CPMpy 0.9.25 and OR-Tools
  9.14.6206. This proves benchmark executability only.
- TorchBench source and Hybrid-ANNS scripts/README were inspected. Hybrid-ANNS
  requires separately hosted data and heterogeneous per-system environments,
  exceeding a useful two-hour pre-gate on this machine.

## Downgrades

AutomationBench, SWE-bench/SWE-bench Live, SAGA/TestGenEval, CP-Bench current
model comparison and AutoPatchBench require a current agent/model invocation.
Historical cached model outputs do not satisfy the currentness rule. AutoPatchBench
also requires dual Linux containers, fuzzing and LLDB-based differential checks.
These are real artifacts, but not bounded current executable baselines here.

No candidate is assigned AP-R0-D: artifact difficulty did not conceal an
otherwise gate-complete best candidate. In several cases the intervention space
was already crowded or official current evidence was negative.
