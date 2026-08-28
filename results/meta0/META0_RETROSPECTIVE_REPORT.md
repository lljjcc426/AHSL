# META0 Full Research-Direction Retrospective

回顾日期：2026-08-28

冻结提交：`198db5f110f5a9daf7debddabf102ce9d1656f4e`

分支：`project-meta0-full-direction-retrospective`

## 1. Executive conclusion

META0 审计了 A0 至 AP-R0 的 17 个方向。唯一 Rank 1 是：**复制噪声与部分组合测量下，完整因子微生物群落功能 landscape 的 order≥3 signed interaction support recovery**，Development-Value 为 **88/100**。唯一备选是 fuzz-found 真实漏洞的 fully verified repair（82/100）。

Rank 1 不是已被证明的论文结果，而是下一个最值得投入 12 个工作日真实开发的方向。决定性依据有四项：Ishizawa 面板中最佳历史 baseline 在 budget 48 的支持 F1 仅 0.235、约 79.6% 强高阶效应未找回；response RMSE 约 0.102，暴露“预测好但结构恢复差”的 estimand mismatch；旧项目只有基础 lasso/OMP/遗传性审计，开发债 D2；2026 年又出现第二个公开完整 8-strain、256-community、3-replicate 因子面板，旧“只有一个真实面板”的控制理由不再成立。

META0 没有训练新模型。它修改的是当前研究管理规则：可执行当前强基线的材料性 residual 在 Confirmation 前必须具备，但不再是进入 Development 的先决条件。

## 2. Why methodology changed

历史流程有效识别了许多伪问题，却把三个阶段压成一个超强前置 gate：方向在造方法之前，就被要求具有广 benchmark、当前强基线 residual、多路线、统一大效应和接近论文的完整证据。结果是大量“审计充分、开发接近零”的候选被写成 NO-GO。

新的 DDC 区分：

- Discovery 只确认任务、评价、机制、信号/失败模式和研究自由度；
- Development 在有界预算内主动优化方法、制度、参数和实现；
- Confirmation 在方法成熟后冻结主张，用当前强基线、公平调参和 held-out evidence 验证。

这不是降低科学标准。H1–H6 仍直接关闭无效目标、非识别问题、近同题占位、无任务/数据和平凡集成；改变的是不再用任意性能阈值或未完成工程代替硬科学事实。

## 3. Historical direction inventory

| # | 历史方向 | 范围 | META0 状态 | 债务 |
|---:|---|---|---|---|
| 1 | α-无环/连通子树结构去噪 | A0–B0 | H4/F，关闭 | D0 |
| 2 | 连通子树后验/决策对齐预测 | A1–A1.5 | H4，关闭 | D0 |
| 3 | CertPath learned costs + directed hyperpath | N0–N1.0 | H1/F，关闭 | D2 |
| 4 | sparse high-order interaction recovery | S0–S1.0 | S/O，重开 | D2 |
| 5 | temporal complete group-event prediction | S0–S2.0 | H3/F，关闭 | D1 |
| 6 | natural partial-observation recovery | S3.0 | H2/H4，关闭 | D3 |
| 7 | learning-augmented exact inference strategy | R0 | S，可重开低优先 | D1 |
| 8 | canonical/rerootable/dynamic HD/GHD/FHD | P0/P1 | O/F，较宽问题开放 | D3 |
| 9 | incremental recursive query execution | AP0/AP1.0 | S，可重开 | D1 |
| 10 | hybrid structured/vector execution | AP-R0 A1 | S，暂不重开 | D3 |
| 11 | reliable executable workflows | AP-R0 B1 | S，暂不重开 | D3 |
| 12 | repository-level semantic test generation | AP-R0 C1 | O，开放低优先 | D3 |
| 13 | dynamic-shape runtime/compiler | AP-R0 D1 | F/H3，关闭精确表述 | D3 |
| 14 | semantic constraint-model synthesis | AP-R0 E1 | O，Rank 3 | D3 |
| 15 | verified fuzz vulnerability repair | AP-R0 F1 | O，Rank 2 | D3 |
| 16 | public industrial scheduling | 旧候选矩阵 | H4，关闭 | D3 |
| 17 | grid outage localization | B0/AP0 | H5，关闭 | D3 |

详细清单见 `docs/META0_ALL_DIRECTION_INVENTORY.md`。

