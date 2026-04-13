# 附录 D：环境变量参考

本附录汇总 Claude Code 支持的环境变量，涵盖 API 连接、模型选择、功能控制及 SDK 集成。可独立查阅，适合配置调试与部署时快速检索。

---

## API 连接类

| 变量名 | 类型 | 说明 | 相关章节 |
|--------|------|------|---------|
| `ANTHROPIC_API_KEY` | string | Anthropic API 密钥，直连 claude.ai 时必填 | — |
| `ANTHROPIC_BASE_URL` | string (URL) | 覆盖默认 API 基础 URL，适用于反向代理或私有部署 | — |
| `ANTHROPIC_AUTH_TOKEN` | string | 替代 API Key 的认证 token，二选一使用 | — |
| `ANTHROPIC_BEDROCK_BASE_URL` | string (URL) | AWS Bedrock 自定义接入点 URL | — |
| `ANTHROPIC_VERTEX_PROJECT_ID` | string | Google Vertex AI 项目 ID | — |
| `ANTHROPIC_FOUNDRY_API_KEY` | string | Azure AI Foundry API 密钥 | — |
| `ANTHROPIC_UNIX_SOCKET` | string (路径) | 通过 Unix domain socket 连接 API，适合本地代理场景 | — |
| `ANTHROPIC_BETAS` | string | 启用 Beta 功能列表，多个功能用逗号分隔 | — |
| `ANTHROPIC_CUSTOM_HEADERS` | JSON string | 注入自定义 HTTP 请求头，格式为 JSON 对象字符串 | — |

---

## 模型选择类

| 变量名 | 类型 | 说明 | 相关章节 |
|--------|------|------|---------|
| `ANTHROPIC_MODEL` | string | 覆盖主对话默认模型（如 `claude-3-5-sonnet-20241022`）| — |
| `ANTHROPIC_SMALL_FAST_MODEL` | string | 覆盖小型/快速任务使用的模型 | — |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | string | 覆盖默认 Haiku 系列模型 | — |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | string | 覆盖默认 Sonnet 系列模型 | — |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | string | 覆盖默认 Opus 系列模型 | — |

---

## 插件沙箱类

> 以下变量由 Claude Code 在启动 MCP/LSP 子进程时自动注入，插件代码可直接读取。

| 变量名 | 类型 | 说明 | 相关章节 |
|--------|------|------|---------|
| `CLAUDE_PLUGIN_ROOT` | string (路径) | 插件安装目录（**只读**），每次插件版本更新后路径会变化 | 第39章 |
| `CLAUDE_PLUGIN_DATA` | string (路径) | 插件持久化数据目录（**可读写**），跨版本升级后继续存在 | 第39章 |

---

## 功能控制类

| 变量名 | 类型 | 说明 | 相关章节 |
|--------|------|------|---------|
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | bool | 禁用非必要网络请求，包括官方插件注册表查询和遥测上报 | 第38章 |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | number | 覆盖上下文自动压缩触发阈值（百分比，默认约 80）| — |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | bool | Bash 工具执行后自动恢复原始工作目录，防止 `cd` 污染会话 | — |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | string (路径) | 额外的 `CLAUDE.md` 搜索目录，多路径用 `:` 分隔 | — |
| `CLAUDE_CODE_ADDITIONAL_PROTECTION` | bool | 启用额外安全保护层（具体机制为内部实现）| — |

---

## SDK 集成类

| 变量名 | 类型 | 说明 | 相关章节 |
|--------|------|------|---------|
| `CLAUDE_AGENT_SDK_CLIENT_APP` | string | SDK 调用方应用标识，用于遥测和日志区分 | — |
| `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS` | bool | 禁用内置 Agent 定义，完全由调用方提供 Agent 配置 | — |
| `CLAUDE_AGENT_SDK_MCP_NO_PREFIX` | bool | MCP 工具注册时不添加服务器名前缀，避免命名冲突 | — |
| `CLAUDE_AGENT_SDK_VERSION` | string | SDK 版本标识，注入到请求元数据中 | — |

---

> **版本说明：** 本参考基于 Claude Code v2.1.88 源码（`src/` 目录）中的环境变量读取点整理，仅列出已验证存在的变量。部分变量的具体默认值或行为可能随版本变更。
