spec: task
name: "第34章：跨会话记忆——extractMemories 与 teamMemorySync"
tags: [book-chapter, part-9]
---

## 意图

本章解析 Claude Code 的跨会话记忆积累机制。核心问题：extractMemories 如何在会话末尾提炼持久记忆？teamMemorySync 如何在团队成员间同步记忆？secretScanner 如何防止敏感信息写入共享记忆？

## 约束

必须：
- 引用 src/services/extractMemories/extractMemories.ts 中的 initExtractMemories（约第296行）、executeExtractMemories（约第598行）、drainPendingExtraction（约第611行）
- 引用 src/services/teamMemorySync/index.ts 中的 SyncState 类型（约第100行）、createSyncState（约第121行）
- 引用 src/services/teamMemorySync/secretScanner.ts 或 scanForSecrets 调用（约第60行）说明安全扫描
- 解释 ETag 追踪在 teamMemorySync 中的作用：防止重复同步相同内容

禁止：
- 不得重复第 26 章的本地 memdir 机制
- 不得深入 OAuth token 认证细节（第 28 章范围）
- 不得分析具体的 secret 检测规则（安全敏感）

## 已定决策

- 开篇问题："Claude Code 能记住上次对话的内容吗？这些记忆怎么在团队成员间共享？"
- Mermaid 流程图展示：会话结束 → extractMemories → teamMemorySync → 远端 → 本地同步
- 源码引用格式：`src/services/extractMemories/extractMemories.ts:行号`

## 边界

### 允许修改
- book/src/part9/ch34.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不重复本地 memdir 机制（第 26 章）

## 验收标准

场景: extractMemories 触发时机说明
  测试: verify_extract_memories_trigger
  假设 读者追问"什么时候会自动提炼记忆"
  那么 章节解释 initExtractMemories 的初始化时机，以及 drainPendingExtraction 的批量执行策略（会话结束时处理积压提炼任务）

场景: teamMemorySync 同步流程说明
  测试: verify_team_memory_sync_flow
  假设 读者追问"团队记忆怎么同步到我的本地"
  那么 章节说明 fetchTeamMemoryOnce 拉取远端记忆、SyncState 追踪同步状态、watcher 监听本地变化并上传的完整流程

场景: secretScanner 防护说明
  测试: verify_secret_scanner_protection
  假设 用户的记忆中包含 API key 或密码
  当 读者检查安全扫描机制
  那么 章节解释 scanForSecrets 在写入共享记忆前扫描敏感信息，检测到时拒绝写入或过滤，但不展示具体检测规则

场景: ETag 防重复同步说明
  测试: verify_etag_deduplication
  假设 读者追问"如果远端记忆没变化，每次都会重新同步吗"
  那么 章节解释 SyncState 中的 ETag 追踪机制：相同 ETag 时跳过同步，只在内容变化时触发

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 extractMemories.ts 中的 executeExtractMemories
  那么 约第598行存在该 async 函数定义

场景: 未认证用户的 teamMemorySync 降级
  测试: verify_unauthenticated_team_sync
  假设 用户未登录 OAuth（isAuthenticated 为 false）
  当 读者检查降级行为
  那么 章节说明未认证时 teamMemorySync 跳过同步（引用约第183行的错误返回），本地记忆功能不受影响

## 排除范围

- 不重复本地 memdir 的发现和注入（第 26 章）
- 不深入 OAuth token 刷新细节（第 28 章）
- 不展示 secretScanner 的具体检测规则（安全敏感）
