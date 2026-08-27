# AP1.0 工作负载分类

| 工作负载 | 递归形态 | 单调性/更新 | 代数 | 拓扑 | 前沿/深度 | 证据角色 |
|---|---|---|---|---|---|---|
| reachability | 线性递归 | 插入单调；删除需撤回 | 集合 | path-like + branching | 中高扩张、可深 | 基础集合递归，小/中规模与删除 stress |
| SSSP | 线性递归 | 聚合结果可因增删改变 | min 聚合 | path-like | 深度依赖路径长度 | 加权递归聚合 |
| connected components | 线性传播式递归 | 删除可拆分分量 | min/标签聚合 | branching | 中高扩张 | 非平凡递归聚合，小/中规模 |
| Polonius subset | 多关系递归 | 混合更新下非单调维护 | 集合、join | 规则图/CFG | 局部传播但可多轮 | 真实程序分析类别 |
| LDBC reachability | 线性递归 | 时间插入与删除级联 | 集合 | 小型社交图 | toy 深度 | 第二数据路线与原生时间语义 |

“reachability small”和“reachability medium”属于同一类别；LDBC reachability 也不能与合成 reachability 一起冒充两个不同递归类别。跨类别门槛只能由例如 reachability + Polonius，或 reachability + recursive aggregate 满足。

正式矩阵覆盖四类：可达性、加权递归聚合、递归聚合、程序分析。每个配置有一个 warm-up 批和五个计量批；关键单元三次完整重复。中规模只对小规模筛查后的 reachability 与 connected components 执行。
