spec: task
name: "第9章：Query Engine——多轮编排与状态管理"
tags: [book-chapter, part-2]
---

## 意图

本章解析 QueryEngine：单轮 query.ts 的调用者和多轮会话的编排层。核心问题：多轮对话的上下文是如何累积的？abort 信号如何跨多轮传播？QueryEngine 和 REPL 之间如何协调？

## 约束

必须：
- 引用 src/QueryEngine.ts 中的 QueryEngine class（约第184行）和 QueryEngineConfig 类型（约第130行）
- 引用 createAbortController（src/utils/abortController.ts）在 QueryEngine 中的使用
- 绘制 Mermaid 序列图展示：REPL → QueryEngine → query.ts 的调用关系及 abort 传播
- 解释 fileStateCache 在多轮间的传递：保证工具读取文件的一致性

禁止：
- 不得重复第 8 章的单轮循环细节
- 不得深入 REPL 的 React 状态机（本章只描述接口，不深入 REPL 实现）
- 不得深入 compact 触发逻辑（第 24 章范围）

## 已定决策

- 开篇问题："query.ts 处理单轮，那谁来管多轮？上下文是怎么不断积累的？"
- Mermaid sequenceDiagram 展示多轮编排
- 源码引用格式：`src/QueryEngine.ts:行号`

## 边界

### 允许修改
- book/src/part2/ch09.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 REPL React 状态机实现

## 验收标准

场景: 多轮上下文累积机制说清
  测试: verify_multi_turn_context_accumulation
  假设 读者追问"第3轮对话时 LLM 能看到前两轮吗"
  当 读者读完上下文管理一节
  那么 能解释 messages 数组如何在每轮后追加，以及 compact boundary 如何截断历史（不深入 compact 实现）

场景: abort 信号传播路径说清
  测试: verify_abort_signal_propagation
  假设 用户按 Ctrl+C 中断对话
  当 读者追踪 abort 信号路径
  那么 章节说明信号从 REPL → QueryEngine.abort() → abortController → query.ts 的传播链

场景: QueryEngine 与 REPL 接口关系说明
  测试: verify_query_engine_repl_interface
  假设 读者想理解 QueryEngine 是如何被 REPL 驱动的
  那么 章节描述接口层面的交互（不深入 REPL 实现），包括 QueryEngine 的输入（用户消息）和输出（消息流）

场景: fileStateCache 跨轮传递说明
  测试: verify_file_state_cache_explained
  假设 读者追问"两轮之间文件状态是否保持一致"
  那么 章节说明 fileStateCache 在 QueryEngine 中的传递方式及其目的

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 src/QueryEngine.ts 中的 QueryEngine class
  那么 约第184行存在 class QueryEngine 定义

场景: 不越界重复第8章
  测试: verify_no_single_turn_deep_dive
  假设 读者检查单轮循环相关段落
  当 读者搜索 tool_use 识别逻辑的详细描述
  那么 最多一句提及并有"详见第 8 章"指引，不重复展开

## 排除范围

- 不重复 query.ts 的单轮循环细节（第 8 章）
- 不深入 REPL React 组件的状态管理
- 不分析 compact 触发逻辑（第 24 章）
- 不覆盖 headless/SDK 模式下的 QueryEngine 用法（第 23 章会话系统范围）
