spec: task
name: "第24章：缓存系统——Prompt Cache 与 Context 压缩四策略"
tags: [book-chapter, part-6]
---

## 意图

本章解析 Claude Code 的上下文管理策略总览。核心问题：Anthropic prompt cache 如何被利用？AutoCompact/ReactiveCompact/MicroCompact/SnipCompact 四种策略各自的触发条件和适用场景是什么？如何选择合适的策略？

## 约束

必须：
- 引用 src/services/compact/autoCompact.ts 中的 AUTOCOMPACT_BUFFER_TOKENS（约第62行）、isAutoCompactEnabled（约第147行）
- 引用 src/services/compact/ 目录下的四个核心文件：autoCompact.ts、reactiveCompact.ts、microCompact.ts、snipCompact.ts
- 用对比表展示四种策略：触发条件、压缩粒度、对话历史损失程度、适用场景
- 解释 prompt cache 的"cache-key 前缀稳定性"要求：为什么频繁变化上下文会降低缓存命中率

禁止：
- 不得深入 AutoCompact 的具体实现（第 25 章范围）
- 不得深入 compact boundary 标记机制（第 25 章范围）
- 不得深入会话持久化（第 23 章范围）

## 已定决策

- 开篇问题："对话越来越长，Claude Code 是怎么防止 context window 溢出的？有几种方案？"
- 对比表展示四种策略的维度对比
- 源码引用格式：`src/services/compact/autoCompact.ts:行号`

## 边界

### 允许修改
- book/src/part6/ch24.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 AutoCompact 具体算法（第 25 章）

## 验收标准

场景: 四种策略对比表完整
  测试: verify_four_strategy_comparison_table
  假设 读者想为自己的场景选择合适策略
  当 读者查看对比表
  那么 表格包含至少四个维度（触发条件、压缩粒度、历史损失、适用场景），四种策略各有一行，每行有具体描述而非泛泛而谈

场景: prompt cache 稳定性说明
  测试: verify_prompt_cache_stability
  假设 读者追问"为什么要保持 cache-key 前缀稳定"
  那么 章节解释：Anthropic prompt cache 按前缀复用，前缀不变则后续 token 走缓存（节省费用），频繁变化上下文会破坏缓存命中，导致重复计费

场景: AUTOCOMPACT_BUFFER_TOKENS 含义说明
  测试: verify_buffer_tokens_explained
  假设 读者追问"为什么不在 context window 完全满时才压缩"
  那么 章节解释 AUTOCOMPACT_BUFFER_TOKENS（13000 tokens）是预留缓冲区，确保压缩操作本身有足够空间执行

场景: 四种策略触发条件说清
  测试: verify_strategy_trigger_conditions
  假设 读者想知道何时会触发 MicroCompact vs AutoCompact
  那么 章节分别描述四种策略的触发条件：AutoCompact（token 达阈值）、ReactiveCompact（feature flag + 响应式）、MicroCompact（单工具结果超限）、SnipCompact（手动或特定条件）

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 autoCompact.ts 中的 AUTOCOMPACT_BUFFER_TOKENS
  那么 约第62行存在该常量，值为 13000

场景: 压缩失败时的降级
  测试: verify_compact_failure_handling
  假设 压缩过程中发生错误（如 API 调用失败）
  当 读者检查失败处理说明
  那么 章节说明压缩失败时的降级行为（保留原始历史继续对话 or 抛出错误）

## 排除范围

- 不深入 AutoCompact 的 compact boundary 标记（第 25 章）
- 不深入 SnipCompact 的 snip projection 算法（第 25 章）
- 不覆盖 sessionMemoryCompact（第 26 章记忆系统范围）
