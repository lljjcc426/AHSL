# AP1.0 LDBC 范围审计

LDBC SNB Interactive v2 是变化图与复杂交互查询基准，不是专门的递归 Datalog 基准。AP1.0 只借用它的时间化边与删除语义，不宣称标准查询组合以递归为中心。基准背景参见 [LDBC SNB Interactive v2 论文](https://arxiv.org/abs/2307.04820) 与 [官方文档](https://ldbcouncil.org/ldbc_snb_docs/)。

## 实际采用范围

本机无法从公开托管路线取得完整可复现规模数据，因此采用官方 example-data 提交 `647eed01859e2115cb06e2a4bda98235943a308f`。从 `Person_knows_Person.csv` 按时间形成 2010–2015 六批更新，并对 person 删除执行 Knows 级联。递归查询是无向 Knows 上的最小可达性，没有把复杂 LDBC 查询扭曲成不自然的 Datalog 递归。

## 证据强度

这条路线有两个有效用途：验证第二公共数据路线可接入；验证 native temporal insertion/deletion 和精确结果对照。其 5-person 尺度不支持现实规模吞吐、内存或深删除性能结论。

该单元增量/重算速度比为 7.303，进程更新峰值比为 1.265，`p99/p50=2.688`。可观察输出变化/输入变化的中位数为 6.5、最大值为 9；由于图极小且没有内部 retraction/rederivation counter，这只是输出敏感度，不是内部删除放大机制。

因此 Route B 在语义与复现层面可用，在性能代表性上被明确降级。它不能单独支持 GO，也不与合成 reachability 合并计作两个递归类别。
