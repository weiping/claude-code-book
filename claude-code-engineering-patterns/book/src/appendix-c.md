# 附录 C：关键类型索引

本附录按功能域整理 Claude Code 源码中的核心 TypeScript 类型，便于在阅读各章节时快速定位定义。

---

## C.1 工具系统（Tool System）

| 类型名 | 定义文件 | 主要字段/值 | 首次出现 |
|--------|----------|------------|---------|
| `Tool` | `src/Tool.ts` | `name`, `description`, `inputSchema`, `execute`, `checkPermissions`, `isEnabled`, `isAllowed` | 第 14 章 |
| `BuiltTool<D>` | `src/Tool.ts:783` | `buildTool<D>(def: D): BuiltTool<D>`——将 `ToolDef` 中可省略的默认方法填充后的完整工具类型 | 第 14 章 |
| `ToolUseContext` | `src/Tool.ts:158` | `getAppState`, `setAppState`, `setAppStateForTasks`, `agentId`, `readFileTimestamps` 等运行时上下文 | 第 14 章 |
| `ToolPermissionContext` | `src/Tool.ts:123` | `mode: PermissionMode`, `prePlanMode?: PermissionMode`——传给 `checkPermissions` 的权限上下文（`DeepImmutable` 包裹） | 第 15 章 |

---

## C.2 消息体系（Message System）

> **注意**：以下类型定义于 `src/types/message.ts`，该文件在源码重建版本中缺失（原编译时内联），字段结构从 `src/utils/messages.ts` 工厂函数与使用处反向推断。

| 类型名 | 定义文件 | 主要字段/值 | 首次出现 |
|--------|----------|------------|----------|
| `Message` | `src/types/message.ts`（缺失） | 判别联合：`AssistantMessage \| UserMessage \| SystemMessage \| AttachmentMessage \| ProgressMessage \| TombstoneMessage \| ...`——会话历史数组元素类型（`messages: Message[]`） | 第 4 章 |
| `AssistantMessage` | `src/types/message.ts`（缺失） | `type: 'assistant'`, `uuid: UUID`, `timestamp: string`, `message: BetaMessage`（含 `role`, `content: BetaContentBlock[]`, `usage`, `model`）, `requestId?`, `apiError?`, `isApiErrorMessage?`, `isVirtual?` | 第 9 章 |
| `UserMessage` | `src/types/message.ts`（缺失） | `type: 'user'`, `uuid: UUID`, `timestamp: string`, `message: { role: 'user', content: string \| ContentBlockParam[] }`, `isMeta?`, `isVirtual?`, `isCompactSummary?`, `toolUseResult?`, `sourceToolAssistantUUID?`, `permissionMode?`, `origin?: MessageOrigin` | 第 4 章 |
| `ContentBlock` | `@anthropic-ai/sdk/resources/index.mjs` | SDK 判别联合：`TextBlock \| ToolUseBlock \| ToolResultBlock \| ImageBlock \| ThinkingBlock \| RedactedThinkingBlock \| ...`——助手消息内容块基础类型 | 第 9 章 |
| `ContentBlockParam` | `@anthropic-ai/sdk/resources/index.mjs` | SDK 判别联合：`TextBlockParam \| ImageBlockParam \| ToolUseBlockParam \| ToolResultBlockParam \| ThinkingBlockParam \| ...`——用户消息内容参数类型 | 第 6 章 |
| `NormalizedAssistantMessage` | `src/types/message.ts`（缺失） | `AssistantMessage` 的规范化形式，用于 `normalizeMessages()` 后将多条相邻消息合并展平，传入 API 前消除重复 | 第 9 章 |
| `NormalizedUserMessage` | `src/types/message.ts`（缺失） | `UserMessage` 的规范化形式，工具调用结果合并后的标准 user-role 消息；与 `NormalizedAssistantMessage` 构成 SDK 侧的完整对话序列 | 第 9 章 |
| `MessageOrigin` | `src/types/message.ts`（缺失） | 消息来源枚举（如 `'human'`、`'bridge'`、`'proactive'` 等），标记 `UserMessage` 的触发来源；影响统计与路由 | 第 4 章 |

---

## C.3 任务系统（Task System）

| 类型名 | 定义文件 | 主要字段/值 | 首次出现 |
|--------|----------|------------|---------|
| `TaskState` | `src/tasks/types.ts:12` | 判别联合：`LocalShellTaskState \| LocalAgentTaskState \| RemoteAgentTaskState \| InProcessTeammateTaskState \| LocalWorkflowTaskState \| MonitorMcpTaskState \| DreamTaskState` | 第 29 章 |
| `LocalShellTaskState` | `src/tasks/LocalShellTask/guards.ts` | `type: 'local-shell'`, `status`, `pid`, `output` 等 Shell 子进程状态 | 第 29 章 |
| `LocalAgentTaskState` | `src/tasks/LocalAgentTask/LocalAgentTask.tsx` | `type: 'local-agent'`, `status`, `agentId`, `messages` 等本地代理任务状态 | 第 30 章 |
| `RemoteAgentTaskState` | `src/tasks/RemoteAgentTask/RemoteAgentTask.tsx` | `type: 'remote-agent'`, `status`, `sessionId`, `transport` 等远程代理任务状态 | 第 31 章 |
| `InProcessTeammateTaskState` | `src/tasks/InProcessTeammateTask/types.ts` | `type: 'in-process-teammate'`, `status`, `permissionMode: PermissionMode`, `agentId` 等进程内队友状态 | 第 32 章 |