## 4. Historical stop reasons

历史停止原因可以归成五组：

1. **真实任务/数据不存在：** A/B 的 scaffold-output-covariate-loss 联合任务、工业排程现代公开 benchmark、电网联合数据。
2. **目标或观测数学上无效：** CertPath 自然真值不可达；S3 非单射观测下的恢复不可识别。
3. **近同题占位：** S2 的 HyperSearch、dynamic-shape 的当前官方能力/ShapesSpec、P1 的 rerootability 新工作。
4. **任意经验 gate：** R0 未过 3×，AP1.0 的 1.969× 未过 2×，S1 只有一个直接可评域。
5. **未完成 Confirmation 被当成失败：** hybrid vector、workflow、test generation、E1、F1 没有跑当前方法或 artifact，但也没有实际方法开发。

前 1–3 组可为硬/F 级事实；第 4–5 组不能自动证明科学失败。

## 5. Hard vs soft closures

**硬关闭的八个精确方向：** A0–B0 的真实结构学习/去噪应用项目、A1–A1.5 后验结构任务、CertPath 正加性精确超路径、S2 完整组事件协议、S3 自然部分观测恢复、dynamic-shape 精确表述、公开工业排程目标、电网定位目标。

**表述关闭（可与硬关闭重叠）：** A0 的神经 fixed-tree 路线、CertPath 正加性 decoder、S2 原开放检索贡献、P1 精确 rerootable-HD 子题、dynamic-shape parity 子题。

**软/可重审：** S1、R0、AP1.0、hybrid vector、reliable workflows。**开放/欠开发：** S1、较宽 decomposition theory、repository test generation、E1、F1。标签并非互斥：S1 的历史停止是 S，但当前研究状态为 O/D2。

## 6. Development debt

A0/A1 是 D0：精确算法、概率模型、拓扑、噪声与 decoder 已系统开发。AP1.0、R0、S2 为 D1：有原型或部分 baseline。CertPath 与 S1 为 D2：前者被可达性事实提前杀死，后者仅有基础估计器，均不能称为“优化后失败”。P1、S3 和 AP-R0 大多数候选为 D3：文献/benchmark/artifact 审计为主。

高开发债提升“1–3 周能学到什么”的杠杆，也提升失败概率。因此 D3 不是加分本身；必须与可信任务、signal、机制和 feasibility 同时存在。

## 7. Recovered positive signals

- A0.5：结构 MLE 相对独立 MLE 平均 Hamming 降低 0.02952、exact-row +0.15269，76.3% 条件为正；path/random/balanced 明显强于 star。
- A1.5：connected Bayes-Hamming 相对 MAP 增益在生成树 0.00459、BinaryMWST 0.00408、估计树 0.00639，置信区间为正。
- S1：294 个 order≥3 系数中 140 个强非零；budget 48 的 tuned lasso F1 0.235、AP 0.506、pure-HOI recall 最高 0.425，response RMSE 约 0.102。
- S2：sampled-negative Recall@10 75–95% 与开放检索 0 的巨大协议差异；候选 recall 仅 0.973%/0.330%。
- R0：经典策略最大 2.23× 跨度，虽未过旧 3×，但并非零信号。
- AP1.0：11 个 cell 全正确；incremental 比 scratch 快 2.560–8.953×，p99/p50 约 3.015，retained growth 2.699 MiB，最大 update-peak 比 1.969×。
- F1：历史 AutoPatchBench 的 crash-stopping 与 full fuzz/differential verification 存在约 60% 对 5–11% 的落差。

## 8. Directions unfairly penalized by old gates

最明显是 S1。旧 gate 要求第二 benchmark family 和更接近 publication-grade 的 residual，却没有给该方向竞争方法开发。其真实结果恰好显示了一个结构性问题：以 response error 选模可以“看似准确”，同时漏掉绝大多数强高阶支持。现在第二个完整微生物面板使聚焦单一科学域的条件论文可被独立检验。

AP1.0 与 R0 也被统一倍数阈值不公平压低。成熟数据库系统中稳定 15–30% 可能已材料性，不能用 2×；策略选择也不能用 3× 作普遍科学界线。但二者即使纠正 gate，仍因机制/novelty/杠杆弱而不进入前四。

