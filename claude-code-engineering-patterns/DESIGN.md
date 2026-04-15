# DESIGN.md
# 《 Claude Code 工程模式》

> **全局不变量**：本文件一旦确认，后续所有阶段不得修改。

---

## 序言

### 一个源码侦探的自白

Claude Code的npm包里意外留了一个60MB的调试文件。

**1902个源文件、51万行TypeScript代码全部暴露。**

我第一次打开 Claude Code 的 `src/main.tsx` 时，文件长度是 8,247 行。彼时我只是想搞清楚"这个 CLI 到底是怎么跑起来的"，但顺着 `launchRepl()` 往下追了三个文件之后，我意识到自己掉进了一个与外部文档完全不符的世界——这个工具的复杂度远超任何官方描述。

这不是一个 CLI。这是一套 **Agent Harness**。

 Harness，是一个工程术语，指的是将不可控的外部系统包裹在可控接口之内的框架结构。Claude Code 把 Anthropic 的 Claude 模型变成一个可编排的 Agent 运行时——它的三层架构（交互层、Harness 控制层、模型层）下，Harness 层的十大子系统（启动、核心循环、提示词、工具编排、上下文、权限、Hooks、任务、多智能体、辅助）都在做同一件事：**在 AI 的不确定性和工程系统的确定性之间，修一道桥梁**。

写作本书的过程中，最让我意外的不是某个具体实现，而是**演化的痕迹**。Claude Code 的 Hook 系统从 3 个事件增长到 20+ 个，Task 类型从 1 种扩展到 7 种，Swarm 从单进程演化为三种 Teammate 后端。每一次演化都留下了接口膨胀和 if/else 分叉——但没有一次是重写。这些"伤疤"恰恰是最有价值的工程证据：它们展示了真实系统如何在约束条件下渐进式扩展，而不是推倒重来。

**你不需要是 Claude 员工才能理解 Claude Code**。源码在那里，符号表在那里，类型定义在那里。任何有耐心的工程师都能顺着线索走完整条追踪线。本书的每一章都遵循同一个结构：先描述一个"猎人发现"（"我在某个文件的第几行发现了一个奇怪的注释……"），然后展开完整的追踪路径，最后提炼出可命名的工程模式。

如果你正在设计自己的 Agent 系统，或者在评估"到底应该用框架还是自己造轮子"，这本书提供了一个 50 万行级别生产代码的真实样本。如果你想理解现代 AI 应用背后的工程基础设施如何层层叠加，这本书的 12 篇结构从输入到渲染逐层剥开这个谜题。如果你只是好奇——序言之后的 45 章随时欢迎你从任意一章跳进去。

阅读建议：

- **按顺序读**：第二篇（交互层）到第四篇（模型层）是一条完整的请求追踪线，适合想从头理解一次交互全貌的读者
- **按图索骥**：如果你对某个子系统特别感兴趣——Hook（第 24 章）、Task（第 29 章）、Swarm（第 33 章）——每章都是独立入口
- **模式优先**：第十二篇（第 44 章）的模式图谱适合作为复习清单，在读完其他章节后回头对照

最后一件事：源码会过时，但模式不会。本书提炼的 12 个 Harness 工程模式，在任何 Agent 系统的设计中都适用。Claude Code 只是它们的一个样本。

---

## 一、核心主张

Claude Code 是一个被误解的工具。外界看到的是一个 CLI，但源码揭示的是一套精密的 **Agent Harness 工程架构**——一个把不可控的 AI 行为变成可编排、可拦截、可扩展工程管道的基础设施。

本书的主张是：**Claude Code 是一个活体样本，展示了"从 CLI 工具到 Agent 平台"的架构跃迁如何在生产级代码中真实发生**。它不是从零设计的 Agent 框架，而是一个 CLI 工具在功能压力下被迫演化——每一个子系统都留下了演化的痕迹：Hook 系统从无到 20+ 事件，Task 系统从单类型到 7 种任务，Swarm 从单进程到三种 Teammate 后端。这些痕迹是任何架构教科书无法提供的真实工程决策证据。

读完本书，你将获得两样东西：第一，对 Claude Code 内部实现的精确理解（源码追踪线）；第二，一套可以移植到你自己项目的 Agent Harness 工程模式（模式提炼线）。这两条线在每章并行展开——前者是证据，后者是结论。

---

## 二、全书结构

### 组成部分

| 部分 | 内容 | 章数 |
|------|------|------|
| 序言 | 一个源码侦探的自白：为何研究 Claude Code、如何阅读本书 | — |
| 第一篇至第十二篇 | 45 章正文 | ch01-ch45 |
| 附录 | Hook 事件速查表 / 工具权限矩阵 / 关键类型索引 / 环境变量参考 / Feature Flag 清单 / 术语表 | 6 篇 |

### 三层架构与篇章映射

