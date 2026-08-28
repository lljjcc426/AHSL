# META0：全历史方向清单

日期：2026-08-28

本清单审计 17 个方向，覆盖 A0 至 AP-R0，并补入旧候选矩阵中的工业排程与电网定位。`旧阶段` 是历史决策记录，`META0` 是按 DDC 的新解释。

| # | 方向 | 历史范围 | 旧停止原因 | 实际到达阶段 | 债务 | META0 分类 | 重开？ |
|---:|---|---|---|---|---|---|---|
| 1 | α-无环/连通子树去噪 | A0–B0 | 神经法无优势；真实任务未找到 | Development + 应用 Discovery | D0 | H4/F | 否 |
| 2 | 连通子树后验/决策对齐预测 | A1–A1.5 | 树增益很小且无真实应用 | Development | D0 | H4 | 否 |
| 3 | CertPath 学习代价 + 精确超路径 | N0–N1.0 | 40.68% 自然任务在目标下不可达 | Discovery | D2 | H1/F | 否 |
| 4 | 稀疏高阶组合交互恢复 | S0–S1.0 | 仅一个直接可评真实域；基线支持恢复弱 | Discovery + 基础 baseline | D2 | S/O | 是，Rank 1 |
| 5 | 时间完整超边/组事件预测 | S0–S2.0 | sampled-negative 假象；HyperSearch 直接占位 | 小型 Development | D1 | H3/F | 否 |
| 6 | 自然部分观测高阶恢复 | S3.0 | gold、可识别性与现实观测不能同时满足 | Discovery | D3 | H2/H4 | 否 |
| 7 | 学习增强精确推理/策略选择 | R0 | 经典策略差距未过 3×，相邻 prior art 强 | 小型 Development | D1 | S | 是，低优先 |
| 8 | canonical/rerootable/dynamic HD/GHD/FHD | P0/P1 | 理论提案，无定理开发 | Discovery | D3 | O/F | 较宽问题可开，Rank 4 |
| 9 | 动态/增量递归查询执行 | AP0/AP1.0 | 峰值内存比 1.969× 未过 2×；归因不足 | Development 原型 | D1 | S | 可开，未入前四 |
| 10 | 混合结构/向量查询执行 | AP-R0 A1 | 当前方法拥挤，artifact 未执行 | Discovery | D3 | S | 暂否 |
| 11 | 可靠可执行业务/tool 工作流 | AP-R0 B1 | verifier/retry 路线拥挤，贡献未收窄 | Discovery | D3 | S | 暂否 |
| 12 | 仓库级测试生成/语义测试质量 | AP-R0 C1 | 无当前基线和方法 | Discovery | D3 | O | 可开，低优先 |
| 13 | 动态形状编译/运行时 | AP-R0 D1 | 官方 parity；ShapesSpec 近同题 | Discovery | D3 | F/H3 | 精确表述否 |
| 14 | 语义约束模型合成 | AP-R0 E1 | 尚未开发；语义 checker 路线后来被 CP-SynC 压缩 | Discovery | D3 | O | 是，Rank 3 |
| 15 | fuzz 发现漏洞的验证修复 | AP-R0 F1 | 初始工程成本 E4；未开发 | Discovery | D3 | O | 是，Rank 2/备选 |
| 16 | 公开工业排程 | AP0 候选矩阵 | 缺现代公开应用 benchmark | Discovery | D3 | H4 | 否 |
| 17 | 电网停电定位 | B0/AP0 候选 | 关键联合数据不可得 | Discovery | D3 | H5 | 否 |

## 审计结论

- **硬关闭的精确方向（8）：** 1、2、3、5、6、13、16、17；其中 1 与 13 同时有 F 级外围知识。
- **非硬关闭（9）：** 4、7、8、9、10、11、12、14、15。
- **最被旧 gate 不公平压低：** 4（S1），因为它有清晰可量化 residual，却几乎未做方法开发；2026 年又出现第二个完整因子微生物面板。
- **最强旧关闭：** 3（CertPath），因为自然真值在目标函数下不可达是目标层事实，不受调参影响。
