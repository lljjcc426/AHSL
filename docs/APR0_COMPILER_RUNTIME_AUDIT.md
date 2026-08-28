# AP-R0 compiler/runtime audit

## D1: dynamic-shape compilation

Problem: shape variation may cause recompilation, compile latency or slow
dynamic kernels. Current system: PyTorch 2.13; primary benchmark: TorchBench;
secondary route: vLLM-style models.

The planned same-system control was eager, default automatic dynamic behavior,
static specialization and the recommended annotation route. No performance
comparison was reached: the Windows CPU artifact first encountered a removable
locale issue and then required MSVC `cl`.

Currentness is decisive. PyTorch's [dynamic-shape documentation](https://docs.pytorch.org/docs/main/user_guide/torch_compiler/torch.compiler_dynamic_shapes.html)
states that automatic dynamic behavior is default and user annotations are
preferred; blanket `dynamic=True` is a testing option, not the universal
recommended mode. The March 2026 [performance-parity report](https://docs.pytorch.org/devlogs/dynamic_shapes/2026-03-25-unbacked-perf-parity/)
reports parity across all tested HuggingFace TorchBench and more than thirty
vLLM configurations. The February [compile-time report](https://docs.pytorch.org/devlogs/dynamic_shapes/2026-02-27-compile-time-unbacked-export/)
also documents a targeted 264 s to 87 s fix, while the June ShapesSpec work adds
declarative control.

Thus the literature pain is current engineering activity, but the proposed
broad parent residual is not established and much of the obvious intervention
space is already implemented. D1 fails G5, G6 and G10.

Generic autotuning was killed without execution: TVM/MetaSchedule, compiler cost
models and kernel search are mature; no new public workload-specific failure was
found that would make the contribution more than another cost model.
