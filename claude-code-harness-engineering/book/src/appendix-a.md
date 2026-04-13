# 附录 A：术语表

本书使用的核心术语，按主题分组。每个术语给出在 Claude Code 语境下的精确定义。

## 架构与系统

**Harness**
: 围绕 LLM/Agent 搭建的运行框架，涵盖提示词管理、工具编排、上下文压缩、多智能体协调、权限护栏等。Claude Code 是目前公开可见的最完整的 Harness 实现。

**QueryEngine**
: Claude Code 的主循环引擎。管理用户输入 → API 调用 → 工具执行 → 响应输出的循环，控制循环的继续、压缩和终止条件。

**REPL**（Read-Eval-Print Loop）
: 交互模式——读取用户输入、模型处理、输出响应、等待下一输入。Claude Code 的 REPL 基于 Ink（React for CLI）渲染。

**Feature Flag**
: 编码"模型能力假设"的编译时/运行时开关。Claude Code 有 89 个 Feature Flag、828 处调用。

**DCE**（Dead Code Elimination，死代码消除）
: Bun 编译时将 `feature()=false` 的代码从产物中物理消除。不是注释掉，不是跳过——代码不存在。

**excluded-strings.txt**
: Bun 的 DCE 配置文件，列出只存在于内部构建的 Feature Flag 名称。flag 名称字符串本身也从外部版本中消除。

## 上下文管理

**autoCompact**
: 上下文接近上限时触发的全量压缩策略。用一次 API 调用生成完整对话摘要，替换整个历史。缓冲区 13000 token，失败 3 次触发熔断。

**microCompact**
: 清除旧工具结果的轻量压缩策略。只处理 COMPACTABLE_TOOLS 白名单中的 8 类工具（FileRead/Shell/Grep/Glob/WebSearch/WebFetch/FileEdit/FileWrite）。

**snipCompact**
: 在历史轮次边界处裁剪消息的压缩策略。删除边界之前的消息块，计算释放的 token 数。

**contextCollapse**
: 投影式上下文折叠。不修改原始消息数组，而是提供一个"折叠视图"。折叠状态存储在独立的 collapse store 中，跨轮次持久化。

**timeBasedMC**（Time-Based MicroCompact）
: 基于 cache TTL 过期的压缩策略。阈值 60 分钟，默认关闭。适合长会话场景。

**Prompt Cache**
: Anthropic API 的缓存机制。相同前缀的消息可以复用之前的计算结果，减少 token 消耗和延迟。缓存 key 由系统提示词、工具、模型、消息前缀和思考配置组成。

**CacheSafeParams**
: fork 时必须与父智能体完全相同的 5 个参数（systemPrompt/userContext/systemContext/toolUseContext/forkContextMessages）。任何一字不同都会导致 Prompt Cache 失效。

## Agent 与并行

**forkedAgent**
: 在主循环之外启动的独立 Agent 会话。隔离对话历史但共享 Prompt Cache。通过 `runForkedAgent` 执行，复用 `lastCacheSafeParams` 全局单例。

**AgentDefinition**
: 智能体的定义结构，包含 agentType、disallowedTools、model、系统提示词等。三种来源：BuiltIn（内置）、Custom（Markdown frontmatter）、Plugin（插件 API），共享 BaseAgentDefinition 接口。

**disallowedTools**
: 智能体的硬性工具禁用列表。被禁用的工具不存在于智能体的工具池中——不是"建议不用"，是"不存在"。planAgent 和 verificationAgent 共享 5 种禁用工具。

**Verification Agent**
: 对抗性验证智能体。目标不是确认代码能运行，而是"拼命让代码崩溃"。系统提示词明确列出模型的 6 种"合理化借口"并逐一对抗。异步执行（background: true）。

**planAgent**
: 只读规划智能体。通过 disallowedTools 硬性保证不能修改文件。系统提示词强调 "CRITICAL: READ-ONLY MODE"。

**exploreAgent**
: 快速搜索智能体。使用 haiku 模型（外部用户）或 inherit（内部用户），每周被调用超过 3400 万次。

**Coordinator Mode**
: 多智能体协调模式。协调器分配任务，worker 独立执行并汇报结果。需要 Feature Flag + 环境变量双重启用。

**BackendType**
: 队友执行后端类型。三种：in-process（同进程）、tmux（独立终端）、iterm2（iTerm2 原生分屏）。控制进程隔离级别。

**teammateMailbox**
: 基于文件系统的 Agent 间消息队列。源码注释定义："File-based messaging system for agent swarms"。跨进程可用，I/O 延迟。