全书按**三层架构**组织阅读顺序——交互层 → Harness 控制层 → 模型层 → Harness 子系统深潜 → 生态 → 模式提炼：

| 层 | 子系统 | 覆盖篇章 | 核心源码路径 |
|---|--------|---------|-------------|
| **交互层** | CLI 入口 | 第二篇 ch04 | `main.tsx`, `cli/` |
| **交互层** | REPL 界面 | 第二篇 ch05 | `screens/REPL.tsx` (Ink/React) |
| **交互层** | 命令系统 | 第二篇 ch06-ch07 | `commands/`, `commands.ts` |
| **交互层** | IDE 集成 | 第二篇 ch08 | `bridge/`, `services/lsp/` |
| **Harness** | 启动系统 | 第一篇 ch02 + 第二篇 ch04 | `setup.ts`, `bootstrap/state.ts` |
| **Harness** | 核心循环 | 第三篇 ch09-ch10 | `query.ts`, `QueryEngine.ts` |
| **Harness** | 提示词管理 | 第六篇 ch19-ch20 | `constants/prompts.ts`, `utils/claudemd.ts` |
| **Harness** | 工具编排 | 第五篇 ch14-ch18 | `Tool.ts`, `services/tools/`, `tools/` |
| **Harness** | 上下文管理 | 第六篇 ch21-ch23 | `services/compact/`, `state/`, `utils/sessionStorage.ts` |
| **Harness** | 权限护栏 | 第五篇 ch15-ch16 + 第十篇 ch37-ch40 | `utils/permissions/` |
| **Harness** | Hooks 引擎 | 第七篇 ch24-ch28 | `utils/hooks.ts` (5022 行), `utils/hooks/` |
| **Harness** | 任务编排 | 第八篇 ch29-ch32 | `tasks/` |
| **Harness** | 多智能体 | 第九篇 ch33-ch36 | `tools/AgentTool/`, `utils/swarm/`, `coordinator/` |
| **Harness** | 辅助系统 | 第四篇 ch11-ch13 | `services/api/claude.ts`, `utils/model/`, `services/analytics/` |
| **模型层** | API 通信 | 第四篇 ch13 | `services/api/claude.ts`, `services/api/client.ts` |
| **模型层** | 模型管理 | 第四篇 ch11-ch12 | `utils/model/` (17 个文件) |
| **模型层** | 流式处理 | 第三篇 ch10 | async generator, SSE 解析 |

### 章节导航

### 第一篇：地图与地基
*目的：建立全局架构认知，再深入细节*

- **第1章：系统总体架构与技术栈——Claude Code 的结构地图**
  一句话主张：读完这章，你将建立 Claude Code 的完整架构认知——三层架构（交互层 / Harness 控制层 / 模型层）、Harness 层十大子系统的职责边界、技术选型（Bun/TypeScript/Ink/OpenTelemetry）的设计动机，以及 2,000 个源码文件的组织逻辑。
  （前置依赖：无）

- **第2章：Bootstrap 与全局状态——50+ 函数背后的单例设计**
  一句话主张：读完这章，你将理解 `bootstrap/state.ts` 为何用模块级变量而非依赖注入，并能在自己的 Agent 项目中复用这一"轻量全局状态"模式。
  （前置依赖：第1章）

- **第3章：构建时特性开关——`bun:bundle feature()` 的死代码消除**
  一句话主张：读完这章，你将理解如何用构建时 DCE（Dead Code Elimination）替代运行时 if/else，实现零成本的特性隔离。
  （前置依赖：第1章）

---

### 第二篇：交互层——用户如何与系统对话
*目的：理解交互层的四个子系统——CLI 入口、REPL 界面、命令系统、IDE 集成——如何接收和路由用户输入*

- **第4章：CLI 入口与模式分叉——从 main.tsx 到 REPL / Headless / SDK**
  一句话主张：读完这章，你将理解 `main.tsx` 的三路并行启动序列（MDM / Keychain / import 求值重叠）、Commander.js 命令解析树，以及交互模式 / Headless / SDK / Assistant 四种运行模式的分叉逻辑。
  （前置依赖：第1章）

- **第5章：REPL 界面架构——5000 行组件的交互设计**
  一句话主张：读完这章，你将理解 `screens/REPL.tsx` 如何基于 Ink（React for CLI）实现消息虚拟化滚动、工具权限弹窗、后台任务面板、远程会话（SSH/DirectConnect）和推测执行（Speculation），并能识别"单文件巨组件"在强内聚场景下的工程合理性。
  （前置依赖：第4章）

- **第6章：用户输入分流——`processUserInput` 的路由决策树**
  一句话主张：读完这章，你将理解 Claude Code 如何在收到用户输入后的第一毫秒内完成分流——斜杠命令、普通消息、特殊模式三条路径的判断逻辑，以及"路由决策先于任何业务逻辑"这一架构原则。
  （前置依赖：第2章、第4章）

