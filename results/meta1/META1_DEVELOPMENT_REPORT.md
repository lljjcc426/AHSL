# META1 Development Report: Noisy Partial-Factorial Higher-Order Interaction Support Recovery

## 1. Executive decision

**结论：D-B PROMISING。** META1 找到一个需要严格 Confirmation、但尚不能视为已确认贡献的条件优势：在 Ishizawa 型六伴随因子、每格至少 5 个复制、log10 CFU、测量比例不超过 50% 的 focal-response landscapes 中，`hybrid_d50 + ElasticNet` 相对同等预算的 uniform ElasticNet 将 macro signed order>=3 support F1 从 0.2001 提高到 0.2509（+0.0508）。同时 precision +0.0217、recall +0.0955、AP +0.0135、FDR -0.0217、seed stability +0.0653，response RMSE 仅增加 0.00151（0.76%）。

该增益在四个 Development seeds 的均值上方向一致，在 7 个 landscapes 中有 6 个方向为正，但仅 50/84 个逐 mask 配对为正。它不延伸到 budget 48，也不延伸到 Díaz-Colunga：Díaz 上 F1 -0.0257、response RMSE +0.0186。因此不满足 D-A 的跨独立证据要求。候选策略及制度又是查看 Development 结果后选出的，必须保留 D-B 的探索性定性。

## 2. Exact scientific problem

问题不是预测完整响应面，而是在只测量部分社区且测量含 biological-replicate noise 时，恢复 AND/Möbius 展开中 order>=3 系数的正确符号支持。核心科学错位是：较低 response RMSE 并不推出正确的 interaction support。META1 以 signed-support F1 为主指标，以 response prediction 作为 guardrail，而不是反过来。

## 3. Data sources and semantics

Ishizawa 面板来自 PNAS 2024 supplement（DOI `10.1073/pnas.2312396121`），共有 127 个非空七菌株组合、2,377 条原始 CFU 测量。以每个 strain 为 focal response，得到七个六因子、64-cell 的完整 landscape。

Díaz-Colunga 面板来自 eLife（DOI `10.7554/eLife.101906.3`）及官方 `full_factorial_design` artifact，固定 git commit `35c150c85df2fc5964523f906ceeb8229f0b1666`。使用源代码指定的 `wavelength=600`、`dilution_factor=0.0025` 选择，得到一个八因子、256-cell、每格三个复制的响应面。OD600 仅称为 quantitative community-function response，不称为精确 biomass truth。

## 4. Data integrity

八个 landscapes 均完整，无缺格。Ishizawa 六个 landscapes 各 341 条记录，DW147 为 331 条；每格复制数通常为 5--12，DW147 为 5--9。Díaz 为 256×3=768 条记录。源数据中未发现 `(strain, system, replicate)` 或 `(community, replicate)` 重复键。详细审计在 `raw/data_audit.csv`、`raw/panel_replicates.csv`、`raw/replicate_statistics.csv`。

这项审计回答了真实风险：因子格是否完整、复制是否真实存在、键是否重复。未添加与该风险无关的 hash 或重复 smoke 检查。

## 5. Factorial representation

对 \(x\in\{0,1\}^d\)，统一使用 AND basis：

\[
f(x)=\sum_{S\subseteq[d]}\beta_S\prod_{j\in S}x_j.
\]

全格 cell means 通过 exact Möbius inversion 得到 \(\beta\)。实现同时验证 zeta/Möbius 互逆。高阶目标限定为 \(|S|\ge3\)。符号错误计为错误支持，而不是 unsigned true positive。由于 AND basis 在分数设计下高度相干，最大列相关常饱和为 1；后续用 exact-alias fraction 作为更有辨识度的设计量。

## 6. Reference support estimand

主 estimand `META1-R1-CI95-practical-effect` 由完整面板构造，但只供评价：先在主尺度上求每格均值与 Möbius 系数，再在每格内部独立 bootstrap biological replicates 1,000 次。仅当 95% percentile interval 不跨零且点估计绝对值超过 practical threshold 时，系数进入 signed support。

