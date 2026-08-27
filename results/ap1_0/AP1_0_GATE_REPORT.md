# AP1.0 Recursive Incremental State–Latency Residual Gate

实验日期：2026-08-27。冻结基线：`f9ac16f418e34a5d130adeb332374493ff254332`。

## 1. Executive decision

**决定：AP1.0-C — NO-GO: MODERN SYSTEMS CLOSE THE RESIDUAL。** 主残差类为 **R7 — NO ACTIONABLE RESIDUAL**。

该措辞严格绑定本轮覆盖：FlowLog 是唯一成功执行完整同引擎矩阵的主系统；Feldera/DBSP 只有冻结实现审计。FlowLog 的 11 个 workload × regime × scale × workers 单元中，增量均比同引擎重算快 2.560–8.953 倍，最大更新峰值 working-set 比为 1.969 倍，未达到 2 倍内存门槛；没有内部 maintained-state/work counter 支持 R1–R6 归因。不存在足以授权 AP1.1 的跨类别现实残差。

## 2. Frozen systems and versions

FlowLog：提交 `6c111b729e4bf8bffb5037b85b894031786140cc`；compiler 0.5.0、runtime 0.3.0、build 0.4.0；Rust 1.89.0；Differential Dataflow 0.25.1；Timely 0.31.0；release/locked/profiled。

Feldera/DBSP：`v0.338.0`，提交 `718320cf1deb49c51f8528f2469fbfc7aac995db`，Rust 1.93.1；native Windows 构建被 `feldera-samply` 的 Unix `nix` API 阻塞，未产生性能数据。可选第三系统未加入。

机器：ASUS TUF Gaming F15 FX507VV，i9-13900H（14C/20T），31.64 GiB RAM，Windows 11 10.0.26200 x64。GPU 为 0。

## 3. Workloads and datasets

成功运行五个查询、四个递归类别：

- reachability：small/medium 合成稀疏图；
- SSSP：small 正权图，加权递归聚合；
- connected components：small/medium，递归聚合；
- Polonius subset：官方 `vec-push-ref/foo1` fixture 上的真实程序分析递归；
- LDBC reachability：官方 5-person example-data 的时间化 Knows 子集。

Route A 查询路线冻结在 flowlog-bench `2db7c2e...`；Polonius 数据冻结在 `d099f36...`；LDBC example-data 冻结在 `647eed0...`。统一种子 `20260827`。

## 4. Exact semantics / correctness

增量输出按 epoch 的正负 diff 累积为当前关系；同批当前数据库由 FlowLog `datalog-batch` fresh process 重算。所有集合与整数聚合输出均规范化后逐行精确比较。

原始行 276，计量行 230，`all_correct=true`；无正确性失败。性能结果不包含冻结前中止的 pilot。

## 5. Realistic update regimes

合成图的 `realistic_mixed` 是每批平衡插入/删除、占基础图不足 1% 的小 churn；Polonius 是真实 fixture 上的确定性局部 CFG/subset 变化；LDBC 是由官方时间字段提取的 2010–2015 更新。

现实单元覆盖 reachability、SSSP、connected-components、program analysis，并保留每批数据。没有现实单元出现内部可归因的材料性残差。

## 6. Stress regimes

对 small reachability 与 small connected-components 执行集中删除 `delete_heavy_stress`。前者增量/重算速度比 4.571×、峰值比 1.302×；后者分别为 2.560×、1.522×。无超时、OOM 或精确性失败。stress 没有产生可独立支持 GO 的效应。

## 7. Same-engine scratch controls

所有执行比较均为 FlowLog `datalog-inc` vs FlowLog `datalog-batch`，使用相同解析器、程序、runtime、数据、worker 数和硬件。每批 batch-mode 从当前快照重算精确结果。

| 单元 | 重算/增量延迟 |
|---|---:|
| reachability medium realistic w1 | 8.953× |
| LDBC toy native temporal w1 | 7.303× |
| reachability small realistic w1 | 6.145× |
| SSSP small realistic w1 | 4.787× |
| connected-components medium realistic w1 | 4.253× |
| Polonius real realistic w1 | 3.785× |
| connected-components small delete stress w1 | 2.560× |

其余单元也全部大于 1。没有“增量比重算慢”的单元；最弱速度优势仍为 2.560×。

## 8. Initial load costs

初始化与更新分开记录。所有正式计量行的 FlowLog incremental `initial_ms` 中位数为 17.967 ms，batch control 为 2.659 ms；这是运行模式的初始化阶段差异，不与 `T_update` 混合。

查询生成/编译按模式约 76–95 秒：CC 76.282/84.730 秒、LDBC 79.576/86.565 秒、Polonius 84.144/94.989 秒、SSSP 82.887/94.880 秒。reachability 的两个已完成编译发生在旧 duration parser 于元数据落盘前中止的 pilot，故正式 CSV 写 `NA`，没有为非核心字段重复编译。

## 9. Steady retained state

FlowLog 内部 maintained-state bytes 不可得，因此真正的 steady-state state amplification 为 `NA`。进程内 `M_post-M_steady` 的中位/最大值为：medium CC 0.984/2.699 MiB，SSSP 0.816/0.949 MiB，Polonius 0.543/0.723 MiB，medium reachability 0.387/0.418 MiB。

