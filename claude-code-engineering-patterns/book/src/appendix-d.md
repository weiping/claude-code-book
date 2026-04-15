# 附录 D：环境变量参考

本附录汇总 Claude Code 支持的环境变量，涵盖 API 连接、模型选择、提供商路由、功能控制、遥测、MCP、SDK 集成及插件沙箱。可独立查阅，适合配置调试与部署时快速检索。

---

## API 连接类

| 变量名 | 类型 | 默认值 | 说明 | 相关章节 |
|--------|------|--------|------|---------|
| `ANTHROPIC_API_KEY` | string | — | Anthropic API 密钥，直连 claude.ai 时必填 | 第13章 |
| `ANTHROPIC_BASE_URL` | string (URL) | `https://api.anthropic.com` | 覆盖默认 API 基础 URL，适用于反向代理或私有部署 | 第13章 |
| `ANTHROPIC_AUTH_TOKEN` | string | — | 替代 API Key 的 Bearer Token，与 `ANTHROPIC_API_KEY` 二选一 | 第13章 |
| `ANTHROPIC_BEDROCK_BASE_URL` | string (URL) | — | AWS Bedrock 自定义接入点 URL（覆盖 `BEDROCK_BASE_URL`）| 第11章 |
| `ANTHROPIC_VERTEX_PROJECT_ID` | string | — | Google Vertex AI 项目 ID | 第11章 |
| `ANTHROPIC_FOUNDRY_API_KEY` | string | — | Azure AI Foundry API 密钥 | 第11章 |
| `ANTHROPIC_FOUNDRY_BASE_URL` | string (URL) | — | Azure AI Foundry 自定义接入点 URL | 第11章 |
| `ANTHROPIC_FOUNDRY_RESOURCE` | string | — | Azure 资源名称（如 `my-resource`），Foundry 模式必填 | 第11章 |
| `ANTHROPIC_UNIX_SOCKET` | string (路径) | — | 通过 Unix domain socket 连接 API，适合本地代理场景 | 第13章 |
| `ANTHROPIC_BETAS` | string | — | 启用 Beta 功能列表，多个功能用逗号分隔 | 第13章 |
| `ANTHROPIC_CUSTOM_HEADERS` | JSON string | — | 注入自定义 HTTP 请求头，格式为 JSON 对象字符串 | 第13章 |
| `API_TIMEOUT_MS` | number | — | API 请求超时时间（毫秒），超时报错时 UI 会提示本变量 | 第13章 |
| `HTTP_PROXY` / `HTTPS_PROXY` | string (URL) | — | 出站 HTTP/HTTPS 代理，自动传递给子进程 | 第13章 |
| `NO_PROXY` | string | — | 不走代理的主机列表，逗号分隔 | 第13章 |
| `NODE_EXTRA_CA_CERTS` | string (路径) | — | 附加受信任 CA 证书文件路径（PEM 格式）| 第13章 |
| `CLAUDE_CODE_CLIENT_CERT` | string (路径) | — | 客户端 TLS 证书路径（mTLS 场景）| 第13章 |
| `CLAUDE_CODE_CLIENT_KEY` | string (路径) | — | 客户端 TLS 私钥路径（mTLS 场景）| 第13章 |
| `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE` | string | — | 客户端 TLS 私钥密码短语 | 第13章 |

---

## 模型选择类