- **第7章：斜杠命令系统——103 个命令的注册、加载与执行**
  一句话主张：读完这章，你将理解 Claude Code 的命令系统如何通过目录约定 + 动态加载 + feature flag 门控实现 103 个命令的一致性管理，并能将这一"目录即注册表"模式用于自己的可扩展 CLI 设计。
  （前置依赖：第6章）

- **第8章：IDE 集成——Bridge 协议与 LSP 服务**
  一句话主张：读完这章，你将理解 `bridge/`（32 个文件）如何通过 Unix Domain Socket / WebSocket 桥接 VS Code 等 IDE，`services/lsp/` 如何提供语言服务协议支持，以及 Bridge 模式如何让同一个 Agent 同时服务终端和 IDE 两种交互界面。
  （前置依赖：第4章）

---

### 第三篇：Harness 核心循环——查询引擎
*目的：深入 Harness 控制层的核心——从用户输入到模型调用的主循环*

- **第9章：QueryEngine 主循环——工具调用的编排逻辑**
  一句话主张：读完这章，你将理解 Claude Code 如何把"用户输入 → AI 响应 → 工具调用 → 再次请求"变成一个稳定的 `while(true)` 异步生成器循环，并能识别其中的状态机转换、Continue 场景（max_output_tokens 恢复、响应式压缩、预算续行）和中断模式。
  （前置依赖：第6章）

- **第10章：流式响应管道——异步生成器的工程应用**
  一句话主张：读完这章，你将理解 `query.ts` 如何用 async generator 把 SSE 流转化为结构化事件序列，`StreamingToolExecutor` 如何在 API 仍在流式输出时就开始并发执行只读工具，以及这一模式在高延迟 AI 调用中的价值。
  （前置依赖：第9章）

---

### 第四篇：模型层——API 通信与推理控制
*目的：理解模型层的三个子系统——API 通信、模型管理、流式处理——如何封装与 Anthropic API 的全部交互细节*

- **第11章：模型自动选择——Opus、Sonnet 与 Haiku 的路由逻辑**
  一句话主张：读完这章，你将理解 Claude Code 如何根据任务复杂度动态路由到 Haiku（高频轻量）、Sonnet（主力开发）、Opus（深度推理）三个模型，`utils/model/`（17 个文件）如何管理模型名称映射、能力缓存和提供商检测（first-party / Bedrock / Vertex），以及 `mainLoopModelOverride` 和 `setModelForTask` 如何实现模型选择与覆盖机制。
  （前置依赖：第9章）

- **第12章：推理深度控制——Effort、Fast Mode 与 Thinking 的三轴设计**
  一句话主张：读完这章，你将理解 Claude Code 如何通过 effort 级别（小时级任务）、fast mode（低延迟优先）、thinking 模式（内部推理链）三个正交维度控制 AI 的推理深度，以及这三者如何与模型选择交叉作用。
  （前置依赖：第11章）

- **第13章：API 通信层——Anthropic 客户端、重试机制与提示词缓存策略**
  一句话主张：读完这章，你将理解 `services/api/claude.ts`（3419 行）如何封装流式/非流式 API 调用、多提供商适配和用量追踪；`withRetry.ts` 如何实现指数退避重试；以及 `addCacheBreakpoints()` / `splitSysPromptPrefix()` 如何精确放置缓存断点以最大化提示词缓存命中率——这是 Claude Code 降低 API 成本的核心工程手段。
  （前置依赖：第9章）

---

### 第五篇：Tool 系统——可扩展的工具协议
*目的：理解 Harness·工具编排子系统——工具如何被定义、注册、权限校验、执行*

- **第14章：Tool 接口契约——`buildTool()` 工厂与 Zod 输入验证**
  一句话主张：读完这章，你将理解 Claude Code 的工具系统如何通过统一工厂函数实现 54 个内置工具（19 个始终启用 + 35 个条件启用）的一致性，并掌握"接口契约 + 运行时验证"的工具注册模式。
  （前置依赖：第2章）

- **第15章：权限决策树——PermissionMode 的四层设计**
  一句话主张：读完这章，你将理解 `PermissionMode` 如何把"默认拒绝 → 配置规则允许 → 分类器自动批准 → 用户交互确认"组织成可组合的决策链——这是 Harness·权限护栏子系统的 Tool 视角入门，与第十篇的安全架构深潜形成递进。
  （前置依赖：第14章）

- **第16章：AI 分类器替代规则引擎——yolo-classifier 的设计哲学**
  一句话主张：读完这章，你将理解为什么 Claude Code 用 AI 模型而非规则集来判断"这个操作是否安全"，以及这一决策的工程成本与收益。
  （前置依赖：第15章）