- Ishizawa：log10 CFU，阈值 0.10 log10 CFU。
- Díaz：raw OD600，阈值为非空 raw response 中位数的 5%，即 0.05127。

阈值来自响应语义和实践尺度，而不是从方法表现反推。参考支持是统计 estimand，不声称为不可观测的绝对生物机制真值。

## 7. Estimand stability

Ishizawa 主支持共 137 个（73 positive、64 negative）；Díaz 共 28 个（23 positive、5 negative）。Ishizawa 各 focal landscape 的 bootstrap-seed pairwise Jaccard 中位数约 0.94，最差 landscape 的最小值 0.824；Díaz 中位数 0.883、最小值 0.803。0.8/1.2 阈值倍率几乎不改变主标签。

尺度敏感性不可忽略：Ishizawa raw 对 log10 的中位 Jaccard 约 0.654，Díaz log1p 对 raw 约 0.475。规则敏感性在 Díaz 尤其明显：CI95、sign95、BH10 分别选择 28、42、9 个支持，后两者对主规则 Jaccard 为 0.667 和 0.321。因而 estimand 足以支撑 Development，但 Díaz 的 scale/rule dependence 是明确限制。

## 8. Partial-measurement protocol

预算单位是 distinct communities。一个 community 被选择后，全部可用 biological replicates 被暴露；v1 不同时优化复制数。Ishizawa budgets 为 16/24/32/48，Díaz 为 64/96/128/192，均对应 25%/37.5%/50%/75%。uniform Development masks 使用 seeds 101/202/303/404；empty/reference cell 强制包含。

seeds 505/606 的 masks 已预生成，但在 META1 中从未用于拟合、选策略、选制度或下结论，保留给 Confirmation。

## 9. Leakage controls

`CompletePanel` 保存完整 replicates；`RevealedPanel` 只包含 mask 内的响应与由其计算的 replicate statistics；`EvaluationOracle` 独占隐藏响应和 reference coefficients。Estimator 只接受 `RevealedPanel`。Acquisition 只接受 factorial design、seed 和已揭示信息，不能接收 oracle。

调参标准为 revealed-response validation、BIC-like criterion 或 revealed-data stability。完整 reference support 从不作为训练或调参目标。针对性的接口测试证明 estimator 不能索引隐藏响应，adaptive policy 不能检查 evaluation oracle。

## 10. Historical lasso mismatch reproduction

历史 mismatch 在更强 estimand 与多预算下仍存在。uniform Lasso 的 Ishizawa 平均 signed F1 为 0.1577、response RMSE 0.1689；Díaz 为 0.0306 和 0.1234。lower-order predictor 的 support F1 按定义为 0，但 response RMSE 在 Ishizawa 为 0.1670、Díaz 为 0.1183，均可优于较高 support-F1 的 ElasticNet。

因此“预测较好但 HOI 支持错误”的现象不是旧阈值或单一 baseline 的偶然产物。与此同时，ElasticNet 和 ARD 显著改变了 baseline frontier，说明旧 tuned-lasso 数字不能继续充当唯一比较对象。

## 11. Strong baseline results

uniform ElasticNet 是跨预算最强的广义主 baseline：

| Panel | F1 | precision | recall | AP | FDR | coefficient RMSE | response RMSE | seed stability |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Ishizawa | 0.2356 | 0.2620 | 0.2713 | 0.5017 | 0.7380 | 0.4314 | 0.1916 | 0.1454 |
| Díaz | 0.0490 | 0.0524 | 0.0580 | 0.1815 | 0.9476 | 0.5102 | 0.1277 | 0.1297 |

按两 panel 等权的次要 macro F1 为 0.1423。ElasticNet 的较高 recall 带来较高 FDR，因此它不是“已解决”支持恢复，而是当前主要 Pareto 对手。

## 12. Direct support-selection baseline

