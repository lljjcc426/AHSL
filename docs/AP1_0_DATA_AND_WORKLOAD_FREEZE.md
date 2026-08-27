# AP1.0 数据与工作负载冻结

统一随机种子为 `20260827`。正式结果生成后未修改查询规则。完整机器可读字段见 `results/ap1_0/raw/workload_metadata.csv` 和 `run_manifest.json`。

## Route A：FlowLog 递归查询路线

查询路线固定自 `flowlog-bench` 提交 `2db7c2eab9f64852242a1691b51707f3fb3454ff`（Apache-2.0）。为保证同引擎增量/重算对照，查询以当前 FlowLog 语法表示，语义输出固定如下。

| 工作负载 | 类别 | 规模 | 数据与预处理 | 更新 | 输出 |
|---|---|---|---|---|---|
| reachability | 集合递归/可达性 | small n=400；medium n=1500 | 固定种子稀疏有向图 | 6 批，现实均衡亚 1% churn；另有集中删除 stress | `Reach` |
| SSSP | 加权递归聚合 | small n=400 | 固定正整数边权 | 6 批均衡亚 1% churn | `Distance` |
| connected components | 递归聚合 | small n=400；medium n=1500 | 固定种子稀疏图 | 6 批现实均衡 churn；另有集中删除 stress | `Component` |
| Polonius subset | 真实程序分析 | 官方真实 fixture | 见下 | 6 批确定性局部 CFG/subset 变化 | `subset`、`loan_live_at`、`errors` |

图更新是合成的，但规则、种子、批次数、插入/删除计数均在运行清单和逐行结果中冻结。现实图场景使用小批混合更新；stress 只用于集中删除诊断，不作为 GO 的独立证据。

### Polonius 数据

- 仓库：<https://github.com/rust-lang/polonius>
- 提交：`d099f36b2c2d8ca531f994fbc2b555732962cbd6`
- 许可：Apache-2.0 OR MIT
- fixture：`inputs/vec-push-ref/nll-facts/foo1`
- 预处理：官方 tab facts 转为关系 CSV；不更改递归规则
- 更新性质：在真实 fixture 上合成确定性局部变化，因此是“真实基础数据 + 合成增量”，不是原生时间流

正式冻结前曾试跑更大的 `clap-rs` fixture；其单个 subset 差分输出约 55.8 MB，规范化成本会把本阶段变成 Python 适配器测试。该 pilot 被停止并在正式矩阵前改用上述官方小 fixture；正式结果不混入 pilot。

## Route B：LDBC 官方示例更新路线

- 仓库：<https://github.com/ldbc/ldbc_snb_example_data>
- 提交：`647eed01859e2115cb06e2a4bda98235943a308f`
- 许可：Apache-2.0
- 数据：官方 `Person_knows_Person.csv`，5 个 person 的 toy 数据
- 预处理：按时间字段形成 2010–2015 六个年度批次；将 Knows 解释为无向边；加入 person 删除级联
- 查询：最小、语义清晰的递归可达性
- 更新性质：从官方时间数据提取，属于 native temporal extraction
- 输出：`Reach`

该路线只证明官方变化图语义和删除链路可以接入，不是现实规模性能证据，也不被表述为 LDBC 标准递归 Datalog benchmark。
