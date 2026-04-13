# DESIGN.md — 《深度解剖 Claude Code 源码》

> **此文件是全书不变量。一旦确认，写作阶段不得修改它。改写作，不改合同。**

---

## 一、核心主张

Claude Code 是 Anthropic 官方发布的 AI 编程助手，但它同时也是一套精心设计的**运行时 Harness**。官方文档告诉你怎么用 `claude` 命令，却从不解释：为什么启动序列要并行发射三个预热任务？为什么工具系统设计了"三元安全模型"？为什么运行模式需要一套状态机来驱动？上下文窗口管理为什么需要四种压缩策略？

这本书的目标是**逆向还原这套 Harness 的工程内核**。我们以 v2.1.88 重建源码为样本，从 `src/main.tsx` 的第一行 `profileCheckpoint('main_tsx_entry')` 出发，沿着真实的代码路径，逐一解剖每一个子系统的数据结构、控制流、并发模型和设计权衡。

这本书和官方文档的本质区别在于：官方文档描述**接口契约**，而本书解析**实现决策**。每一个"为什么这样设计"，都有对应的源码行号作为证据，而非猜测。

读完这本书，你将能回答：当你在终端输入一条指令按下回车，Claude Code 内部经历了怎样的旅程？哪些工程决策保证了它的安全性？哪些架构选择支撑了它的可扩展性？

---

## 二、全书结构

### 序：为什么要解剖 Claude Code

全书序文——不编章节号，独立于正文之前。内容包括：
- **写作动机**：源码逆向工程的价值与局限，以及本书与官方文档的本质区别
- **阅读地图**：全书 11 篇的逻辑脉络，以及如何按需跳读
- **源码说明**：v2.1.88 重建版本的完整度（60-70%）、stub 模块的分布，以及读者如何自行验证书中引用
- **致谢**：向所有让 AI Coding Agent 成为可能的工程决策致敬

---

### 第一篇：地基——总体架构与技术栈

- **第1章：运行时 Harness 全景——总体架构解析**
  — 读完这章，你将能用一张模块关系图描述 Claude Code 的整体架构，理解各子系统的边界与依赖方向（前置依赖：无）

- **第2章：技术栈选型——React/Ink + Bun + TypeScript 的工程逻辑**
  — 读完这章，你将理解为什么用 React 渲染 CLI 界面、Bun 相比 Node 的构建优势，以及 `bun:bundle` API 在死代码消除上的关键作用（前置依赖：第1章）

- **第3章：启动流水线的并发艺术**
  — 读完这章，你将理解 `main.tsx` 如何在模块加载期间并行发射 MDM 读取、Keychain 预取、Bootstrap 请求三路任务，以及 `profileCheckpoint` 埋点如何量化每段延迟（前置依赖：第1章）

- **第4章：Feature Flag 的双层架构**
  — 读完这章，你将理解 `bun:bundle feature()` 编译期死代码消除与 GrowthBook 运行期 A/B 测试如何构成两层 flag 体系，以及 60+ 标志背后的功能模块化策略（前置依赖：第2章）

- **第5章：Bootstrap 全局状态——进程的状态脊梁**
  — 读完这章，你将理解 `src/bootstrap/state.ts` 如何充当整个进程的状态单一来源，以及 OpenTelemetry 指标计数器为何被直接嵌入全局状态而非独立服务（前置依赖：第1章）

---

### 第二篇：Agent 主循环

- **第6章：用户输入的三条分叉路**
  — 读完这章，你将理解 `processUserInput` 如何将用户输入分流为普通文本提示、Bash 命令和 Slash 命令三条处理路径，以及优先级队列的调度机制（前置依赖：第1章）

- **第7章：斜杠命令系统——内置命令的注册与执行**
  — 读完这章，你将理解 `src/commands/` 下 100+ 个命令如何通过目录约定注册、`getCommands()` 如何动态加载与过滤，以及斜杠命令如何被解析为 `SystemLocalCommandMessage` 并绕过 LLM 直接执行（前置依赖：第6章）

- **第8章：query.ts——单轮对话的原子循环**
  — 读完这章，你将理解 `query.ts` 作为一次 LLM 调用的完整原子单元——流式 token 接收、`tool_use` 块识别、工具并发执行、结果回填，以及 `FallbackTriggeredError` 的重试路径（前置依赖：第6章）

