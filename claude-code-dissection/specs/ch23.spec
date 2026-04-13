spec: task
name: "第23章：会话系统——标识、持久化与恢复"
tags: [book-chapter, part-6]
---

## 意图

本章解析 Claude Code 的会话管理机制。核心问题：会话 ID 如何生成和传递？对话记录如何以追加写入的 JSONL 格式持久化？/resume 命令如何查找并恢复历史会话？并发会话如何隔离？

## 约束

必须：
- 引用 src/utils/sessionStorage.ts 中的 getTranscriptPath（约第202行）、MAX_TRANSCRIPT_READ_BYTES（约第229行）
- 引用 src/bootstrap/state.ts 中的 getSessionId 和 switchSession 展示会话 ID 的状态管理
- 引用 src/utils/concurrentSessions.ts 中的 SessionKind 枚举（interactive/bg/daemon/daemon-worker）
- 说明 .jsonl 追加写入模式的设计：为什么用追加而非覆盖

禁止：
- 不得深入 compact 策略（第 24-25 章范围）
- 不得深入 agentTranscript 路径（第 31 章 Subagent 范围）
- 不得深入 sessionStorage 的加密（本版本未实现）

## 已定决策

- 开篇问题："会话结束后数据存在哪里？下次 /resume 时如何找回？"
- ASCII 目录树展示 .claude/projects/ 下的 JSONL 文件结构
- 源码引用格式：`src/utils/sessionStorage.ts:行号`

## 边界

### 允许修改
- book/src/part6/ch23.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 compact 策略
- 不深入 agentTranscript

## 验收标准

场景: JSONL 存储路径说明
  测试: verify_jsonl_storage_path
  假设 读者想手动查看会话记录
  当 读者读完存储路径说明
  那么 章节展示 getTranscriptPath() 返回的路径格式（.claude/projects/{hash}/{sessionId}.jsonl），并说明 {hash} 的生成方式

场景: 追加写入设计原因说清
  测试: verify_append_write_rationale
  假设 读者追问"为什么用追加而不是每次覆写整个文件"
  那么 章节给出具体理由：追加写入不会丢失数据（崩溃安全）、减少写入量、便于增量读取

场景: 会话恢复查找逻辑说明
  测试: verify_resume_lookup_logic
  假设 用户执行 /resume 命令
  当 读者追踪查找逻辑
  那么 章节说明如何扫描 .claude/projects/ 目录、按时间排序、读取最近会话的机制

场景: 并发会话隔离说明
  测试: verify_concurrent_session_isolation
  假设 用户同时开了两个 Claude Code 窗口
  当 读者检查并发隔离机制
  那么 章节说明 SessionKind 枚举的四种类型（interactive/bg/daemon/daemon-worker），以及如何通过独立 JSONL 文件实现隔离

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 sessionStorage.ts 中的 getTranscriptPath
  那么 约第202行存在该函数，返回 join(projectDir, `${getSessionId()}.jsonl`)

场景: 会话文件超出大小限制时的处理
  测试: verify_transcript_size_limit_handling
  假设 长时间会话导致 JSONL 文件超过 MAX_TRANSCRIPT_READ_BYTES
  当 读者检查超出限制的处理
  那么 章节说明 MAX_TRANSCRIPT_READ_BYTES（50MB）的截断策略，以及对 /resume 功能的影响

## 排除范围

- 不深入 compact 压缩策略（第 24-25 章）
- 不分析 agentTranscript 子目录（第 31 章）
- 不覆盖 sessionIngress 远程会话接入（第 32 章 Swarm 范围）
