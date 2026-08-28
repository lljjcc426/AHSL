# META0：旧 NO-GO 重审矩阵

日期：2026-08-28

| 方向 | 旧决定/控制原因 | 旧阶段实际到达 | META0 硬/软 | 被丢弃的正证据 | 既有开发 | 当前 prior art | 重开？及理由 |
|---|---|---|---|---|---|---|---|
| A0–B0 | NO-GO；真实任务缺失、神经法无胜势 | Development | H4/F | 精确结构去噪与 exact-row 增益 | D0 | classical structured inference 成熟 | 否；任务缺失未变 |
| A1–A1.5 | NO-GO；总体树价值小、无应用 | Development | H4 | MBR 相对 MAP 稳定小增益 | D0 | 属于 classical Bayes action | 否；没有新 real task |
| CertPath | NO-GO；正加性目标不可达 | Discovery | H1/F | 可达子集较干净 | D2 | 不改变可达性事实 | 否；最强硬关闭 |
| S1 HOI | NO-GO；一域且未过跨域 gate | Discovery/基础 baseline | S/O | support F1 0.235、约 79.6% strong effects 漏检；response RMSE 却低 | D2 | ASMT 构成邻近威胁；2026 新完整微生物面板 | **是；旧理由已被新数据和 DDC 共同削弱** |
| S2 组事件 | NO-GO；开放检索失败且 HyperSearch 碰撞 | 小型 Development | H3/F | sampled/open protocol gap 极大 | D1 | HyperSearch 直接同题 | 否；正证据是评价教训，不是贡献空白 |
| S3 部分观测 | NO-GO；非识别/无 gold | Discovery | H2/H4 | 自然观测机制确实存在 | D3 | graph/matrix/tensor/latent 方法覆盖可识别子问题 | 否；无新观测路线 |
| R0 精确策略 | NO-GO；未过 3× | 小型 Development | S | 最佳策略跨度最高 2.23× | D1 | JoinInfer 强邻近 | 可重开但不优先；旧阈值错误、实际杠杆仍低 |
| P0/P1 理论 | 提案未启动 | Discovery | O/F | 可复用/动态分解问题有理论价值 | D3 | Rerootable HD 直接占精确子题 | 仅重开较宽理论程序 |
| AP1.0 递归查询 | NO-GO；1.969× 未过 2×，无内部计数 | Development 原型 | S | 2.560–8.953× 对 scratch；尾部/retained-state 信号 | D1 | FlowLog/Feldera 强，difference dropping 已知 | 可重开但不进前四；需先有新归因 |
| 混合向量查询 | 未选；拥挤/未跑 artifact | Discovery | S | 真实复合过滤负载 | D3 | ACORN/SIEVE/DIGRA/RangePQ 等拥挤 | 暂否；明显路线低杠杆 |
| 可靠工作流 | 未选；贡献泛化 | Discovery | S | verifier/retry 有现实价值 | D3 | agent/tool verification 活跃 | 暂否；缺独立 residual |
| 仓库测试生成 | 未选；未跑方法 | Discovery | O | benchmark 可执行、语义测试重要 | D3 | 领域拥挤 | 可开但排位低 |
| 动态形状 | NO-GO；官方 parity/近同题 | Discovery | F/H3 | 初期真实工程痛点 | D3 | PyTorch parity、ShapesSpec | 精确表述否 |
| 约束合成 | 未选；current residual 未执行 | Discovery | O | 可执行 ground truth、语义错配 | D3 | CP-Agent/CP-SynC 强占明显路线 | 是，Rank 3；需新错误机制 |
| fuzz 修复 | 未选；E4 setup | Discovery | O | crash-stop 与 full verification gap | D3 | PatchEval/ContraFix 抬高基线 | 是，Rank 2；高价值但重 |
| 工业排程 | NO-GO；无现代公开应用任务 | Discovery | H4 | 调度本身重要 | D3 | benchmark mismatch 未解 | 否 |
| 电网定位 | conditional hold；联合数据缺失 | Discovery | H5 | 结构传感想法合理 | D3 | 无新公开联合资源 | 否 |
