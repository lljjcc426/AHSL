# AP1.0 Feldera / DBSP 审计

冻结对象：<https://github.com/feldera/feldera>，`v0.338.0`，提交 `718320cf1deb49c51f8528f2469fbfc7aac995db`。理论依据为 [DBSP: Automatic Incremental View Maintenance for Rich Query Languages](https://docs.feldera.com/vldb23.pdf)。

## 语义与固定点

DBSP 以 Z-set 表示带整数权重的集合/多重集合；负权重自然表达删除。关系算子被表示为电路并通过微分/积分变换增量化。递归查询先由内部固定点电路表达，再以 nested streams 维护外层输入时间与内层固定点迭代的变化。

该理论保证精确增量语义和工作量方面的渐近关系，但不等于低状态。DBSP 论文明确说明：递归增量电路会缓存先前时间戳的固定点迭代变化，空间用量与内层固定点迭代数相关。这正是 AP1.0 合理审计而不能预设为缺陷的理论来源。

## 状态实现

冻结代码中的 DBSP 以 batch、indexed/non-indexed Z-set、trace 和 spine/merge 路径组织状态；同键权重可 consolidation，零净权重可在合并后消除。实现还包括缓存、批大小、merge 和存储相关配置。状态大小受逻辑差分历史、批次组织、合并/压实、索引与递归嵌套共同影响，不能由单次 RSS 直接识别。

## 批与 profiling

DBSP 的输入和 operator 接口围绕 batches 执行，Feldera 上层提供 pipeline/runtime metrics；代码库也含 trace/batch 级 benchmark 和存储路径。若后续有独立、被授权的系统复现实验，应直接采集 batch/trace/storage counters，而不是仅做进程级 RSS 比较。

## 本阶段系统访问结果

依赖及 Rust 1.93.1 已固定，旧 MinGW 问题通过 GCC 16.2.0 与 `CFLAGS=-std=gnu11` 排除。最终失败稳定发生于 `feldera-samply` 的 Unix `nix` API（`clock_gettime`、`getpid`）在 native Windows target 不存在。WSL 因主机 HCS 服务不可用无法启动。没有修改 Feldera 源码绕过该依赖，因为那会把本阶段变成移植工程并破坏“当前系统”的公平版本冻结。

因此 Feldera 只提供实现/理论审计，不提供性能行。该限制削弱“现代系统”外推范围，但不改变 Gate 决策：FlowLog 数据中没有潜在强残差，所以不满足 AP1.0-B 的前提。
