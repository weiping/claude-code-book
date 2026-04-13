# 附录 E：Feature Flag 完整清单

本附录列出 Claude Code v2.1.88 中所有已知的编译期 Feature Flag。这些 Flag 通过 `bun:bundle` 的 `feature()` 调用在**编译期固化**，打包后即成为死代码消除（DCE）的判断依据，**运行时无法动态切换**。如需启用某 Flag，须重新编译。

---

## 核心功能 Flag

| Flag 名 | 功能描述 | 相关工具/模块 | 正文章节 |
|---------|---------|-------------|---------|
| `HISTORY_SNIP` | 历史记录压缩优化，裁剪过长对话历史以节省 Token | QueryEngine | 第 9 章 |
| `BASH_CLASSIFIER` | Bash 命令分类器，为自动权限模式提供命令风险评估 | BashTool / PermissionClassifier | 第 33 章 |
| `TRANSCRIPT_CLASSIFIER` | 转录分类器，对会话历史内容进行分类处理 | TranscriptManager | 第 8 章 |
| `REACTIVE_COMPACT` | 响应式压缩，上下文超出窗口时自动触发压缩流程 | CompactionEngine | 第 19 章 |
| `CONTEXT_COLLAPSE` | 上下文折叠功能，将多轮历史折叠为摘要节点 | QueryEngine | 第 9 章 |
| `FORK_SUBAGENT` | 子 Agent fork 模式，支持从当前会话 fork 出独立子 Agent | AgentFork | 第 26 章 |
| `HISTORY_PICKER` | 历史对话选择器，允许用户浏览并恢复历史会话 | HistoryUI | 第 17 章 |
| `TOKEN_BUDGET` | Token 预算管理，为 Agent 执行设置最大 Token 用量上限 | BudgetManager | 第 19 章 |

---

## Agent / 多智能体 Flag

| Flag 名 | 功能描述 | 相关工具/模块 | 正文章节 |
|---------|---------|-------------|---------|
| `KAIROS` | Kairos 模式整体开关，启用异步 Agent 功能集合 | assistant/index.js | 第 20 章 |
| `KAIROS_CHANNELS` | Kairos 通道功能，支持多通道异步消息传递 | KairosChannel | 第 20 章 |
| `KAIROS_DREAM` | DreamTask 功能，扩展后台任务系统 | DreamTaskManager | 第 25 章 |
| `KAIROS_BRIEF` | Brief 功能，生成 Agent 执行摘要报告 | BriefGenerator | 第 41 章 |
| `KAIROS_GITHUB_WEBHOOKS` | GitHub Webhook 集成，支持事件驱动触发 Agent | GitHubWebhookServer | 第 41 章 |
| `KAIROS_PUSH_NOTIFICATION` | 推送通知功能，Agent 完成时发送通知 | PushNotificationService | 第 41 章 |
| `TERMINAL_PANEL` | 终端面板功能，影响 Swarm 后端的终端显示 | SwarmBackend | 第 31 章 |
| `BRIDGE_MODE` | Bridge 模式，支持远程连接和会话桥接 | BridgeServer | 第 32 章 |
| `BG_SESSIONS` | 后台会话功能，允许 Agent 在后台持续运行 | BackgroundSessionManager | 第 28 章 |
| `AGENT_TRIGGERS` | Agent 触发器功能，支持条件驱动的 Agent 启动 | TriggerEngine | 第 20 章 |
| `AGENT_TRIGGERS_REMOTE` | 远程 Agent 触发器，启用 RemoteTriggerTool | RemoteTriggerTool | 第 28 章 |
| `TEAMMEM` | 队友记忆功能，Swarm 中各 Teammate 共享记忆池 | TeamMemoryStore | 第 29 章 |
| `COORDINATOR_MODE` | 协调者模式，启用 Coordinator Agent 角色 | CoordinatorAgent | 第 29 章 |
| `BUDDY` | Buddy 功能，启用辅助 Agent 伴随主 Agent 运行 | BuddyAgent | 第 30 章 |
| `MONITOR_TOOL` | 启用 MonitorTool，提供任务监控和状态查询工具 | MonitorTool | 第 28 章 |
| `DAEMON` | Daemon 模式，启用后台守护进程管理 Agent 生命周期 | DaemonManager | 第 28 章 |

---

## 工具 / 插件 Flag

| Flag 名 | 功能描述 | 相关工具/模块 | 正文章节 |
|---------|---------|-------------|---------|
| `WEB_BROWSER_TOOL` | 启用 WebBrowserTool，基于无头浏览器的网页抓取工具 | WebBrowserTool | 第 10 章 |
| `REVIEW_ARTIFACT` | 启用 ReviewArtifactTool，代码产物审查工具 | ReviewArtifactTool | 第 10 章 |
| `OVERFLOW_TEST_TOOL` | 启用 OverflowTestTool，用于测试上下文溢出边界 | OverflowTestTool | 开发专用 |
| `MCP_SKILLS` | MCP Skills 功能，支持插件技能系统 | MCPSkillManager | 第 39 章 |
| `MCP_RICH_OUTPUT` | MCP 丰富输出格式，支持结构化媒体响应 | MCPClient | 第 13 章 |
| `EXPERIMENTAL_SKILL_SEARCH` | 实验性技能搜索，模糊匹配 Skill 调用 | SkillSearch | 第 14 章 |
| `BUILTIN_EXPLORE_PLAN_AGENTS` | 内置 Explore / Plan Agent，无需外部插件即可使用 | ExploreAgent / PlanAgent | 第 14 章 |
| `EXTRACT_MEMORIES` | 自动提取记忆，从对话中提炼知识写入 Memory 文件 | MemoryExtractor | 第 16 章 |
| `ULTRAPLAN` | UltraPlan 高级计划模式，生成多层次执行计划 | UltraPlanEngine | 第 34 章 |
| `ULTRATHINK` | UltraThink 深度推理，延长思考预算以提升推理质量 | UltraThinkEngine | 第 34 章 |
| `TORCH` | Torch 功能，推断为特殊执行模式（内部实验功能） | TorchRunner | 内部功能 |

---

## 系统 / 部署 Flag

| Flag 名 | 功能描述 | 相关工具/模块 | 正文章节 |
|---------|---------|-------------|---------|
| `AUTO_THEME` | 终端主题自动检测，根据终端背景色切换配色方案 | ThemeDetector | 第 2 章 |
| `SSH_REMOTE` | SSH 远程模式，通过 SSH 连接远程主机运行（stub） | ssh/ | 第 41 章 |
| `VOICE_MODE` | 语音模式，支持语音输入/输出（stub） | voice/ | 第 41 章 |
| `PROACTIVE` | 主动模式，允许 Agent 主动发起交互（stub） | proactive/ | 第 41 章 |
| `NATIVE_CLIENT_ATTESTATION` | 原生客户端认证，验证客户端身份的安全机制 | AttestationService | 安全功能 |
| `SELF_HOSTED_RUNNER` | 自托管运行环境，支持私有部署场景 | RunnerBootstrap | 部署功能 |

---

> **版本说明**：以上 Flag 清单基于 Claude Code **v2.1.88** 逆向重建版本，通过分析 `src/tools.ts` 及各源文件的 `feature()` 调用整理。标注 `stub` 的模块仅有骨架实现，标注"内部功能"的 Flag 用途尚不完全明确。