五个 measured batches 上没有持续单调增长证据。`M_inc_post/M_recompute_post` 最大 6.384×，但 batch process 的退出前最后采样偏低，不能被称为 maintained-state amplification。

## 10. Update peak memory

最大 FlowLog 引擎 working set 为 23.703 MiB。按同一单元的中位 `M_update_peak`，增量/重算最大比值为 medium connected-components 的 1.969×；其次是 small CC delete stress 1.522×、small CC realistic 1.493×。其余单元为 1.265–1.454×。

没有单元达到预设 2× 更新峰值门槛。该指标仍是 OS working set，不被解释为 arrangement 或 differential history 字节数。

## 11. p50/p95/p99 latency

代表性 FlowLog incremental 结果：

| 单元 | p50 ms | p95 ms | p99 ms | p99/p50 |
|---|---:|---:|---:|---:|
| CC medium realistic | 15.061 | 43.367 | 45.405 | 3.015 |
| reachability medium realistic | 3.142 | 7.408 | 9.181 | 2.922 |
| LDBC toy temporal | 3.898 | 10.398 | 10.480 | 2.688 |
| reachability small realistic | 7.431 | 14.299 | 14.578 | 1.962 |
| Polonius real realistic | 8.905 | 12.480 | 12.493 | 1.403 |
| SSSP small realistic | 6.105 | 7.509 | 7.713 | 1.263 |

三个单元自身 `p99/p50` 超过 2，但这不是相对策略的 p99 恶化；其 incremental p99 均低于相应 recompute p99。每个关键单元只有 15 个计量点，因此只把它作为粗粒度尾部诊断。

## 12. Throughput

逐行 throughput 为 `(|insert|+|delete|)/T_update`。所有计量行的描述性中位数为 incremental 1570.5 changes/s、recompute 352.1 changes/s；该跨单元数只用于检查量级，不作为综合排名或决策分数。科学判断仍按 cell 分开。

## 13. Delete/retraction amplification

内部 differential tuples、retractions 和 re-derivations 不可得，CSV 对应字段均为 `NA`。可观察输出 diff 单独存入 `observed_output_changes`/`observed_output_retractions`，不与内部工作混用。

输出变化/输入变化的最大值：LDBC toy 9×（中位 6.5×），SSSP 3×（中位 1.375×），reachability delete stress 0.2×（中位 0.086×）。LDBC 图只有 5 人，SSSP 只有一次完整重复；二者不能组成同一内部删除机制的跨类别证据。

## 14. State amplification

定义要求 maintained physical/logical state 除以当前输出或相关 base size。FlowLog 正式接口未给出逐批 physical state/arrangement bytes，所以该量为 `NOT AVAILABLE`。本报告没有用 RSS、output cardinality 或 profiler operator flow 猜测它；因此没有生成误导性的 state-amplification 图，改为展示 `retained_growth.png`。

## 15. Recursion-shape analysis

线性集合递归、加权 min 聚合、标签/分量递归聚合和多关系程序分析递归均被覆盖。最接近 2× 峰值的是 medium CC，而 reachability、SSSP 与 Polonius 明显更低；没有同一失效机制沿“集合→聚合→程序分析”结构重复。尾部离散也没有与单一 recursion shape 稳定对应。

## 16. Parallelism diagnostic

small realistic 的 1→4 worker 干预结果：

- reachability：中位更新 7.431→6.267 ms；post RSS 11.422→13.441 MiB；
- connected-components：11.520→11.256 ms；post RSS 14.453→17.469 MiB。

多 worker 带来固定内存成本，延迟没有按预测方向恶化。结果不支持 parallel/frontier scheduling collapse。

## 17. FlowLog-specific findings

FlowLog 经 typed/stratified relational IR、planner 与 codegen 生成 DD executable；递归 stratum 使用 DD iterate/Variable；输入以 `i32` diff 表达插入和删除；planner 已跨规则共享 content-canonical arrangement。现有 profiler 能识别 operator/channel flow，但本轮日志没有逐批内部 state bytes。

系统自身已有 arrangement sharing、DD trace/compaction 基础和 profiling。一般性的“复用索引”或“差分状态换时间”不是空白机制。

## 18. Feldera/DBSP-specific findings

DBSP 用 Z-set 权重表达增删，通过 circuit derivatives 和 nested streams 增量化递归固定点；论文明确指出缓存固定点迭代变化会带来与内层迭代数相关的空间。冻结实现包含 batch、trace、merge/consolidation 和存储机制。

本机 native Windows 构建在 `feldera-samply` 的 Unix API 停止；WSL 服务不可用。因此没有 Feldera 性能数据，只有源码/论文审计。该事实限制外推，但不是 R1–R6 的实证。

## 19. Cross-engine comparison

没有公平的 FlowLog-vs-Feldera 性能比较，故该问题为 `NOT AVAILABLE`。这符合“跨引擎比较次要”的设计，也避免把平台构建差异错归因于增量状态设计。当前最强且实际运行的系统是 FlowLog。

