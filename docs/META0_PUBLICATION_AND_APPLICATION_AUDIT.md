# META0：应用与发表审计

日期：2026-08-28

| 候选 | 应用价值 | 可信主张形态 | 现实 community/venue | 上限条件 | 主要降级因素 |
|---|---|---|---|---|---|
| S1 因子微生物 HOI | 合成菌群设计、生态交互解释、减少组合实验成本 | 在复制噪声与非遗传高阶效应活跃的全因子/分数因子菌群中，提高 order≥3 signed-support recovery，并控制 FDR 与预测误差 | KDD、AAAI、IJCAI、UAI；RECOMB、Bioinformatics；方法足够一般时 ICML/NeurIPS | 两个公开面板均有稳定机制证据，且方法不只是生物特例 | 样本维度小；真实“强支持”由统计阈值定义；ASMT 理论威胁 |
| fuzz 验证修复 | 直接安全价值，真实漏洞和强 verifier | 对某一可预声明漏洞/失败边界类，提高 fully verified repair，而非只停止 crash | ICSE、FSE、ISSTA、ASE；安全 venue | 在当前强 agent 上仍有可归因 residual，并能控制成本 | 容器/agent 成本高；当前结果已强；错误高度异质 |
| 语义约束合成 | 自动化优化建模，solver 提供客观反馈 | 对某一语义错配类，用结构化表征/证明义务提高独立语义正确性 | AAAI、IJCAI、KR、CP | 超越 CP-SynC/CP-Agent 的独立机制与新 benchmark | 明显 checker/多轨迹路线已被占据；应用可能退化成 generic agent |
| 较宽超图分解理论 | CQ 优化、分解复用与动态查询的基础价值 | 给出 canonical/dynamic reusable decomposition 的新定义、定理与算法 | PODS、ICDT；理论 AI/DB | 避开 2026 rerootable HD，形成非平凡定理链 | 应用导向较弱；D3；定理风险高 |
| AP1.0 递归查询 | 图/递归 SQL 更新的实际延迟与状态成本 | 对机制定义的 recursion/churn 制度改善尾延迟或状态 | SIGMOD、PVLDB、ICDE | 新内部机制、强 Feldera/FlowLog 对比、跨 workload 稳定 15–30% 也可有价值 | 当前 signal 归因不足；系统强；Difference dropping 已知 |
| 仓库测试生成 | 软件质量与 agent reliability | 提高语义 fault detection，而非生成更多 tests | ICSE、FSE、ISSTA、ASE | 可执行 benchmark + 新语义覆盖机制 | 极拥挤，尚无 residual |
| R0 精确推理策略 | 精确概率推理和编译策略选择 | 在可预声明模型结构上减少 exact runtime，同时保持证书 | UAI、AAAI、IJCAI、MLSys | 重复 workload/摊销场景与远强于经典启发式的条件 residual | JoinInfer 邻近；策略差距小；标签昂贵 |

## 结论

应用导向偏好不意味着排除理论，而是要求 Rank 1 同时拥有现实任务和算法/AI 贡献。S1 满足这一点：问题来自真实 microbial community-function landscapes，但核心工作是带不确定性控制的组合结构恢复。F1 的应用价值更直接，却因当前基线和工程成本降低短期开发回报。理论方向保留为 Rank 4，不因缺少 ML 被扣分，但其应用契合和当前 formulation headroom 较弱。
