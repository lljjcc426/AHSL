# META0：2025–2026 定向 prior-art 更新

日期：2026-08-28

本次只更新最强候选及其直接威胁，共使用 13 项新近 primary work/artifact，低于 30 项上限；没有重新做广泛主题搜索。

## 1. S1 因子微生物高阶交互

- Díaz-Colunga 等的 2026 eLife 正式版本构造 8 个 *Pseudomonas aeruginosa* strains 的全部 256 个组合，每个组合 3 个 biological replicates，并公开完整吸收谱和 OD600 biomass 数据及代码。这直接消除了旧 S1.0 “只有一个完整真实面板”的控制理由。[eLife](https://elifesciences.org/articles/101906)；[artifact](https://github.com/jdiazc9/full_factorial_design)
- Ishizawa 等的 2024 PNAS 七菌株面板仍是互补 benchmark：全部 127 个非空社区、按 focal strain 构造 64-cell landscape、每格 5–12 次测量。[DOI](https://doi.org/10.1073/pnas.2312396121)
- 2026 的 Adaptive Sparse Möbius Transform 给出 AND basis 下稀疏 Boolean polynomial 的 adaptive query 理论：FASMT 为 `O(sd log(n/d))` queries，PASMT 为 `O(sd^2 log(n/d))`。这是最接近的算法威胁，但其主张是精确稀疏函数/模拟超图恢复，不直接解决复制噪声、异方差、支持不确定性和微生物 FDR。[arXiv](https://arxiv.org/abs/2602.06246)

结论：任务没有被解决；数据条件明显变好。新颖性必须定位到“replicate-aware、uncertainty-controlled、部分测量下 order≥3 signed support recovery”，不能泛称 sparse Möbius learning。

## 2. fuzz-found vulnerability repair

- AutoPatchBench 提供 136 个真实 C/C++ fuzz-found vulnerabilities（Lite 113），突出 crash-stopping 与完整 fuzz/differential verification 的差距。[项目介绍](https://engineering.fb.com/2025/04/29/ai-research/autopatchbench-benchmark-ai-powered-security-fixes/)
- PatchEval 的 verified subset 现有 230 个容器化案例，形成更现代且语言更广的强评价路线。[artifact](https://github.com/bytedance/PatchEval)
- 2026 ContraFix 已用 differential runtime evidence、failure-boundary mutations 与 agentic patching，在 SEC-Bench 和 PatchEval 报告 84.0% 与 73.8%。这证明方向活跃，也直接占据最显然的“反例/差分证据驱动 agent”路线。[arXiv](https://arxiv.org/abs/2605.17450)

结论：应用和 venue ceiling 极高，但当前方法基线强、工程重、剩余失败异质，1–3 周杠杆不如 S1。

## 3. 语义约束模型合成

- CP-Bench 在 MiniZinc、CPMpy 与 OR-Tools CP-SAT 上提供多类组合问题和可执行正确性；documentation-rich prompt、重复采样与 self-verification 报告最高约 70%。[arXiv](https://arxiv.org/abs/2506.06052)
- CP-Agent 报告纯 agentic 路线解决 CP-Bench 的 101/101 问题，说明原 benchmark 可能已被 agent scaffold 饱和。[arXiv](https://arxiv.org/abs/2508.07468)
- CP-SynC 用多 agent 建模、合成 semantic checker、并行轨迹与 evidence aggregation，直接覆盖 META0 曾设想的明显干预。[arXiv](https://arxiv.org/abs/2605.01675)
- CP-SynC-XL 把评价扩到 100 问题、4577 instances，并显示“formalize 而非让 LLM 优化 search”的可辨机制。[arXiv](https://arxiv.org/abs/2605.12421)

结论：任务依旧真实，但要进入 Development 必须找到 CP-SynC/CP-Agent 之外的机制型错误子类，不能只做 prompting + solver feedback。

## 4. 超图分解理论

- 2026 Rerootable Hypertree Decompositions 是首次深入讨论 rerootability，并提出 relaxed normal form 与真正可重根的可处理类；实验显示 width increase 通常中等。[arXiv](https://arxiv.org/abs/2608.17853)
- 2024 branch-and-bound FHD 与已有 incremental GHD 工作继续压缩“把经典分解算法工程化”这一朴素空间。

结论：P1 的精确 rerootability 表述已被直接占据；canonical family representation、跨查询复用或可证明 dynamic maintenance 的较宽程序仍可研究，但必须重新定理化。

## 5. 递归查询执行

- Feldera/DBSP 当前实现已经覆盖递归 SQL、增量计算和 spill-to-disk 等生产特性；FlowLog 仍是强直接系统基线。[Feldera](https://github.com/feldera/feldera)

结论：旧 2× 阈值应撤销，但没有内部 state/work 归因时，现有 AP1.0 signal 更像系统表征而非尚未占据的贡献。

## 当前性结论

定向更新只使 S1 的可开发性显著上升。F1 的 benchmark 更好但 baseline 更强；E1 和 P1 的明显方法表述被新工作压缩；AP1.0 没出现足以改变机制判断的新空白。