**SendMessage**
: 队友间实时通信工具。通过 `to: "<name>"` 发送给指定队友，`to: "*"` 广播。

## 提示词与记忆

**System Prompt**（系统提示词）
: 分层构建的完整系统提示词。通过 DYNAMIC_BOUNDARY 分为静态区（缓存友好）和动态区（每次重新生成）。

**DYNAMIC_BOUNDARY**
: 系统提示词中静态区与动态区的分界标记。静态区包含角色定义和工具说明（缓存命中），动态区包含当前工作目录、文件列表等（每次不同）。

**CLAUDE.md**
: 四层记忆体系：Managed（全局管理） → User（用户全局） → Project（项目级） → Local（本地私有）。后加载的优先级更高。

**MEMORY.md**
: 记忆系统的入口文件。限制 200 行 / 25000 字节。通过 `@include` 指向详细记忆文件。

**memoryTypes**
: 4 种记忆类型：user（用户偏好）、feedback（用户反馈）、project（项目知识）、reference（参考资料）。选择标准：只存"不可从项目状态推导的信息"。

**omitClaudeMd**
: 子智能体省略 CLAUDE.md 加载的配置。Explore 智能体每周 3400 万次调用，省略不必要的 CLAUDE.md 每周节省 5-15 Gtoken。

**自动记忆提取**（initExtractMemories）
: 从对话中自动识别值得记忆的内容并写入记忆文件。每次会话独立初始化（闭包隔离），异步执行。

## 安全与权限

**Permission Mode**（权限模式）
: 权限谱系模式。5 个外部模式（default/acceptEdits/plan/dontAsk/bypassPermissions）+ 2 个内部模式（auto/bubble）。默认值是 default（最严格）。

**auto 模式**
: AI 分类器自动判断工具调用是否安全的内部模式。通过 `USER_TYPE === 'ant'` 判断和 Feature Flag 控制，仅内部用户可用。

**4 层纵深防御**
: auto 模式下的权限判断链：规则分类器 → 危险模式库 → AI 分类器 → 否决追踪。每层独立判断，互为兜底。

**DENIAL_LIMITS**
: 否决追踪上限：maxConsecutive=3（连续否决不超过 3 次）、maxTotal=20（总计否决不超过 20 次）。超限后 shouldFallbackToPrompting=true，强制回退人工确认。

**CROSS_PLATFORM_CODE_EXEC**
: 危险模式库。硬编码的代码执行入口点列表（python/node/bash/sh 等），在 AI 分类器之前提供不可绕过的硬拒绝。

**Hook**
: 在 Harness 生命周期特定时机点插入自定义逻辑的事件系统。27 种事件类型（HOOK_EVENTS），4 种执行方式（command/prompt/agent/http）。

**Stop Hook**
: 查询循环结束时触发的事件。通常配置为 agent Hook，用 AI 验证任务是否真正完成。

**HOOK_EVENTS**
: 27 个预定义触发点的完整列表。覆盖工具调用（Pre/PostToolUse）、会话边界（SessionStart/End）、权限（PermissionRequest）、压缩（Pre/PostCompact）等。

## 工具系统

**buildTool**
: 工具的工厂函数。统一接口定义 isEnabled（是否可用）、isAllowed（是否被允许）、execute（执行逻辑）。所有工具共享相同的注册和调度路径。

**StreamingToolExecutor**
: 并发工具执行器。支持工具的流式输出（yield），只读工具可并发执行，写操作工具串行执行。

**SkillTool**
: 技能工具。延迟加载技能定义，将 100+ 技能文件缩减为 1% 上下文预算。模型看到技能摘要，需要时才加载全文。

**COMPACTABLE_TOOLS**
: microCompact 可清除的工具白名单。8 类：FileRead、Shell、Grep、Glob、WebSearch、WebFetch、FileEdit、FileWrite。白名单外的工具结果不会被清除。

## 压缩常量

**AUTOCOMPACT_BUFFER_TOKENS**
: autoCompact 的摘要生成缓冲区，13000 token。编码假设"模型需要至少 13000 token 才能完成高质量摘要"。

**POST_COMPACT_TOKEN_BUDGET**
: 压缩后资源恢复预算，50000 token。压缩后重新读取最近 5 个文件，重建模型的工作记忆。

**MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES**
: autoCompact 连续失败熔断阈值，3 次。源码注释记录真实生产数据：曾有 1279 个会话 50+ 次连续失败，每天浪费约 25 万次 API 调用。

---

> 参见正文各章节获取每个术语的完整分析和源码锚点。