- **第9章：Query Engine——多轮编排与状态管理**
  — 读完这章，你将理解 `QueryEngine.ts` 如何在多轮对话中编排 `query.ts` 的调用序列、管理会话上下文累积、处理 abort 信号，以及与 REPL 状态机的协调机制（前置依赖：第8章）

- **第10章：运行模式状态机——Plan、Auto、Worktree 等模式的实现**
  — 读完这章，你将理解 `PermissionMode` 的完整枚举（default/plan/auto/acceptEdits/bypassPermissions/bubble）、`handlePlanModeTransition` 的状态转移逻辑、Plan V2 多 Agent 并行计数策略，以及 Worktree 模式的隔离机制（前置依赖：第9章）

---

### 第三篇：工具系统——AI 的手

- **第11章：Tool 接口与 buildTool 工厂**
  — 读完这章，你将理解 `Tool` 类型的完整接口契约——从 `call/description/inputSchema` 核心三元组，到 `isReadOnly/isDestructive/interruptBehavior` 安全三元模型，以及 `buildTool()` 工厂如何填充默认实现（前置依赖：第9章）

- **第12章：BashTool 解剖——最复杂工具的实现**
  — 读完这章，你将理解 BashTool 如何处理命令语义分类（读/搜/写/破坏性）、沙箱路由、后台任务化、输出截断，以及 sed/图像等特殊结果类型（前置依赖：第11章）

- **第13章：AgentTool——递归智能体的工具接口**
  — 读完这章，你将理解 AgentTool 作为工具接口层的职责——输入 schema 设计、权限检查逻辑、进度上报机制，以及 built-in agents 的注册与选择（前置依赖：第11章）

- **第14章：工具注册与条件加载**
  — 读完这章，你将理解 `tools.ts` 如何根据 `process.env.USER_TYPE` 和 feature flag 动态组装工具集，以及 MCP 工具如何被热插入这个集合（前置依赖：第4章、第11章）

---

### 第四篇：安全和权限系统

- **第15章：权限系统的三层决策架构**
  — 读完这章，你将理解 Claude Code 如何将权限决策分为"规则引擎快速路径"、"AI 分类器中路"、"用户交互慢路"三层，以及这三层的性能/安全权衡（前置依赖：第11章）

- **第16章：YOLO 模式与 AI 分类器**
  — 读完这章，你将理解 `yoloClassifier.ts` 如何用 LLM 判断命令安全性（用 AI 判断 AI 的操作），以及 `dangerousPatterns.ts` 黑名单与分类器的互补关系（前置依赖：第15章）

- **第17章：PermissionRule 与规则引擎**
  — 读完这章，你将理解权限规则的完整数据模型、`permissionRuleParser` 的解析逻辑、规则来源（global/local/managed）的优先级，以及 shadowed rule 检测机制（前置依赖：第15章）

- **第18章：Hooks 系统——生命周期拦截点**
  — 读完这章，你将理解 `src/utils/hooks/` 中 pre/post sampling hooks、tool permission hooks、session hooks 等拦截点的注册与触发机制，以及 `AsyncHookRegistry` 的异步协调设计（前置依赖：第9章、第15章）

---

### 第五篇：提示词工程

- **第19章：系统提示的优先级堆叠与组装**
  — 读完这章，你将理解 `buildEffectiveSystemPrompt` 如何按"Override → Coordinator → Agent → Custom → Default"五级优先级组装系统提示，以及每一级的触发条件与覆盖语义（前置依赖：第9章）

- **第20章：CLAUDE.md 的发现、解析与注入**
  — 读完这章，你将理解 CLAUDE.md 文件如何通过目录层级遍历被发现、如何被解析和缓存、何时被注入系统提示，以及多工作区场景下的合并策略（前置依赖：第19章）

- **第21章：上下文组装——git 状态、工具描述与用户上下文的构建**
  — 读完这章，你将理解 `fetchSystemPromptParts` 如何将 git status、工具列表、工作目录等信息编织进 API 请求的 cache-key 前缀，以及 `getUserContext` 与 `getSystemContext` 的分工（前置依赖：第19章、第20章）

