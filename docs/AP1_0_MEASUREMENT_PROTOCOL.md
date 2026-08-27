# AP1.0 测量协议

## 对照与阶段

每个 FlowLog 单元比较同一提交生成的 `datalog-inc` 与 `datalog-batch`：前者在一个进程中提交 `+1/-1` 事务，后者在每批后的当前数据库快照上从头计算。解析器、查询、事实、输出语义、硬件和 worker 数保持一致。

阶段分离为：`T_compile`、初始物化/固定点、每批 `T_update`。编译结果在不同重复间复用。由于最早两个 reachability pilot 在编译完成后、元数据落盘前被旧版 duration 解析器中止，该查询的 `compile_ms` 为 `NA`；没有为填补一个非核心字段而重复编译。其他程序的生成/编译约为 76–95 秒/模式。

## 正确性

每批把增量输出的带符号差分累积成当前关系，再与 fresh batch-mode 的完整输出按关系、按行、去重排序后精确比较。集合关系不使用容差；整数聚合同样逐值精确比较。任何不一致都会阻止性能解释。正式矩阵全部一致。

## 延迟与吞吐

每配置 6 批：batch 0 为 warm-up，batch 1–5 计量。关键单元完整重复 3 次；探索性 SSSP、stress 和 4-worker 因果诊断各 1 次。保留每批 `update_ms`，按 workload × scale × regime × workers 汇总 median、p50、p95、p99、mean 与范围。吞吐为输入变化数除以更新时间，只作辅助指标。

## 内存

Windows 上以 `psutil` 轻量采样引擎进程 working set：

- `M_load_peak`：初始化期间峰值；
- `M_steady`：批提交前采样；
- `M_update_peak`：传播期间峰值；
- `M_post`：提交完成后的最后稳定采样；
- `transient_update_memory = M_update_peak - M_steady`；
- `retained_growth = M_post - M_steady`。

这些都是进程 RSS/working-set 诊断量。FlowLog 当前生成程序虽输出 profiler 日志，但本次可用日志没有直接给出逐批 maintained-state bytes。因此 `engine_state_mb`、arrangement bytes 和 state amplification 均写 `NA`，不从 RSS 反推。

特别地，batch-mode 进程结束前的最后采样可能偏低，所以 `M_inc_post/M_recompute_post` 仅作诊断，不被解释为内部状态放大。更可靠的材料性内存筛查采用同批进程峰值比和增量进程内 retained growth。

## 工作量与删除

记录输入 insert/delete 数和可观察输出差分数。内部 differential tuples、retractions、re-derivations、arrangement size、iterations、frontier size、worker utilization 在此次公开接口中均为 `NA`。`derived_changes/input_delta` 只称“可观察派生输出变化放大”，不替代内部删除工作。

## 资源、统计与停止

- 固定种子：`20260827`
- worker：核心为 1；reachability 和 connected components 各增加 4-worker 诊断
- GPU：0
- 正式运行峰值引擎 working set：23.703 MiB
- CPU 消耗：按构建和运行墙钟乘活跃并行度做保守上界，少于 8 CPU-hours
- 存储：远低于 100 GB

关键结论只使用重复单元的中位数和范围。短序列 p99 是经验分位数，不给出虚假的高精度置信结论。没有为低于 10–20% 的差异赋予科学意义，也没有将跨工作负载平均成一个冠军分数。
