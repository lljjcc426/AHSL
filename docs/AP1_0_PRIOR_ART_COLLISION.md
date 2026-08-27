# AP1.0 既有工作碰撞审计

## 与本问题最直接的工作

1. [FlowLog](https://www.vldb.org/pvldb/vol19/p361-zhao.pdf) 已将 Datalog 编译到 Differential Dataflow，并在 planner 中共享 sub-plan/arrangement。一般性的“把递归查询做成差分增量”和“跨规则复用 arrangement”不是新机制。
2. [Differential Dataflow](https://github.com/TimelyDataflow/differential-dataflow) 已提供全增量 collection、iterate、arrangement/trace 与 compaction 基础。其 [diagnostics](https://github.com/TimelyDataflow/diagnostics) 已能直接观测 arrangement tuple 数及随输入累积/compaction 的变化。
3. Ammar 等人的 [Optimizing Differentially-Maintained Recursive Queries on Dynamic Graphs](https://arxiv.org/abs/2208.00273) 直接研究差分递归查询的高内存问题，并通过全部或部分丢弃 operator differences、需要时重算来降低内存。这与任何“保留差分历史过大→选择性重算”的直觉正面碰撞。
4. [DBSP](https://docs.feldera.com/vldb23.pdf) 已给出递归固定点的自动增量化和 nested-stream 状态分析，并明确讨论递归迭代历史带来的空间复杂度。
5. 经典 [DRed](https://doi.org/10.1145/170036.170066) 与 counting 系列已处理删除后的 over-deletion/rederivation；[Optimised Maintenance of Datalog Materialisations](https://doi.org/10.1609/aaai.v32i1.11554) 继续优化该路线。
6. [Fixing Incremental Computation: Derivatives of Fixpoints](https://arxiv.org/abs/1811.06069) 从固定点导数给出一般增量递归框架；递归聚合维护也已有长期数据库研究。

## 对 AP1.0 的含义

如果本阶段观测到明确的“差分历史占用过大且延迟恶化”，最直接的修复族已经有强先例；如果观测到删除重推导，DRed/counting 也已构成强碰撞。要进入 AP1.1，必须在这些机制之下留下更具体、跨类别、现实且当前系统尚未解决的残差。

本次没有形成这种候选：内部 arrangement/history bytes、retractions、rederivations 均不可得；最大进程峰值比低于 2；可观察输出删除放大仅在 LDBC toy 与 SSSP 上数值较高，且两者机制和证据强度不同。因此最终不是 AP1.0-F——不是“实证残差真实但已被 prior art 解决”，而是更早的材料性/归因门槛就未通过。
