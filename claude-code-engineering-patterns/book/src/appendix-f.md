# 附录 F：术语表

本附录收录全书涉及的核心技术术语与专有名词，按英文字母顺序排列，每条包含中英文名称、简明定义及首次出现章节，供交叉查阅使用。

---

## A

**Agent Harness**（Agent 运行框架）
包裹 AI Agent 的工程基础设施层，提供工具调用、上下文管理、权限控制等能力，将 AI 的不确定性约束在确定性边界内。区别于模型本身，Harness 是让模型"能做事"的工程系统。首次出现：第 1 章。

---

**ANSI Escape Sequence**（ANSI 转义序列）
嵌入终端文本输出中的控制序列（格式：ESC + `[` + 参数 + 命令字节），用于控制光标移动、文本颜色和文本样式。Claude Code 的 TUI 界面广泛使用此类序列实现终端渲染效果。首次出现：第 5 章。

---

**Async Generator**（异步生成器）
TypeScript / JavaScript 中的 `async function*` 语法，可通过 `yield` 分批产出中间结果，调用方以 `for await...of` 消费。Claude Code 的工具执行接口普遍采用此模式，用于流式返回 AI 响应和工具输出。首次出现：第 10 章。

---

**AsyncHookRegistry**（异步钩子注册表）
管理异步钩子执行的注册表，追踪待处理的钩子 Promise 并施加超时限制，防止钩子阻塞主执行循环。位于 `src/utils/hooks/`。首次出现：第 26 章。

---

## B

**Bridge Protocol**（桥接协议）
Claude Code 中的远程连接协议（由 `BRIDGE_MODE` Feature Flag 控制），允许外部客户端通过桥接服务器连接并控制正在运行的 Claude Code 会话。首次出现：第 12 章。

---

**buildTool**（工具工厂函数）
Claude Code 中统一创建工具实例的工厂函数，位于 `src/Tool.ts:783`。接收包含 `isMcp`、`isEnabled`、`isAllowed`、`execute` 等字段的配置对象，返回符合 `Tool` 接口的工具实例。所有内置工具均通过此函数注册。首次出现：第 14 章。

---

## C

**CacheSafeParams**（缓存安全参数）
为最大化提示缓存命中率而设计的 API 请求参数集合，通过确保请求的可缓存前缀在多个对话轮次中保持稳定来利用 Anthropic 的提示缓存功能。首次出现：第 13 章。

---

**CLAUDE.md**（Claude 指令文件）
放置在项目根目录（或用户 Home 目录）的 Markdown 文件，Claude Code 启动时自动加载并注入为系统指令。用于声明项目约定、编码规范、禁止行为等持久化上下文。首次出现：第 12 章。

---

**Compact / Compaction**（上下文压缩）
当对话历史长度接近模型上下文窗口上限时，自动生成摘要替换早期消息，以释放 Token 空间同时保留关键信息。Claude Code 中由 `REACTIVE_COMPACT` 和 `CONTEXT_COLLAPSE` Feature Flag 控制。首次出现：第 22 章。

---

**Compact Boundary**（压缩边界）
触发自动上下文压缩的 Token 阈值，通常设置在上下文窗口的约 80% 处。当对话历史超过此边界时，压缩过程会对早期消息生成摘要以释放空间。首次出现：第 22 章。

---

**CSI / OSC / SGR**
终端控制序列的分类：CSI（Control Sequence Introducer，ESC+[）用于光标和显示控制；OSC（Operating System Command，ESC+]）用于操作系统级功能；SGR（Select Graphic Rendition）用于文本样式设置。三者均为 ANSI 转义序列的子类别。首次出现：第 5 章。

---

**Cursor Managed**（光标托管模式）
一种终端渲染模式，应用程序完全接管光标定位控制权，隐藏系统光标并在每次状态变更时重绘整个 UI。Claude Code 的交互式 REPL 模式采用此模式实现流畅的终端界面渲染。首次出现：第 5 章。

---

## D

**DCE**（Dead Code Elimination，死代码消除）
编译期移除程序中永远不会被执行的代码分支的优化技术。Claude Code 通过 `bun:bundle` 的 `feature('FLAG_NAME')` 调用实现 DCE，未启用的 Feature Flag 对应代码在打包时被完全移除，不参与运行时。首次出现：第 1 章。

---