- **第22章：模型自动选择——Opus、Sonnet 与 Haiku 的路由逻辑**
  — 读完这章，你将理解 `getDefaultMainLoopModelSetting()` 如何按订阅级别（Max/TeamPremium → Opus，Pro/Enterprise/PAYG → Sonnet）路由默认模型、`getSmallFastModel()` 何时切换为 Haiku、`opusplan`/`sonnetplan` 别名如何在 Plan 模式下触发模型升级，以及 `getMainLoopModelOverride()` 的用户覆盖优先级链（前置依赖：第5章、第10章、第19章）

---

### 第六篇：上下文工程

- **第23章：会话系统——标识、持久化与恢复**
  — 读完这章，你将理解 `sessionStorage.ts` 如何管理会话 ID、对话记录的追加写入、会话恢复（`ResumeConversation`）的查找逻辑，以及并发会话注册与 daemon 模式的会话隔离（前置依赖：第5章）

- **第24章：缓存系统——Prompt Cache 与 Context 压缩四策略**
  — 读完这章，你将理解 Anthropic API 的 prompt cache 机制在 Claude Code 中的利用方式，以及 AutoCompact、ReactiveCompact、MicroCompact、SnipCompact 四种策略各自的触发条件与适用场景（前置依赖：第9章）

- **第25章：AutoCompact 与边界标记的实现**
  — 读完这章，你将理解 `autoCompact.ts` 如何计算 token 使用警告状态、compact boundary message 如何分割历史，以及 `PROMPT_CACHE_BREAK_DETECTION` flag 下的异常检测机制（前置依赖：第24章）

- **第26章：本地记忆系统——memdir 与 SessionMemory**
  — 读完这章，你将理解 `src/memdir/` 如何扫描 CLAUDE.md 记忆层级、`findRelevantMemories` 的检索逻辑，以及 `SessionMemory` 服务如何在会话内提取并持久化记忆片段（前置依赖：第20章、第23章）

---

### 第七篇：MCP 集成——可插拔的外部能力

- **第27章：MCP 客户端的三协议实现**
  — 读完这章，你将理解 `src/services/mcp/client.ts` 如何支持 SSE、Stdio、StreamableHTTP 三种传输协议，MCP 工具如何被包装为内部 `Tool` 对象，以及资源/Prompt 的动态注册流程（前置依赖：第11章、第14章）

- **第28章：MCP 认证——OAuth、JWT 与 xaa**
  — 读完这章，你将理解 MCP 连接的三种认证路径（OAuth PKCE + 本地回调服务器、JWT 令牌刷新、xaa 企业身份登录），以及 `oauthPort.ts` 的端口分配与回调处理机制（前置依赖：第27章）

---

### 第八篇：多智能体系统

- **第29章：多智能体架构总览——Swarm 的层次模型**
  — 读完这章，你将理解 Claude Code 多智能体系统中 Swarm、Task、Agent 三个层次的职责划分，以及 InProcess/Local/Remote 三种协作拓扑的选择逻辑（前置依赖：第13章）

- **第30章：Task 类型体系——三种执行模式的实现**
  — 读完这章，你将理解 `InProcessTeammateTask`、`LocalAgentTask`、`RemoteAgentTask` 的内部实现差异，以及 `LocalShellTask` 如何管理后台 Shell 进程的前台化与生命周期（前置依赖：第29章）

- **第31章：Subagent 的生命周期——forkSubagent、runAgent 与内存隔离**
  — 读完这章，你将理解 `forkSubagent.ts` 的隐式 fork 机制、`runAgent.ts` 的完整 Agent 执行循环与主循环（第8章）的同构与隔离关系、`resumeAgent.ts` 的 transcript 恢复路径，以及 `agentMemorySnapshot.ts` 如何在子 Agent 间隔离和同步记忆（前置依赖：第8章、第30章）

- **第32章：Swarm 权限同步——沙箱中的信任传递**
  — 读完这章，你将理解 `permissionSync.ts` 如何通过 Mailbox 机制在 Leader 和 Worker 之间同步权限请求，以及 `leaderPermissionBridge.ts` 的确认队列设计动机（前置依赖：第15章、第30章）

---

### 第九篇：高级功能

- **第33章：Effort、Fast Mode 与 Thinking——推理深度控制**
  — 读完这章，你将理解 `effort.ts` 的四级推理深度（low/medium/high/max）、`fastMode.ts` 的模型切换策略、`thinking.ts` 中 `ultrathink` 关键词触发扩展 token budget 的完整机制（前置依赖：第9章）

