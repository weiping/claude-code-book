spec: task
name: "第8章：query.ts——单轮对话的原子循环"
tags: [book-chapter, part-2]
---

## 意图

本章解析 query.ts 这个全书最核心的函数：一次 LLM 调用的完整原子单元。核心问题：流式 token 是如何被消费的？tool_use 块何时被识别？工具执行和 token 流是串行还是并行？FallbackTriggeredError 触发什么？

## 约束

必须：
- 引用 src/query.ts 中的 query 函数签名（约第219行）和 QueryParams 类型（约第181行）
- 引用 FallbackTriggeredError（src/services/api/withRetry.ts）的用途
- 绘制 Mermaid 流程图展示单轮循环：stream_request_start → token 流 → tool_use 识别 → 工具执行 → tool_result 回填 → 循环结束判断
- 说明 streamingToolExecution（约第561行）的设计：streaming 期间并发执行工具 vs 等待 stream 结束

禁止：
- 不得深入具体工具的执行逻辑（第 11-14 章范围）
- 不得深入 QueryEngine 的多轮编排（第 9 章范围）
- 不得深入 compact 相关逻辑（第 24-25 章范围）

## 已定决策

- 开篇问题："query.ts 的函数签名是 async function*——为什么用 generator 而不是普通 async？"
- 核心流程用 Mermaid flowchart 展示
- 源码引用格式：`src/query.ts:行号`

## 边界

### 允许修改
- book/src/part2/ch08.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入具体工具执行逻辑
- 不深入 compact 策略

## 验收标准

场景: generator 函数设计原因说清
  测试: verify_generator_rationale
  假设 读者熟悉 async/await 但不熟悉 async generator
  当 读者读完"为什么用 generator"一节
  那么 能解释：generator 让调用方（QueryEngine）可以在每个 yield 点处理中间结果（如进度更新），同时保持流的连续性

场景: 单轮循环流程图正确
  测试: verify_single_turn_flowchart
  假设 读者阅读 Mermaid 流程图
  当 读者追踪一次包含工具调用的完整循环
  那么 图中包含：流式接收 → tool_use 块识别 → 工具并发执行 → tool_result 构建 → 回填消息 → 判断是否继续

场景: streamingToolExecution 设计权衡说明
  测试: verify_streaming_tool_execution_tradeoff
  假设 读者追问"为什么工具可以在 stream 期间执行"
  那么 章节说明并发执行的性能收益（减少等待）和风险（工具结果可能与后续 token 交错），并引用源码行号

场景: FallbackTriggeredError 作用说明
  测试: verify_fallback_error_explained
  假设 读者看到 FallbackTriggeredError 被 catch
  那么 章节解释该异常触发重试或降级的场景

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 src/query.ts 中 query 函数
  那么 约第219行存在 async function* query 定义，QueryParams 类型约在第181行

场景: 循环终止条件说明
  测试: verify_loop_termination_explained
  假设 读者追问"什么时候循环停止"
  那么 章节说明终止条件：stop_reason 非 tool_use、abort 信号触发、工具执行失败等

## 排除范围

- 不深入具体工具（BashTool 等）的实现（第 11-14 章）
- 不深入 QueryEngine 的多轮状态管理（第 9 章）
- 不分析 compact 触发逻辑（第 24-25 章）
- 不深入 thinking blocks 的处理（第 33 章）
