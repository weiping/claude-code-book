spec: task
name: "第32章：Swarm 权限同步——沙箱中的信任传递"
tags: [book-chapter, part-8]
---

## 意图

本章解析 Swarm 中跨进程的权限请求同步机制。核心问题：Worker Agent 需要权限时如何通知 Leader？Mailbox 机制如何避免进程间的直接调用？leaderPermissionBridge 的确认队列解决什么竞争问题？

## 约束

必须：
- 引用 src/utils/swarm/permissionSync.ts 中的 SwarmPermissionRequestSchema（约第49行）、createPermissionRequest（约第167行）、writePermissionRequest（约第215行）、readPendingPermissions（约第256行）
- 引用 src/utils/swarm/leaderPermissionBridge.ts 中的 registerLeaderToolUseConfirmQueue（约第28行）
- 解释 Mailbox 机制：以文件系统或共享内存为媒介的异步消息传递，避免进程间直接 IPC
- 说明 generateRequestId（约第160行）的作用：确保权限请求的幂等性

禁止：
- 不得重复第 15 章的权限决策三层架构
- 不得深入 Worker 的 Task 实现（第 30 章范围）
- 不得分析 UI 权限对话框（TUI 层范围）

## 已定决策

- 开篇问题："子 Agent 在沙箱里运行，它需要执行危险操作时，谁来决定允许还是拒绝？"
- Mermaid sequenceDiagram 展示 Worker 请求 → Mailbox → Leader 决策 → 结果回传的完整流程
- 源码引用格式：`src/utils/swarm/permissionSync.ts:行号`

## 边界

### 允许修改
- book/src/part8/ch32.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入权限决策三层（第 15 章）

## 验收标准

场景: Mailbox 机制说清
  测试: verify_mailbox_mechanism
  假设 读者追问"Worker 怎么告诉 Leader 它需要权限"
  那么 章节解释 writePermissionRequest 将请求写入 Mailbox（文件系统目录），Leader 通过 readPendingPermissions 轮询读取，避免进程间直接调用

场景: 权限请求序列图完整
  测试: verify_permission_sync_sequence_diagram
  假设 读者阅读 Mermaid 序列图
  当 读者追踪一次权限请求的完整流程
  那么 图中包含：Worker 发起 → writePermissionRequest → Leader 轮询发现 → 用户确认 → resolvePermission 写入结果 → Worker 读取结果五步

场景: leaderPermissionBridge 确认队列说明
  测试: verify_leader_confirm_queue
  假设 读者追问"多个 Worker 同时请求权限时如何排队"
  那么 章节解释 registerLeaderToolUseConfirmQueue 注册的确认队列如何串行化并发权限请求，避免竞争条件

场景: generateRequestId 幂等性说明
  测试: verify_request_id_idempotency
  假设 读者追问"权限请求如何防止重复处理"
  那么 章节说明 generateRequestId 生成唯一 ID，Leader 通过 ID 避免重复响应同一请求

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 permissionSync.ts 中的 SwarmPermissionRequestSchema
  那么 约第49行存在该 schema 定义（使用 lazySchema 包装）

场景: Leader 无响应时 Worker 的超时处理
  测试: verify_leader_timeout_handling
  假设 Leader 进程崩溃或无响应
  当 读者检查超时处理机制
  那么 章节说明 Worker 等待权限响应的超时策略（超时后拒绝操作或抛出异常），引用相关代码

## 排除范围

- 不重复权限决策三层架构（第 15 章）
- 不深入 Worker 的 Task 执行实现（第 30 章）
- 不分析权限对话框的 React 组件（TUI 层）
