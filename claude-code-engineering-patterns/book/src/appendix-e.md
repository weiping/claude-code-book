# 附录 E：Feature Flag 完整清单

Claude Code 使用 `bun:bundle` 提供的编译期 `feature()` 函数来实现功能开关。与运行时条件分支不同，`feature()` 在打包阶段即被求值：当某个 Flag 被禁用时，其对应的代码分支在编译期就会被消除（Dead Code Elimination，DCE），最终产物中不含任何残留字节码。这一机制使得同一份源码可以生成面向不同市场、不同部署场景的二进制产物，同时保持极低的运行时开销。关于 DCE 原理与 `bun:bundle` 构建流程的详细分析，请参见**第 3 章**。

本附录收录了在 v2.1.88 重建源码中发现的全部 **89 个**唯一 Feature Flag，涵盖 6 个功能域分组。各 Flag 的引用次数基于对 `src/` 目录 `.ts`/`.tsx` 文件的 `grep` 统计。

> **关于 `COMPUTER_USE`**：源码中存在 `COMPUTER_USE_MCP_SERVER_NAME` 常量及 `computerUse/` 目录，但 `feature('COMPUTER_USE')` 在重建版中**引用次数为 0**。Computer Use 功能通过 MCP 服务器注册机制（`CHICAGO_MCP` flag）而非独立 Feature Flag 来控制，详见 `src/utils/computerUse/` 及 `src/main.tsx`。

---

## E.1 核心功能 Flag

这些 Flag 控制 Claude Code 主会话循环中的核心行为，包括消息分类、上下文管理与历史处理。

| Flag 名 | 功能描述 | 引用次数 | 主要模块（真实源文件路径） | 正文章节 |
|---|---|---|---|---|
| `TRANSCRIPT_CLASSIFIER` | 启用会话转录分类器，对对话历史进行自动分类和路由，影响 Auto 模式的行为决策 | 107 | `src/main.tsx`、`src/tools/AgentTool/AgentTool.tsx`、`src/migrations/resetAutoModeOptInForDefaultOffer.ts` | 第 9–10 章 |
| `BASH_CLASSIFIER` | 启用 Bash 命令安全分类器，对 shell 命令进行危险性评分，决定是否需要用户确认 | 45 | `src/tools/BashTool/bashPermissions.ts`、`src/utils/permissions/yoloClassifier.ts`、`src/utils/swarm/inProcessRunner.ts` | 第 37–40 章 |
| `REACTIVE_COMPACT` | 启用响应式上下文压缩——在 token 接近上限时自动触发压缩，而非依赖固定阈值 | 4 | `src/utils/analyzeContext.ts`、`src/services/compact/autoCompact.ts`、`src/commands/compact/compact.ts` | 第 22 章 |
| `CONTEXT_COLLAPSE` | 启用上下文折叠机制，将历史消息折叠为摘要以节省 token | 20 | `src/utils/analyzeContext.ts`、`src/utils/sessionRestore.ts`、`src/screens/REPL.tsx` | 第 22 章 |
| `HISTORY_SNIP` | 启用对话历史裁剪，从旧消息中移除冗余内容（如大文件读取结果） | 15 | `src/QueryEngine.ts`、`src/utils/messages.ts`、`src/utils/attachments.ts` | 第 9–10 章 |
| `TOKEN_BUDGET` | 启用 token 预算跟踪与可视化，在 UI 中显示剩余 token 配额 | 9 | `src/constants/prompts.ts`、`src/screens/REPL.tsx`、`src/components/PromptInput/PromptInput.tsx` | 第 22 章 |
| `FORK_SUBAGENT` | 启用 fork 模式子代理——通过进程级复制创建隔离的子代理实例 | 4 | `src/tools/AgentTool/forkSubagent.ts`、`src/commands/branch/index.ts`、`src/commands.ts` | 第 33–36 章 |
| `HISTORY_PICKER` | 启用历史会话搜索与选择 UI，允许用户从历史对话中快速检索并恢复 | 4 | `src/hooks/useHistorySearch.ts`、`src/components/PromptInput/PromptInput.tsx` | 第 9–10 章 |

---

## E.2 Agent / 多智能体 Flag

这些 Flag 控制 Kairos 异步代理框架、协调者模式、后台会话及多智能体协作相关功能。

