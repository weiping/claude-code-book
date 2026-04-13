spec: task
name: "第28章：MCP 认证——OAuth、JWT 与 xaa"
tags: [book-chapter, part-7]
---

## 意图

本章解析 MCP 连接的三种认证路径。核心问题：OAuth PKCE 流程如何通过本地回调服务器完成？JWT 令牌刷新调度器如何工作？xaa（跨应用访问）企业认证与标准 OAuth 有何不同？

## 约束

必须：
- 引用 src/services/mcp/auth.ts 中的 OAuth 相关导入和 performCrossAppAccess（xaa）调用（约第48-60行）
- 引用 src/services/mcp/oauthPort.ts 中的 buildRedirectUri 和 findAvailablePort
- 引用 src/services/mcp/xaa.ts 中的 XaaTokenExchangeError 或 performCrossAppAccess
- 绘制 OAuth PKCE 流程的 Mermaid 序列图：用户授权 → 本地回调 → token 交换

禁止：
- 不得重复第 27 章的协议选择逻辑
- 不得深入 MCP 工具的执行（第 27 章范围）
- 不得分析 JWT 令牌的加密算法细节

## 已定决策

- 开篇问题："MCP 服务器需要登录时，Claude Code 怎么帮你完成认证？本地为什么要起一个 HTTP 服务器？"
- Mermaid sequenceDiagram 展示 OAuth PKCE 完整流程
- 源码引用格式：`src/services/mcp/auth.ts:行号`

## 边界

### 允许修改
- book/src/part7/ch28.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 JWT 加密算法

## 验收标准

场景: OAuth PKCE 流程图完整
  测试: verify_oauth_pkce_flow_diagram
  假设 读者阅读 Mermaid 序列图
  当 读者追踪 OAuth 认证流程
  那么 图中包含：Claude Code 发起 → 浏览器打开授权页 → 用户授权 → 重定向到本地回调端口 → token 交换 → 存储 token 五个步骤

场景: 本地回调端口机制说明
  测试: verify_local_callback_port
  假设 读者追问"为什么需要本地起一个 HTTP 服务器"
  那么 章节解释 findAvailablePort 动态分配端口、buildRedirectUri 构造回调 URL，以及本地服务器接收授权码的机制

场景: JWT 令牌刷新说明
  测试: verify_jwt_refresh_mechanism
  假设 读者追问"token 过期后如何自动刷新"
  那么 章节说明 checkAndRefreshOAuthTokenIfNeeded 的调用时机，以及刷新失败时的处理（重新触发 OAuth 流程）

场景: xaa 企业认证说明
  测试: verify_xaa_enterprise_auth
  假设 读者追问"xaa 和标准 OAuth 有什么区别"
  那么 章节解释 performCrossAppAccess 的企业身份场景（利用已有的 Claude.ai 身份换取 MCP 访问 token），引用 xaa.ts 中的 XaaTokenExchangeError

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 auth.ts 中的 performCrossAppAccess 调用
  那么 约第51行存在 import { performCrossAppAccess, XaaTokenExchangeError } from './xaa.ts' 导入

场景: 认证 token 存储安全
  测试: verify_token_storage_security
  假设 读者追问"OAuth token 存储在哪里，安全吗"
  那么 章节说明 token 的存储位置（安全存储，非明文配置文件）和有效期管理，有"详见附录 C"指引

## 排除范围

- 不深入 JWT 的 RS256/HS256 加密算法
- 不覆盖 MCP 工具的执行流程（第 27 章）
- 不分析 MCP channel 订阅机制（channelPermissions.ts 范围）