| 变量名 | 类型 | 默认值 | 说明 | 相关章节 |
|--------|------|--------|------|---------|
| `ANTHROPIC_MODEL` | string | — | 覆盖主对话默认模型（如 `claude-opus-4-5`）| 第11章 |
| `ANTHROPIC_SMALL_FAST_MODEL` | string | — | 覆盖小型/快速任务使用的模型 | 第11章 |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | string | — | 专门用于小型快速模型（Haiku）的 AWS 区域覆盖 | 第11章 |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | string | — | 覆盖默认 Haiku 系列模型标识符 | 第11章 |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | string | — | 覆盖默认 Sonnet 系列模型标识符 | 第11章 |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | string | — | 覆盖默认 Opus 系列模型标识符 | 第11章 |
| `ANTHROPIC_CUSTOM_MODEL_OPTION` | string | — | 自定义模型选项值，与 `_NAME`/`_DESCRIPTION` 配合使用 | 第11章 |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` | string | — | 自定义模型选项在 UI 中显示的名称 | 第11章 |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` | string | — | 自定义模型选项描述文本 | 第11章 |
| `CLAUDE_CODE_SUBAGENT_MODEL` | string | — | 覆盖子 Agent 使用的模型，不影响主 Agent | 第11章 |
| `CLAUDE_CODE_AUTO_MODE_MODEL` | string | — | 自动模式下使用的专用模型 | 第11章 |
| `FALLBACK_FOR_ALL_PRIMARY_MODELS` | bool | false | 所有主模型均启用降级回退逻辑 | 第11章 |

---

## 提供商选择类

> 三个云提供商互斥：同时只应设置其中一个 `USE_*` 标志。

| 变量名 | 类型 | 默认值 | 说明 | 相关章节 |
|--------|------|--------|------|---------|
| `CLAUDE_CODE_USE_BEDROCK` | bool | false | 启用 AWS Bedrock 作为 API 提供商 | 第11章 |
| `CLAUDE_CODE_USE_VERTEX` | bool | false | 启用 Google Vertex AI 作为 API 提供商 | 第11章 |
| `CLAUDE_CODE_USE_FOUNDRY` | bool | false | 启用 Azure AI Foundry 作为 API 提供商 | 第11章 |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH` | bool | false | 跳过 Bedrock 凭证检查（用于自定义认证代理）| 第11章 |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH` | bool | false | 跳过 Vertex AI 凭证检查 | 第11章 |
| `CLAUDE_CODE_SKIP_FOUNDRY_AUTH` | bool | false | 跳过 Foundry 凭证检查 | 第11章 |
| `AWS_DEFAULT_REGION` | string | — | AWS 默认区域，影响 Bedrock 接入点选择 | 第11章 |
| `AWS_BEARER_TOKEN_BEDROCK` | string | — | Bedrock 专用 Bearer Token 认证 | 第11章 |
| `BEDROCK_BASE_URL` | string (URL) | — | Bedrock 基础 URL（被 `ANTHROPIC_BEDROCK_BASE_URL` 覆盖）| 第11章 |
| `VERTEX_BASE_URL` | string (URL) | — | Vertex AI 基础 URL 覆盖 | 第11章 |
| `GOOGLE_CLOUD_PROJECT` | string | — | Google Cloud 项目 ID，Vertex AI 场景下使用 | 第11章 |
| `CLOUD_ML_REGION` | string | — | Vertex AI 所在 Google Cloud 区域 | 第11章 |

---

## 思考/推理控制类

