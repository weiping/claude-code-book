# 附录 B：工具权限矩阵

本附录列出 Claude Code 的内置工具及其权限分类，供快速查阅工具的风险等级和权限要求。工具权限系统的详细设计见第 10-11 章（工具契约）和第 33 章（权限防线）。

**权限级别说明**：
- **只读**：不修改任何文件或系统状态，通常自动允许
- **写入**：修改文件内容，需通过权限规则检查
- **执行**：运行系统命令或代码，高风险，通常需用户确认
- **AI协作**：启动子 Agent 或多智能体操作
- **网络**：发起外部网络请求
- **配置**：修改会话设置或模式

**源码来源**：`src/tools/` 各工具目录；`src/utils/permissions/permissions.ts`

---

## 文件操作类

| 工具名 | 操作类型 | 权限级别 | 典型操作 | 源码位置 |
|--------|---------|---------|---------|---------|
| `FileReadTool` | 读取文件 | 🟢 只读 | 读取任意文件内容 | `src/tools/FileReadTool/` |
| `FileEditTool` | 编辑文件 | 🟡 写入 | 精确替换文件内容（需确认路径存在）| `src/tools/FileEditTool/` |
| `FileWriteTool` | 写入文件 | 🟡 写入 | 创建或覆盖文件 | `src/tools/FileWriteTool/` |
| `NotebookEditTool` | 编辑 Notebook | 🟡 写入 | 编辑 Jupyter Notebook 单元格 | `src/tools/NotebookEditTool/` |
| `TodoWriteTool` | 写入待办 | 🟡 写入 | 创建/更新会话 Todo 列表 | `src/tools/TodoWriteTool/` |

---

## 搜索与浏览类

| 工具名 | 操作类型 | 权限级别 | 典型操作 | 源码位置 |
|--------|---------|---------|---------|---------|
| `GlobTool` | 文件名匹配 | 🟢 只读 | 按 glob 模式列出文件路径 | `src/tools/GlobTool/` |
| `GrepTool` | 内容搜索 | 🟢 只读 | 正则搜索文件内容 | `src/tools/GrepTool/` |
| `SnipTool` | 代码片段 | 🟢 只读 | 提取文件的特定行范围 | `src/tools/SnipTool/` |
| `CtxInspectTool` | 上下文检查 | 🟢 只读 | 检查当前上下文使用情况 | `src/tools/CtxInspectTool/` |
| `ToolSearchTool` | 工具搜索 | 🟢 只读 | 在可用工具中搜索 | `src/tools/ToolSearchTool/` |
| `LSPTool` | 语言服务 | 🟢 只读 | LSP 代码分析（悬停/引用/定义）| `src/tools/LSPTool/` |

---

## 代码执行类（高风险）

| 工具名 | 操作类型 | 权限级别 | 典型操作 | 注意事项 |
|--------|---------|---------|---------|---------|
| `BashTool` | Shell 执行 | 🔴 执行 | 运行任意 Bash 命令 | 支持沙箱；有 dangerouslyDisableSandbox 参数；权限规则可拦截 |
| `PowerShellTool` | PowerShell 执行 | 🔴 执行 | 运行 PowerShell 命令（Windows）| 与 BashTool 权限机制类似 |
| `REPLTool` | 代码解释器 | 🔴 执行 | 在沙箱 REPL 中执行代码 | 有 `isAllowed()` 守卫；需运行时检查 |

---

## 网络类

| 工具名 | 操作类型 | 权限级别 | 典型操作 | 源码位置 |
|--------|---------|---------|---------|---------|
| `WebFetchTool` | HTTP 获取 | 🟠 网络 | 发起 HTTP 请求获取页面 | `src/tools/WebFetchTool/` |
| `WebSearchTool` | 搜索 | 🟠 网络 | 调用搜索引擎 API | `src/tools/WebSearchTool/` |
| `WebBrowserTool` | 浏览器 | 🟠 网络+执行 | 控制无头浏览器 | `src/tools/WebBrowserTool/` |

---

## MCP 工具类

| 工具名 | 操作类型 | 权限级别 | 典型操作 | 备注 |
|--------|---------|---------|---------|------|
| `MCPTool` | MCP 工具调用 | 🟠 可变 | 调用 MCP 服务器提供的工具 | `isMcp: true`；权限由 MCP 服务器决定 |
| `ListMcpResourcesTool` | 列出 MCP 资源 | 🟢 只读 | 列出 MCP 服务器的可用资源 | `src/tools/ListMcpResourcesTool/` |
| `ReadMcpResourceTool` | 读取 MCP 资源 | 🟢 只读 | 读取 MCP 资源内容 | `src/tools/ReadMcpResourceTool/` |
| `McpAuthTool` | MCP 认证 | 🟠 网络 | 处理 MCP OAuth 认证流程 | `isMcp: true` |

---

## AI 协作类

| 工具名 | 操作类型 | 权限级别 | 典型操作 | 备注 |
|--------|---------|---------|---------|------|
| `AgentTool` | 子 Agent | 🔴 AI协作 | 启动子 Agent 执行复杂任务 | 通过 `getDenyRuleForAgent` 做权限检查 |
| `SkillTool` | 技能调用 | 🟡 可变 | 加载并执行插件 Skill | 详见第 14 章 |
| `SendMessageTool` | 发送消息 | 🟡 AI协作 | 向队友 Agent 发送消息 | Swarm 功能 |
| `ListPeersTool` | 列出队友 | 🟢 只读 | 列出当前活跃的队友 Agent | Swarm 功能 |
| `MonitorTool` | 监控 | 🟢 只读 | 监控 Agent 任务状态 | Feature Flag 控制 |