## 9. Directions correctly killed regardless of methodology

CertPath 的关闭最强：961/1620（59.32%）自然任务可达，456/1620 在不做被禁止的内部修补时不可行。目标函数排除自然真值，增加训练、调参或模型规模不会修复。

S3 的非识别性同样不能靠开发预算解决；需要新观测、新 gold 或新定理。S2 的正确协议和安全搜索贡献被 HyperSearch 直接占位。A/B 即使有漂亮合成增益，也没有找到结构 posterior 自身具有外部价值的真实任务。它们均保持关闭。

## 10. Current prior-art refresh

本次只定向更新 13 项 2025–2026 primary work/artifact。

- S1 获得 eLife 2026 的 8-strain、256-community、3-replicate 完整面板和公开代码，这是唯一显著打开空间的新事实。Adaptive Sparse Möbius Transform 是最强算法威胁，但目前针对精确稀疏 Boolean polynomial/模拟超图，不直接覆盖真实 replicate-noisy FDR support。
- F1 获得 230-case PatchEval-Verified；ContraFix 已用 differential runtime evidence 和 failure-boundary mutation 报告强结果，抬高 baseline 并占据明显路线。
- E1 中 CP-Agent 报告 CP-Bench 101/101，CP-SynC 直接采用 synthesized semantic checkers、并行轨迹与 evidence aggregation；简单“prompt + solver feedback”没有足够新颖性。
- P1 的 rerootability 被 2026 Rerootable Hypertree Decompositions 直接占据；只能保留 canonical/dynamic/reuse 的更宽理论程序。
- AP1.0 面对当前 Feldera/DBSP 和 FlowLog，旧 signal 仍缺少新的内部机制归因。

## 11. Application fit

S1 的应用对象是合成 microbial consortia 的功能解释和组合实验节省，同时核心贡献可保持 CS/AI 性质：带噪组合设计、支持恢复、不确定性控制和 adaptive acquisition。F1 的直接安全价值最高；E1 面向自动优化建模；AP1.0 面向动态递归数据系统；理论方向为数据库查询基础。

按“应用优先但保留算法/AI/系统/理论潜力”的偏好，S1 比纯理论更均衡，也比通用 agent scaffold 更具稳定科学对象。

## 12. Publication fit

S1 的现实 community 是 KDD/AAAI/IJCAI/UAI、RECOMB/Bioinformatics；若方法和一般性充分，才讨论 ICML/NeurIPS。F1 对应 ICSE/FSE/ISSTA/ASE 及安全 venue，上限最高但执行负担也最高。E1 对应 AAAI/IJCAI/KR/CP，但 prior-art collision 显著。理论方向对应 PODS/ICDT。AP1.0 若形成新执行机制，可达 SIGMOD/PVLDB/ICDE。

排序没有用 venue prestige 代替可开发性。S1 要保住 CS 贡献，论文必须以组合结构恢复方法和可验证条件优势为中心，而不是只做微生物 case study。

## 13. Development leverage

S1 的 12 日杠杆最高：数据小且完整，可精确模拟 partial measurement；已有 failure taxonomy 指向 replicate variance、设计相干、非遗传支持和 estimand mismatch；可以尝试多个机制不同的估计/采样方法；历史上几乎未优化。

F1 的技术空间丰富，但容器、agent 成本和异质 failure modes 会吞噬短期预算。E1 易执行，但两天内就可能发现明显路线被 CP-SynC/CP-Agent 封住。理论方向无需大型工程，但发现可证明的未占据命题高度不确定。AP1.0 若无内部 counters 和新机制，更多 benchmark 只会变成 outcome hunting。

## 14. Candidate scores