---

## C.4 钩子引擎（Hooks Engine）

| 类型名 | 定义文件 | 主要字段/值 | 首次出现 |
|--------|----------|------------|---------|
| `HookEvent` | `src/entrypoints/sdk/coreTypes.ts:25` | 字符串字面量联合：`'PreToolUse' \| 'PostToolUse' \| 'Notification' \| 'SessionStart' \| 'SessionEnd' \| 'Stop' \| ...`（共 27 个事件） | 第 24 章 |
| `HookMatcher` | `src/schemas/hooks.ts:221` | `event`, `tools?: string[]`, `hooks: HookCommand[]`——将事件/工具过滤条件与待执行钩子命令绑定 | 第 24 章 |
| `PendingAsyncHook` | `src/utils/hooks/AsyncHookRegistry.ts:12` | `id: string`, `hookEvent`, `toolUseID`, `promise`, `abortController` 等异步钩子挂起状态 | 第 26 章 |
| `AsyncHookRegistry` | `src/utils/hooks/AsyncHookRegistry.ts` | 模块级 `Map<string, PendingAsyncHook>`——注册/查询/完成挂起异步钩子的函数集合 | 第 26 章 |

---

## C.5 权限系统（Permission System）

| 类型名 | 定义文件 | 主要字段/值 | 首次出现 |
|--------|----------|------------|---------|
| `PermissionMode` | `src/types/permissions.ts:29` | `'default' \| 'acceptEdits' \| 'autoEdit' \| 'bypassPermissions' \| 'plan' \| 'auto' \| 'bubble'` 等内部模式枚举 | 第 15 章 |
| `PermissionResult` | `src/types/permissions.ts:251` | `behavior: 'allow' \| 'deny' \| 'ask'`, `rule?: PermissionRule`, `mode?: PermissionMode`, `reasons?: Map<string, PermissionResult>`——`checkPermissions` 返回值 | 第 37 章 |
| `PermissionRule` | `src/types/permissions.ts:75` | `source: PermissionRuleSource`, `behavior: PermissionBehavior`, `ruleValue: PermissionRuleValue`——持久化权限规则 | 第 38 章 |

---

## C.6 MCP 与插件（MCP / Plugin）

| 类型名 | 定义文件 | 主要字段/值 | 首次出现 |
|--------|----------|------------|---------|
| `McpServerConfig` | `src/services/mcp/types.ts:161` | `type`, `command?`, `url?`, `env?`, `args?`——MCP 服务器连接配置（`z.infer` 自 `McpServerConfigSchema`） | 第 11 章 |
| `PluginManifest` | `src/utils/plugins/schemas.ts:884` | `metadata`, `hooks`, `commands`, `agents`, `skills`, `mcpServers`, `settings` 等插件声明（`z.infer` 自 `PluginManifestSchema`） | 第 43 章 |
| `MarketplaceSource` | `src/utils/plugins/schemas.ts:1648` | 判别联合：`{ source: 'npm', package: string } \| { source: 'file', path: string } \| { source: 'directory', path: string } \| ...`（`z.infer` 自 `MarketplaceSourceSchema`） | 第 42 章 |

---

## C.7 上下文与状态（Context / State）

| 类型名 | 定义文件 | 主要字段/值 | 首次出现 |
|--------|----------|------------|---------|
| `AppState` | `src/state/AppStateStore.ts:89` | `mcp`, `tasks`, `hooks`, `permissionMode`, `messages`, `sessionId` 等——全局会话状态（`DeepImmutable` 包裹） | 第 02 章 |
| `State`（查询循环） | `src/query.ts:204` | `messages`, `toolResults`, `aborted`, `usage`——`query()` 函数内部单次迭代状态机载体 | 第 09 章 |
| `CacheSafeParams` | `src/utils/forkedAgent.ts:57` | `model`, `maxTokens`, `systemPrompt`, `tools`, `thinkingConfig`——可安全传入提示缓存的参数集合 | 第 13 章 |
| `StreamingToolExecutor` | `src/services/tools/StreamingToolExecutor.ts:40` | `execute(toolUse, context)`, `abort()`——将流式 `tool_use` 块与并发工具执行协调的执行器类 | 第 10 章 |

---

## 版本说明

本索引基于 Claude Code **v2.1.88** 源码重建版本（约 60–70% 完整度）。部分类型定义位于重建过程中新增的拆分文件（如 `src/types/permissions.ts`、`src/types/hooks.ts`），与原始编译产物中的内联位置可能存在差异。章节编号对应本书目录结构。
