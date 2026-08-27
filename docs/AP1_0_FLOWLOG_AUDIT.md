# AP1.0 FlowLog 实现审计

冻结对象：<https://github.com/flowlog-rs/flowlog>，提交 `6c111b729e4bf8bffb5037b85b894031786140cc`。论文为 [FlowLog: Efficient and Extensible Datalog via Incrementality](https://www.vldb.org/pvldb/vol19/p361-zhao.pdf)。

## 编译管线与 IR

FlowLog 不是把文本规则直接解释执行。实现经过 parser、类型检查、stratifier、planner、关系/规则 IR 与 Rust codegen。递归规则被划入共同迭代的 stratum，并生成 Differential Dataflow 的 `Variable`/iterate 反馈结构。查询程序最后生成独立的 Rust executable。

## 增量与删除语义

生成程序以 Differential Dataflow collection 表示关系。当前 Datalog 模式使用 `i32` difference 追踪 multiplicity；输入事务把插入表示为正 diff，把删除表示为负 diff。`datalog-inc` 在 epoch/transaction 边界推进并发布每 epoch 输出差分；本实验累积这些差分后与 `datalog-batch` 当前快照精确比较。

## arrangement、索引与已有优化

planner 会把规则降为 Differential Dataflow plan，并通过 content-canonical materialization 跨规则共享 arrangement/sub-plan。join、anti-join、threshold/reduce 和递归变量依赖 DD 的 arrangement/trace 实现；当前依赖为 DD 0.25.1、Timely 0.31.0。因而“简单地跨规则共享重复索引”已经不是空白机制。

FlowLog profiler 能输出计划图、operator/channel tuple flow，并识别 arrangement 产生者。正式运行生成了逐 transaction profiler 文件，但现有输出没有直接给出可靠的逐批 maintained-state bytes；本阶段未改造 profiler，也没有把 RSS 转译为 arrangement 大小。

## 聚合与递归

SSSP 与 connected-components 查询通过递归 reduce/min 路径执行。实现对 arrangement 和 threshold/reduce 有专门 codegen 及 operator-accounting；stratum 内规则共同迭代到固定点。此次测量没有发现这两类聚合形成材料性内部残差：最接近门槛的是 medium connected-components 的 1.969 倍进程更新峰值比，但增量仍快 4.253 倍，增量进程内 retained growth 中位数仅 0.984 MiB，且没有内部 state counter 支持 arrangement 归因。

## worker 模型

生成程序由 Timely workers 并行执行；输入文件按 worker 分片，事务由协调逻辑统一提交。1→4 worker 小型诊断中，reachability 延迟由 7.43 ms 降到 6.27 ms、post RSS 由 11.42 MiB 升到 13.44 MiB；connected-components 延迟由 11.52 ms 降到 11.26 ms、post RSS 由 14.45 MiB 升到 17.47 MiB。方向是小幅延迟改善伴随固定并行开销，没有出现调度崩溃。

## 与新颖性的关系

FlowLog 自身公开结果已报告：在 DOOP 上相对 Soufflé 有显著速度优势，同时可能使用更多内存。这说明一般性的“速度—内存权衡”不是新问题。AP1.0 需要更窄的、跨类别和可因果归因的内部残差；本矩阵没有提供该证据。
