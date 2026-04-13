spec: task
name: "第26章：本地记忆系统——memdir 与 SessionMemory"
tags: [book-chapter, part-6]
---

## 意图

本章解析 Claude Code 的本地记忆机制。核心问题：memdir 如何组织和检索记忆文件？buildMemoryPrompt 如何将记忆内容注入到系统提示？SessionMemory 如何在会话内提炼和持久化记忆片段？

## 约束

必须：
- 引用 src/memdir/memdir.ts 中的 buildMemoryPrompt（约第272行）、loadMemoryPrompt（约第419行）、MAX_ENTRYPOINT_BYTES（约第38行）
- 引用 src/services/SessionMemory/sessionMemory.ts 中的 shouldExtractMemory（约第134行）和 initSessionMemory（约第357行）
- 解释 ENTRYPOINT_NAME（MEMORY.md）的作用：记忆目录的入口索引文件
- 说明记忆大小限制（MAX_ENTRYPOINT_BYTES = 25000 字节）的设计原因

禁止：
- 不得深入 extractMemories 的跨会话记忆提炼（第 34 章范围）
- 不得深入 teamMemorySync（第 34 章范围）
- 不得重复第 20 章的 CLAUDE.md 发现逻辑

## 已定决策

- 开篇问题："Claude Code 每次对话结束后，它'记住了什么'？下次打开时能想起来吗？"
- ASCII 目录树展示 .claude/memory/ 的结构
- 源码引用格式：`src/memdir/memdir.ts:行号`

## 边界

### 允许修改
- book/src/part6/ch26.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 extractMemories 跨会话提炼（第 34 章）

## 验收标准

场景: memdir 目录结构说明
  测试: verify_memdir_structure
  假设 读者想手动查看 Claude Code 存储的记忆
  当 读者读完目录结构说明
  那么 章节展示 .claude/memory/ 下 MEMORY.md 入口文件和子目录的组织方式，ASCII 图可视化

场景: buildMemoryPrompt 注入机制说明
  测试: verify_memory_prompt_injection
  假设 读者追问"记忆内容是怎么进入系统提示的"
  那么 章节解释 loadMemoryPrompt → buildMemoryPrompt 的调用链，说明记忆内容在系统提示中的插入位置

场景: 记忆大小限制说明
  测试: verify_memory_size_limit
  假设 用户积累了大量记忆导致超出限制
  当 读者检查大小限制机制
  那么 章节说明 MAX_ENTRYPOINT_BYTES（25000字节）的截断策略，以及 truncateEntrypointContent 的处理方式

场景: SessionMemory 触发条件说明
  测试: verify_session_memory_trigger
  假设 读者追问"什么时候会从会话中提炼记忆"
  那么 章节引用 shouldExtractMemory 的判断逻辑，说明触发条件（如对话长度、特定模式等）

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 memdir.ts 中的 loadMemoryPrompt
  那么 约第419行存在该函数的 async 定义

场景: 记忆文件损坏时的处理
  测试: verify_corrupt_memory_handling
  假设 MEMORY.md 文件内容格式损坏或不可读
  当 读者检查错误处理说明
  那么 章节说明记忆读取失败时的降级行为（忽略损坏记忆，继续正常对话）

## 排除范围

- 不深入 extractMemories 的会话末提炼（第 34 章）
- 不覆盖 teamMemorySync（第 34 章）
- 不重复 CLAUDE.md 发现逻辑（第 20 章）