---

## 任务管理类

| 工具名 | 操作类型 | 权限级别 | 典型操作 | 源码位置 |
|--------|---------|---------|---------|---------|
| `TaskCreateTool` | 创建任务 | 🟡 AI协作 | 创建新的后台任务 | `src/tools/TaskCreateTool/` |
| `TaskGetTool` | 获取任务 | 🟢 只读 | 获取任务状态和结果 | `src/tools/TaskGetTool/` |
| `TaskListTool` | 列出任务 | 🟢 只读 | 列出所有任务 | `src/tools/TaskListTool/` |
| `TaskUpdateTool` | 更新任务 | 🟡 AI协作 | 更新任务状态 | `src/tools/TaskUpdateTool/` |
| `TaskStopTool` | 停止任务 | 🔴 AI协作 | 强制终止任务 | `src/tools/TaskStopTool/` |
| `TaskOutputTool` | 任务输出 | 🟢 只读 | 获取任务的输出流 | `src/tools/TaskOutputTool/` |
| `WorkflowTool` | 工作流 | 🟡 AI协作 | 执行预定义工作流 | Feature Flag 控制 |

---

## 团队管理类

| 工具名 | 操作类型 | 权限级别 | 典型操作 | 备注 |
|--------|---------|---------|---------|------|
| `TeamCreateTool` | 创建团队 | 🟡 AI协作 | 创建多 Agent 团队 | Swarm 功能 |
| `TeamDeleteTool` | 删除团队 | 🔴 AI协作 | 解散 Agent 团队 | Swarm 功能 |

---

## 会话与配置类

| 工具名 | 操作类型 | 权限级别 | 典型操作 | 源码位置 |
|--------|---------|---------|---------|---------|
| `ConfigTool` | 会话配置 | 🟡 配置 | 读取或修改会话配置 | `src/tools/ConfigTool/` |
| `EnterPlanModeTool` | 进入计划模式 | 🟡 配置 | 切换到需要人工审批的计划模式 | `src/tools/EnterPlanModeTool/` |
| `ExitPlanModeTool` | 退出计划模式 | 🟡 配置 | 退出计划模式 | `src/tools/ExitPlanModeTool/` |
| `EnterWorktreeTool` | 进入 Worktree | 🟡 配置 | 切换到隔离的 Git Worktree | `src/tools/EnterWorktreeTool/` |
| `ExitWorktreeTool` | 退出 Worktree | 🟡 配置 | 退出当前 Worktree | `src/tools/ExitWorktreeTool/` |
| `DiscoverSkillsTool` | 发现技能 | 🟢 只读 | 扫描可用的 Skill 列表 | `src/tools/DiscoverSkillsTool/` |
| `AskUserQuestionTool` | 询问用户 | 🟢 只读 | 向用户提出问题（非执行）| `src/tools/AskUserQuestionTool/` |
| `BriefTool` | 简报 | 🟢 只读 | 生成会话简报摘要 | `src/tools/BriefTool/` |

---

## 定时任务类

| 工具名 | 操作类型 | 权限级别 | 典型操作 | 备注 |
|--------|---------|---------|---------|------|
| `CronCreateTool` | 创建定时任务 | 🟡 配置 | 创建定时执行的任务 | Feature Flag 控制 |
| `CronDeleteTool` | 删除定时任务 | 🔴 配置 | 删除定时任务 | Feature Flag 控制 |
| `CronListTool` | 列出定时任务 | 🟢 只读 | 列出所有定时任务 | Feature Flag 控制 |
| `ScheduleCronTool` | 调度 Cron | 🟡 配置 | 调度 cron 表达式任务 | Feature Flag 控制 |

---

## 其他工具

| 工具名 | 操作类型 | 权限级别 | 典型操作 | 备注 |
|--------|---------|---------|---------|------|
| `VerifyPlanExecutionTool` | 验证计划 | 🟢 只读 | 验证计划模式的执行结果 | `src/tools/VerifyPlanExecutionTool/` |
| `RemoteTriggerTool` | 远程触发 | 🔴 AI协作 | 触发远程 Agent 操作 | Feature Flag 控制 |
| `SuggestBackgroundPRTool` | 建议 PR | 🟡 AI协作 | 建议在后台创建 PR | Feature Flag 控制 |
| `SubscribePRTool` | 订阅 PR | 🟠 网络 | 订阅 PR 状态变化 | Feature Flag 控制 |
| `SleepTool` | 等待 | 🟢 只读 | 等待指定时间 | Feature Flag 控制 |
| `SendUserFileTool` | 发送文件给用户 | 🟡 配置 | 向用户会话发送文件 | Feature Flag（KAIROS）控制 |
| `PushNotificationTool` | 推送通知 | 🟠 网络 | 发送推送通知 | Feature Flag 控制 |

---

## 权限级别图例

| 图标 | 级别 | 说明 |
|------|------|------|
| 🟢 只读 | 低风险 | 不修改任何状态，通常自动允许 |
| 🟡 写入/配置 | 中等风险 | 修改文件或配置，权限规则可拦截 |
| 🟠 网络 | 中等风险 | 发起外部请求，依赖网络权限设置 |
| 🔴 执行/协作 | 高风险 | 执行命令或启动 Agent，建议用户确认 |

---

*基于 `src/tools.ts` v2.1.88 工具列表提取，共收录 55+ 工具。Feature Flag 控制的工具仅在对应 Flag 开启时可用。*
