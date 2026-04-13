# 序：为什么要解剖 Claude Code

---

官方文档告诉你怎么用 `claude` 命令——如何配置 API Key，如何启用 MCP 服务器，如何写 CLAUDE.md。但它不会告诉你，为什么 `src/main.tsx` 的前三行是副作用而不是函数调用，不会告诉你一个 CLI 工具的冷启动路径上为什么要并行发射三个异步任务，也不会告诉你"YOLO 模式"背后其实是另一个 LLM 在帮 LLM 做安全判断。

这本书解析的是**实现决策**，而不是接口契约。

## 为什么写这本书

`src/main.tsx` 的第 2-8 行有一段注释：

```
// 1. profileCheckpoint marks entry before heavy module evaluation begins
// 2. startMdmRawRead fires MDM subprocesses (plutil/reg query) so they run in
//    parallel with the remaining ~135ms of imports below
// 3. startKeychainPrefetch fires both macOS keychain reads (OAuth + legacy API
//    key) in parallel — isRemoteManagedSettingsEligible() otherwise reads them
//    sequentially via sync spawn inside applySafeConfigEnvironmentVariables()
//    (~65ms on every macOS startup)
```

这段注释说的不是功能，而是**工程决策的理由**：为了节省 65ms，他们愿意在 `import` 语句之间执行副作用，违反所有 ESLint 最佳实践，并在每一行旁边加上 `// eslint-disable` 注释。

这种决策在源码里随处可见。工具系统有一个三元安全模型（`isReadOnly`/`isDestructive`/`interruptBehavior`），不是两态的允许/拒绝。权限系统有三层决策，分别针对不同的性能和安全权衡。Context 压缩有四种策略，AutoCompact/ReactiveCompact/MicroCompact/SnipCompact，各有触发条件。

这些设计选择，官方文档里一个字都没有。

## 阅读地图

本书分 11 篇，从骨架到血肉：

| 篇 | 主题 | 你会看到什么 |
|----|------|------------|
| 第一篇 | 总体架构与技术栈 | Harness 的骨架、Bun 的编译期能力、并发启动优化 |
| 第二篇 | Agent 主循环 | 输入分流、斜杠命令体系、`query.ts` 原子循环、运行模式状态机 |
| 第三篇 | 工具系统 | `Tool` 接口、`buildTool` 工厂、BashTool 完整流程、AgentTool 接口层 |
| 第四篇 | 安全和权限系统 | 三层决策架构、YOLO 分类器、规则引擎、Hooks 体系 |
| 第五篇 | 提示词工程 | 系统提示优先级堆叠、CLAUDE.md 发现机制、上下文组装、模型路由 |
| 第六篇 | 上下文工程 | 会话持久化、Prompt Cache、AutoCompact 实现、本地记忆系统 |
| 第七篇 | MCP 集成 | 三协议客户端、OAuth/JWT/xaa 认证 |
| 第八篇 | 多智能体系统 | Swarm 层次模型、三种 Task 类型、Subagent 生命周期、Mailbox 权限同步 |
| 第九篇 | 高级功能 | Effort/Thinking 控制、跨会话记忆、Plugin/Skill 架构、未发布功能总线 |
| 第十篇 | TUI 层 | Ink 自建 Reconciler、termio ANSI 解析 |
| 第十一篇 | 工程原则 | 从 42 章提炼的三个可复用设计原则 |

可以从头读，也可以直接跳到感兴趣的篇。每章开头的"前置依赖"标注会告诉你需要先读哪些章节。

## 关于源码版本

本书基于 **Claude Code v2.1.88 的重建版本**（`@anthropic-ai/claude-code@2.1.88`），从编译后的二进制和 source map 逆向还原而来。源码**约 60-70% 完整**，有些模块（如 `src/assistant/`、`src/coordinator/`）是骨架实现，本书已将其标注为排除范围，不做分析。

书中所有源码引用使用 `路径:行号` 格式，例如 `src/main.tsx:12`。你可以在项目目录中运行：

```bash
sed -n '12p' src/main.tsx
```

直接验证引用是否准确。这是本书的承诺：每一个断言都有可验证的源码证据，而不是 AI 的推断。（无法找到直接源码证据的结论会标注「推断」。）

## 致谢

感谢 Anthropic 的工程师们，他们不仅写出了精心设计的代码，还在注释里留下了设计理由——这让逆向工程变成了一次有来有往的对话，而不是纯粹的猜测。

---

*下一章：第1章将建立全书的模块地图——那 2000 个文件是如何组织的。*