| 变量名 | 类型 | 默认值 | 说明 | 相关章节 |
|--------|------|--------|------|---------|
| `MAX_THINKING_TOKENS` | number | — | 覆盖扩展思考允许使用的最大 token 数；设为 0 等同于禁用 | 第12章 |
| `CLAUDE_CODE_DISABLE_THINKING` | bool | false | 禁用扩展思考功能（Claude 3.7+ 的 extended thinking）| 第12章 |
| `DISABLE_INTERLEAVED_THINKING` | bool | false | 禁用交错思考（thinking 与工具调用交替进行）| 第12章 |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` | bool | false | 禁用自适应思考预算调整逻辑 | 第12章 |
| `CLAUDE_CODE_EFFORT_LEVEL` | string | — | 设置推理努力程度（如 `low` / `medium` / `high`）| 第12章 |
| `CLAUDE_CODE_ALWAYS_ENABLE_EFFORT` | bool | false | 强制启用 effort 参数，即使模型不支持也传递 | 第12章 |

---

## 上下文与压缩类

| 变量名 | 类型 | 默认值 | 说明 | 相关章节 |
|--------|------|--------|------|---------|
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | number | ~80 | 覆盖上下文自动压缩触发阈值（百分比）| 第22章 |
| `DISABLE_COMPACT` | bool | false | 完全禁用压缩功能（含手动 `/compact` 命令）| 第22章 |
| `DISABLE_AUTO_COMPACT` | bool | false | 仅禁用自动压缩，保留手动压缩能力 | 第22章 |
| `CLAUDE_CODE_MAX_CONTEXT_TOKENS` | number | — | 覆盖最大上下文 token 数（默认从模型能力读取）| 第22章 |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | number | — | 覆盖最大输出 token 数 | 第22章 |
| `CLAUDE_CODE_AUTO_COMPACT_WINDOW` | number | — | 自动压缩窗口大小设置 | 第22章 |
| `CLAUDE_CODE_DISABLE_PRECOMPACT_SKIP` | bool | false | 禁用压缩前跳过逻辑，强制每次都压缩 | 第22章 |
| `CLAUDE_AFTER_LAST_COMPACT` | string | — | 记录上次压缩后的时间戳（运行时内部注入）| 第22章 |
| `API_MAX_INPUT_TOKENS` | number | — | 微压缩（micro-compact）触发阈值，超过则删减历史消息 | 第22章 |
| `API_TARGET_INPUT_TOKENS` | number | — | 微压缩保留目标 token 数 | 第22章 |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT` | bool | false | 禁用 100 万 token 超长上下文功能 | 第22章 |
| `ENABLE_CLAUDE_CODE_SM_COMPACT` | bool | false | 启用 SM 压缩实验功能 | 第22章 |
| `DISABLE_CLAUDE_CODE_SM_COMPACT` | bool | false | 禁用 SM 压缩实验功能 | 第22章 |

---

## Swarm / 协调器类

| 变量名 | 类型 | 默认值 | 说明 | 相关章节 |
|--------|------|--------|------|---------|
| `CLAUDE_CODE_COORDINATOR_MODE` | bool | false | 启用协调器模式，当前实例作为 Swarm 编排节点 | 第33章 |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | bool | false | 启用实验性多 Agent 团队协作功能 | 第33章 |
| `CLAUDE_CODE_PLAN_V2_AGENT_COUNT` | number | — | Plan v2 模式下并发 Agent 数量 | 第33章 |
| `CLAUDE_CODE_PLAN_V2_EXPLORE_AGENT_COUNT` | number | — | Plan v2 探索阶段 Agent 数量 | 第33章 |
| `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY` | number | — | 工具调用最大并发数 | 第33章 |

---

## 功能控制类

