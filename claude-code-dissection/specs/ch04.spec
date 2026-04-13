spec: task
name: "第4章：Feature Flag 的双层架构"
tags: [book-chapter, part-1]
---

## 意图

本章解析 Claude Code 的功能开关体系。核心问题：为什么一个产品需要 60+ 个 feature flag？编译期消除和运行期 A/B 的分工边界在哪里？这套机制如何支撑"同一代码库服务不同用户群"的目标？

## 约束

必须：
- 引用 src/main.tsx 中至少 3 处 feature() 调用（如 KAIROS、COORDINATOR_MODE、TRANSCRIPT_CLASSIFIER）
- 引用 src/services/analytics/growthbook.ts 中的 initializeGrowthBook 或 checkGate_CACHED_OR_BLOCKING
- 用对比表展示两层 flag 的差异（编译期 vs 运行期：触发时机、修改成本、影响范围）
- 给出 flag 的 4 种分类示例：已发布功能、实验特性、内部测试、死亡开关

禁止：
- 不得列举全部 60+ flag（附录 B 的范围）
- 不得深入 GrowthBook 实验配置的数据格式
- 不得分析 stub 模块（KAIROS 等）的实现内容

## 已定决策

- 开篇问题："普通用户安装的 claude 命令和 Anthropic 内部员工用的，是同一个二进制吗？"
- ASCII 或 Markdown 表格展示两层 flag 对比
- 源码引用格式：`src/main.tsx:行号`

## 边界

### 允许修改
- book/src/part1/ch04.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 GrowthBook 实验配置格式
- 不分析 stub 模块实现

## 验收标准

场景: 编译期消除语义正确
  测试: verify_compile_time_elimination_semantics
  假设 读者熟悉 webpack tree-shaking
  当 读者读完编译期 feature() 一节
  那么 能解释 feature('KAIROS') 在 Bun 构建时返回 false 导致整个 require 分支从产物中物理删除，不是运行时跳过

场景: 双层对比表可读
  测试: verify_two_layer_comparison_table
  假设 读者阅读对比表
  当 读者比对两行（编译期 vs 运行期）
  那么 表格包含触发时机、修改是否需重新发布、对外部用户是否可见三个维度

场景: flag 分类有真实示例
  测试: verify_flag_categories_have_examples
  假设 读者想了解不同类型 flag 的实际用途
  当 读者阅读分类说明
  那么 每类至少有一个真实 flag 名称（如 TRANSCRIPT_CLASSIFIER、VOICE_MODE、BREAK_CACHE_COMMAND），且名称可在源码中 grep 验证

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找引用的 main.tsx 行号
  那么 引用行存在 feature() 调用，上下文与描述一致

场景: 设计权衡有说明
  测试: verify_tradeoff_explained
  假设 读者问"为什么不全用运行期 flag"
  那么 章节给出编译期 flag 的三个优势：产物体积减小、内部代码不泄露给外部用户、消除运行时分支判断

场景: 不泄露 stub 模块实现
  测试: verify_stub_not_analyzed
  假设 读者检查 KAIROS 相关段落
  当 读者搜索 src/assistant/ 的实现分析
  那么 章节只提 KAIROS 是通过 feature flag 门控的条件特性，不分析其内部实现

## 排除范围

- 不列举全部 60+ flag（见附录 B）
- 不分析 GrowthBook A/B 实验的 JSON 配置格式
- 不分析 src/assistant/ 等 stub 模块的实现