- **第17章：MCP 工具协议——把第三方工具变成一等公民**
  一句话主张：读完这章，你将理解 Model Context Protocol 如何让外部服务注册为 Claude Code 工具（`services/mcp/` ~12310 行，支持 SSE / Stdio / Streamable HTTP / WebSocket 四种传输协议），并能分析协议化扩展与插件化扩展的架构差异。
  （前置依赖：第14章）

- **第18章：Skill 系统——声明式能力包的加载与执行**
  一句话主张：读完这章，你将理解 `SkillTool` 和 `DiscoverSkillsTool` 如何把 Markdown frontmatter 变成可执行的能力扩展，以及"声明式能力包"与传统插件系统在架构上的本质差异。
  （前置依赖：第14章）

---

### 第六篇：上下文工程——控制 AI 的信息视野
*目的：理解 Harness·提示词管理与上下文管理两个子系统——Claude Code 如何精确控制送入 AI 的每一个 token*

- **第19章：提示词装配——`fetchSystemPromptParts()` 的分层组装**
  一句话主张：读完这章，你将理解每次 API 调用前系统提示是如何被动态构建的——`getSystemPrompt()` 的分段式组装（缓存友好段落 vs 动态段落）、工具声明列表、MCP 服务器指令、Skill 工具命令的注入顺序，以及 `fetchSystemPromptParts()` 如何并行获取三部分以减少延迟。
  （前置依赖：第9章）

- **第20章：CLAUDE.md 注入——层级化指令的加载与优先级**
  一句话主张：读完这章，你将理解 `utils/claudemd.ts` 如何从当前目录向上扫描 CLAUDE.md 文件、合并五个层级的指令（Managed memory → User memory → Project memory → Rules → Local memory），以及 `@include` 指令如何实现文件级指令复用。
  （前置依赖：第19章）

- **第21章：会话持久化——转录、快照与断点续写**
  一句话主张：读完这章，你将理解 `sessionStorage` 如何在进程重启后恢复会话状态（JSONL 格式 transcript），并能识别"写入先于执行"这一持久化模式在 Agent 系统中的可靠性保证价值。
  （前置依赖：第9章）

- **第22章：AutoCompact 与上下文折叠——窗口压缩的触发机制**
  一句话主张：读完这章，你将理解 Claude Code 如何检测上下文窗口临界、自动触发压缩（电路断路器模式，连续失败 3 次后停止重试）、通过 fork agent 生成摘要、维护 `compact_boundary` 标记，以及微压缩（Microcompact）和 `contextCollapse` 在保证语义连续性的同时缩减 token 用量的实现原理。
  （前置依赖：第19章、第21章）

- **第23章：记忆系统——本地、跨会话与团队记忆的三层架构**
  一句话主张：读完这章，你将理解 Claude Code 如何通过 `memdir`（本地记忆）、`services/extractMemories/SessionMemory`（跨会话提取）、`services/teamMemorySync`（团队共享）三层架构，让 AI 在不同范围内积累和共享知识，并能将这一分层记忆模式用于自己的 Agent 设计。
  （前置依赖：第20章）

---

### 第七篇：Hooks 引擎——Harness 的核心
*目的：深入理解 Harness·Hooks 引擎子系统——独立的用户扩展接口，贯穿工具执行、会话生命周期和智能体协作全流程*

- **第24章：20+ 事件的生命周期地图——Hooks 全景**
  一句话主张：读完这章，你将能从 `PreToolUse` 到 `SubagentStop` 完整描述一个 AI 操作的钩子触发序列，并理解每个事件的设计意图。
  （前置依赖：第14章）

- **第25章：四种执行器——`command/prompt/agent/http` 的多态设计**
  一句话主张：读完这章，你将理解 Claude Code 如何用多态执行器把"运行 shell 命令"、"调用 AI"、"发 HTTP 请求"统一在同一个 Hook 接口下，并能识别开放-封闭原则在此的体现。
  （前置依赖：第24章）

- **第26章：AsyncHookRegistry——异步钩子的注册、超时与并发控制**
  一句话主张：读完这章，你将理解 `AsyncHookRegistry` 如何处理钩子的异步生命周期——挂起、超时、取消、结果回调——并能将这一注册表模式用于自己的异步钩子系统。
  （前置依赖：第24章）

- **第27章：hooksConfigSnapshot——配置快照隔离模式**
  一句话主张：读完这章，你将理解为什么 Claude Code 在会话启动时"冻结"Hook 配置而非实时读取，以及这一快照隔离模式如何防止配置变更影响正在运行的会话。
  （前置依赖：第24章）

- **第28章：Frontmatter Hooks——Skill 与 Agent 的声明式钩子注册**
  一句话主张：读完这章，你将理解 `registerSkillHooks()` 和 `registerFrontmatterHooks()` 如何让用户通过 Markdown frontmatter 声明钩子，以及"声明式注册 vs 命令式注册"的工程权衡。
  （前置依赖：第27章、第18章）