| Flag 名 | 功能描述 | 引用次数 | 主要模块（真实源文件路径） | 正文章节 |
|---|---|---|---|---|
| `KAIROS` | Kairos 异步代理框架总开关，控制全部异步后台代理能力的启用 | 154 | `src/main.tsx`、`src/commands.ts`、`src/tools/AgentTool/AgentTool.tsx` | 第 33–36 章 |
| `KAIROS_BRIEF` | 启用 Kairos Brief 工具——代理生成结构化简报并上传至协作频道 | 39 | `src/tools/BriefTool/BriefTool.ts`、`src/main.tsx`、`src/keybindings/defaultBindings.ts` | 第 33–36 章 |
| `KAIROS_CHANNELS` | 启用 Kairos 消息频道机制，用于代理间的异步消息传递 | 19 | `src/utils/messageQueueManager.ts`、`src/tools/AskUserQuestionTool/AskUserQuestionTool.tsx`、`src/main.tsx` | 第 33–36 章 |
| `KAIROS_DREAM` | 启用 Kairos Dream 模式——代理在空闲时进行自主探索与学习 | 1 | `src/skills/bundled/index.ts` | 第 33–36 章 |
| `KAIROS_GITHUB_WEBHOOKS` | 启用 Kairos GitHub Webhook 集成，允许代理响应 GitHub 事件触发 | 3 | `src/hooks/useReplBridge.tsx`、`src/tools.ts`、`src/commands.ts` | 第 33–36 章 |
| `KAIROS_PUSH_NOTIFICATION` | 启用 Kairos 推送通知，向用户设备推送代理状态更新 | 4 | `src/tools/ConfigTool/supportedSettings.ts`、`src/components/Settings/Config.tsx`、`src/tools.ts` | 第 33–36 章 |
| `COORDINATOR_MODE` | 启用协调者模式——一个专用的 orchestrator 代理负责分配子任务给多个工作代理 | 32 | `src/coordinator/coordinatorMode.ts`、`src/tools/AgentTool/builtInAgents.ts`、`src/main.tsx` | 第 33–36 章 |
| `BG_SESSIONS` | 启用后台会话管理，允许多个 Claude 会话并发运行而不阻塞前台 UI | 11 | `src/utils/concurrentSessions.ts`、`src/utils/conversationRecovery.ts`、`src/main.tsx` | 第 33–36 章 |
| `BRIDGE_MODE` | 启用桥接模式，允许 Claude 作为代理桥接器连接远端会话 | 28 | `src/bridge/remoteBridgeCore.ts`、`src/tools/BriefTool/upload.ts`、`src/main.tsx` | 第 33–36 章 |
| `TERMINAL_PANEL` | 启用终端面板 UI 组件，在 IDE 集成场景下提供嵌入式终端 | 4 | `src/tools.ts`、`src/keybindings/defaultBindings.ts`、`src/utils/permissions/classifierDecision.ts` | 第 33–36 章 |
| `AGENT_TRIGGERS` | 启用代理触发器（含定时调度 Cron），允许注册基于事件或时间的代理激活条件 | 11 | `src/tools/ScheduleCronTool/prompt.ts`、`src/constants/tools.ts`、`src/screens/REPL.tsx` | 第 33–36 章 |
| `AGENT_TRIGGERS_REMOTE` | 启用远程代理触发器，允许来自外部系统的 HTTP/Webhook 触发 | 2 | `src/tools.ts`、`src/skills/bundled/index.ts` | 第 33–36 章 |
| `TEAMMEM` | 启用团队共享记忆（Team Memory）目录，多代理可共同读写共享知识库 | 51 | `src/memdir/memdir.ts`、`src/utils/memory/types.ts`、`src/utils/memoryFileDetection.ts` | 第 33–36 章 |
| `BUDDY` | 启用 Buddy 伴侣精灵——一个显示在 UI 角落的动画小精灵，提供状态反馈 | 15 | `src/buddy/prompt.ts`、`src/buddy/CompanionSprite.tsx`、`src/buddy/useBuddyNotification.tsx` | — |
| `MONITOR_TOOL` | 启用 Monitor Tool，允许代理监控其他代理的状态和输出 | 13 | `src/commands.ts`（多处引用） | 第 33–36 章 |
| `DAEMON` | 启用守护进程模式，Claude 作为后台服务常驻运行 | 3 | `src/entrypoints/cli.tsx`、`src/commands.ts` | 第 33–36 章 |
| `AGENT_MEMORY_SNAPSHOT` | 启用代理内存快照，在会话切换时保存和恢复代理的工作状态 | 2 | `src/main.tsx`（多处引用） | 第 33–36 章 |

