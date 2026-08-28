# META0：被旧 gate 遮蔽的正信号

日期：2026-08-28

| 方向 | 信号、数据与指标 | 机制假说 | 方法是否优化 | 旧拒绝原因 | 拒绝现在是否成立 |
|---|---|---|---|---|---|
| A0 精确结构去噪 | 合成已知树中，精确投影/MAP 相对观测均值的 clean-F1 增益 0.0175/0.0312，exact-row 增益 0.1380/0.1745 | 连通子树约束消除独立噪声不一致 | 是，D0 | 神经模型反而比 nearest/MAP 低 0.0236/0.0373；无真实任务 | 数学信号成立，应用关闭仍成立 |
| A0.5 结构 MLE | 相对独立非空 MLE，平均 Hamming 降低 0.02952，exact-row +0.15269，76.3% 条件为正；path/random/balanced 增益明显，star 仅 0.00389 | 树拓扑决定约束可提供的信息量 | 是，D0 | 星形可有害；generator-prior oracle 仍有差距；B0 任务缺失 | 不足以重开，但保留 topology-conditioned 知识 |
| A1.5 连通 MBR | 相对 MAP 的 Bayes-Hamming 增益：生成树 0.00459、BinaryMWST 0.00408、估计树 0.00639，置信区间均为正 | 决策损失与 MAP 状态概率不一致 | 是，D0 | 整体树价值仅 0.00093 且无真实任务 | decoder 信号成立，H4 仍致命 |
| S1 微生物 HOI | Ishizawa 完整面板中 order≥3 的 294 个系数有 140 个强非零；budget=48 的最佳支持 F1 仅 0.235、AP 0.506、pure-HOI recall 最高 0.425，而 response RMSE 仍约 0.102 | AND/Möbius 设计相干、复制/异方差噪声及非遗传性使预测调优的稀疏法漏掉结构 | 否，D2 | 只有一个直接可评真实域，且未达到跨域 benchmark gate | 不成立；2026 又出现公开 8-strain 全因子面板，且旧方法未开发 |
| S2 开放检索 | sampled-negative Recall@10 可达 75–95%，开放新组检索却为 0；候选 recall 仅 Ubuntu 0.973%、Congress 0.330% | 负采样把组合空间难度隐藏掉 | 仅协议/基线，D1 | HyperSearch 已在正确任务上直接占位 | 作为评价警示保留，精确贡献仍关闭 |
| R0 精确策略 | 四种经典策略的运行时跨度为 1.28×、1.46×、1.37×、2.23× | 模型结构可能决定策略排序 | 仅经典策略，D1 | 未过统一 3× | 阈值理由不成立；但幅度和 novelty 仍弱 |
| AP1.0 递归查询 | 11 个 cell 均精确；incremental 相对 scratch 快 2.560–8.953×；最大 update-peak 比 1.969×，p99/p50 约 3.015，retained growth 2.699 MiB | 递归形状、删除传播与保留状态导致尾部/内存差异 | FlowLog 原型，D1 | 1.969× 未过 2×，且缺内部 state/work counters | 2× 理由不成立；归因与当前系统竞争问题仍在 |
| 约束合成 | CP-Bench 的可执行 ground truth 可直接区分语法/可行性与语义建模正确性；历史强方法最高约 70% | 自然语言中的量词、索引、目标及隐含约束产生可分类语义错配 | 否，D3 | 当前模型未跑、具体干预未形成 | 可作为 Development，但 CP-SynC/CP-Agent 已压缩明显空间 |
| fuzz 漏洞修复 | AutoPatchBench 历史结果显示“停止 crash”约 60%，完整 fuzz/differential 验证仅 5–11%；PatchEval-Verified 提供 230 个可容器验证案例 | 单 PoC 修复易过拟合，失败边界与反例可驱动语义修复 | 否，D3 | 初始设置成本高且当前模型未执行 | 工程成本不是硬关闭；当前强 agent 已显著抬高基线 |

## 最重要的 recovered residual

S1 的“低 response RMSE、极低高阶支持 F1”不是普通预测误差，而是 estimand 错位：一个模型可以预测总体功能，却漏掉约 79.6% 的强高阶效应。这给出了明确的主指标、失败机制和方法空间；与新的第二完整因子面板结合，它是本次回顾中开发价值最高的信号。