---

### 第八篇：Task 系统——后台执行的基础设施
*目的：理解 Harness·任务编排子系统——7 种后台任务的生命周期管理*

- **第29章：7 种任务类型的状态机——Task 系统设计**
  一句话主张：读完这章，你将理解 `local_bash/local_agent/remote_agent/in_process_teammate/local_workflow/monitor_mcp/dream` 七种任务如何用统一状态机管理，并能识别"类型收窄 + 状态守卫"的并发安全模式。
  （前置依赖：第9章）

- **第30章：LocalAgentTask——子 Agent 的进程模型与 I/O 协议**
  一句话主张：读完这章，你将理解如何通过子进程隔离运行独立的 Agent，以及父子 Agent 之间的结构化 I/O 协议设计。
  （前置依赖：第29章）

- **第31章：RemoteAgentTask——远程任务的通信架构**
  一句话主张：读完这章，你将理解 Claude Code 如何把本地任务模型扩展到远程执行，以及 SSE/WebSocket/轮询三种通信方式的选型逻辑。
  （前置依赖：第29章）

- **第32章：DreamTask——后台自主执行的设计意图**
  一句话主张：读完这章，你将理解 DreamTask 代表的"Agent 主动触发后台工作"模式，以及自主任务调度与用户触发任务在架构上的本质差异。
  （前置依赖：第29章）

---

### 第九篇：Swarm——多智能体协作架构
*目的：理解 Harness·多智能体子系统——从单 Agent 扩展到多 Agent 协作*

- **第33章：Teammate 生命周期——Swarm 架构总览**
  一句话主张：读完这章，你将理解 Claude Code 的多智能体模型——Leader/Teammate 角色划分、生命周期管理、资源清理——并能与其他 Agent 框架的 Swarm 设计进行比较。
  （前置依赖：第29章）

- **第34章：leaderPermissionBridge——跨进程权限协商模式**
  一句话主张：读完这章，你将理解当子 Agent 需要用户确认权限时，消息如何跨越进程边界传递到 Leader 的 UI 层，以及这一"权限代理"模式的实现机制。
  （前置依赖：第33章）

- **第35章：三种 Teammate 后端——`in-process/tmux/auto` 的选型逻辑**
  一句话主张：读完这章，你将理解为什么同一个 Teammate 需要三种不同的运行后端，以及 Claude Code 的自动后端选择算法如何在性能与隔离性之间取得平衡。
  （前置依赖：第33章）

- **第36章：permissionSync——多智能体间的权限同步协议**
  一句话主张：读完这章，你将理解在并发 Agent 场景中，权限状态如何在 Leader 和多个 Teammate 之间保持一致，以及乐观锁与消息广播在此的应用。
  （前置依赖：第34章）

---

### 第十篇：安全权限——Agent 行为的边界工程
*目的：从安全架构视角深潜 Harness·权限护栏子系统——超越第五篇的 Tool 视角入门（ch15-ch16），进入规则引擎、处理器分态和审计追踪的实现细节。注意：Hook 系统已在第七篇（ch24-ch28）作为独立子系统分析，本章聚焦纯权限机制*

- **第37章：权限系统全景——拦截→规则→确认的三层防线**
  一句话主张：读完这章，你将能从全局视角描述 Claude Code 的完整安全架构——PreToolUse 拦截层、PermissionRule 规则层、用户确认层三者如何协同，以及任意一层失守时的降级策略。
  （前置依赖：第15章、第24章）

- **第38章：PermissionRule 规则引擎——`allowedTools` 的 glob 匹配与优先级链**
  一句话主张：读完这章，你将理解 Claude Code 如何用 glob 模式匹配、前缀匹配、精确匹配三种算法处理 `allowedTools` 规则，以及多来源规则（用户/项目/策略）冲突时的优先级解决机制。
  （前置依赖：第37章）

- **第39章：权限处理器三态——`interactive/coordinator/swarmWorker` 的策略差异**
  一句话主张：读完这章，你将理解同一个权限请求在三种运行场景下为何走不同的处理路径——交互模式弹出确认框、协调器模式转发给 Leader、Swarm Worker 模式使用预授权缓存——以及这三个 handler 的分叉判断逻辑。
  （前置依赖：第37章、第33章）

- **第40章：信任对话与拒绝追踪——用户决策的持久化与安全审计**
  一句话主张：读完这章，你将理解 `TrustDialog` 如何把用户的"本次允许/永久允许/拒绝"决策持久化到配置文件，`denialTracking` 如何在跨轮次中记忆拒绝历史以避免重复打扰，以及这一决策审计机制对 Agent 安全可信度的工程价值。
  （前置依赖：第37章）

---

### 第十一篇：Marketplace 与 Plugins——生态扩展架构
*目的：理解 Claude Code 如何通过插件市场和包管理机制实现无源码修改的功能扩展*

