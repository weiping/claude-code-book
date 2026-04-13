spec: task
name: "第5章：Bootstrap 全局状态——进程的状态脊梁"
tags: [book-chapter, part-1]
---

## 意图

本章解析 Claude Code 的全局状态管理方案。核心问题：为什么把 50+ 个状态变量集中在一个模块里？这种"反模式"背后有什么工程理由？OpenTelemetry 指标为什么嵌入状态而非独立服务？

## 约束

必须：
- 引用 src/bootstrap/state.ts 中的 State 类型定义（type State，约第45行）
- 展示 State 的关键字段分组：会话标识（sessionId、originalCwd）、成本追踪（totalCostUSD）、模型配置（mainLoopModelOverride）、遥测（meter、sessionCounter）
- 解释"bootstrap-isolation"注释的含义：为什么这个模块不允许被其他模块循环导入
- 说明 createSignal 在状态变化通知中的作用

禁止：
- 不得深入 OpenTelemetry SDK 的配置细节
- 不得分析每一个状态变量（选最有代表性的 6-8 个）
- 不得重复第3章的启动时序内容

## 已定决策

- 开篇问题："为什么要把进程的全部状态放进一个全局对象？这不是反模式吗？"
- 用分组表格展示 State 的字段分类
- 源码引用格式：`src/bootstrap/state.ts:行号`

## 边界

### 允许修改
- book/src/part1/ch05.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 OpenTelemetry SDK 配置

## 验收标准

场景: State 类型关键字段有分组展示
  测试: verify_state_fields_grouped
  假设 读者阅读状态字段说明
  当 读者查看分组表格
  那么 至少展示会话标识、成本追踪、模型配置、遥测四个分组，每组有 1-2 个代表性字段名

场景: 单一来源设计理由说清
  测试: verify_single_source_rationale
  假设 读者质疑"全局状态是反模式"
  当 读者读完设计权衡一节
  那么 章节给出至少两个"集中比分散更合适"的具体理由（如：避免在每个工具函数中传递上下文、便于跨模块的会话级计量）

场景: bootstrap-isolation 规则解释清晰
  测试: verify_bootstrap_isolation_explained
  假设 读者看到源码中的 eslint 自定义规则 bootstrap-isolation
  当 读者读完这一节
  那么 能解释该规则禁止哪类导入，以及为什么违反会造成循环依赖

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 src/bootstrap/state.ts 中 type State 的定义
  那么 引用行号指向真实的 State 类型定义

场景: OpenTelemetry 嵌入设计说明
  测试: verify_otel_embedded_rationale
  假设 读者追问"为什么 meter、sessionCounter 等遥测对象在 State 里"
  那么 章节有说明：嵌入 State 保证遥测与会话生命周期对齐，避免单独初始化的时序问题

场景: 字段数量适当
  测试: verify_field_count_appropriate
  假设 读者检查章节覆盖的字段数量
  当 读者统计详细分析的字段
  那么 详细分析的字段不超过 10 个（避免流水账），其余以"（还有 N 个相关字段）"概括

## 排除范围

- 不深入 OpenTelemetry SDK 的 exporter 配置
- 不覆盖会话持久化逻辑（第 23 章范围）
- 不分析 AppState（REPL 层状态，与 bootstrap state 不同）