| 候选 | A | B | C | D | E | F | G | H | I | J | /100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S1 microbial HOI support | 9 | 9 | 9 | 8 | 10 | 8 | 9 | 8 | 9 | 9 | **88** |
| F1 verified vulnerability repair | 10 | 9 | 8 | 8 | 8 | 8 | 4 | 10 | 9 | 8 | **82** |
| E1 semantic constraint synthesis | 8 | 8 | 7 | 7 | 9 | 5 | 9 | 7 | 7 | 8 | **75** |
| broader decomposition theory | 7 | 7 | 6 | 8 | 8 | 6 | 9 | 8 | 9 | 5 | **73** |
| AP1.0 recursive queries | 9 | 8 | 6 | 6 | 6 | 5 | 5 | 8 | 7 | 6 | 66 |
| repository semantic tests | 9 | 8 | 5 | 6 | 7 | 5 | 6 | 7 | 6 | 5 | 64 |
| R0 exact strategy | 8 | 8 | 5 | 6 | 7 | 4 | 7 | 7 | 6 | 3 | 61 |
| hybrid structured/vector | 9 | 8 | 2 | 6 | 5 | 3 | 4 | 8 | 7 | 6 | 58 |
| reliable workflows | 9 | 8 | 3 | 5 | 6 | 3 | 6 | 7 | 6 | 4 | 57 |

A–J 的定义和评分解释见 `docs/META0_DIRECTION_RANKING.md`。

## 15. Shortlist

最多四项，按同一 rubric 排序：

1. S1 因子微生物 order≥3 signed-support recovery（88）；
2. F1 fuzz-found fully verified vulnerability repair（82）；
3. E1 semantic constraint-model synthesis（75）；
4. canonical/dynamic reusable hypergraph decomposition（73）。

没有并列 Rank 1，也不并行启动多个 Development 项目。

## 16. Rank 4

**较宽的 canonical/dynamic reusable hypergraph decomposition。** 精确 rerootability 已被 2026 工作占位，剩余机会必须是新的规范表示、跨查询复用或更新维护定理，而不是改名重做 rerootable HD。它有长期理论深度、低计算成本和 PODS/ICDT 上限；但 D3、命题风险和应用偏好使它只排第四。

## 17. Rank 3

**语义约束模型合成。** CP-Bench 的真值和 solver 反馈使评价很干净，工程成本低，适合 Development。问题是 CP-Agent 与 CP-SynC 已覆盖通用 agent、synthesized checker、多轨迹和选择。只有先找到可预声明、尚未被覆盖的语义错误机制，才值得继续；不能把 prompt engineering 包装成算法贡献。

## 18. Rank 2

**fuzz-found 真实漏洞的 fully verified repair。** 它拥有最强直接应用价值、真实漏洞、build/PoC/fuzz/differential verifier 和顶级软件工程/安全发表上限。它没有排名第一，是因为 PatchEval/ContraFix 等已抬高当前基线，短期工程成本高，剩余错误异质；同样 12 天投入，得到可归因方法信号的概率低于 S1。它被指定为唯一备选。

## 19. Rank 1

**精确问题：** 从只测部分组合、带 biological replicate noise 的完整因子微生物 community-function landscape 中，恢复 order≥3 signed Möbius support 并给出不确定性控制。

**两个真实 benchmark：** Ishizawa 7-strain/127 nonempty communities/2377 CFU measurements；Díaz-Colunga 8-strain/256 communities/3 biological replicates 的 OD600 biomass landscape。

**当前历史最强可执行 baseline：** tuned lasso，在 budget 48 上 support F1 0.235、AP 0.506；META1 还必须加入 elastic net、OMP、weak heredity、stability selection 和可行 ASMT-style baseline，不能只赢默认 lasso。

**Primary metric：** 固定 measurement fraction 下的 macro order≥3 signed-support F1。**Guardrails：** empirical FDR/precision、recall/AP、pure-HOI recall、coefficient/response RMSE、panel/scale/seed stability、测量数和运行时间。

## 20. Strongest argument FOR Rank 1

它同时具备真实未解决 residual、可证伪机制、两个完整可公开面板、低成本精确评价和极高开发债。尤其重要的是 residual 不是“某个模型少赢几分”，而是 prediction 与 scientific estimand 分离：response RMSE 约 0.102 时，最佳 support F1 仍只有 0.235。该错位直接定义了算法问题，也提供多种非平凡干预和清晰 guardrail。

## 21. Strongest argument AGAINST Rank 1

面板维度只有 7/8 strains，完整数据构造的“强支持”仍是统计 estimand 而非绝对生物真值；若支持对 raw/log、bootstrap 或 threshold 不稳定，整个任务会退化。另一方面，Adaptive Sparse Möbius Transform 可能经过少量噪声改造后已成为强基线。如果 META1 只在一个 threshold/seed/面板获胜，则不构成可信条件优势。

## 22. Why Rank 1 beats the newest alternatives