- **第41章：Plugin 生命周期——发现、安装、更新与卸载**
  一句话主张：读完这章，你将理解插件从 Marketplace 发现、到本地安装、版本检查、自动更新、到最终卸载的完整生命周期，以及 `plugins/` 目录下的状态管理机制。
  （前置依赖：第14章）

- **第42章：Marketplace 协议——官方注册表与第三方源**
  一句话主张：读完这章，你将理解 Claude Code 的 Marketplace 协议如何支持官方注册表和第三方 npm 源两种插件来源，以及索引协议、签名校验、版本解析的实现细节。
  （前置依赖：第41章）

- **第43章：Plugin 包结构——目录约定、`package.json` 契约与沙箱边界**
  一句话主张：读完这章，你将理解插件包的内部结构——`package.json` 的扩展字段、`antDeps` 依赖隔离；以及 `commands/`、`skills/`、`hooks/`、`agents/`、`mcp/` 等目录约定的绑定机制；以及插件与宿主进程之间的隔离边界。
  （前置依赖：第41章）

---

### 第十二篇：模式提炼——工程启示录
*目的：从具体实现抽象出可复用的 Agent Harness 模式*

- **第44章：Harness 工程模式图谱——12 个可复用设计模式**
  一句话主张：读完这章，你将拥有一张从 Claude Code 提炼的 Agent Harness 模式图谱，每个模式都有名称、问题陈述、解决方案和源码锚点，可直接用于你自己的 Agent 系统设计。
  （前置依赖：第1-43章）

- **第45章：从 CLI 到 Agent 平台——架构跃迁的路线图**
  一句话主张：读完这章，你将理解 Claude Code 的架构演化路径，并能为自己的产品绘制"CLI → 工具宿主 → Agent Harness → 多智能体平台"的演化路线图。
  （前置依赖：第44章）

---

## 三、每章一句话主张（汇总）