| 变量名 | 类型 | 默认值 | 说明 | 相关章节 |
|--------|------|--------|------|---------|
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | bool | false | 禁用非必要网络请求（插件注册表查询、遥测上报等）| 第41章 |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | bool | false | Bash 工具执行后自动恢复原始工作目录，防止 `cd` 污染会话 | 第14章 |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | string (路径) | — | 额外的 `CLAUDE.md` 搜索目录，多路径用 `:` 分隔 | — |
| `CLAUDE_CODE_ADDITIONAL_PROTECTION` | bool | false | 启用额外安全保护层（内部实现机制）| 第37章 |
| `CLAUDE_CODE_DISABLE_COMMAND_INJECTION_CHECK` | bool | false | 禁用 Bash 命令注入检查（**高风险**，不建议生产使用）| 第37章 |
| `BASH_MAX_OUTPUT_LENGTH` | number | — | Bash 工具单次输出最大字符数 | 第14章 |
| `TASK_MAX_OUTPUT_LENGTH` | number | — | Task 工具单次输出最大字符数 | 第29章 |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` | number | — | 文件读取工具单次返回最大 token 数 | 第14章 |
| `DISABLE_COST_WARNINGS` | bool | false | 禁用 API 费用超额警告提示 | — |
| `DISABLE_PROMPT_CACHING` | bool | false | 禁用所有模型的 Prompt 缓存 | 第13章 |
| `DISABLE_PROMPT_CACHING_HAIKU` | bool | false | 仅禁用 Haiku 系列的 Prompt 缓存 | 第13章 |
| `DISABLE_PROMPT_CACHING_SONNET` | bool | false | 仅禁用 Sonnet 系列的 Prompt 缓存 | 第13章 |
| `DISABLE_PROMPT_CACHING_OPUS` | bool | false | 仅禁用 Opus 系列的 Prompt 缓存 | 第13章 |
| `ENABLE_PROMPT_CACHING_1H_BEDROCK` | bool | false | 在 Bedrock 上启用 1 小时长效 Prompt 缓存 | 第13章 |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` | bool | false | 禁用系统提示中注入的 Git 相关操作指导 | — |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | bool | false | 禁用自动记忆功能 | — |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | bool | false | 禁用后台任务执行 | 第29章 |
| `CLAUDE_CODE_DISABLE_FAST_MODE` | bool | false | 禁用快速模式（强制使用完整推理路径）| — |
| `CLAUDE_CODE_DISABLE_ATTACHMENTS` | bool | false | 禁用文件附件功能 | — |
| `CLAUDE_CODE_DISABLE_CLAUDE_MDS` | bool | false | 禁用 CLAUDE.md 配置文件加载 | — |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY` | bool | false | 禁用反馈调查弹出 | — |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` | bool | false | 禁用动态设置终端窗口标题 | — |
| `CLAUDE_CODE_DISABLE_MOUSE` | bool | false | 禁用鼠标事件捕获 | — |
| `CLAUDE_CODE_DISABLE_MOUSE_CLICKS` | bool | false | 仅禁用鼠标点击事件 | — |
| `CLAUDE_CODE_DISABLE_VIRTUAL_SCROLL` | bool | false | 禁用虚拟滚动（调试 UI 渲染时有用）| — |
| `CLAUDE_CODE_DISABLE_MESSAGE_ACTIONS` | bool | false | 禁用消息右键操作菜单 | — |
| `CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK` | bool | false | 禁用非流式响应降级逻辑 | 第13章 |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | bool | false | 禁用所有实验性 Beta 功能 | — |
| `CLAUDE_CODE_DISABLE_POLICY_SKILLS` | bool | false | 禁用策略技能注入 | — |
| `CLAUDE_CODE_DISABLE_ADVISOR_TOOL` | bool | false | 禁用 Advisor 工具 | — |
| `DISABLE_TELEMETRY` | bool | false | 完全禁用遥测上报（使隐私级别升至 no-telemetry）| — |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | bool | false | 显式启用遥测（覆盖默认关闭状态）| — |
| `CLAUDE_CODE_ENABLE_TASKS` | bool | false | 启用任务管理功能 | 第29章 |
| `CLAUDE_CODE_ENABLE_CFC` | bool | false | 启用 Continuous Function Calling 功能 | — |
| `CLAUDE_CODE_ENABLE_FINE_GRAINED_TOOL_STREAMING` | bool | false | 启用细粒度工具流式传输 | 第13章 |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION` | bool | false | 启用提示词建议功能 | — |
| `CLAUDE_CODE_ENABLE_XAA` | bool | false | 启用 XAA 跨 Agent 认证功能 | 第33章 |
| `CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING` | bool | false | SDK 模式下启用文件检查点 | — |
| `CLAUDE_CODE_ENABLE_TOKEN_USAGE_ATTACHMENT` | bool | false | 将 token 用量附加到消息中 | — |
| `CLAUDE_CODE_GLOB_HIDDEN` | bool | false | Glob 匹配时包含隐藏文件（以 `.` 开头）| 第14章 |
| `CLAUDE_CODE_GLOB_NO_IGNORE` | bool | false | Glob 匹配时忽略 `.gitignore` 等排除规则 | 第14章 |
| `CLAUDE_CODE_GLOB_TIMEOUT_SECONDS` | number | — | Glob 操作超时时间（秒）| 第14章 |
| `CLAUDE_CODE_USE_NATIVE_FILE_SEARCH` | bool | false | 使用系统原生文件搜索代替内置实现 | 第14章 |
| `USE_BUILTIN_RIPGREP` | bool | false | 强制使用内置 ripgrep 而非系统 PATH 中的版本 | 第14章 |
| `EMBEDDED_SEARCH_TOOLS` | bool | false | 启用内嵌搜索工具 | 第14章 |
| `ENABLE_TOOL_SEARCH` | bool | false | 启用工具搜索功能 | 第14章 |
| `ENABLE_LSP_TOOL` | bool | false | 启用 LSP（Language Server Protocol）工具 | — |
| `CLAUDE_CODE_USE_POWERSHELL_TOOL` | bool | false | 在 Windows 上使用 PowerShell 工具替代 Bash | 第14章 |
| `CLAUDE_CODE_PWSH_PARSE_TIMEOUT_MS` | number | — | PowerShell 命令解析超时（毫秒）| 第14章 |
| `CLAUDE_CODE_TWO_STAGE_CLASSIFIER` | bool | false | 启用两阶段安全分类器 | 第37章 |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET` | number | — | Slash 命令工具的字符预算上限 | — |
| `MAX_STRUCTURED_OUTPUT_RETRIES` | number | — | 结构化输出解析失败的最大重试次数 | 第13章 |
| `CLAUDE_CODE_MAX_RETRIES` | number | — | API 请求最大重试次数 | 第13章 |
| `CLAUDE_CODE_UNATTENDED_RETRY` | bool | false | 无人值守模式下自动重试（不提示用户）| — |
| `CLAUDE_CODE_PLAN_MODE_REQUIRED` | bool | false | 强制进入 Plan 模式，不能直接执行 | — |
| `CLAUDE_CODE_PLAN_MODE_INTERVIEW_PHASE` | bool | false | Plan 模式启用访谈阶段 | — |
| `CLAUDE_CODE_VERIFY_PLAN` | bool | false | 执行前要求用户验证计划 | — |
| `CLAUDE_CODE_RESUME_INTERRUPTED_TURN` | bool | false | 启动时自动恢复被中断的对话轮次 | — |
| `CLAUDE_CODE_PROACTIVE` | bool | false | 启用主动建议功能 | — |
| `CLAUDE_CODE_AUTO_BACKGROUND_TASKS` | bool | false | 自动将长任务移入后台执行 | 第29章 |
| `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING` | bool | false | 禁用文件变更检查点（减少磁盘写入）| — |
| `CLAUDE_CODE_IDLE_THRESHOLD_MINUTES` | number | — | 空闲检测阈值（分钟），超过则触发空闲回调 | — |
| `CLAUDE_CODE_IDLE_TOKEN_THRESHOLD` | number | — | 基于 token 数的空闲触发阈值 | — |
| `CLAUDE_CODE_SIMPLE` | bool | false | 启用简化模式（禁用部分高级功能）| — |
| `CLAUDE_CODE_BRIEF` | bool | false | 启用简洁输出模式 | — |
| `CLAUDE_CODE_STREAMLINED_OUTPUT` | bool | false | 启用流式精简输出格式 | — |
| `CLAUDE_CODE_STRICT` | bool | false | 严格模式，不允许任何隐式操作 | 第37章 |