ARD sparse Bayesian selection 直接作用于 relevance/support，而不只是凸 prediction loss。它在 Ishizawa 平均 F1 0.0726、precision 0.1310、FDR 0.3868、response RMSE 0.1687，不及 ElasticNet 的支持 F1。

在 Díaz，ARD 平均 F1 0.0788，高于 ElasticNet 的 0.0490。尤其 budget 192 时，ARD 达到 F1 0.2248、precision 0.7713、recall 0.2589、AP 0.2577、FDR 0.2288、response RMSE 0.0959。这证明“只需换掉弱 Lasso”在高预算 Díaz 有一定解释力，也收窄了候选论文的普适 claim；但它没有关闭 Ishizawa 低预算 design-aware 增益。

## 13. Sparse Möbius / ASMT baseline

实现了一个计算可控的 sparse Möbius IHT/BIC comparator，模拟 noisy partial AND-basis 下的稀疏恢复，但不冒充完整 FASMT/PASMT。其 uniform signed F1 在两面板均接近零，未关闭 gap。

这一结果只说明该可行 IHT comparator 不够强，不能据此推断 ASMT 在复制噪声设定下失败。Erginbas et al. 2026 已给出 exact sparse polynomial 的 FASMT `O(sd log(n/d))` 与 PASMT `O(sd^2 log(n/d))` query bounds，仍是最强算法 prior-art threat。

## 14. Noise-aware prototype

P1 使用仅由 revealed replicates 估计的方差进行 weighted ElasticNet。相对 Lasso，它在 Ishizawa 平均 +0.0592 F1，并且七个 focal landscapes 的均值均为正；Díaz +0.0058。但相对 tuned ElasticNet，Ishizawa -0.0187，Díaz -0.0126。

P1 gain 与 replicate SNR 几乎无相关（Spearman rho 0.002，p=0.987）。因此不能把其对 Lasso 的改善归因于成功利用异方差；更符合证据的解释是 ElasticNet 的 regularization/flexibility，而不是 M1 被验证。

## 15. Stability/FDR prototype

P2 在 bootstrap/stability selection 上使用严格 inclusion threshold。严格版本确实降低 empirical FDR，但主要通过拒绝选择实现，panel-macro F1 约 0.0003；较松的 0.6 threshold 的 panel-macro F1 也只有约 0.0102。

这是一条可见的 precision/abstention frontier，不是有效 recovery。当前样本预算下，单纯提高 selection frequency threshold 会同时移除多数真实效应，M2 不能作为候选独立机制。

## 16. Non-hereditary/order-aware prototype

P3 对高阶系数施加 order-dependent penalty，并允许非 heredity support。相对 Lasso，Ishizawa F1 -0.0004、Díaz +0.0224；相对 ElasticNet，分别 -0.0783 和 +0.0039。Díaz FDR 仍约 0.9407。

主 estimand 仅有 7 个 Ishizawa pure HOIs（5.11%）且 Díaz 为 0，pure-HOI 信号不足以支持 M3 为主要杠杆。strong heredity 会遗漏部分真实效应，但解除 heredity 本身没有产生可靠优势。

## 17. Adaptive acquisition

早期 `row_cosine_v0` 使用行余弦启发式，实测增加 exact aliases，作为失败版本完整保留。修正的 `d_optimal_rows` 在 column-scaled AND design 上进行 greedy pivot selection，不使用 response oracle。

全 D-opt 在 Ishizawa 将 F1 从 0.2356 提至 0.2765（+0.0409），FDR 轻微改善，但 response RMSE 从 0.1916 升至 0.2522，约恶化 32%；Díaz F1 从 0.0490 降至 0.0453，response RMSE 从 0.1277 升至 0.2536。因 guardrail 明显失败，该版本不晋级。

随后 Development 搜索 hybrid D-opt fractions 0.25/0.50/0.75。D50 在预定义因素可描述的 Ishizawa 低预算子域形成最佳 Pareto 结果，但该 fraction 是 outcome-aware Development 选择。

## 18. Hyperparameter development