- **第34章：跨会话记忆——extractMemories 与 teamMemorySync**
  — 读完这章，你将理解 `extractMemories` 如何从会话末尾提炼持久记忆、`teamMemorySync` 如何在团队成员间同步记忆，以及 `secretScanner` 如何防止敏感信息写入共享记忆（前置依赖：第26章）

- **第35章：Plugin 系统——DXT 包的生命周期**
  — 读完这章，你将理解 DXT 插件包格式、`PluginInstallationManager` 的安装/升级/卸载流程、bundled plugins 与 marketplace plugins 的区别，以及插件 hook 的注入机制（前置依赖：第18章）

- **第36章：Skill 系统——Markdown 封装的 AI 能力**
  — 读完这章，你将理解 Skill 如何将 Markdown 文档 + 代码片段打包为可发现、可调用的 AI 能力单元，`SkillTool` 的执行路径，以及 `EXPERIMENTAL_SKILL_SEARCH` flag 下的语义检索机制（前置依赖：第14章）

- **第37章：未发布的功能总线——Feature Flag 背后的实验特性**
  — 读完这章，你将理解 `ULTRAPLAN`、`DAEMON`、`BG_SESSIONS`、`COORDINATOR_MODE`、`BYOC_ENVIRONMENT_RUNNER` 等实验 flag 对应的代码骨架，以及从 flag 分布推断 Claude Code 产品演进方向的方法（前置依赖：第4章）

---

### 第十篇：TUI 层——在终端里渲染 React

- **第38章：Ink 的自建 Reconciler**
  — 读完这章，你将理解 `src/ink/reconciler.ts` 如何将 React 虚拟 DOM 映射到终端字符网格，Yoga layout 引擎如何在终端中实现 Flexbox，以及 `render-node-to-output.ts` 的输出合成逻辑（前置依赖：第1章、第2章）

- **第39章：termio——终端原语的解析与发送**
  — 读完这章，你将理解 `src/ink/termio/` 如何解析 ANSI escape 序列（CSI/OSC/DEC/SGR），以及光标控制、颜色渲染、选区管理等终端能力的底层实现（前置依赖：第38章）

---

### 第十一篇：工程原则——从实现提炼的设计智慧

- **第40章：并发优先的启动哲学**
  — 提炼：Claude Code 在冷启动路径上"能并行就不串行"的每一个决策，以及如何用 profiler checkpoint 量化并持续优化启动延迟（源码依据：第3章）

- **第41章：安全性的三道防线**
  — 提炼：从工具三元安全模型、权限三层决策，到 SSRF 防护（`ssrfGuard.ts`）、沙箱隔离、secret scanner——Claude Code 在不同层次构筑防御纵深的系统性方法（源码依据：第11-18章）

- **第42章：可扩展性的四种机制**
  — 提炼：Feature flag 模块化、Tool 工厂模式、Plugin/Skill 包格式、MCP 协议——四种不同粒度的扩展点设计哲学及其各自的适用边界（源码依据：第4、11、27、35-36章）

---

## 三、每章一句话主张（完整列表）

