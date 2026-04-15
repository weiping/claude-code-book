# 附录 A：Hook 事件速查表

本附录列出 Claude Code 支持的全部 27 个 Hook 事件，供快速查阅。每个事件包含触发时机、输入格式、退出码语义和典型用途。完整的钩子系统设计分析见第 24-26 章。

**源码来源**：`src/utils/hooks/hooksConfigManager.ts`（事件定义与描述）

---

## 工具调用类（5 个）

| 事件名 | 触发时机 | 输入 JSON 字段 | 退出码语义 | 典型用途 |
|--------|---------|--------------|----------|---------|
| `PreToolUse` | 工具执行前 | 工具调用参数 | 0=不显示；2=拦截并报错给模型；其他=仅报错给用户 | 记录工具调用、拦截危险操作 |
| `PostToolUse` | 工具执行后 | `inputs`（参数）+ `response`（结果）| 0=输出到转录模式；2=立即报错给模型；其他=仅报错给用户 | 结果后处理、审计日志 |
| `PostToolUseFailure` | 工具执行失败后 | `tool_name`, `tool_input`, `tool_use_id`, `error`, `error_type`, `is_interrupt`, `is_timeout` | 0=输出到转录；2=立即报错给模型；其他=仅报错给用户 | 失败监控、重试逻辑 |
| `PermissionDenied` | Auto 模式分类器拒绝工具调用后 | `tool_name`, `tool_input`, `tool_use_id`, `reason` | 0=输出到转录；其他=仅报错给用户 | 可返回 `{"hookSpecificOutput":{"retry":true}}` 让模型重试 |
| `PermissionRequest` | 显示权限确认对话框时 | `tool_name`, `tool_input`, `tool_use_id` | 0=使用钩子决策（如有）；其他=仅报错给用户 | 自定义权限逻辑，输出 JSON 决策 |

**matcher 字段**：以上 5 个事件均支持按 `tool_name` 过滤，只对特定工具触发。

---

## 会话生命周期类（5 个）

| 事件名 | 触发时机 | 输入 JSON 字段 | 退出码语义 | 典型用途 |
|--------|---------|--------------|----------|---------|
| `SessionStart` | 新会话开始时 | `source`（`startup` / `resume` / `clear` / `compact`）| 0=stdout 传给 Claude；阻断错误被忽略；其他=仅报错给用户 | 注入初始上下文、配置检查 |
| `SessionEnd` | 会话即将结束时 | `reason`（`clear` / `logout` / `prompt_input_exit` / `other`）| 0=正常完成；其他=报错给用户 | 会话摘要、清理工作 |
| `Stop` | Claude 即将结束响应前 | —（无特定字段）| 0=不显示；2=报错给模型并继续对话；其他=仅报错给用户 | 响应后处理 |
| `StopFailure` | 因 API 错误结束时 | `error`（`rate_limit` / `authentication_failed` / `billing_error` / `server_error` 等）| Fire-and-forget：钩子输出和退出码均被忽略 | 错误监控（不可阻断）|
| `Setup` | 仓库初始化和维护时 | `trigger`（`init` 或 `maintenance`）| 0=stdout 传给 Claude；阻断错误被忽略；其他=仅报错给用户 | 项目初始化脚本、依赖检查 |

---

## 用户交互类（2 个）

| 事件名 | 触发时机 | 输入 JSON 字段 | 退出码语义 | 典型用途 |
|--------|---------|--------------|----------|---------|
| `UserPromptSubmit` | 用户提交 prompt 时 | 原始 prompt 文本 | 0=stdout 传给 Claude；2=拦截并清除 prompt；其他=仅报错给用户 | prompt 预处理、敏感词过滤 |
| `Notification` | 系统发送通知时 | `message`, `notification_type`（`permission_prompt` / `idle_prompt` / `auth_success` / `elicitation_dialog` 等）| 0=不显示；其他=仅报错给用户 | 自定义通知转发（如发到 Slack）|

---

## 压缩类（2 个）

| 事件名 | 触发时机 | 输入 JSON 字段 | 退出码语义 | 典型用途 |
|--------|---------|--------------|----------|---------|
| `PreCompact` | 对话压缩前 | 压缩详情（含 `trigger`：`manual` 或 `auto`）| 0=stdout 追加为自定义压缩指令；2=阻止压缩；其他=继续压缩但仅报错给用户 | 自定义压缩摘要策略 |
| `PostCompact` | 对话压缩后 | 压缩详情 + 摘要内容 | 0=stdout 展示给用户；其他=仅报错给用户 | 压缩后通知 |

---

## 多智能体协作类（5 个）