---

## E.3 工具 / 插件 / Skill Flag

这些 Flag 控制内置工具、MCP 插件扩展以及 Skill 系统的功能开关。

| Flag 名 | 功能描述 | 引用次数 | 主要模块（真实源文件路径） | 正文章节 |
|---|---|---|---|---|
| `MCP_SKILLS` | 启用通过 MCP 服务器发布和加载 Skill 的能力 | 9 | `src/services/mcp/client.ts`、`src/services/mcp/useManageMCPConnections.ts`、`src/commands.ts` | 第 41–43 章 |
| `MCP_RICH_OUTPUT` | 启用 MCP 工具的富文本输出渲染（含图像、Markdown 等格式） | 3 | `src/tools/MCPTool/UI.tsx` | 第 41–43 章 |
| `WEB_BROWSER_TOOL` | 启用内置 Web 浏览器工具，允许 Claude 浏览网页 | 4 | `src/tools.ts`、`src/screens/REPL.tsx`、`src/main.tsx` | 第 41–43 章 |
| `REVIEW_ARTIFACT` | 启用代码审查产物（Artifact）生成，将审查结果结构化输出 | 4 | `src/components/permissions/PermissionRequest.tsx`、`src/skills/bundled/index.ts` | 第 29–32 章 |
| `EXPERIMENTAL_SKILL_SEARCH` | 启用实验性 Skill 搜索功能，通过语义检索在 Skill 库中查找最匹配的技能 | 21 | `src/tools/SkillTool/SkillTool.ts`、`src/constants/prompts.ts`、`src/utils/messages.ts` | 第 41–43 章 |
| `BUILTIN_EXPLORE_PLAN_AGENTS` | 启用内置的探索（Explore）和计划（Plan）内置代理 | 1 | `src/tools/AgentTool/builtInAgents.ts` | 第 33–36 章 |
| `EXTRACT_MEMORIES` | 启用自动记忆提取，Claude 在对话结束后将关键信息写入记忆目录 | 7 | `src/memdir/paths.ts`、`src/utils/backgroundHousekeeping.ts`、`src/query/stopHooks.ts` | 第 33–36 章 |
| `ULTRAPLAN` | 启用 UltraPlan 扩展计划模式，提供更强大的多步骤任务规划能力 | 10 | `src/screens/REPL.tsx`、`src/utils/processUserInput/processUserInput.ts`、`src/commands.ts` | 第 29–32 章 |
| `ULTRATHINK` | 启用 UltraThink 深度思考模式，增加扩展思考的 token 预算 | 1 | `src/utils/thinking.ts` | 第 9–10 章 |
| `TORCH` | 启用 Torch 工具（实验性，具体功能未完全重建） | 1 | `src/commands.ts` | — |
| `OVERFLOW_TEST_TOOL` | 启用溢出测试工具，用于测试上下文超限场景 | 2 | `src/tools.ts`、`src/utils/permissions/classifierDecision.ts` | — |
| `WORKFLOW_SCRIPTS` | 启用工作流脚本功能，允许用户定义和运行自动化工作流 | 10 | `src/constants/tools.ts`、`src/components/tasks/BackgroundTasksDialog.tsx`、`src/components/permissions/PermissionRequest.tsx` | 第 29–32 章 |
| `VERIFICATION_AGENT` | 启用验证代理，在任务完成后自动运行验证检查 | 4 | `src/tools/AgentTool/builtInAgents.ts`、`src/tools/TaskUpdateTool/TaskUpdateTool.ts`、`src/constants/prompts.ts` | 第 33–36 章 |
| `SKILL_IMPROVEMENT` | 启用 Skill 自动改进功能，收集执行反馈并更新 Skill 定义 | 1 | `src/utils/hooks/skillImprovement.ts` | 第 41–43 章 |
| `RUN_SKILL_GENERATOR` | 启用 Skill 生成器运行，允许 Claude 自动创建新的 Skill | 1 | `src/skills/bundled/index.ts` | 第 41–43 章 |

---

## E.4 上下文 / 压缩 / 提示词 Flag