| 章 | 篇 | 层 | 一句话主张 |
|----|----|----|-----------|
| 第1章 | 一 | 全局 | 建立 Claude Code 完整架构认知：三层架构与 Harness 层十大子系统职责、技术选型动机、源码组织逻辑 |
| 第2章 | 一 | Harness·辅助 | 掌握"轻量全局状态"模式：模块级单例 vs 依赖注入的工程权衡 |
| 第3章 | 一 | 全局 | 用构建时 DCE 替代运行时 if/else 实现零成本特性隔离 |
| 第4章 | 二 | 交互层·CLI | 理解三路并行启动序列与交互/Headless/SDK/Assistant 四种模式分叉 |
| 第5章 | 二 | 交互层·REPL | 理解 Ink/React 5000 行巨组件的交互设计与推测执行 |
| 第6章 | 二 | 交互层·命令 | 理解"路由决策先于业务逻辑"原则：三条分流路径的判断逻辑 |
| 第7章 | 二 | 交互层·命令 | 掌握"目录即注册表"模式：103 个命令的动态加载与 feature flag 门控 |
| 第8章 | 二 | 交互层·IDE | 理解 Bridge 协议如何桥接终端和 IDE 两种交互界面 |
| 第9章 | 三 | Harness·核心循环 | 识别 AI 工具调用主循环的状态机转换与 Continue/中断设计 |
| 第10章 | 三 | Harness·核心循环 | 掌握 async generator 在高延迟 AI 流式响应中的工程应用 |
| 第11章 | 四 | 模型层·管理 | 理解 Haiku/Sonnet/Opus 三层模型路由与多提供商适配机制 |
| 第12章 | 四 | 模型层·管理 | 理解 effort/fast/thinking 三轴如何交叉控制 AI 推理深度 |
| 第13章 | 四 | 模型层·通信 | 掌握 API 客户端封装、重试机制与提示词缓存命中率优化策略 |
| 第14章 | 五 | Harness·工具 | 掌握统一工厂函数 + 运行时验证的 54 个工具注册模式 |
| 第15章 | 五 | Harness·权限 | 理解四层权限决策链（Tool 视角入门）并将其用于自己的 Agent 权限系统 |
| 第16章 | 五 | Harness·权限 | 分析用 AI 分类器替代规则引擎的工程成本与收益 |
| 第17章 | 五 | Harness·工具 | 对比协议化扩展（MCP）与插件化扩展的架构差异 |
| 第18章 | 五 | Harness·工具 | 理解"声明式能力包"模式：Skill frontmatter 到可执行工具的完整转化链路 |
| 第19章 | 六 | Harness·提示词 | 掌握系统提示分段式组装（缓存/非缓存段落）的顺序与优先级规则 |
| 第20章 | 六 | Harness·提示词 | 理解 CLAUDE.md 五层级扫描与 @include 指令复用的防冲突机制 |
| 第21章 | 六 | Harness·上下文 | 理解"写入先于执行"持久化模式与跨进程会话恢复 |
| 第22章 | 六 | Harness·上下文 | 掌握上下文窗口压缩的触发时机、fork agent 摘要与语义连续性保证 |
| 第23章 | 六 | Harness·上下文 | 理解本地/跨会话/团队三层记忆架构的边界与同步机制 |
| 第24章 | 七 | Harness·Hook | 完整描述一个 AI 操作从 PreToolUse 到 SubagentStop 的钩子序列 |
| 第25章 | 七 | Harness·Hook | 识别多态执行器模式在 Hook 系统中的开放-封闭原则体现 |
| 第26章 | 七 | Harness·Hook | 掌握异步钩子注册表的挂起、超时、取消、回调完整生命周期 |
| 第27章 | 七 | Harness·Hook | 理解配置快照隔离如何保证会话内行为一致性 |
| 第28章 | 七 | Harness·Hook | 分析声明式钩子注册 vs 命令式注册的工程权衡 |
| 第29章 | 八 | Harness·任务 | 理解 7 种任务类型的统一状态机与并发安全的类型守卫 |
| 第30章 | 八 | Harness·任务 | 掌握子进程 Agent 的 I/O 协议设计 |
| 第31章 | 八 | Harness·任务 | 分析远程任务中 SSE/WebSocket/轮询三种通信方式的选型逻辑 |
| 第32章 | 八 | Harness·任务 | 理解"Agent 主动触发"与"用户触发"任务的架构本质差异 |
| 第33章 | 九 | Harness·多智能体 | 理解 Leader/Teammate 多智能体模型与资源清理机制 |
| 第34章 | 九 | Harness·多智能体 | 掌握跨进程权限代理模式的实现机制 |
| 第35章 | 九 | Harness·多智能体 | 分析 in-process/tmux/auto 三种后端的性能与隔离性权衡 |
| 第36章 | 九 | Harness·多智能体 | 理解并发 Agent 场景中权限状态的一致性保证机制 |
| 第37章 | 十 | Harness·权限 | 描述三层防线的整体协同架构及任意层失守时的降级策略 |
| 第38章 | 十 | Harness·权限 | 掌握 allowedTools 规则的三种匹配算法与多来源冲突优先级解决机制 |
| 第39章 | 十 | Harness·权限 | 理解同一权限请求在 interactive/coordinator/swarmWorker 三态下的分叉逻辑 |
| 第40章 | 十 | Harness·权限 | 掌握用户决策持久化、跨轮次拒绝追踪与安全审计机制 |
| 第41章 | 十一 | Harness·辅助 | 理解插件从发现到卸载的完整生命周期及状态管理机制 |
| 第42章 | 十一 | Harness·辅助 | 掌握 Marketplace 协议支持官方注册表和第三方 npm 源的扩展机制 |
| 第43章 | 十一 | Harness·辅助 | 理解插件包的内部结构、依赖隔离与进程沙箱边界 |
| 第44章 | 十二 | 全局 | 获得可直接使用的 12 个 Agent Harness 工程模式图谱 |
| 第45章 | 十二 | 全局 | 能为自己的产品绘制从 CLI 到多智能体平台的演化路线图 |

---

## 四、排除范围

以下内容**不在本书写作范围内**：

1. **Stub 模块**：`src/assistant/`（Assistant 模式，3 个 stub）、`src/ssh/`（SSH 功能）、`src/server/`（服务端组件）、`src/proactive/`（主动建议）——实现缺失，无法提供源码证据
2. **UI 组件细节**：`src/buddy/`（伴侣精灵）、`src/voice/`（语音）、Ink React 组件的渲染逻辑——与 Harness 工程主题关联弱
3. **功能使用教程**：如何配置 Hook、如何使用 MCP——本书分析工程实现，不是用户手册
4. **历史版本对比**：不分析 v2.1.88 之前的版本演化历史（无源码证据）
5. **背景知识补充**：不解释 TypeScript 语法、React 基础、Bun 运行时——假设读者已具备这些知识
6. **`src/components/` 渲染细节**：144 个 Ink 组件的 UI 实现——仅在涉及 Hook/Permission 交互时引用相关组件
7. **Bridge 远程控制协议深潜**：第 8 章覆盖 Bridge 与 LSP 的架构概览，但不深入 `bridge/` 32 个文件中每一个的完整实现细节
8. **外部服务实现**：AWS Bedrock、Azure、GCP 等云平台的具体集成细节

---

## 五、写作风格约定

**写作风格**：`hunter`（模式猎人）

**风格选择理由**：本书的核心读者包括架构师，他们最需要的不是"Claude Code 是什么"，而是"Claude Code 用了什么模式、为什么这样用、我能复用什么"。`hunter` 风格在每章都以"识别一个模式"为主线，先命名、再证伪、再提炼——最终给读者一个有名字的、可携带的工程模式，而非一段孤立的源码分析。

