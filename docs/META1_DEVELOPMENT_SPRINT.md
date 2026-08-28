# META1 Development Sprint：复制噪声下的微生物高阶交互支持恢复

计划日期：2026-08-31 至 2026-09-15（12 个工作日）

## 1. 精确目标

在完整因子 microbial community-function landscape 上模拟部分组合测量，从 biological replicates 中估计噪声，恢复 order≥3 的 signed Möbius support。META1 是 Development，不以当前 SOTA 或论文结论为门槛。

## 2. 冻结 benchmark

1. **Ishizawa 7-strain panel：** 127 个非空 communities、2377 个 CFU measurements；按 focal strain 形成七个 64-cell landscape，每格 5–12 replicates。
2. **Díaz-Colunga 8-strain panel：** 全部 256 个 *P. aeruginosa* consortia、3 biological replicates；主响应先用 OD600 biomass，其他波长只作预先记录的 sensitivity analysis。

完整面板用于构造参考系数及 held-out response；训练时只暴露预算内的组合和其复制测量。这里的“support truth”是由完整面板与预先声明的不确定性规则得到的统计 estimand，不宣称等同于不可观测的绝对生物机制真值。

## 3. 指标

**Primary metric：** 固定 measurement fraction/budget 下，order≥3 的 macro signed-support F1；先在 landscape 内计算，再在 panel 间宏平均。

**Guardrails：**

- empirical FDR / signed precision；
- signed recall 与 average precision；
- pure-HOI recall；
- coefficient RMSE；
- held-out response RMSE；
- panel/scale/seed stability；
- measurement count 与运行时间。

不要求所有 guardrail 同时改善。任何主指标增益必须报告对应 FDR、response RMSE 和成本。

## 4. 强 baseline 集

- tuned lasso / elastic net；
- OMP；
- weak-heredity sparse interaction model；
- stability selection / bootstrap lasso；
- 可在该噪声设定运行的 sparse Möbius / adaptive-query baseline；
- response-only low-order baseline，用于显示结构指标与预测指标的错位。

历史上最强的可执行 support baseline 是 tuned lasso（budget 48：F1 0.235、AP 0.506）。META1 不能只和默认 lasso 比，必须给上述强 baseline 合理调参预算。

## 5. 机制假说

AND/Möbius 高阶列的相干性、replicate-dependent/heteroscedastic noise 与 pure/non-hereditary interactions 共同导致以 response loss 选模的 lasso/OMP 在低预算时获得较低 prediction RMSE，却漏掉大量真实强支持。使用复制噪声权重、支持稳定性/错误率控制和允许非遗传 support 的估计器，应在该机制活跃的制度提升 signed-support F1。

机制制度可由方法结果之外的属性描述：measurement fraction、design coherence、replicate SNR、order 分布和 pure-HOI 比例。禁止以“本方法胜出”定义制度。

## 6. 允许的 Development 搜索

- 响应尺度：raw/log 与预声明变换 sensitivity；
- 模型：lasso、elastic net、OMP、遗传/非遗传稀疏模型、noise-weighted estimator；
- loss 与 penalty：replicate variance weighting、group/order penalty、stability/FDR threshold；
- 采样：uniform、order-balanced、合理 adaptive acquisition；
- 超参数、optimizer/solver 配置、bootstrap 次数和实现优化；
- measurement budget、seed 与机制属性分层。

所有尝试保留配置、数据属性、seed、成功/失败结果。META1 不按最终胜负删掉运行。

## 7. 十二日计划

| 工作日 | 工作包 | 完成证据 |
|---:|---|---|
| 1 | 获取并统一两个公开面板；明确 community bitmask、replicate、response | 两个 adapter 与字段说明；无数据泄漏 |
| 2 | 冻结 support estimand、预算 mask、seed、raw/log sensitivity | 数据/estimand 协议与首轮统计 |
| 3 | 复现 lasso、elastic net、OMP | 调参曲线和 primary/guardrail 表 |
| 4 | weak-heredity、stability selection、可行 sparse Möbius baseline | 同预算公平 baseline 表 |
| 5 | noise-weighted loss 原型 | 单独归因于 replicate variance 的对照 |
| 6 | stability/FDR support 原型 | precision–recall/FDR 路径 |
| 7 | non-hereditary/group-order 变体 | pure-HOI 与普通 HOI 分层结果 |
| 8 | uniform 与机制合理 adaptive measurement | 固定预算比较，不增加隐性测量 |
| 9 | 合理超参数与实现调优；记录失败变体 | 完整开发日志 |
| 10 | 机制分层：SNR、coherence、budget、pure-HOI | 预定义属性上的 conditional analysis |
| 11 | 跨面板、跨尺度和 seed 复核；误差 taxonomy | Pareto 表和失败实例 |
| 12 | D-A/B/C/D 判定，若有前景则冻结候选制度供后续 Confirmation | 决策报告与下一阶段定义 |

## 8. Sprint 判定

- **D-A 强信号：** 在两个面板或两个预先声明的独立 landscape family 上均出现重复、方向一致的条件优势；机制分层与改善一致，主指标提升具有材料性，FDR/response RMSE guardrail 可接受。
- **D-B 有希望：** 机制得到支持，且至少一个科学上有意义、可独立定义的 panel/regime 上，对调优强 baseline 有重复的主指标改善，guardrail 可接受；允许另一个 panel 中性。
- **D-C 模糊：** 改善依赖 seed、support threshold、response scale 或 outcome-only 子集，尚不能排除选择/噪声；只允许一个很小的后续澄清。
- **D-D 无开发杠杆：** 数据审计使第二面板/estimand 无效，或在合理 baseline 调参后，noise weighting、support stability/FDR、non-hereditary structure（至少三类机制不同干预）均不能产生可重复材料性改善。

“材料性”不预设统一百分点：用 paired seed variation、baseline maturity 及 precision–recall/FDR Pareto 判断，并在 Day 2 记录最小实践相关差异的解释。不得事后降低标准。

## 9. 停止条件

发生任一条件即停止或判 D-D：

1. 第二面板不能合法形成所声明的 support estimand，导致证据重新退化为单一且不可验证的面板；
2. 完整数据上的 support 在 replicate/bootstrap 下本身不稳定，无法提供可评价目标；
3. 至少三类合理干预加公平 baseline 调参仍无可重复的 primary-metric 改善；
4. 发现当前工作已在同样两个真实面板、相同 partial-measurement protocol、相同不确定性目标上完成近同题贡献。

## 10. META1 的精确第一步

下载并固定 Díaz-Colunga artifact 与 Ishizawa 现有数据资产，建立只负责 community-bitmask、replicate 和 response 的最小 adapter；随后输出两个面板的 cell/replicate 完整性与 support-estimand 稳定性表。此处不添加仪式化 hash 或与实际风险无关的 smoke test。