## 20. Cross-workload residual

没有同一材料性内部机制出现在两个不同类别。medium CC 的峰值比 1.969× 未过阈值；LDBC/SSSP 的输出差分放大不是内部 work，且类别与重复证据不支持统一归因；自身 p99/p50 离散没有相对重算恶化。因此 cross-workload hard gate 失败。

## 21. Realistic-vs-stress comparison

现实混合单元无材料性内部残差；集中删除 stress 也未制造 timeout/OOM 或 2× 峰值。结果不是“只在 stress 中出现”的 AP1.0-D，而是材料性候选本身没有形成。

## 22. Mechanism attribution

`STATE_RETENTION`：缺少内部 state bytes，且峰值未过 2×。`RETRACTION_PROPAGATION/REDERIVATION`：缺少内部 counters。`ARRANGEMENT_DUPLICATION`：FlowLog 已共享 arrangement，且无大小证据。`FRONTIER_SCHEDULING/PARALLEL_GRANULARITY`：worker 干预不支持。`RECURSIVE_AGGREGATION`：medium CC 接近门槛但未过，SSSP 更弱。

所以不能诚实选择 R1–R6，主类为 R7。

## 23. Causal micro-diagnostics

执行了两类小干预：1→4 workers，以及 realistic mixed→delete-heavy stress。前者没有导致预测的调度延迟恶化，后者没有导致删除传播的材料性内存/延迟崩溃。两项都是否定性归因结果，没有实现新算法。

## 24. Prior-art collision

最强碰撞是 [Ammar et al.](https://arxiv.org/abs/2208.00273)：它直接针对差分维护递归图查询的高内存，用选择性丢弃 operator differences 并按需重算降低状态。FlowLog 已有 arrangement sharing；Differential Dataflow 已有 trace/compaction 与 arrangement diagnostics；DBSP 已分析 nested fixed-point state；DRed/counting 已覆盖删除重推导。

由于本轮连可归因实证残差都未建立，最终不是“残差真实但被既有工作解决”的 F，而是 C。

## 25. Strongest evidence FOR continuation

唯一接近材料性的单元是 medium connected-components realistic：增量更新峰值/重算峰值 1.969×，自身 `p99/p50=3.015×`，进程内 retained growth 最大 2.699 MiB。LDBC toy 的输出变化/输入变化最大 9×。这些量说明未来若有独立新证据，应优先检查递归聚合 state 与删除历史，而不是盲目扩大矩阵。

但上述第一项低于阈值，第二项不是相对策略恶化，第三项是 toy 输出量，均不满足 AP1.0 GO。

## 26. Strongest evidence AGAINST continuation

最强反证是：五个查询、四个递归类别、现实与删除 stress、1/4 worker 共 230 个计量行全部精确；所有 11 个单元增量都比同引擎重算快至少 2.560×；最大更新峰值比仅 1.969×；没有 timeout/OOM；内部机制 counters 不支持任何 R1–R6；worker 与删除干预均未把候选推向预测方向。

继续增加系统/数据会变成寻找性挖掘，不符合 bounded kill-test。

## 27. G1-G10 table

| Gate | 状态 | 证据 |
|---|---|---|
| G1 exact correctness | PASS | 276/276 原始行正确 |
| G2 >=2× material residual | FAIL | 合法峰值最大 1.969×；无内部 work/state 2× |
| G3 same mechanism in >=2 classes | FAIL | 无候选机制 |
| G4 realistic residual | FAIL | 现实单元无可归因材料效应 |
| G5 internal and actionable | FAIL | 内部 counters 不可得且干预不支持 |
| G6 causal diagnostic | FAIL | 两类干预均否定候选归因 |
| G7 strongest system does not solve it | FAIL/NA | 没有先建立待解决残差 |
| G8 primary and secondary routes usable | PASS with limitation | Route A 完整；Route B 仅 toy 语义证据 |
| G9 focused fix in one engine | FAIL | 无可聚焦机制 |
| G10 algorithmic/systemic contribution | FAIL | 余下问题是访问/观测工程，不是已证实算法残差 |

AP1.0-A 要求全部通过，故不能 GO。

## 28. Final decision

**AP1.0-C — NO-GO: MODERN SYSTEMS CLOSE THE RESIDUAL。** 精确含义是：冻结的强 FlowLog 系统和本轮证据路线没有显示可行动的跨类别现实残差。主类：**R7 — NO ACTIONABLE RESIDUAL**。

不选 B：没有“潜在强残差仅被系统访问阻塞”。不选 D：并非只在 stress 才有残差，而是没有合法候选。不选 E：Feldera 构建虽属工程问题，但不控制科学结论。不选 F：prior art 很强，但材料性与归因门槛先失败。

## 29. Exact next action

停止该具体执行算法方向，不创建 AP1.1 proposal。将本分支、原始数据、审计与 NO-GO 报告提交 GitHub，返回项目级评审；不得通过新增 GPU、分布式、ML、更多图数据或新语言来绕过本 kill-test。

本阶段没有实现任何新算法，也没有使用 ML/AI。
