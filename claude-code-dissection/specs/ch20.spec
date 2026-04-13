spec: task
name: "第20章：CLAUDE.md 的发现、解析与注入"
tags: [book-chapter, part-5]
---

## 意图

本章解析 CLAUDE.md 文件的完整生命周期。核心问题：Claude Code 如何在目录层级中发现 CLAUDE.md？三种记忆类型（Managed/User/Project）的路径规则是什么？发现后如何缓存和注入系统提示？

## 约束

必须：
- 引用 src/utils/claudemd.ts 中的 getMemoryFiles 函数（约第790行）和文件头部的三种记忆类型注释（约第4-16行）
- 引用 isClaudeMdExcluded（约第540行）说明排除机制
- 解释三种路径：Managed（/etc/claude-code/CLAUDE.md）、User（~/.claude/CLAUDE.md）、Project（项目根 CLAUDE.md 及 .claude/rules/*.md）
- 说明 memoize 缓存策略：何时缓存失效（setSystemPromptInjection 调用时清除）

禁止：
- 不得深入系统提示的优先级堆叠（第 19 章范围）
- 不得深入记忆系统的 findRelevantMemories（第 26 章范围）
- 不得深入 teamMem 团队记忆路径（第 34 章范围）

## 已定决策

- 开篇问题："CLAUDE.md 文件放在 /etc、~/.claude、还是项目目录，有什么区别？"
- ASCII 目录树展示三种路径的优先级和作用范围
- 源码引用格式：`src/utils/claudemd.ts:行号`

## 边界

### 允许修改
- book/src/part5/ch20.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 findRelevantMemories（第 26 章）

## 验收标准

场景: 三种路径说明完整
  测试: verify_three_path_types
  假设 读者想在不同层级放置指令
  当 读者查看三种路径说明
  那么 章节展示 Managed/User/Project 三个路径的具体位置、优先级顺序、作用范围（全局/用户/项目）

场景: 目录层级遍历逻辑说明
  测试: verify_directory_traversal
  假设 读者的项目在 /home/user/projects/myapp
  当 读者追问"Claude Code 会查找哪些目录的 CLAUDE.md"
  那么 章节解释从当前工作目录向上遍历到项目根的扫描逻辑，并引用 getMemoryFiles 中的实现

场景: 排除机制说明
  测试: verify_exclusion_mechanism
  假设 读者想排除某个 CLAUDE.md 文件
  当 读者读完排除机制一节
  那么 能理解 claudeMdExcludes 配置项和 isClaudeMdExcluded 的工作方式

场景: 缓存失效条件说明
  测试: verify_cache_invalidation
  假设 读者在会话中修改了 CLAUDE.md
  当 读者检查缓存更新机制
  那么 章节说明 memoize 缓存的失效条件，以及 setSystemPromptInjection 如何触发 cache.clear()

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 claudemd.ts 中的 getMemoryFiles
  那么 约第790行存在 export const getMemoryFiles = memoize(...) 定义

场景: .claude/rules 目录说明
  测试: verify_rules_directory_explained
  假设 读者想组织多个规则文件
  当 读者读完 .claude/rules/ 目录说明
  那么 章节解释 .claude/rules/*.md 文件如何被自动扫描并合并到 Project 记忆中

## 排除范围

- 不深入系统提示优先级堆叠（第 19 章）
- 不深入 findRelevantMemories 语义检索（第 26 章）
- 不覆盖 teamMem 路径（第 34 章）