| 事件名 | 触发时机 | 输入 JSON 字段 | 退出码语义 | 典型用途 |
|--------|---------|--------------|----------|---------|
| `SubagentStart` | Agent 工具调用启动子 Agent 时 | `agent_id`, `agent_type` | 0=stdout 传给子 Agent；阻断错误被忽略；其他=仅报错给用户 | 子 Agent 上下文注入 |
| `SubagentStop` | 子 Agent 完成后 | `agent_id`, `agent_type`, `agent_transcript_path` | 0=不显示；2=报错给子 Agent 并继续运行；其他=仅报错给用户 | 子 Agent 结果审计 |
| `TeammateIdle` | 队友即将空闲时 | `teammate_name`, `team_name` | 0=不显示；2=报错给队友阻止空闲（队友继续工作）；其他=仅报错给用户 | 防止队友提前退出 |
| `TaskCreated` | 任务被创建时 | `task_id`, `task_subject`, `task_description`, `teammate_name`, `team_name` | 0=不显示；2=报错给模型并阻止创建；其他=仅报错给用户 | 任务审批流程 |
| `TaskCompleted` | 任务被标记完成时 | `task_id`, `task_subject`, `task_description`, `teammate_name`, `team_name` | 0=不显示；2=报错给模型并阻止完成；其他=仅报错给用户 | 完成条件验证 |

---

## MCP 交互类（2 个）

| 事件名 | 触发时机 | 输入 JSON 字段 | 退出码语义 | 典型用途 |
|--------|---------|--------------|----------|---------|
| `Elicitation` | MCP 服务器请求用户输入时 | `mcp_server_name`, `message`, `requested_schema` | 0=使用钩子响应（`accept`/`decline`/`cancel` + `content`）；2=拒绝请求；其他=仅报错给用户 | 自动回填 MCP 输入 |
| `ElicitationResult` | 用户响应 MCP 输入后 | `mcp_server_name`, `action`, `content`, `mode`, `elicitation_id` | 0=使用钩子响应覆盖；2=响应变为 decline；其他=仅报错给用户 | 响应后处理 |

---

## 配置与文件系统类（6 个）

| 事件名 | 触发时机 | 输入 JSON 字段 | 退出码语义 | 典型用途 |
|--------|---------|--------------|----------|---------|
| `ConfigChange` | 会话期间配置文件变更时 | `source`（`user_settings` / `project_settings` / `local_settings` / `policy_settings` / `skills`）, `file_path` | 0=允许变更；2=阻止变更应用到会话；其他=仅报错给用户 | 配置变更审计 |
| `InstructionsLoaded` | 加载 CLAUDE.md 或规则文件时 | `file_path`, `memory_type`, `load_reason`（`session_start` / `nested_traversal` / `path_glob_match` / `include` / `compact`）, `globs`, `trigger_file_path`, `parent_file_path` | 0=正常；其他=仅报错给用户 | **仅观测，不可阻断** |
| `WorktreeCreate` | 创建隔离 Worktree 时 | `name`（建议的 worktree slug）| 0=成功，stdout 必须包含绝对路径；其他=创建失败 | 自定义 worktree 初始化 |
| `WorktreeRemove` | 删除 Worktree 时 | `worktree_path`（绝对路径）| 0=成功；其他=仅报错给用户 | 自定义清理逻辑 |
| `CwdChanged` | 工作目录切换后 | `old_cwd`, `new_cwd` | 0=正常；其他=仅报错给用户 | 目录切换时更新环境变量（写入 `CLAUDE_ENV_FILE`）；可返回 `hookSpecificOutput.watchPaths` 注册文件监控 |
| `FileChanged` | 被监听的文件变更时 | `file_path`, `event`（`change` / `add` / `unlink`）| 0=正常；其他=仅报错给用户 | 自动触发重新分析；可返回 `hookSpecificOutput.watchPaths` 动态更新监控列表 |

---

## 退出码速查

| 退出码 | 通用语义 | 注意 |
|--------|---------|------|
| `0` | 成功，根据事件类型决定 stdout 去向 | 部分事件 0 表示不显示，部分表示传给模型 |
| `2` | 阻断操作，stderr 报告给模型或用户 | 只有部分事件支持 exit 2 的阻断语义 |
| 其他 | 报错，但通常不阻断 | stderr 仅展示给用户，操作继续 |

**Fire-and-forget 事件**：`StopFailure` 和 `InstructionsLoaded` 忽略退出码和钩子输出。

---

*基于 `src/utils/hooks/hooksConfigManager.ts` v2.1.88 提取，共 27 个事件（5 + 5 + 2 + 2 + 5 + 2 + 6）。*
