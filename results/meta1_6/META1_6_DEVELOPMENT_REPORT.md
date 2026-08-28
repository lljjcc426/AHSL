# META1.6 Development Report

## 1. Executive decision

最终分类为 **D-C**。证据阈值由预注册规则机械给出，而不是按结果修改。

## 2. Modified problem

固定 d=6 Boolean 行池，在预算 16/24/32 下恢复 42 个三阶及以上 AND 系数的带符号支持；21 个一至二阶项是 nuisance。

## 3. Why broad META1 novelty was insufficient

META1 的一般稀疏回归比较没有把设计目标、目标/干扰不对称和符号恢复事件合成一个可审计对象。

## 4. AND dictionary structure

使用 64 个 Boolean 行与 63 个非空 AND 列；空行固定测量并承担基线锚定。

## 5. Target/nuisance decomposition

目标为阶数>=3，nuisance 为阶数1-2；主指标只评价目标支持和符号。

## 6. Dense-nuisance identifiability

预算16的 D-opt 设计 rank(X_L)=15，投影后目标秩=0、零残差目标列=42。因此 N0 不能作为主问题。

## 7. Sparse/regularized nuisance alternatives

N1 对全部63项联合稀疏惩罚；N2 对低阶块作 ridge 残差化，仅作为敏感性分析。

## 8. Frozen nuisance formulation

冻结 N1：Lasso 联合估计，评价仅作用于高阶符号支持；不假设 heredity。

## 9. Structural identifiability

原始秩、投影秩、零列、目标-目标别名、目标-低阶别名、互相关与限制奇异值均逐设计记录。

## 10. Sparse null-space analysis

q=1,2,3 穷举，q=4 固定抽样128组；只把实际线性依赖计为失败。

## 11. Recoverability phase diagram

相图跨 k_H、k_L、SNR 和预算；奇异场景未被删除。

## 12. Support ensemble Pi

Pi 与 Ishizawa 标签独立：高阶支持按阶数轮转平衡抽样，低阶均匀抽样，正负号平衡，效应由 SNR 网格控制。

## 13. Prior sensitivity

比较 sparser、primary、denser、weak 四种先验；结果见 aggregated/prior_sensitivity.csv。

## 14. Primary estimator decision

冻结 Route B：Lasso 目标与 KKT 条件直接对应。ElasticNet 只做 transfer 检查。

## 15. Sign-recovery objective derivation

对每个支持/符号场景直接模拟高斯 score，并同时检查活跃符号与目标非活跃 KKT 不等式；lambda 在预设三点路径上取最好事件概率。

## 16. Faithful HILS baseline

HILS 使用相同 Pi、lambda 路径和噪声抽样，但要求全部63项的支持与符号正确，最后对场景取均值。

## 17. DCD baseline

DCD 由支持子 Gram 最小特征值与 irrepresentability margin 的乘积构成，奇异支持计零。

## 18. Classical comparators

比较 uniform、D-opt、hybrid_d50、HILS、DCD。

## 19. Modified objective

新目标为高阶 target-only KKT 概率的 0.8 mean + 0.2 CVaR20，并把奇异场景集成成零分。

## 20. Row-search algorithm

Boolean 可行行池上的确定性多起点交换；强制空行，2 个起点、每轮16个 proposal、patience=2。

## 21. Synthetic validation

candidate_full-HILS 的跨预算 synthetic signed-F1 差为 -0.0207。

## 22. Random-design cloud

每个预算24个随机可行设计；同时记录 objective、synthetic signed F1 与 Ishizawa macro F1。

## 23. Objective/recovery alignment

跨全部随机设计 objective 对 real macro F1 的 Spearman rho=0.195。

## 24. Real Ishizawa Development results

| budget | design_method | primary_f1 | precision | recall |
| --- | --- | --- | --- | --- |
| 16 | D-opt | 0.2074 | 0.3251 | 0.2301 |
| 16 | HILS | 0.2013 | 0.3075 | 0.1973 |
| 16 | candidate_full | 0.1598 | 0.2066 | 0.1835 |
| 16 | uniform | 0.1212 | 0.2015 | 0.1062 |
| 24 | D-opt | 0.1952 | 0.2415 | 0.2081 |
| 24 | HILS | 0.1602 | 0.2074 | 0.1464 |
| 24 | candidate_full | 0.0908 | 0.1184 | 0.0832 |
| 24 | uniform | 0.1214 | 0.2543 | 0.1050 |
| 32 | D-opt | 0.2078 | 0.2534 | 0.2404 |
| 32 | HILS | 0.2175 | 0.2509 | 0.2370 |
| 32 | candidate_full | 0.2103 | 0.2547 | 0.2250 |
| 32 | uniform | 0.1860 | 0.2226 | 0.1924 |

## 25. Per-landscape heterogeneity

所有7个 landscape、4个 Development seed 都保留；配对差异见 figures/per_landscape_delta.png。

## 26. Guardrails

主比较按 landscape-macro signed F1；同时报告 precision、recall、FDR、sign flips，不能用单个 landscape 胜利替代总体证据。

## 27. Díaz diagnostic

Díaz 仍只作历史负向诊断；META1.6 未用其结果调 Pi、目标或搜索。

## 28. Estimator-transfer analysis

HILS 与 candidate_full 额外用 ElasticNet 重估；KKT 目标仍属于 Lasso，二者不被宣称为同一事件。

## 29. Ablations

A1 uniform；A2 D-opt；A3 hybrid_d50；A4 HILS；A5 去除 target/nuisance 不对称；A6 仅 target-aware mean；A7 不集成奇异失败；A8 full。DCD 单列。

## 30. Scaling

d=7/8 只做结构与单次评分计时，不把小规模结果外推为可扩展性证明。

## 31. Selection-bias audit

Pi、主指标、预算、开发 seed 和决策阈值在读取 Ishizawa 开发 F1 前冻结；真实 support frequency 未进入 Pi。

## 32. Strongest evidence FOR novelty

目标/干扰不对称、阶数平衡支持 Pi、奇异失败积分与 Boolean 行约束被放在同一个可计算目标中。

## 33. Strongest evidence AGAINST novelty

核心仍建立在经典 Lasso KKT/HILS 与行交换上；增量主要是问题特化组合，不是新的恢复定理。

## 34. Strongest evidence FOR continuation

真实开发集 candidate_full-HILS 平均差=-0.0394，并与 synthetic/随机云证据联合判断。

## 35. Strongest evidence AGAINST continuation

真实支持较稠密，预算远小于63列；目标概率下尾大量为零，限制了优化目标的分辨率。

## 36. Final D-A/B/C/D decision

**D-C**。D-A 要求真实差>=0.03、synthetic 差>0、real alignment rho>0.2；D-B/C/D 按脚本中的冻结分支判定。

## 37. New reserve status

未创建、未生成、未运行任何新 reserve；退役的505/606未被读取或再生。

## 38. Exact next action

停止该设计方法方向，保留结构不可识别性结果作为负结果。