这些 Flag 控制上下文压缩策略、提示词缓存检测以及 UI 输出行为。

| Flag 名 | 功能描述 | 引用次数 | 主要模块（真实源文件路径） | 正文章节 |
|---|---|---|---|---|
| `CACHED_MICROCOMPACT` | 启用缓存感知的微型压缩——在压缩时尽量保留 prompt cache 命中率 | 12 | `src/services/compact/microCompact.ts`、`src/constants/prompts.ts`、`src/services/api/claude.ts` | 第 22 章 |
| `COMPACTION_REMINDERS` | 启用压缩提醒——在系统提示中插入提醒文字，告知模型历史已被压缩 | 1 | `src/utils/attachments.ts` | 第 22 章 |
| `PROMPT_CACHE_BREAK_DETECTION` | 启用 prompt cache 断裂检测，识别并上报破坏缓存命中的操作 | 9 | `src/services/compact/compact.ts`、`src/services/compact/autoCompact.ts`、`src/tools/AgentTool/runAgent.ts` | 第 22 章 |
| `CONNECTOR_TEXT` | 启用连接器文本 beta 功能（`connector-text-modality` API beta），扩展多模态连接能力 | 7 | `src/constants/betas.ts`、`src/utils/messages.ts`、`src/services/api/claude.ts` | 第 9–10 章 |
| `HOOK_PROMPTS` | 启用 Hook 提示词注入，允许用户钩子向系统提示中插入自定义内容 | 1 | `src/screens/REPL.tsx` | 第 24–26 章 |
| `STREAMLINED_OUTPUT` | 启用精简输出模式，减少 CLI 非交互场景中的冗余 UI 渲染 | 1 | `src/cli/print.ts` | — |
| `AWAY_SUMMARY` | 启用离开摘要——用户离开后返回时显示任务进展摘要 | 2 | `src/hooks/useAwaySummary.ts`、`src/screens/REPL.tsx` | 第 9–10 章 |
| `MESSAGE_ACTIONS` | 启用消息操作菜单，允许用户对单条消息执行编辑、复制、重试等操作 | 5 | `src/keybindings/defaultBindings.ts`、`src/screens/REPL.tsx` | — |
| `QUICK_SEARCH` | 启用快速搜索快捷键，通过键盘快捷方式搜索历史消息或文件 | 5 | `src/keybindings/defaultBindings.ts`、`src/components/PromptInput/PromptInput.tsx` | — |
| `FILE_PERSISTENCE` | 启用文件持久化机制，将对话状态、输出等写入磁盘以供后续恢复 | 3 | `src/utils/filePersistence/filePersistence.ts`、`src/cli/print.ts` | — |

---

## E.5 连接 / 通信 Flag

这些 Flag 控制网络连接模式、远程会话桥接、Unix Domain Socket 通信及用户设置同步。

| Flag 名 | 功能描述 | 引用次数 | 主要模块（真实源文件路径） | 正文章节 |
|---|---|---|---|---|
| `DIRECT_CONNECT` | 启用直连模式，绕过代理服务器直接连接 Anthropic API | 5 | `src/main.tsx` | — |
| `SSH_REMOTE` | 启用 SSH 远程模式，允许 Claude 通过 SSH 隧道连接远端工作目录 | 4 | `src/main.tsx`（多处引用） | — |
| `UDS_INBOX` | 启用 Unix Domain Socket 收件箱，用于进程间消息传递（IPC） | 17 | `src/tools/SendMessageTool/SendMessageTool.ts`、`src/setup.ts`、`src/main.tsx` | 第 33–36 章 |
| `LODESTONE` | 启用 Lodestone 功能——用于工作目录锁定与项目定位的导航机制 | 6 | `src/utils/settings/types.ts`、`src/utils/backgroundHousekeeping.ts`、`src/main.tsx` | — |
| `CCR_MIRROR` | 启用 CCR（Claude Code Remote）镜像模式，将本地会话镜像到远端 | 4 | `src/bridge/remoteBridgeCore.ts`、`src/bridge/bridgeEnabled.ts`、`src/main.tsx` | 第 33–36 章 |
| `CCR_AUTO_CONNECT` | 启用 CCR 自动连接，检测到可用远端时自动建立镜像连接 | 3 | `src/bridge/bridgeEnabled.ts`、`src/utils/config.ts` | 第 33–36 章 |
| `CCR_REMOTE_SETUP` | 启用 CCR 远端初始化向导，引导用户完成远端环境配置 | 1 | `src/commands.ts` | 第 33–36 章 |
| `CHICAGO_MCP` | 启用 Chicago MCP 服务器——Computer Use 功能的核心 MCP 集成 | 16 | `src/utils/computerUse/wrapper.tsx`、`src/state/AppStateStore.ts`、`src/entrypoints/cli.tsx` | 第 41–43 章 |
| `UPLOAD_USER_SETTINGS` | 启用用户设置上传，将本地配置同步到 Anthropic 云端 | 2 | `src/services/settingsSync/index.ts`、`src/main.tsx` | — |
| `DOWNLOAD_USER_SETTINGS` | 启用用户设置下载，从云端拉取并应用用户配置 | 5 | `src/services/settingsSync/index.ts`、`src/commands/reload-plugins/reload-plugins.ts` | — |

