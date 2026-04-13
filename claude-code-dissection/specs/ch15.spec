spec: task
name: "第15章：权限系统的三层决策架构"
tags: [book-chapter, part-4]
---

## 意图

本章解析权限决策的整体架构。核心问题：allow/deny/ask/passthrough 四种结果各代表什么？规则引擎/AI 分类器/用户交互三层的触发条件和性能差异是什么？分类器不可用时如何降级？

## 约束

必须：
- 引用 src/utils/permissions/permissions.ts 中的 getAllowRules/getDenyRules/getAskRules（约第122-227行）
- 引用 src/utils/permissions/PermissionResult.ts 中的四种结果类型
- 绘制三层决策的 Mermaid 流程图：规则引擎快速路径 → AI 分类器中路 → 用户交互慢路
- 量化三层的典型延迟差异

禁止：
- 不得深入 YOLO 分类器实现（第 16 章范围）
- 不得深入规则解析逻辑（第 17 章范围）

## 已定决策

- 开篇："`rm -rf /tmp/test` 执行时，系统经过多少次判断才决定拦不拦截？"
- 源码引用格式：`src/utils/permissions/permissions.ts:行号`

## 边界

### 允许修改
- book/src/part4/ch15.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件

## 验收标准

场景: 三层决策路径图正确
  测试: verify_three_layer_flowchart
  假设 读者阅读 Mermaid 流程图
  当 读者追踪一个危险命令的决策路径
  那么 图中依次经过规则引擎→AI分类器→用户交互，三层有明确进入条件

场景: 四种权限结果语义清晰
  测试: verify_four_permission_results
  假设 读者阅读 PermissionResult 类型说明
  当 读者查看四种结果定义
  那么 章节解释 allow/deny/ask/passthrough 的语义差异

场景: 三层延迟量化有说明
  测试: verify_latency_quantification
  假设 读者追问三层的性能开销差多少
  那么 章节给出各层的典型延迟量级

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 permissions.ts 中的 getAllowRules
  那么 约第122行存在该函数定义

场景: 三层权衡说明充分
  测试: verify_tradeoff_explained
  假设 读者追问为什么不只用 AI 分类器一层
  那么 章节给出具体权衡

场景: 分类器失败时的降级
  测试: verify_classifier_failure_fallback
  假设 AI 分类器 API 调用失败
  当 读者检查降级策略
  那么 章节说明失败时回退到用户交互层

## 排除范围

- 不深入 YOLO 分类器的 prompt 设计（第 16 章）
- 不深入规则解析语法（第 17 章）