| 章 | 一句话主张 |
|----|-----------|
| 1 | 读完这章，你将能用一张模块关系图描述 Claude Code 的整体架构，并理解各子系统的边界与依赖方向 |
| 2 | 读完这章，你将理解 React/Ink + Bun + TypeScript 的技术选型动机，以及 `bun:bundle` 相比 webpack/rollup 在死代码消除上的结构性优势 |
| 3 | 读完这章，你将理解 `profileCheckpoint` 埋点与三路并发预热的具体实现，并能将这一模式用于自己的 CLI 启动优化 |
| 4 | 读完这章，你将理解编译期 `feature()` 与运行期 GrowthBook 的差异，并能解释为什么某些功能在普通用户构建中完全消失 |
| 5 | 读完这章，你将理解全局状态集中在单一模块的设计动机，以及 OpenTelemetry 指标为何作为状态的一部分而非独立 sidecar |
| 6 | 读完这章，你将理解 slash 命令、bash 命令、普通提示的分流逻辑，并能追踪任意输入的完整处理路径 |
| 7 | 读完这章，你将理解 100+ 个斜杠命令的注册约定、动态加载过滤机制，以及斜杠命令如何绕过 LLM 直接执行本地逻辑 |
| 8 | 读完这章，你将理解 `query.ts` 的单轮原子循环——流式 token 如何变成工具调用、工具结果如何回填，以及重试机制的触发条件 |
| 9 | 读完这章，你将理解 `QueryEngine.ts` 如何跨轮次编排对话、累积上下文，以及 abort 信号如何在多轮调用链中传播 |
| 10 | 读完这章，你将理解 Claude Code 的六种运行模式及其状态转移规则，并能解释 Plan V2 的多 Agent 并行计数策略 |
| 11 | 读完这章，你将理解 Tool 类型的完整契约，并能从头实现一个符合 Claude Code 规范的自定义工具 |
| 12 | 读完这章，你将理解 BashTool 为何是代码库中最复杂的工具，以及命令语义分类对 UI 折叠展示的影响 |
| 13 | 读完这章，你将理解 AgentTool 作为工具接口层的职责边界，以及 built-in agents 的注册与选择机制 |
| 14 | 读完这章，你将理解工具集是动态装配而非静态注册的，并能解释 MCP 工具如何被热插入工具集 |
| 15 | 读完这章，你将理解为何权限系统需要三层决策而非单一策略，以及各层的性能与安全权衡 |
| 16 | 读完这章，你将理解"用 AI 判断 AI 行为安全性"的实现细节，以及黑名单与 LLM 分类器的互补关系 |
| 17 | 读完这章，你将理解权限规则的完整数据模型，并能解释 managed settings 如何覆盖用户本地规则 |
| 18 | 读完这章，你将理解 Claude Code 的生命周期拦截点体系，并能在正确的 hook 点注入自定义逻辑 |
| 19 | 读完这章，你将理解系统提示的五级优先级堆叠，并能预测任意场景下最终生效的系统提示内容 |
| 20 | 读完这章，你将理解 CLAUDE.md 的发现算法和注入时机，以及多工作区下的合并行为 |
| 21 | 读完这章，你将理解 git status、工具描述、工作目录等上下文是如何被组装进 API cache-key 前缀的 |
| 22 | 读完这章，你将理解 Claude Code 如何按订阅级别自动选择 Opus/Sonnet/Haiku，以及 Plan 模式下的模型升级触发逻辑 |
| 23 | 读完这章，你将理解会话 ID 的生命周期、对话记录的追加写入机制，以及 `/resume` 命令的查找和恢复逻辑 |
| 24 | 读完这章，你将理解 prompt cache 的利用策略，以及四种 context 压缩策略各自的触发条件与适用场景 |
| 25 | 读完这章，你将理解 AutoCompact 的 token 警告状态计算、compact boundary 标记机制，以及 prompt cache 破坏检测的防御逻辑 |
| 26 | 读完这章，你将理解 CLAUDE.md 记忆层级的扫描逻辑，以及 SessionMemory 如何从对话中提炼并持久化记忆片段 |
| 27 | 读完这章，你将理解三种 MCP 传输协议的适用场景，并能解释 MCP 工具如何变成 Claude 可调用的内部工具 |
| 28 | 读完这章，你将理解 MCP 的三种认证路径，以及本地 OAuth 回调服务器的端口分配与安全设计 |
| 29 | 读完这章，你将理解 Swarm、Task、Agent 三层模型的职责划分，以及三种协作拓扑的适用场景 |
| 30 | 读完这章，你将理解三种 Task 类型的内部实现差异，并能解释何时选择 InProcess、何时选择 Remote 执行模式 |
| 31 | 读完这章，你将理解 forkSubagent 的隐式继承机制、runAgent 与主循环的同构与隔离关系，以及 agentMemorySnapshot 如何在子 Agent 间隔离记忆 |
| 32 | 读完这章，你将理解 Swarm 中权限请求如何跨进程传递，以及 Mailbox 机制解决的核心问题 |
| 33 | 读完这章，你将理解 Effort 四级控制、Fast Mode 的模型切换逻辑，以及 `ultrathink` 关键词如何扩展 thinking token budget |
| 34 | 读完这章，你将理解 extractMemories 的记忆提炼策略、teamMemorySync 的协作同步机制，以及 secretScanner 的安全防护逻辑 |
| 35 | 读完这章，你将理解 DXT 插件的完整生命周期，并能解释插件如何向运行时注入新工具和 hook |
| 36 | 读完这章，你将理解 Skill 与 Tool 的本质区别，以及语义搜索如何帮助模型在大量 Skill 中定位正确能力 |
| 37 | 读完这章，你将能从 feature flag 分布推断 Claude Code 的产品演进方向，以及 ULTRAPLAN、DAEMON 等实验特性的代码骨架 |
| 38 | 读完这章，你将理解 Ink 如何在没有 DOM 的终端中运行 React，以及 reconciler 调和阶段的关键设计决策 |
| 39 | 读完这章，你将理解终端控制序列的解析与生成，以及 Claude Code 如何精确控制光标位置和颜色输出 |
| 40 | 读完这章，你将掌握"并发优先"的启动设计原则，并能将其应用于自己的 CLI 工具冷启动优化 |
| 41 | 读完这章，你将能完整描述 Claude Code 的安全防御纵深，并理解各层防线的设计取舍与互补关系 |
| 42 | 读完这章，你将能识别 Claude Code 使用的四种扩展点模式，并理解其各自的边界与适用场景 |

