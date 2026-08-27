# AP1.0 机制归因

## 观测与候选

| 观测 | 最大值/代表值 | 是否材料 | 能否归因 |
|---|---:|---|---|
| 增量/重算更新峰值 RSS 比 | 1.969×，medium CC | 否，低于 2× | 否；RSS 不是内部 state bytes |
| 增量进程内 retained growth | 最大 2.699 MiB，medium CC | 否 | 仅进程诊断 |
| 增量 `p99/p50` | 3.015×，medium CC | 有离散尾部 | 否；增量 p99 仍低于重算 p99，样本短 |
| 输出变化/输入变化 | 最大 9×，LDBC toy | 数值超过 2 | 否；是 5-person 输出敏感度，不是内部 retraction work |
| 超时/OOM | 0 | 否 | 不适用 |

`M_inc_post/M_recompute_post` 最大 6.384×，但 batch-mode 的 `M_post` 是短生命周期进程退出前最后采样，分母可被 teardown 压低。它不满足 state-specific audit 对 maintained physical/logical state 的定义，故不用于材料性结论。

## 分类别结论

- Reachability：medium 现实混合速度比 8.953×，更新峰值比 1.348×，retained growth 中位 0.387 MiB。没有状态残差。
- Recursive aggregate：medium connected-components 是最接近门槛的单元，速度比 4.253×、峰值比 1.969×、retained growth 中位 0.984 MiB；没有越过阈值，也没有 arrangement counter 支持机制归因。
- Weighted aggregate：SSSP 速度比 4.787×、峰值比 1.316×。输出差分放大最大 3×，但只有一次探索重复且不是内部工作量。
- Program analysis：Polonius 速度比 3.785×、峰值比 1.340×、retained growth 中位 0.543 MiB；没有跨到材料区。
- LDBC toy：速度比 7.303×、峰值比 1.265×。输出放大高但规模与内部计数均不支持算法归因。

## 小型因果诊断

对最重要的 reachability 与 connected-components small realistic cells 将 worker 从 1 改为 4。预测若主要问题是 parallel/frontier scheduling collapse，多 worker 应显著恶化更新延迟或尾部。实际中位更新延迟分别改善约 15.6% 和 2.3%，post RSS 分别增加约 17.7% 和 20.9%。这是常规并行固定开销，没有支持 `PARALLEL_GRANULARITY` 或 `FRONTIER_SCHEDULING` 残差。

删除 stress 与现实混合对照也未支持 deletion mechanism：两类查询的增量仍快于重算 2.560–4.571×，峰值比分别为 1.522 和 1.302，且没有超时/OOM。

## 最终归因

不能把任何观测可靠归入 R1–R6。唯一符合证据强度的主类是 `R7 NO ACTIONABLE RESIDUAL`。这不是“增量系统已被普遍解决”的结论，而是说本阶段没有测出足以进入机制开发的残差。