uniform 比较覆盖 14 个 method families；acquisition ledger 覆盖 uniform、row-cosine v0、full D-opt 和三个 hybrid fractions。四个 budgets、四个 Development seeds 与八个 landscapes 共同形成 3,200 个 experiment rows。51,168 个 tuning-trial evaluations 全部保留；它们是条件特定评估，不是 51,168 个互异超参数元组。

所有主要 baseline 均使用相同量级的 revealed-data search。少量 ElasticNet candidate 出现 convergence warnings；最终选择配置正常返回。未以 reference-support F1 选择超参数，也未删除失败 trial。

最终 ledger 中各方法调用的累计 runtime 为 213.19 秒，GPU 使用为 0；分阶段重生成时记录的进程 peak working set 为 268.59 MiB。该累计 runtime 是逐方法计时之和，不等同于端到端 wall time。

## 19. Support F1 results

候选制度内（Ishizawa，budgets 16/24/32）共有 84 个 paired conditions：

| Policy | macro signed F1 |
|---|---:|
| uniform ElasticNet | 0.2001 |
| hybrid D50 ElasticNet | 0.2509 |
| paired mean difference | +0.0508 |

按预算的平均增益分别为：budget 16 +0.0519，budget 24 +0.0451，budget 32 +0.0554。budget 48 不属于候选制度，因为增益反转约 -0.0314。逐 pair 仅 50/84 为正，42/84 至少 +0.05，表明方差仍大，不能只报告 aggregate mean。

## 20. Precision/recall/FDR

候选制度内，uniform 到 hybrid D50 的 precision 从 0.2444 升至 0.2661，recall 从 0.2101 升至 0.3056，FDR 从 0.7556 降至 0.7339。F1 gain 的主要数量来源是 recall +0.0955，同时 precision 没有下降，因此并非通过无控制地扩大支持集获得。

绝对 FDR 仍高达 0.734，是下一阶段的核心限制。META1 只称 guardrail “相对可接受/未恶化”，不称已实现 FDR control。

## 21. Pure-HOI results

候选制度中 pure-HOI recall 在 uniform 与 hybrid D50 下均为 0.1806，无改善。Ishizawa 的七个 pure HOIs 分布于 DW039、DW100 和 DW155；Díaz 没有 pure HOI。因此最终方向不能包装为 pure/non-hereditary interaction recovery，且 P3 失败与此稀疏机制质量一致。

## 22. Coefficient RMSE

在所有方法中 coefficient RMSE 对不同稀疏支持结果并不敏感，原因是大量系数接近零且高阶误差被总体均方平均稀释。uniform ElasticNet 的 panel means 为 Ishizawa 0.4314、Díaz 0.5102。该指标作为系数幅度 guardrail 保留，但不能替代 signed-support metrics。

候选制度没有以 coefficient RMSE 选策略，详细 paired 值保留在 raw ledger。下一阶段仍应报告它，以识别通过阈值改变 F1、但系数估计整体恶化的情形。

## 23. Response RMSE

response RMSE 与 support F1 的错位在两面板均存在。lower-order predictor 支持 F1 为零，却在 Díaz 达到 0.1183 的平均 response RMSE，优于 ElasticNet 的 0.1277；Ishizawa 同样是 0.1670 对 0.1916。

候选制度内，hybrid D50 的 response RMSE 为 0.20137，uniform 为 0.19986，差 +0.00151（0.76%）。按 budget 看，16 时改善 -0.00821，24 时恶化 +0.00856，32 时恶化 +0.00418。相比 full D-opt 的 32% 恶化，这属于小幅 tradeoff，但必须在 Confirmation 中冻结为 guardrail。

## 24. Measurement efficiency

hybrid D50 在 budgets 16/24/32 的 F1 增益相近，说明结果不是单一预算尖峰；但现有 Development 没有证明“用更少 communities 达到与更高 uniform budget 完全相同的支持质量”。Figure 10 给出 budget curve，正确 claim 是 fixed-budget support recovery 改善，而不是已经建立样本复杂度或测量倍数节省。