---

## E.6 遥测 / 调试 Flag

这些 Flag 控制性能统计、链路追踪、调试输出以及 A/B 测试基线设置。

| Flag 名 | 功能描述 | 引用次数 | 主要模块（真实源文件路径） | 正文章节 |
|---|---|---|---|---|
| `SHOT_STATS` | 启用会话统计面板，显示 token 使用量、工具调用次数等指标 | 10 | `src/utils/stats.ts`、`src/utils/statsCache.ts`、`src/components/Stats.tsx` | — |
| `PERFETTO_TRACING` | 启用 Perfetto 性能追踪，将事件写入 Perfetto 格式的追踪文件 | 1 | `src/utils/telemetry/perfettoTracing.ts` | — |
| `ENHANCED_TELEMETRY_BETA` | 启用增强遥测 beta——收集更详细的会话追踪数据（需用户同意） | 2 | `src/utils/telemetry/sessionTracing.ts` | — |
| `COMMIT_ATTRIBUTION` | 启用提交归因，在 git commit 中记录 Claude 生成的元数据 | 12 | `src/utils/attribution.ts`、`src/utils/worktree.ts`、`src/utils/shell/bashProvider.ts` | — |
| `SLOW_OPERATION_LOGGING` | 启用慢操作日志，记录超过阈值的操作耗时 | 1 | `src/utils/slowOperations.ts` | — |
| `DUMP_SYSTEM_PROMPT` | 启用系统提示导出模式，将完整 system prompt 写入文件供调试 | 1 | `src/entrypoints/cli.tsx` | 第 3 章 |
| `HARD_FAIL` | 启用硬失败模式，遇到非致命错误时立即抛出异常而非静默恢复 | 2 | `src/utils/log.ts`、`src/main.tsx` | — |
| `ABLATION_BASELINE` | 启用消融实验基线模式，禁用所有优化特性以建立性能对照组 | 1 | `src/entrypoints/cli.tsx` | — |
| `ANTI_DISTILLATION_CC` | 启用反蒸馏保护——在 API 响应中注入特殊标记以阻止模型蒸馏 | 1 | `src/services/api/claude.ts` | — |
| `UNATTENDED_RETRY` | 启用无人值守重试，在 API 失败时自动重试而无需用户确认 | 1 | `src/services/api/withRetry.ts` | — |
| `TREE_SITTER_BASH` | 启用 Tree-sitter Bash 解析器，用语法树分析代替正则表达式进行 bash 解析 | 3 | `src/utils/bash/parser.ts` | 第 37–40 章 |
| `TREE_SITTER_BASH_SHADOW` | 启用 Tree-sitter Bash 影子模式——同时运行新旧解析器并对比结果用于验证 | 5 | `src/tools/BashTool/bashPermissions.ts`、`src/utils/bash/parser.ts` | 第 37–40 章 |
| `COWORKER_TYPE_TELEMETRY` | 启用协作者类型遥测，统计不同类型代理的使用分布 | 2 | `src/services/analytics/metadata.ts` | — |
| `MEMORY_SHAPE_TELEMETRY` | 启用记忆形态遥测，追踪记忆目录结构的演化情况 | 3 | `src/memdir/findRelevantMemories.ts`、`src/utils/sessionFileAccessHooks.ts` | — |

---

## E.7 平台 / 部署 / 杂项 Flag

这些 Flag 控制平台适配、部署环境检测、UI 外观以及其他不归属前述类别的杂项功能。