**Discriminated Union**（判别联合类型）
TypeScript 中通过公共字面量字段（判别符，discriminant）区分多个不同 shape 的 union 类型。编译器可在 `switch/if` 分支中自动收窄（narrow）类型，无需手动类型断言。Claude Code 大量使用此模式描述工具结果、Agent 消息等多态结构。首次出现：第 37 章。

---

## F

**Fail-closed**（失败关闭默认）
系统在状态不确定时默认拒绝操作而非允许，是安全敏感系统的防守性设计原则。Claude Code 权限系统在无法确定操作是否安全时采用此策略，宁可误拒也不误放。首次出现：第 37 章。

---

**Feature Flag**（特性开关）
编译期条件开关，在 Claude Code 中通过 `feature('FLAG_NAME')` 表达。与运行时开关不同，Feature Flag 在 `bun build` 时即被固化，未启用的分支经 DCE 完全消除。详见附录 E。首次出现：第 1 章。

---

**Fire-and-forget**（即发即忘）
触发异步操作后不等待其完成、不处理其返回值的编程模式。适用于非关键路径的后台任务（如遥测上报、日志写入）。在 Claude Code 中常见于 analytics 和 prefetch 场景。首次出现：第 4 章。

---

**Frontmatter**（文档前置元数据）
Markdown 文件开头由 `---` 包裹的 YAML 格式元数据区块。Claude Code 的 slash 命令通过 Frontmatter 声明 `allowed-tools`、`description` 等属性，插件系统在加载时解析此区块。首次出现：第 14 章。

---

## H

**Harness**（运行框架 / 执行环境）
包裹和管理 AI 行为的工程系统，提供执行环境、工具接口、权限约束等。与"Agent"概念区分：Agent 是 AI 决策实体，Harness 是承载 Agent 运行的工程基础设施。首次出现：第 1 章。

---

**Hook**（钩子）
在特定生命周期事件（`PreToolUse`、`PostToolUse`、`SessionStart`、`Stop` 等）触发的用户自定义脚本。通过 `~/.claude/settings.json` 的 `hooks` 字段配置，支持 shell 脚本或可执行程序。首次出现：第 24 章。

---

**HookEvent**（钩子事件）
对钩子触发时机进行分类的事件类型枚举，包括 `PreToolUse`、`PostToolUse`、`SessionStart`、`Stop` 等值。与 Hook 概念不同，HookEvent 专指触发分类，定义于 `src/entrypoints/sdk/coreTypes.ts`。首次出现：第 24 章。

---

## I

**Ink**（终端 React 框架）
用于在终端环境中渲染 React 组件树的 JavaScript 库。Claude Code 的整个 TUI 界面基于 Ink 构建，将 React 的声明式 UI 模型引入命令行交互场景。首次出现：第 5 章。

---

**Interaction Layer**（交互层）
Claude Code 基于 Ink/React 构建的 UI 与输入层，处理用户键盘/鼠标输入、渲染终端 UI 组件、处理来自 REPL 的事件。在架构上位于用户与核心循环（Core Loop）之间。首次出现：第 4 章。

---

## L

**LSP**（Language Server Protocol，语言服务器协议）
由 Microsoft 提出的编辑器与语言工具之间的标准通信协议，定义了代码补全、跳转定义、诊断等语言特性的请求/响应格式。Claude Code 通过 LSPTool 与外部语言服务器集成，获取代码语义信息。首次出现：第 8 章。

---

## M

**Marketplace**（插件市场）
Claude Code 的插件来源管理系统，支持 GitHub 仓库、远程 URL、本地路径等多种插件安装来源，提供版本管理、信任验证和权限审批功能。首次出现：第 42 章。

---

**MCP**（Model Context Protocol，模型上下文协议）
Anthropic 开发并开源的 AI 工具调用标准协议，定义了模型与外部工具/数据源之间的通信规范，支持 stdio 和 SSE 两种传输层。Claude Code 内置 MCP 客户端，可挂载任意符合协议的 MCP Server。首次出现：第 21 章。

---

**Model Layer**（模型层）
负责模型选择、提供商路由（Anthropic 直连、Bedrock、Vertex、Foundry）、推理配置和 API 通信的子系统。将上层查询请求转化为具体的模型调用，屏蔽不同云提供商之间的差异。首次出现：第 11 章。

---

## P

