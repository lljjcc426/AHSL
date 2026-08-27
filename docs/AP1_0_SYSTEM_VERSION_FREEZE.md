# AP1.0 系统版本冻结

实验日期：2026-08-27（Asia/Shanghai）。

## 机器

- ASUS TUF Gaming F15 FX507VV
- Intel Core i9-13900H，14 核、20 逻辑处理器
- 31.64 GiB RAM
- Microsoft Windows 11 家庭版中文版，10.0.26200，x64
- Python 3.11.5
- GPU 未使用

## FlowLog（实际执行）

- 仓库：<https://github.com/flowlog-rs/flowlog>
- 提交：`6c111b729e4bf8bffb5037b85b894031786140cc`
- 同一提交标签：`flowlog-compiler-v0.5.0`、`flowlog-runtime-v0.3.0`、`flowlog-build-v0.4.0`
- Rust：`rustc 1.89.0 (29483883e 2025-08-04)`，GNU target
- C 工具链：MinGW-w64 UCRT GCC 16.2.0
- 运行依赖：`differential-dataflow 0.25.1`、`timely 0.31.0`（由冻结的 `Cargo.lock` 解析）
- 编译：`cargo +1.89.0 build --release --locked`
- 查询生成：`flowlog-compiler PROGRAM -F FACTS -D OUTPUT -o BINARY --mode datalog-inc|datalog-batch -P`
- 特性：release、locked、FlowLog profiling；工作线程为 1 或 4
- 增量控制：`datalog-inc`
- 同引擎重算控制：`datalog-batch`

两种控制使用相同 FlowLog 提交、解析器、查询、运行时、事实快照和机器，仅执行模式不同。

## Feldera / DBSP（实现审计，未执行性能矩阵）

- 仓库：<https://github.com/feldera/feldera>
- 标签：`v0.338.0`
- 提交：`718320cf1deb49c51f8528f2469fbfc7aac995db`
- Rust：`rustc 1.93.1 (01f6ddf75 2026-02-11)`，GNU target
- C 工具链：MinGW-w64 UCRT GCC 16.2.0，`CFLAGS=-std=gnu11`
- 尝试命令：`cargo +1.93.1 build --release --locked -p dbsp --tests`
- 结果：原生 Windows 构建在 `feldera-samply` 停止；该 crate 导入 `nix::time::{ClockId, clock_gettime}` 和 `nix::unistd::getpid`，这些接口在当前 native Windows target 不可用。
- WSL：已安装发行版但主机 HCS 服务返回 `HCS_E_SERVICE_NOT_AVAILABLE`，无法作为执行环境。

这是一项精确的系统访问限制。它没有被归入科学残差，也没有触发 AP1.0-B，因为已执行的 FlowLog 数据中不存在“潜在强残差等待第二系统确认”。

## 可选第三系统

未加入。继续扩展引擎会增加工程面，而当前主实验已经因缺少材料性残差触发停止条件。

机器可读冻结见 `results/ap1_0/raw/system_metadata.csv`。