---

## 四、排除范围

1. **`src/assistant/`（KAIROS 模式）**：stub 实现，feature flag 门控，排除（第37章会提及其 flag 但不分析实现）
2. **`src/ssh/`**：最小实现（2 文件），排除
3. **`src/proactive/`**：最小实现（2 文件），排除
4. **`src/coordinator/`**：stub 实现，feature flag 门控，排除（第37章会提及）
5. **`src/voice/`**：接口层（1 文件），排除
6. **功能使用教程**：如何使用 `claude` 命令、如何配置 API key 等入门内容，排除
7. **历史版本差异**：不对比 v2.1.88 与其他版本的变化，排除
8. **`src/commands/` 命令细节**：100+ 个命令目录不逐一分析，仅第7章概述注册机制
9. **Analytics/Telemetry 内部配置**：GrowthBook 实验配置和 DataDog 上报细节不深入，排除
10. **`src/bridge/` 远程模式**：完整的 Bridge 远程会话管理不作为独立章节，仅在多智能体章节中概述

---

## 五、写作风格约定

**写作风格：`autopsy` 工程师解剖**

**风格选择理由**：Claude Code 是一个已发布的成熟工具，我们面对的是一个"黑盒"——源码就是唯一的真相来源。`autopsy` 风格最适合这种反向工程场景：每一个断言都需要源码证据，每一个设计决策都要分析"为什么选 A 不选 B"。读者是工程师，他们不需要手把手引导，他们需要可验证的事实和有深度的分析。

### 格式规则

1. **源码引用格式**：`相对路径:行号` 或 `相对路径:函数名`，例如 `src/main.tsx:14` 或 `src/Tool.ts:buildTool`
2. **语言规则**：中文正文，英文技术术语保留原文（如 `feature flag`、`reconciler`、`YOLO mode`），工程师读者无需括号注释
3. **代码片段长度**：关键逻辑不超过 25 行，超过则用注释标注省略部分
4. **推断标注**：无源码直接依据的结论注明「（推断）」
5. **章节开篇**：每章以"一个让读者产生认知冲突的问题"开场，而非"本章介绍……"
6. **设计权衡**：每章至少分析一处"为什么这样设计而不是……"，有明确 trade-off 分析
7. **Mermaid 图表**：核心数据流和模块关系用 Mermaid 流程图可视化，辅助文字描述

---

## 六、附录规划

| 附录 | 工具价值 |
|------|---------|
| **附录 A：关键文件索引** | 按子系统分组列出核心文件路径，方便读者自行验证源码引用 |
| **附录 B：Feature Flag 完整清单** | 60+ feature flag 的名称、功能描述、相关模块及状态（已发布/实验中/stub），帮助读者理解功能边界 |
| **附录 C：环境变量参考** | Claude Code 使用的 `process.env.*` 变量及其作用范围（含模型后端切换变量）|
| **附录 D：术语表** | 书中专有名词中英对照（Harness、YOLO mode、Mailbox、DXT、compact boundary、fork subagent、inference profile 等）|
