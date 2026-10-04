# F1-D1 Development Report

## 1. Executive decision

**F1-D1-C（基础设施限定的歧义结论）**。研究对象和协议可执行化已完成，但当前主机无法启动 Linux 容器，且存储低于官方最小要求；因此没有把任何 F9 记录伪装成 repair failure，也没有声称存在 intervention signal。

## 2. Exact research problem

目标是以固定预算产生通过 build、原始 PoC、benchmark fuzzing 和 white-box differential verification 的 C/C++ 漏洞补丁；V4 是唯一主成功。

## 3. Benchmark choice

主基准为 AutoPatchBench-Lite；当前 artifact 的实际 Lite 列表为113例。Lite 只代表单 hunk root-cause 路线。

## 4. AutoPatchBench setup

官方 PurpleLlama commit `4be64c3a24442b51c76175e6ec67722cc3f5fe38` 已做 sparse checkout。官方要求 Podman/Linux、约2TB用于 Lite；当前 Windows 主机无 Docker/Podman，WSL2 报虚拟化不可用，E盘剩余约268GB。

## 5. Secondary benchmark route

SEC-Bench 支持 patch/poc 任务与 SWE-agent、OpenHands、Aider、smolagents，但要求 Python>=3.12、Docker 和>200GB。其正确性语义与 AutoPatchBench 的固定程序 differential verifier不同，只能作为后续独立安全修复路线。

## 6. Agent/model access

Codex CLI 0.149.1 使用 ChatGPT 登录可启动；gpt-5.6-luna ephemeral 只读探针最终返回 ACCESS_OK，但经历 WebSocket 超时和 HTTPS 回退。API key 型官方 reference agent 当前不可执行。

## 7. Frozen baseline

预注册候选 baseline 为 Codex CLI 0.149.1 + gpt-5.6-luna，同一 vulnerable-container workspace；每实例1条 outer trajectory、1个候选补丁、3600秒，plugins disabled、ephemeral。CLI 不暴露 sampling temperature 或硬 token cap，因此记录实际 token，并以同一 trajectory/wall envelope 做配对。由于容器未通过 sanity，该配置尚未产生 scientific baseline。

## 8. Development/untouched split

按 project 整组、固定 seed 20260828 生成：Development 25例、8个项目；untouched 87例。10445 因 schema 审计标为 ANALYSIS-EXPOSED。

## 9. Verification protocol

V0 patch produced；V1 build；V2 original crash stopped；V3 benchmark fuzz；V4 differential behavior。任一失败终止后续阶段。

## 10. Ground-truth firewall

适配器不读取 `*-patch.json`，generation metadata 丢弃 fix/fix_commit；fixed container、differential label 和 reference state 只属于 EvaluationOracle。

## 11. Infrastructure sanity

未通过：无容器运行时、WSL2 虚拟化不可用、存储不足。因而 vulnerable build、crash reproduction、reference-patch evaluator sanity 和 final verifier 均未运行。

## 12. Baseline repair success

不可估计；科学分母为0。25个预注册 Development 实例均为 INFRA-BLOCKED，而非 agent failure。

## 13. Verification funnel

V0-V4 均无合格 trajectory；baseline_funnel.csv 明确记录每阶段25个 infrastructure-blocked。

## 14. Failure taxonomy

只有 F9 infrastructure 记录；不存在可用于方法选择的 F0-F8 分布。

## 15. Semantic failure taxonomy

未建立；没有 candidate patch 或 V3/V4 失败证据。

## 16. Patch-pattern analysis

未建立；patches.csv 为空，不能推断 guard、clamp 或 multi-location pattern。

## 17. Project/crash-type heterogeneity

Development 项目：c-blosc2, librawspeed, libredwg, libxml2, open62541, ots, php-src, yara。crash 类型：Heap-buffer-overflow READ 1, Heap-buffer-overflow READ {*}, Heap-buffer-overflow WRITE 1, Heap-buffer-overflow WRITE 2, Heap-double-free, Heap-use-after-free READ 4, Heap-use-after-free READ 8, UNKNOWN READ, Use-after-poison WRITE 2, Use-of-uninitialized-value。这里只是预注册覆盖，不是效果异质性。

## 18. Current prior-art boundary

AutoPatchBench 官方 reference agent只在 generation 时使用 build+原始 crash；其公开案例显示 V2 与完整正确性存在明显落差。

## 19. ContraFix overlap

ContraFix 已占据 failure-boundary mutation、crash/non-crash state differential、repair specification 和 skill reuse。当前没有基线机制证据，故未进行8-15篇候选机制深审。

## 20. Selected mechanism

未选择。基础设施 F9 不能支持 M1/M2/M3 任一科学机制。

## 21. Intervention 1

未运行；禁止在真实 failure taxonomy 前设计。

## 22. Intervention 2

未运行。

## 23. Intervention 3 if needed

未运行。

## 24. Same-backbone comparisons

协议与测试已实现，但没有 paired outcome。

## 25. Fully verified success

NA；不能把0/0写成0%。

## 26. V2->V4 promotion

NA；无 V2-valid patch。

## 27. Guardrails

build、repro、fuzz、differential、tests、patch size 和修复成本均未产生；基础设施阻塞率为100%（25/25 Development）。

## 28. Cost analysis

repair model calls/tokens/cost为0。agent access probe使用1次 ephemeral 调用、6366 tokens，不属于 baseline。

## 29. Agent stochasticity

未估计；没有 baseline trajectory。

## 30. Mechanism analysis

未进行；不存在合法 failure evidence。

## 31. Conditional regime analysis

未定义；不能以未来 candidate 胜负定义 regime。

## 32. Failure cases

25例均为环境阻塞，详见 instances.csv；不计为科学失败。

## 33. Selection-bias audit

Development split只使用 project/crash/sanitizer和补丁规模元数据，不使用修复结果。没有读取 untouched outcome。

## 34. Strongest evidence FOR continuation

官方 benchmark 明确存在 crash-stopping 到完整验证的语义缺口；当前协议和113例 project-disjoint split 已可复现。

## 35. Strongest evidence AGAINST continuation

本机无法运行任何 V1-V4，agent transport probe也不稳定；当前没有真实 Development leverage 证据。

## 36. Publication-shape assessment

尚不能判断；benchmark/failure-study或方法论文均无数据支撑。

## 37. F1-D1-A/B/C/D classification

**F1-D1-C**，仅表示一次有界基础设施澄清被授权；不是 intervention signal，也不是 F1-D1-D。

## 38. Untouched-pool status

87例保持 UNTOUCHED；未构建镜像、未运行 agent、未读取 evaluator outcome。

## 39. Exact next action

在具备 x86-64 Linux、Podman/Docker、至少500GB可用空间的主机上，先运行2-3个 ANALYSIS-EXPOSED sanity case；通过后才对25例 Development 启动同骨干 baseline。

## 40. 2026-10-04 runtime re-entry addendum

WSL2、Docker 和 Podman 已可运行，Python 3.12 专用环境中的 F1 协议测试
12/12 通过。但容器存储所在 `C:` 仅余 46.87 GiB，低于未修改的 50 GiB
预下载保护线；WSL-native Codex CLI 也因未认证返回 401。基准容器、官方
验证器和 baseline 均未运行，V0-V4 均为 NOT_RUN。原 Development/UNTOUCHED/
ANALYSIS-EXPOSED 划分保持不变，旧 F9 记录未覆盖。
