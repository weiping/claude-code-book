spec: task
name: "第27章：MCP 客户端的三协议实现"
tags: [book-chapter, part-7]
---

## 意图

本章解析 Claude Code 的 MCP 客户端实现。核心问题：SSE、Stdio、StreamableHTTP 三种传输协议各适用什么场景？MCP 工具如何被包装成内部 Tool 对象？资源和 Prompt 如何动态注册？

## 约束

必须：
- 引用 src/services/mcp/client.ts 中的 connectToServer（约第595行）和三种传输类型的选择逻辑（约第626-683行）
- 引用 SSEClientTransport、StdioClientTransport、StreamableHTTPClientTransport 三个导入（约第9-15行）
- 引用 MCPTool 和 createMcpAuthTool 的包装逻辑，说明 MCP 工具如何转换为内部 Tool
- 解释 connectToServer 使用 memoize 的原因：同一服务器地址只建立一次连接

禁止：
- 不得深入 MCP 认证机制（第 28 章范围）
- 不得深入 MCP 工具的权限检查（第 15 章范围）
- 不得深入 MCP 工具的 UI 展示（TUI 层范围）

## 已定决策

- 开篇问题："你配置了一个 MCP 服务器，Claude Code 是怎么连上去、拿到工具列表的？"
- 对比表展示三种传输协议：适用场景、连接方式、认证支持
- 源码引用格式：`src/services/mcp/client.ts:行号`

## 边界

### 允许修改
- book/src/part7/ch27.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 MCP OAuth 认证（第 28 章）

## 验收标准

场景: 三协议选择逻辑说清
  测试: verify_three_protocol_selection
  假设 读者配置了不同类型的 MCP 服务器
  当 读者读完协议选择逻辑
  那么 章节说明 connectToServer 如何根据配置类型（stdio/sse/http）选择对应传输类，并给出每种协议的适用场景

场景: MCP 工具包装机制说明
  测试: verify_mcp_tool_wrapping
  假设 读者追问"MCP 工具怎么变成 Claude 能调用的工具"
  那么 章节解释 MCPTool 类包装 MCP 工具定义的方式，使其符合内部 Tool 接口，包括 name/description/inputSchema 的映射

场景: connectToServer memoize 原因说明
  测试: verify_connect_memoize_rationale
  假设 读者追问"为什么 connectToServer 用 memoize"
  那么 章节解释：同一服务器地址多次调用返回同一 client 实例，避免重复建立连接，引用第595行的 memoize 包装

场景: 资源和 Prompt 动态注册说明
  测试: verify_resource_prompt_registration
  假设 读者追问"MCP 服务器的资源列表怎么注册到 Claude"
  那么 章节说明 ListResourcesResult 和 ListPromptsResult 如何在连接时被获取并注册为可用能力

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 client.ts 中的 connectToServer
  那么 约第595行存在 export const connectToServer = memoize(...) 定义

场景: MCP 服务器连接失败处理
  测试: verify_connection_failure_handling
  假设 MCP 服务器地址不可达或启动失败
  当 读者检查连接失败处理
  那么 章节说明连接失败时工具集的变化（该服务器工具不可用）和用户提示方式

## 排除范围

- 不深入 MCP OAuth/JWT 认证（第 28 章）
- 不分析 MCP 工具的权限检查流程（第 15 章）
- 不覆盖 InProcessTransport（SDK 内部传输，非用户配置场景）