---

## 遥测 / 可观测性类

| 变量名 | 类型 | 默认值 | 说明 | 相关章节 |
|--------|------|--------|------|---------|
| `OTEL_TRACES_EXPORTER` | string | — | OpenTelemetry Traces 导出器（`console` / `otlp` 等）| — |
| `OTEL_METRICS_EXPORTER` | string | — | OpenTelemetry Metrics 导出器 | — |
| `OTEL_LOGS_EXPORTER` | string | — | OpenTelemetry Logs 导出器 | — |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | string (URL) | — | OTLP 导出端点 URL | — |
| `OTEL_EXPORTER_OTLP_HEADERS` | string | — | OTLP 请求头（格式：`key=value,key2=value2`）| — |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | string | — | OTLP 协议（`grpc` / `http/protobuf` / `http/json`）| — |
| `OTEL_LOG_TOOL_CONTENT` | bool | false | OTEL Logs 中记录工具输入/输出内容 | — |
| `OTEL_LOG_TOOL_DETAILS` | bool | false | OTEL Logs 中记录工具调用详情 | — |
| `OTEL_LOG_USER_PROMPTS` | bool | false | OTEL Logs 中记录用户提示词（**隐私敏感**）| — |
| `OTEL_METRIC_EXPORT_INTERVAL` | number | — | Metrics 导出间隔（毫秒）| — |
| `OTEL_TRACES_EXPORT_INTERVAL` | number | — | Traces 导出间隔（毫秒）| — |
| `OTEL_LOGS_EXPORT_INTERVAL` | number | — | Logs 导出间隔（毫秒）| — |
| `ANT_OTEL_TRACES_EXPORTER` | string | — | 内部覆盖 `OTEL_TRACES_EXPORTER` 的 Anthropic 私有变量 | — |
| `ANT_OTEL_METRICS_EXPORTER` | string | — | 内部覆盖 `OTEL_METRICS_EXPORTER` 的 Anthropic 私有变量 | — |
| `ANT_OTEL_LOGS_EXPORTER` | string | — | 内部覆盖 `OTEL_LOGS_EXPORTER` 的 Anthropic 私有变量 | — |
| `ANT_OTEL_EXPORTER_OTLP_ENDPOINT` | string (URL) | — | 内部 OTLP 端点变量 | — |
| `ANT_OTEL_EXPORTER_OTLP_HEADERS` | string | — | 内部 OTLP 请求头变量 | — |
| `ANT_OTEL_EXPORTER_OTLP_PROTOCOL` | string | — | 内部 OTLP 协议变量 | — |
| `CLAUDE_CODE_OTEL_FLUSH_TIMEOUT_MS` | number | — | OTEL 数据刷新超时（毫秒）| — |
| `CLAUDE_CODE_OTEL_SHUTDOWN_TIMEOUT_MS` | number | — | OTEL 关闭等待超时（毫秒）| — |
| `DISABLE_TELEMETRY` | bool | false | 完全禁用遥测（见"功能控制类"）| — |
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` | bool | false | 启用增强遥测 Beta 功能 | — |
| `ENABLE_ENHANCED_TELEMETRY_BETA` | bool | false | 同上，另一种写法 | — |
| `CLAUDE_CODE_JSONL_TRANSCRIPT` | string (路径) | — | 将对话记录导出为 JSONL 文件路径 | — |
| `CLAUDE_CODE_SESSION_LOG` | string (路径) | — | Session 级别日志输出路径 | — |
| `CLAUDE_CODE_DEBUG_LOGS_DIR` | string (路径) | — | 调试日志目录 | — |
| `CLAUDE_CODE_DEBUG_LOG_LEVEL` | string | — | 调试日志级别（如 `debug` / `info` / `warn`）| — |
| `CLAUDE_DEBUG` | bool | false | 启用通用调试输出 | — |
| `DEBUG` | string | — | 标准 Node.js debug 命名空间过滤器 | — |

---

## MCP 集成类

| 变量名 | 类型 | 默认值 | 说明 | 相关章节 |
|--------|------|--------|------|---------|
| `MCP_TIMEOUT` | number | 30000 | MCP 服务器连接超时（毫秒）| — |
| `MCP_TOOL_TIMEOUT` | number | ~27.8h | MCP 工具调用超时（毫秒，默认极大以支持长任务）| — |
| `MAX_MCP_OUTPUT_TOKENS` | number | 25000 | MCP 工具单次输出最大 token 数 | — |
| `MCP_SERVER_CONNECTION_BATCH_SIZE` | number | — | MCP 服务器批量连接数 | — |
| `MCP_REMOTE_SERVER_CONNECTION_BATCH_SIZE` | number | — | 远程 MCP 服务器批量连接数 | — |
| `ENABLE_MCP_LARGE_OUTPUT_FILES` | bool | false | 允许 MCP 工具返回大文件内容 | — |
| `CLAUDE_CODE_MCP_INSTR_DELTA` | string | — | MCP 工具指令差量注入 | — |
| `ENABLE_CLAUDEAI_MCP_SERVERS` | bool | false | 启用 claude.ai 平台 MCP 服务器 | — |
| `MCP_CLIENT_SECRET` | string | — | MCP OAuth 客户端密钥 | — |
| `MCP_OAUTH_CALLBACK_PORT` | number | — | MCP OAuth 回调端口 | — |
| `MCP_OAUTH_CLIENT_METADATA_URL` | string (URL) | — | MCP OAuth 客户端元数据 URL | — |
| `MCP_XAA_IDP_CLIENT_SECRET` | string | — | MCP XAA 身份提供商客户端密钥 | — |

---

## SDK 集成类

| 变量名 | 类型 | 默认值 | 说明 | 相关章节 |
|--------|------|--------|------|---------|
| `CLAUDE_AGENT_SDK_CLIENT_APP` | string | — | SDK 调用方应用标识，用于遥测和日志区分 | — |
| `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS` | bool | false | 禁用内置 Agent 定义，完全由调用方提供 Agent 配置 | — |
| `CLAUDE_AGENT_SDK_MCP_NO_PREFIX` | bool | false | MCP 工具注册时不添加服务器名前缀，避免命名冲突 | — |
| `CLAUDE_AGENT_SDK_VERSION` | string | — | SDK 版本标识，注入到请求元数据中 | — |
| `CLAUDE_CODE_EMIT_SESSION_STATE_EVENTS` | bool | false | 以事件形式发射 Session 状态变化（SDK 场景使用）| — |
| `CLAUDE_CODE_EMIT_TOOL_USE_SUMMARIES` | bool | false | 发射工具调用摘要事件 | — |
| `CLAUDE_CODE_INCLUDE_PARTIAL_MESSAGES` | bool | false | SDK 流中包含未完成的消息片段 | — |
| `CLAUDE_CODE_EXTRA_BODY` | JSON string | — | 附加到 API 请求 body 的 JSON 字段 | 第13章 |
| `CLAUDE_CODE_EXTRA_METADATA` | JSON string | — | 附加到请求的元数据 JSON | 第13章 |
| `CLAUDE_CODE_ATTRIBUTION_HEADER` | string | — | 请求归因标识头，标记调用来源 | 第13章 |

---

## 插件 / Marketplace 类

> 以下变量由 Claude Code 在启动 MCP/LSP 子进程时自动注入，插件代码可直接读取。

| 变量名 | 类型 | 默认值 | 说明 | 相关章节 |
|--------|------|--------|------|---------|
| `CLAUDE_PLUGIN_ROOT` | string (路径) | — | 插件安装目录（**只读**），每次插件版本更新后路径会变化 | 第43章 |
| `CLAUDE_PLUGIN_DATA` | string (路径) | — | 插件持久化数据目录（**可读写**），跨版本升级后继续存在 | 第43章 |
| `CLAUDE_CODE_PLUGIN_CACHE_DIR` | string (路径) | — | 插件 ZIP 缓存目录，与 `CLAUDE_CODE_PLUGIN_USE_ZIP_CACHE` 配合 | 第43章 |
| `CLAUDE_CODE_PLUGIN_SEED_DIR` | string (路径) | — | 插件种子 Marketplace 目录，启动时预注册 | 第43章 |
| `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` | number | 120000 | Git 拉取插件更新的超时时间（毫秒）| 第43章 |
| `CLAUDE_CODE_PLUGIN_USE_ZIP_CACHE` | bool | false | 从 ZIP 缓存安装插件，不走 Git 克隆 | 第43章 |
| `FORCE_AUTOUPDATE_PLUGINS` | bool | false | 忽略版本检查，强制更新所有插件 | 第43章 |
| `CLAUDE_CODE_DISABLE_POLICY_SKILLS` | bool | false | 禁用通过策略注入的技能（见"功能控制类"）| 第41章 |

---

## 配置与会话类

| 变量名 | 类型 | 默认值 | 说明 | 相关章节 |
|--------|------|--------|------|---------|
| `CLAUDE_CONFIG_DIR` | string (路径) | `~/.claude` | 覆盖 Claude Code 配置目录路径 | — |
| `CLAUDE_ENV_FILE` | string (路径) | — | Hook 脚本写入 Bash exports 的临时 env 文件路径（运行时注入）| — |
| `CLAUDE_CODE_API_KEY_FILE_DESCRIPTOR` | number | — | 从指定文件描述符读取 API Key（安全传参）| 第13章 |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` | number | — | API Key Helper 缓存 TTL（毫秒）| 第13章 |
| `CLAUDE_CODE_OAUTH_TOKEN` | string | — | OAuth Access Token | — |
| `CLAUDE_CODE_OAUTH_REFRESH_TOKEN` | string | — | OAuth Refresh Token | — |
| `CLAUDE_CODE_OAUTH_CLIENT_ID` | string | — | OAuth 客户端 ID | — |
| `CLAUDE_CODE_OAUTH_SCOPES` | string | — | OAuth 请求的权限范围，逗号分隔 | — |
| `CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR` | number | — | 从文件描述符读取 OAuth Token | — |
| `CLAUDE_CODE_SESSION_ACCESS_TOKEN` | string | — | Session 级别访问 Token | — |
| `CLAUDE_CODE_WEBSOCKET_AUTH_FILE_DESCRIPTOR` | number | — | 从文件描述符读取 WebSocket 认证信息 | — |
| `CLAUDE_CODE_ORGANIZATION_UUID` | string | — | 组织 UUID，用于多租户场景 | — |
| `CLAUDE_CODE_ACCOUNT_UUID` | string | — | 账户 UUID | — |
| `CLAUDE_CODE_ACCOUNT_TAGGED_ID` | string | — | 账户带标签的 ID | — |
| `CLAUDE_CODE_USER_EMAIL` | string | — | 用户邮箱，注入到会话元数据 | — |
| `CLAUDE_CODE_TAGS` | string | — | 会话标签，逗号分隔，用于遥测分类 | — |
| `CLAUDE_CODE_SESSION_NAME` | string | — | 会话显示名称 | — |
| `CLAUDE_CODE_SESSION_KIND` | string | — | 会话类型标识 | — |
| `CLAUDE_CODE_CONTAINER_ID` | string | — | 容器 ID，容器化部署时使用 | — |
| `CLAUDE_CODE_REMOTE` | bool | false | 标记当前为远程会话 | — |
| `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` | string | — | 远程环境类型（如 `ssh` / `container`）| — |
| `CLAUDE_CODE_ENVIRONMENT_KIND` | string | — | 环境种类（如 `local` / `ci` / `sandbox`）| — |
| `CLAUDE_CODE_ENTRYPOINT` | string | — | 入口点标识，记录启动来源 | — |
| `CLAUDE_CODE_IS_COWORK` | bool | false | 标记当前为协作（Cowork）会话 | — |

---

> **版本说明：** 本参考基于 Claude Code v2.1.88 源码（`src/` 目录）中的环境变量读取点整理，仅列出已验证存在的变量。部分变量的具体默认值或行为可能随版本变更。未注明默认值（`—`）的变量，未设置时通常意味着功能关闭或使用代码内硬编码默认值。