**格式规则**：

1. **源码引用格式**：`src/相对路径:行号` 或 `src/相对路径:函数名`（引用前必须用 `sed -n '[行号]p'` 验证存在）
2. **语言规则**：中文正文，英文技术术语保留原文（如 `AsyncHookRegistry`、`PermissionMode`、`buildTool()`）
3. **代码片段长度**：关键逻辑不超过 25 行；超长时用 `// ...省略N行...` 标注
4. **推断标注**：无源码直接依据的结论标注「（推断）」
5. **模式命名框**：每章识别的核心模式用如下格式展示：
   ```
   ┌─────────────────────────────────────┐
   │ 模式名称：[模式名]                    │
   │ 问题：[一句话描述问题]                │
   │ 解决方案：[一句话描述方案]            │
   │ 源码锚点：[文件:行号 或 函数名]       │
   └─────────────────────────────────────┘
   ```
6. **章节开篇**：每章以一个具体的"猎人发现"场景开篇（如："我在 `hooks.ts:73` 发现了一个奇怪的注释……"），再展开追踪
7. **双线结构**：每章分"源码追踪"和"模式提炼"两节——前者是证据，后者是结论

---

## 六、附录规划

### 附录 A：Hook 事件速查表
- **内容**：所有 20+ HookEvent 类型的速查表
- **列**：事件名 | 触发时机 | Input 类型 | Output 类型 | 典型用途 | 源码位置
- **来源**：`src/utils/hooks.ts` + `src/entrypoints/agentSdkTypes.ts`

### 附录 B：工具权限矩阵
- **内容**：54 个内置工具的权限状态速查
- **列**：工具名 | isMcp | 默认 PermissionMode | 需要用户确认的操作 | 源码位置
- **来源**：`src/tools/` 各工具目录

### 附录 C：关键类型索引
- **内容**：全书引用的核心 TypeScript 类型速查
- **列**：类型名 | 定义文件 | 主要字段摘要 | 首次出现章节
- **关键类型**：`Tool`、`Task`、`TaskType`、`TaskStatus`、`HookEvent`、`HookCommand`、`PermissionMode`、`PermissionResult`、`ToolUseContext`、`AppState`、`State`（query 循环状态）、`CacheSafeParams`

### 附录 D：环境变量参考
- **内容**：Claude Code 所有支持的环境变量速查
- **列**：变量名 | 类型 | 默认值 | 说明 | 影响的模块
- **关键变量**：`ANTHROPIC_API_KEY`、`CLAUDE_MODEL`、`CLAUDE_API_BASE`、`HTTP_PROXY`、`NO_COLOR`、`CLAUDE_CFG_HOOKS_PATH`、`CLAUDE_CODE_COORDINATOR_MODE`
- **来源**：`src/bootstrap/state.ts` + `src/utils/settings/`

### 附录 E：Feature Flag 完整清单
- **内容**：所有 `bun:bundle feature('xxx')` 的条件分支与 flag 名称
- **列**：Flag 名 | 条件分支 | 影响的模块 | 用途说明
- **关键 Flags**：`KAIROS`（Assistant 模块）、`FORK_SUBAGENT`（Fork 子智能体）、`COORDINATOR_MODE`（Coordinator 多智能体编排）、`TRANSCRIPT_CLASSIFIER`（Auto 模式分类器）、`COMPUTER_USE`（计算机使用）
- **来源**：`src/main.tsx` + `bun:bundle` 使用处

### 附录 F：术语表
- **内容**：全书使用的技术术语与专有名词定义
- **格式**：术语（英文原文）| 章节语境 | 一句话定义 | 关联术语
- **收录范围**：Harness、Agent Harness、Interaction Layer、Model Layer、Reconciler、Yoga Layout、Yoga Node、ANSI Escape Sequence、CSI/OSC/DEC/SGR、Feature Flag、DCE（Dead Code Elimination）、PermissionMode、HookEvent、Swarm、Teammate、Ink、termio、SGR、Cursor Managed、Compact Boundary、CacheSafeParams、StreamingToolExecutor、AsyncHookRegistry、Bridge Protocol 等

---

## 元信息

```
PROJECT_ROOT=/Users/liuweiping/repos/claude-code-sourcemap
BOOK_ROOT=/Users/liuweiping/repos/claude-code-sourcemap/book
STYLE_ID=hunter
CHAPTER_COUNT=45
APPENDIX_COUNT=6
PART_COUNT=12
SOURCE_LINES=514678
SOURCE_FILES=2000
VERSION=Claude Code v2.1.88（重建版）
ARCHITECTURE_LAYERS=3
HARNESS_SUBSYSTEMS=10
INTERACTION_SUBSYSTEMS=4
MODEL_SUBSYSTEMS=3
```