相对 F1，S1 的工程成本低、评价闭环紧、failure mechanism 更同质，12 天更可能区分 D-B 与 D-D；F1 的当前 agent 已强且环境成本大。相对 E1，S1 的明显技术干预没有被一篇 2026 工作整体占据，而 E1 的 semantic checker + multi-trajectory 路线已被 CP-SynC 直接实现。相对 repository tests/hybrid workflows，S1 已有定量 residual，不依赖先造大 agent/system scaffold。

该判断不是 recency bias：新工作对 S1 是新增独立数据，对 E1/F1 则主要是更强 prior art。两者作用方向相反。

## 23. Why Rank 1 beats the old hypergraph alternatives

A0/A1 有真实合成数学信号，但 B0 的真实任务缺失未改变；CertPath 目标不可达；S2 被同题占位；S3 不可识别；R0 residual 小且 JoinInfer 邻近；P1 rerootability 已被 2026 论文直接占据。S1 则把超图/Boolean lattice 结构保留在真实应用里：研究对象仍是高阶组合支持，但不要求一个不存在的 latent tree 或不可得 gold。

它也比纯 decomposition theory 更符合应用偏好，同时保留算法、统计学习和潜在 adaptive sensing 的长期程序。

## 24. Development risks

1. **Estimand instability：** full-panel support 对尺度/threshold/bootstrap 不稳定。
2. **Small-n ceiling：** 7/8 维可能不足以支撑一般算法结论。
3. **Prior-art compression：** ASMT-style baseline 在 noisy partial setting 已足够强。
4. **Mechanism misdiagnosis：** 失败可能来自 support definition，而非设计相干或复制噪声。
5. **Selection bias：** 只报告某预算/seed/面板获胜。
6. **Application overclaim：** Möbius coefficient support 不必然等于因果微生物机制。

对应控制是预先记录 estimand/sensitivity、同时报告两个面板、按方法结果之外的 SNR/coherence/pure-HOI 属性定义制度、保留所有开发日志，并把生物结论限定为 functional interaction estimand。

## 25. Exact META1 sprint

时长 12 个工作日。Days 1–2 统一两个面板并冻结 estimand/masks/seeds；Days 3–4 公平调优 lasso/elastic net/OMP/weak heredity/stability/ASMT baseline；Days 5–8 分别开发 replicate-noise weighting、stability/FDR、non-hereditary structure 和 adaptive measurement；Days 9–10 调参并按 SNR/coherence/budget/pure-HOI 做机制分层；Days 11–12 跨面板/尺度/seed 复核并判 D-A/B/C/D。

D-B 的最低含义是：机制被证据支持，且在至少一个科学上有意义、可独立定义的 panel/regime 中，对合理调优强 baseline 有重复的主指标材料性改善，FDR 与 response RMSE 可接受；允许另一面板中性。三类机制不同干预均失败或 estimand 本身不稳，则判 D-D 并停止。完整协议见 `docs/META1_DEVELOPMENT_SPRINT.md`。

## 26. Backup direction

唯一备选是 **fuzz-found 真实漏洞的 fully verified repair**。若 META1 在前两日发现 S1 的第二面板不能形成稳定 estimand，或后续三类干预均无开发杠杆，则不自动切换；先提交 D-D 证据，再单独启动 F1 的环境/当前 baseline Discovery 更新。备选不与 Rank 1 并行消耗预算。

## 27. Final decision

决定：**启动 S1 的窄化 META1 Development sprint；不重开广义“跨域高阶交互发现”，不把 META0 结果写成确认性主张。**

当前管理规则已由 `docs/RESEARCH_MANAGEMENT.md` 更新：Discovery 需要可信任务、机制和信号；Development 可以有界优化；当前强基线 Confirmation 在冻结出版主张前完成。机制驱动制度选择允许，结果驱动最终 benchmark 选择禁止。

## 28. Exact next action

从 Díaz-Colunga 的公开 artifact 与仓库现有 Ishizawa 数据开始，建立只统一 `community bitmask / replicate / response` 的两个最小 adapter；输出 cell/replicate 完整性、raw/log support-estimand stability 和预声明 measurement masks。随后才运行调优 baseline。不要在这一第一步训练新方法，也不要增加无现实风险依据的 hash、重复 smoke test 或防御分支。
