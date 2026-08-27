# AP1.0 风险登记

| 风险 | 实际状态 | 对结论的影响 | 处理 |
|---|---|---|---|
| Feldera 无法在 native Windows 构建 | 已发生 | 限制跨引擎外推 | 精确冻结错误；不改源码移植；不把它当科学残差 |
| WSL 不可用 | 已发生，HCS 服务错误 | 无法补充 Linux Feldera 运行 | 记录平台限制；停止扩展工程面 |
| LDBC 只有官方 toy | 已发生 | Route B 只支持语义复现，不能支持现实规模性能 | 报告中明确降级，不夸大 |
| FlowLog engine-state counter 不可得 | 已发生 | 无法计算物理/逻辑 state amplification | 写 `NA`；不从 RSS 推断 |
| batch-mode post RSS 采样偏低 | 已观察 | post ratio 可能虚高 | 只作诊断，材料性以内存峰值比和进程内增长为主 |
| p99 样本较短 | 已发生，每关键单元 15 个 measured batches | 尾部估计不适合精细统计 | 保留原始值；只判 2× 级大效应，不过度解释 |
| 合成图更新可能落在输出不敏感边 | 已观察部分派生变化为 0 | 削弱删除工作量判断 | 另设 delete-heavy stress；仍不把输出变化当内部 work |
| Polonius 大 fixture 适配成本过高 | 冻结前 pilot 发生 | 大规模程序分析覆盖受限 | 正式矩阵改用官方小 fixture并记录，不混入 pilot |
| 编译时间缺失（reachability） | 两个早期 pilot 的解析器在元数据落盘前停止 | 不影响核心 T_update/状态判断 | 保持 `NA`，避免为非核心字段重复编译 |
| 系统结果只来自一台 Windows 笔记本 | 已知 | 不支持跨硬件普遍结论 | 决策仅绑定冻结系统和矩阵 |

剩余不确定性不能把 NO-GO 自动改成 HOLD。AP1.0-B 要求先存在潜在强残差；本轮 FlowLog 没有这样的候选。最合理的下一步是按 stop-loss 返回项目评审，而不是继续加环境或基准。