所有选择一个 community 即揭示全部 replicates，因此计算的 measurement count 不包含对 replicate allocation 的优化。复制预算与 community 预算的联合设计留作后续问题。

## 25. Panel-specific results

Ishizawa 的 7 个 landscapes 提供重复 focal-response 单元。uniform ElasticNet 全预算平均 F1 0.2356；候选低预算制度内 uniform 为 0.2001、hybrid D50 为 0.2509。七个 landscape 的平均增益有六个为正，DW102 为负，DW155 仅轻微为正。

Díaz 的主 estimand 只有一个 landscape，且规则/尺度敏感性更强。uniform ElasticNet 全预算 F1 0.0490；hybrid D50 为 0.0233，下降 0.0257。ARD 在其高预算处明显更强。两个面板必须分别解释，不能将八个 landscapes 直接视为同质重复。

## 26. Cross-panel comparison

候选 design rule 未跨 panel 重复：Ishizawa 低预算为正，Díaz 为负。可能相关的结构差异包括维度 6 对 8、每格复制 5--12 对 3、focal-strain CFU 对 consortium OD600、support density/sign balance 以及 scale/rule stability，但 META1 没有足够独立 panels 对这些因素作因果分解。

因此跨 panel 结论是异质性，而不是总体平均成功。D-B 允许一个科学上可定义的 panel/regime 有希望，但 D-A 要求的跨独立 family 证据不成立。

## 27. Mechanism analysis

M1 noise weighting 未超过 ElasticNet且 gain 与 SNR 无关；M2 通过 abstention 降 FDR但 recovery 崩溃；M3 缺少足够 pure-HOI mass且 order penalty 不胜；M4 是唯一与候选结果一致的机制。

候选制度中 uniform 的 exact design-alias fraction 均值约 0.0168，hybrid D50 降为 0；与此同时 recall +0.0955、F1 +0.0508、seed stability +0.0653。最大相关系数自身常为 1，不能分层；exact-alias fraction 更直接解释为何 pivot rows 有价值。这仍是机制一致证据，而非随机化的因果证明。

## 28. Conditional-regime analysis

最终 regime 由以下 outcome-free 属性定义：Ishizawa 型 focal-response factorial landscape；6 个 companion factors；每格至少 5 个 replicates；log10 CFU；distinct-community fraction `<=0.50`；选中格暴露全部 replicates；一半 column-scaled greedy pivot rows、一半 uniform；ElasticNet 仅以 revealed responses 调参。

在该 regime，四个 seeds 的 mean gain 全为正，6/7 landscapes 的 mean gain 为正，15/21 个 landscape-budget cells 的 mean gain 为正，其中 12/21 至少 +0.05。regime 的文字定义不含“方法获胜”条件，但 D50 fraction 与 boundary 确实是结果后选出的。

## 29. Failure taxonomy

主要失败类型如下：

1. **support under-selection**：OMP、strict stability、IHT 多数时候漏检真实 HOIs；
2. **false-HOI expansion**：ElasticNet/weighted/order variants 在部分 masks 提高 recall 但绝对 FDR 仍高；
3. **sign error**：selected magnitude 不等于 signed correctness；ledger 单列 sign flips；
4. **pure-HOI miss**：绝大多数 pure effects 未因 D50 得到改善；
5. **response/support mismatch**：lower-order 模型预测好但结构 F1 为零；
6. **design over-specialization**：full D-opt 去 alias 却严重损伤 response coverage，尤其 Díaz；
7. **estimand sensitivity**：Díaz 的 rule/scale 变化可大幅改变 reference support。

机器可读计数在 `aggregated/failure_taxonomy.csv`。

## 30. Selection-bias audit

每 panel 尝试两个尺度、三种支持规则和两个固定阈值倍率敏感性；14 个 uniform method families、6 种 acquisition policies（含 uniform）、4 budgets、4 Development seeds。结果后决策包括修正 row-cosine、搜索 D25/D50/D75、选择 D50，并把 candidate boundary 限定到 Ishizawa budgets 16/24/32。