**PermissionMode**（权限模式）
Claude Code 的权限级别枚举，包括 `auto`（自动判断）、`plan`（计划确认后执行）、`bypass`（跳过确认）等模式，决定工具调用时的授权方式和用户交互方式。首次出现：第 11 章。

---

**Plugin**（插件）
通过 Marketplace 安装的功能扩展包。遵循目录约定，可在 `commands/`、`agents/`、`hooks/`、`skills/` 等子目录下声明对应能力。Claude Code 在启动时扫描并加载已安装插件。首次出现：第 29 章。

---

## Q

**QueryEngine**（查询引擎）
Claude Code 的核心协调类，负责管理多轮工具调用循环、组装系统提示与对话上下文、调度子 Agent 任务、处理流式响应。是连接用户输入、模型推理与工具执行的枢纽组件，位于 `src/QueryEngine.ts`。首次出现：第 10 章。

---

## R

**Reconciler**（协调器）
Ink 的 React 协调器，将 React 虚拟 DOM 适配到终端输出，管理 ANSI 转义序列和光标定位以实现终端渲染。它是 Ink 框架的核心机制，使 React 的差量更新模型能够在 TTY 环境中高效运作。首次出现：第 5 章。

---

## S

**SDK Mode**（SDK 模式）
通过编程接口将 Claude Code 嵌入其他应用的运行模式，以库而非 CLI 的形式提供 Agent 能力。在此模式下，宿主应用控制输入输出，Claude Code 仅提供推理和工具调用能力。首次出现：第 4 章。

---

**Skill**（技能）
可复用的 Markdown 指令包，通过 `SKILL.md` 文件声明。可由插件提供，也可内置于 Claude Code。用户通过 slash 命令调用 Skill，系统将其内容注入对话上下文作为行为指令。首次出现：第 18 章。

---

**StreamingToolExecutor**（流式工具执行器）
在流式 API 响应过程中负责执行工具的组件，协调流式消息解析器与工具执行管道之间的交互，确保工具调用在流式输出中被正确识别、调度和结果回填。首次出现：第 10 章。

---

**Swarm**（集群）
Claude Code 的多智能体协作架构，由一个领导者（Leader）Agent 协调多个队友（Teammate）Agent 并行工作，通过共享 Memory 和消息通道协同完成复杂任务。首次出现：第 29 章。

---

## T

**Task**（任务）
Claude Code 中封装后台 Agent 执行单元的对象，具有 `pending` → `running` → `complete` / `failed` 生命周期状态机。由 TaskTool 创建，可被 MonitorTool 查询，支持结果持久化。首次出现：第 29 章。

---

**Teammate**（队友）
Swarm 架构中由领导者 Agent 派生和管理的子 Agent 实例。每个 Teammate 拥有独立的上下文和工具权限，完成分配的子任务后将结果汇报给领导者。首次出现：第 29 章。

---

**termio**（终端 I/O）
Claude Code 中的终端 I/O 抽象层，封装原始 TTY 操作，处理光标可见性控制、原始模式切换管理，并为 Ink 提供渲染表面。首次出现：第 5 章。

---

**Token Budget**（Token 预算）
分配给 Agent 单次执行任务的最大 Token 使用量上限。超出预算时触发截断、压缩或任务中止逻辑，防止单次任务无限消耗资源。由 `TOKEN_BUDGET` Feature Flag 控制启用。首次出现：第 22 章。

---

**Transcript**（转录文件）
记录完整对话历史（包括用户消息、Assistant 响应、工具调用结果）的持久化 JSON 文件，存储于 `~/.claude/projects/` 目录下。用于会话恢复（`--continue`）和历史回放，也是 `TRANSCRIPT_CLASSIFIER` 处理的数据源。首次出现：第 21 章。

---

## Y

**Yoga Layout**（Yoga 布局引擎）
Facebook 开发的跨平台布局引擎，在非浏览器环境中实现 CSS Flexbox 规范。Ink 使用 Yoga 计算终端组件的尺寸和位置，使 Box 组件能够基于 Flexbox 模型进行弹性布局。首次出现：第 5 章。

---

**Yoga Node**（Yoga 节点）
Yoga 引擎中的布局计算单元。每个 Ink Box 组件对应一个 Yoga Node，参与 Flexbox 布局计算，最终由 Yoga 引擎确定该组件在终端中的坐标和尺寸。首次出现：第 5 章。
