spec: task
name: "第16章：YOLO 模式与 AI 分类器"
tags: [book-chapter, part-4]
---

## 意图

本章解析 AI 分类器的实现——用 LLM 判断 LLM 的操作是否安全。核心问题：递归调用如何避免？AutoModeRules 的三区域结构是什么？dangerousPatterns 黑名单与分类器如何互补？

## 约束

必须：
- 引用 src/utils/permissions/yoloClassifier.ts 中的 AutoModeRules（约第85行）、buildYoloSystemPrompt（约第484行）、YOLO_CLASSIFIER_TOOL_NAME（约第260行）
- 引用 src/utils/permissions/dangerousPatterns.ts 展示黑名单的代表性危险模式
- 说明递归调用问题的解决方案（sideQuery/独立路径）
- 解释 buildTranscriptForClassifier（约第434行）：对话历史如何序列化为分类器输入

禁止：
- 不得重复第 15 章的三层决策架构
- 不得深入规则引擎逻辑（第 17 章范围）

## 已定决策

- 开篇："谁来判断 AI 的行为是否安全？另一个 AI——但这不会导致无限递归吗？"
- 源码引用格式：`src/utils/permissions/yoloClassifier.ts:行号`

## 边界

### 允许修改
- book/src/part4/ch16.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件

## 验收标准

场景: 递归调用问题解决方案说清
  测试: verify_recursive_call_solution
  假设 读者追问"分类器调用 LLM，那 LLM 调用的工具还需要分类器判断吗"
  那么 章节解释分类器使用独立路径，避免递归

场景: AutoModeRules 三区域说明
  测试: verify_auto_mode_rules_structure
  假设 读者阅读 AutoModeRules 结构
  那么 章节解释 allow/soft_deny/environment 三个区域的用途

场景: dangerousPatterns 与分类器互补关系说明
  测试: verify_dangerous_patterns_complementary
  假设 读者追问有了 AI 分类器为什么还需要 dangerousPatterns 黑名单
  那么 章节解释黑名单零延迟同步拦截，分类器处理模糊场景

场景: 分类器结果结构说明
  测试: verify_classifier_output_structure
  假设 读者追问分类器返回什么格式
  那么 章节引用 YOLO_CLASSIFIER_TOOL_NAME 展示输出结构

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 yoloClassifier.ts 中的 YOLO_CLASSIFIER_TOOL_NAME
  那么 约第260行存在该常量定义

场景: 分类器失败降级
  测试: verify_classifier_failure_fallback
  假设 分类器 LLM 调用超时或返回无法解析的结果
  当 读者检查错误处理
  那么 章节说明失败时回退到用户交互层

## 排除范围

- 不重复三层决策架构（第 15 章）
- 不深入规则引擎的匹配算法（第 17 章）
