# META0：四项 Development shortlist

日期：2026-08-28

## Rank 1 — 因子微生物群落中的高阶交互支持恢复（88/100）

- **精确问题：** 从只测部分组合、带 biological replicate noise 的完整因子 microbial community-function landscape 中，恢复 order≥3 的 signed Möbius support，并量化不确定性。
- **为何值得开发：** 两个公开完整面板允许模拟测量预算并用未采样组合检验；旧基线在 budget 48 时 support F1 仅 0.235，方法几乎未开发。
- **旧 gate 低估：** 把“只有一个域”当成硬失败，并用 response RMSE 掩盖 support estimand 的崩溃。
- **可能主张：** 在由复制 SNR、设计相干性和非遗传高阶效应定义的制度中，replicate-aware uncertainty control 提高 signed-support F1，同时维持 FDR 与 response RMSE。
- **最强威胁：** Adaptive Sparse Möbius Transform；若其在真实 noisy partial panels 上经合理改造已同样强，则 novelty 和效果空间缩小。
- **1–3 周杠杆：** 很高；可直接比较 weighted loss、stability/FDR、非遗传 sparse estimator 与 adaptive acquisition。

## Rank 2 — fuzz-found 真实漏洞的完全验证修复（82/100，备选）

- **精确问题：** 对真实 fuzz-found C/C++/多语言漏洞，利用 failure-boundary evidence 生成能通过 build、PoC、fuzz 与 differential verification 的补丁。
- **为何值得开发：** 安全价值直接，验证器客观，crash-stopping 与真正 verified patch 有历史差距。
- **旧 gate 低估：** 把 E4 setup 与“当前 agent 尚未执行”当成近似科学否定。
- **可能主张：** 对预先定义的某类 failure-boundary 漏洞，以反例状态摘要改善 fully verified repair rate/成本 Pareto。
- **最强威胁：** ContraFix 和 PatchEval 上的当前强 agent 已覆盖差分运行证据与 mutation。
- **1–3 周杠杆：** 中高但方差大；相当预算会花在容器和 agent 执行。

## Rank 3 — 语义约束模型合成（75/100）

- **精确问题：** 将自然语言组合优化需求转成语义正确的 MiniZinc/CPMpy/CP-SAT 模型，而非仅可运行或有可行解。
- **为何值得开发：** CP-Bench 提供可执行真值，solver 给客观反馈，工程成本低。
- **旧 gate 低估：** 在方法开发前要求当前模型 residual，未先建立语义错误 taxonomy。
- **可能主张：** 对一种可预声明的量词/索引/目标错配，用结构化语义 obligations 改善独立正确性。
- **最强威胁：** CP-Agent 的 101/101 与 CP-SynC 的 synthesized checker、多轨迹选择直接压缩路线。
- **1–3 周杠杆：** 中高；若两天 taxonomy 后找不到新机制，应快速停止。

## Rank 4 — canonical/dynamic reusable hypergraph decompositions（73/100）

- **精确问题：** 避开已占据的 rerootable HD，研究可规范表示、跨查询复用或更新下可维护的 HD/GHD/FHD 家族。
- **为何值得开发：** 理论深度和数据库接口长期存在，计算实验门槛低。
- **旧 gate 低估：** 纯理论不需要 ML residual，也不应因缺应用 benchmark 被自动否定。
- **可能主张：** 新分解对象/等价类的结构定理，加可证明算法和实证 width/更新代价。
- **最强威胁：** 2026 Rerootable Hypertree Decompositions 与既有 incremental GHD/FHD 算法。
- **1–3 周杠杆：** 中；能否找到未占据、非平凡定理命题高度不确定。

## 唯一选择

Rank 1 为 S1 因子微生物高阶交互恢复。Rank 2 F1 记录为唯一备选。其余两项只保留排序，不并行启动。
