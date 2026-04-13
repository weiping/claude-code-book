# 附录 C：关键类型索引

本附录汇总全书引用的核心 TypeScript 类型，供快速定位类型定义、字段结构及首次出现位置。可独立查阅，无需按顺序阅读正文。

---

## Tool 体系

| 类型名 | 定义文件 | 主要字段/值 | 首次出现 |
|--------|----------|------------|---------|
| `Tool` | `src/Tool.ts` | `name`, `description`, `execute`, `isAllowed`, `isEnabled`, `isMcp` | 第10章 |
| `BuiltTool<D>` | `src/Tool.ts:783` | `buildTool()` 工厂函数的泛型返回类型，`D` 为输入 schema | 第10章 |
| `ToolPermissionContext` | `src/Tool.ts` | 工具权限检查上下文，传入 `isAllowed` 回调 | 第11章 |
| `ToolUseContext` | `src/Tool.ts` | 工具调用执行上下文，传入 `execute` 回调 | 第8章 |

---

## Task 体系

| 类型名 | 定义文件 | 主要字段/值 | 首次出现 |
|--------|----------|------------|---------|
| `TaskState` | `src/tasks/types.ts:12` | 判别联合：`LocalShell \| LocalAgent \| Remote \| InProcess \| LocalWorkflow \| MonitorMcp \| Dream` | 第25章 |
| `LocalShellTaskState` | `src/tasks/LocalShellTask/` | Shell 子进程任务的运行状态 | 第25章 |
| `LocalAgentTaskState` | `src/tasks/LocalAgentTask/` | 本地 Agent 子任务的运行状态 | 第26章 |
| `RemoteAgentTaskState` | `src/tasks/RemoteAgentTask/` | 远程 Agent 任务状态（跨主机调度）| 第28章 |
| `InProcessTeammateTaskState` | `src/tasks/InProcessTeammateTask/` | 进程内队友 Agent 的任务状态 | 第30章 |

---

## Hook 体系

| 类型名 | 定义文件 | 主要字段/值 | 首次出现 |
|--------|----------|------------|---------|
| `HookEvent` | `src/entrypoints/agentSdkTypes.ts` | 27个事件类型的判别联合，包含 `PreToolUse`、`PostToolUse`、`Notification` 等；完整列表见附录 A | 第20章 |
| `HookMatcher` | `src/utils/hooks/` | 钩子匹配规则，决定 Hook 监听哪些事件 | 第21章 |
| `PendingAsyncHook` | `src/utils/hooks/AsyncHookRegistry.ts:28` | 异步钩子追踪记录，含 `hookId`、`promise`、超时信息 | 第22章 |

---

## Permission 体系

| 类型名 | 定义文件 | 主要字段/值 | 首次出现 |
|--------|----------|------------|---------|
| `PermissionMode` | `src/utils/permissions/PermissionMode.ts` | 权限模式枚举：`default`、`autoApprove`、`plan` 等 | 第11章 |
| `PermissionResult` | `src/utils/permissions/PermissionResult.ts` | 三态判别联合：`allow \| deny \| ask` | 第33章 |
| `PermissionRule` | `src/utils/permissions/PermissionRule.ts` | 权限规则定义：工具名称模式 + 结果策略 | 第33章 |

---

## MCP 体系

| 类型名 | 定义文件 | 主要字段/值 | 首次出现 |
|--------|----------|------------|---------|
| `McpServerConfig` | `src/services/mcp/types.ts` | MCP 服务器配置：`type`、`command`/`url`、`env`、`args` | 第13章 |
| `MarketplaceSource` | `src/utils/plugins/schemas.ts:906` | 插件来源协议判别联合：`npm \| github \| url \| local` | 第38章 |
| `PluginManifest` | `src/utils/plugins/schemas.ts:884` | 插件清单完整定义：`id`、`version`、`mcp`、`permissions`、`sandbox` | 第39章 |

---

## Context / Message 体系

| 类型名 | 定义文件 | 主要字段/值 | 首次出现 |
|--------|----------|------------|---------|
| `AssistantMessage` | `src/types/message.ts` | 助手消息类型：`role: 'assistant'`、`content: ContentBlock[]` | 第4章 |

---

> **版本说明：** 本索引基于 Claude Code v2.1.88 的重构源码，类型定义来自 `src/` 目录。部分文件为存根实现，字段摘要以可确认的公开接口为准。