| Flag 名 | 功能描述 | 引用次数 | 主要模块（真实源文件路径） | 正文章节 |
|---|---|---|---|---|
| `VOICE_MODE` | 启用语音交互模式，支持语音输入和合成语音输出 | 46 | `src/tools/ConfigTool/ConfigTool.ts`、`src/tools/ConfigTool/supportedSettings.ts`、`src/keybindings/defaultBindings.ts` | — |
| `PROACTIVE` | 启用主动建议模式，Claude 在用户无输入时主动推送任务建议 | 37 | `src/main.tsx`、`src/tools/AgentTool/AgentTool.tsx`、`src/constants/prompts.ts` | 第 9–10 章 |
| `AUTO_THEME` | 启用自动主题切换，根据系统外观设置（Light/Dark）自动切换 Claude 的 UI 主题 | 2 | `src/tools/ConfigTool/supportedSettings.ts`、`src/components/design-system/ThemeProvider.tsx` | — |
| `NATIVE_CLIENT_ATTESTATION` | 启用原生客户端证明，通过平台原生机制验证客户端身份 | 1 | `src/constants/system.ts` | — |
| `SELF_HOSTED_RUNNER` | 启用自托管运行器模式，为私有化部署环境提供适配 | 1 | `src/entrypoints/cli.tsx` | — |
| `IS_LIBC_GLIBC` | 运行时环境探测 Flag——标记当前系统使用 glibc（GNU C 库），影响原生模块加载策略 | 1 | `src/utils/envDynamic.ts` | 第 3 章 |
| `IS_LIBC_MUSL` | 运行时环境探测 Flag——标记当前系统使用 musl libc（Alpine Linux 等），影响原生模块加载策略 | 1 | `src/utils/envDynamic.ts` | 第 3 章 |
| `TEMPLATES` | 启用项目模板功能，支持从预定义模板初始化项目结构 | 6 | `src/utils/markdownConfigLoader.ts`、`src/entrypoints/cli.tsx`、`src/query.ts` | — |
| `NEW_INIT` | 启用新版 `/init` 命令实现，提供改进的项目初始化流程 | 2 | `src/commands/init.ts` | — |
| `NATIVE_CLIPBOARD_IMAGE` | 启用原生剪贴板图像粘贴，支持直接从剪贴板粘贴图片到对话 | 2 | `src/utils/imagePaste.ts` | — |
| `POWERSHELL_AUTO_MODE` | 启用 PowerShell 自动模式检测，在 Windows PowerShell 环境下自动调整权限判断逻辑 | 2 | `src/utils/permissions/yoloClassifier.ts`、`src/utils/permissions/permissions.ts` | 第 37–40 章 |
| `BUILDING_CLAUDE_APPS` | 启用「构建 Claude 应用」上下文，为开发者模式提供额外的 Skill 和工具 | 1 | `src/skills/bundled/index.ts` | 第 41–43 章 |
| `ALLOW_TEST_VERSIONS` | 启用测试版本安装，允许通过自动更新渠道安装预发布版本 | 2 | `src/utils/nativeInstaller/download.ts` | — |
| `BREAK_CACHE_COMMAND` | 启用 `/break-cache` 命令，手动破坏当前 prompt cache 以强制重建 | 2 | `src/context.ts` | 第 22 章 |
| `BYOC_ENVIRONMENT_RUNNER` | 启用 BYOC（Bring Your Own Compute）环境运行器，支持用户自定义计算后端 | 1 | `src/entrypoints/cli.tsx` | — |

---

## 版本说明

本附录基于 **Claude Code v2.1.88** 的重建源码统计，共发现 **89 个**唯一 Feature Flag。

- **引用次数最高**：`KAIROS`（154 次）、`TRANSCRIPT_CLASSIFIER`（107 次）、`TEAMMEM`（51 次）
- **引用次数最低**：多个 Flag 仅出现 1 次（如 `KAIROS_DREAM`、`ULTRATHINK`、`TORCH` 等）
- **重建版未找到**：`COMPUTER_USE` 在 `feature()` 调用中引用次数为 0，该功能通过 `CHICAGO_MCP` 及 MCP 服务器注册机制实现
- 由于重建过程中部分代码路径已被 DCE 消除，实际 v2.1.88 二进制中的 Flag 总数可能略有差异