因此 +0.0508 是 Development estimate，可能乐观。它不能作为无偏 confirmation effect。seeds 505/606 未使用，为一次性检验保留。所有 3,200 experiment rows 与 51,168 tuning evaluations 均保留，包括失败/中性配置。

## 31. Strongest evidence FOR continuation

最强支持证据不是单一最佳行，而是机制和重复性的组合：在 84 个配对条件组成的可定义 regime 内，F1 +0.0508；四个 Development seeds 均值全部为正；6/7 landscapes 与三个 budgets 均值方向为正；precision、FDR 和 seed stability 同时改善；response RMSE 只轻微恶化；exact aliases 从 0.0168 降为 0。

该证据足以支持一次严格、低成本的 Confirmation，而不是继续无边界搜索。

## 32. Strongest evidence AGAINST continuation

最强反证有四点：Díaz 上候选 F1 和 response RMSE 均变差；逐 mask 只有 50/84 为正，方差不低；budget 48 优势反转；候选 fraction/regime 是 Development 结果后选择。其次，绝对 FDR 仍约 0.734，pure-HOI recall 不变，Díaz reference 又高度 rule/scale-sensitive。

如果 reserve seeds 不能重复 landscape-macro gain，或 prior-art audit 显示同一 noisy-support-aware design 已被覆盖，应停止论文方向而不是再次移动制度边界。

## 33. Prior-art collision

ASMT 已占据 coherent AND basis 中 adaptive sparse polynomial learning与 query complexity；Kang et al. 和 Wendler et al. 占据 sparse Möbius/set-function recovery；classical D-optimal/fractional factorial design 占据设计几何；Suzumura et al. 已研究 sparse high-order interactions 的 selective inference。META1 的差异只可能位于 replicated biological response noise、明确的 signed-support estimand、现实 partial measurement 与错误/预测 guardrails 的交叉处。

当前 hybrid D50 只是简单设计规则，没有新理论，也未跨 panel 成功。因此 paper-ready novelty 尚未建立。最强威胁是 ASMT 与 classical optimal-design 的组合，而不是当前 IHT comparator 的数值结果。

## 34. Development classification

**D-B PROMISING。** D-A 不成立，因为没有跨两个 panels/独立 families 的一致优势，候选又经过 outcome-aware Development selection。D-C 过于保守，因为 Ishizawa regime 内存在材料性、机制一致且跨 seed/多数 landscapes 重复的平均提升，主要 guardrails 未失控。D-D 也不成立，因为 design-aware measurement 提供了可确认的杠杆。

该 classification 的含义是“值得一次冻结后的 Confirmation”，不是“方法已经成立”或“可投稿”。

## 35. Candidate paper shape

若 Confirmation 成功且 novelty audit 通过，候选问题可表述为：**replicated focal-response factorial landscapes 中，用 design-aware partial-factorial measurement 提高可靠 signed high-order support recovery**。

claim 应限定在 noisy partial factorial measurements、明确的 AND/Möbius estimand 与可描述的低预算 regime。不能声称普适 microbial prediction、发现因果生态机制、FDR 已受严格控制，或优于完整 ASMT。

## 36. Exact next action

先冻结当前 final SHA、`hybrid_d50`、Ishizawa regime、R1 estimand 和 budgets 16/24/32。随后做一次 bounded prior-art collision audit，范围仅限 noisy/adaptive sparse Möbius recovery、support-aware fractional factorial design 和 error-controlled high-order interaction selection。

若未发现直接覆盖，再只运行 reserve seeds 505/606：candidate `hybrid_d50 + ElasticNet`、primary comparator `uniform + ElasticNet`、secondary comparator `uniform + ARD`。以 paired landscape-macro signed F1 为主指标，同时报告 precision/recall/AP/FDR、response/coefficient RMSE、seed stability 和 runtime。不得重调 D-opt fraction、scale、threshold 或 regime boundary。META1 本阶段不消耗 reserve；待用户审核后再进入该动作。
