spec: task
name: "第3章：启动流水线的并发艺术"
tags: [book-chapter, part-1]
---

## 意图

本章解析 Claude Code 冷启动路径上的并发优化策略。核心问题：一个 CLI 工具为什么要在模块加载期间就触发异步任务？这些并发操作节省了多少时间，又引入了什么复杂度？

## 约束

必须：
- 引用 src/main.tsx:12（profileCheckpoint 调用）、src/utils/startupProfiler.ts、src/utils/settings/mdm/rawRead.ts、src/utils/secureStorage/keychainPrefetch.ts
- 绘制 Mermaid sequenceDiagram 展示三路任务与模块加载的并行关系
- 量化说明代码注释中给出的延迟数字（Keychain 约 65ms，模块加载约 135ms）
- 解释"为什么在 import 副作用中而非 main 函数中触发任务"的设计原因

禁止：
- 不得深入 MDM 配置内容（只分析触发时机，不分析策略本身）
- 不得深入 Keychain 存储加密格式
- 不得重复第 5 章的 Bootstrap State 初始化内容

## 已定决策

- 开篇问题："为什么 src/main.tsx 的前三行是副作用，而不是函数体内的调用？"
- 时序图用 Mermaid sequenceDiagram
- 源码引用格式：`src/main.tsx:行号`

## 边界

### 允许修改
- book/src/part1/ch03.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 MDM 策略内容（plutil/reg query 的业务含义）
- 不深入 OAuth token 加密存储细节

## 验收标准

场景: 时序图展示并行关系
  测试: verify_sequence_diagram_shows_parallelism
  假设 读者阅读 Mermaid 时序图
  当 读者跟踪模块加载与三路任务的时间线
  那么 图中清楚展示 profileCheckpoint、startMdmRawRead、startKeychainPrefetch 三个调用在 import 语句之间发生，三路任务与后续模块加载并行

场景: 副作用 import 设计意图说清
  测试: verify_import_sideeffect_rationale
  假设 读者看到 main.tsx 开头的 eslint-disable-no-top-level-side-effects 注释
  当 读者读完这一节
  那么 能解释"在 import 时机而非函数调用触发"的具体工程原因（模块求值时机保证）

场景: 延迟数字有量化
  测试: verify_latency_numbers_cited
  假设 读者想知道优化实际节省多少时间
  那么 章节给出 CLAUDE.md 注释中的具体数字（65ms Keychain，135ms 并行窗口）并标注来源

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 src/main.tsx:12
  那么 该行是 profileCheckpoint('main_tsx_entry') 调用

场景: 设计风险有说明
  测试: verify_design_risks_acknowledged
  假设 读者问"这种 import 副作用模式有什么风险"
  那么 章节说明潜在风险（测试隔离困难、顺序依赖）及其为何被接受

场景: 不越界进入 Bootstrap State
  测试: verify_no_bootstrap_state_deep_dive
  假设 读者检查是否有 state.ts 内部函数分析
  当 读者搜索 bootstrap/state 相关段落
  那么 最多提及 Bootstrap State 作为后续步骤，有"详见第 5 章"指引，不展开内部实现

## 排除范围

- 不分析 MDM 策略内容
- 不分析 OAuth token 的加密存储机制（第 28 章 MCP 认证范围）
- 不覆盖 Bootstrap State 初始化（第 5 章）
