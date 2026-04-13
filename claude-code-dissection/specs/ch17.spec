spec: task
name: "第17章：PermissionRule 与规则引擎"
tags: [book-chapter, part-4]
---

## 意图

本章解析权限规则的数据模型和匹配机制。核心问题：规则来源（global/local/managed）优先级如何确定？shadowedRuleDetection 解决什么问题？permissionRuleValueFromString 的解析语法是什么？

## 约束

必须：
- 引用 src/utils/permissions/PermissionRule.ts 中的 PermissionRule 和 PermissionBehavior 类型
- 引用 src/utils/permissions/permissionRuleParser.ts 中的 permissionRuleValueFromString（约第93行）
- 引用 src/utils/permissions/shadowedRuleDetection.ts 中的 detectUnreachableRules（约第193行）
- 解释三种规则来源优先级：managed > global > local

禁止：
- 不得重复第 15 章的三层决策架构
- 不得深入 YOLO 分类器（第 16 章范围）

## 已定决策

- 开篇："用户说'允许所有 git 命令'，这条规则存在哪里？格式是什么？企业管控能覆盖它吗？"
- 源码引用格式：`src/utils/permissions/permissionRuleParser.ts:行号`

## 边界

### 允许修改
- book/src/part4/ch17.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件

## 验收标准

场景: 规则数据结构说明清晰
  测试: verify_rule_data_structure
  假设 读者想创建一条自定义权限规则
  那么 章节展示规则的关键字段和格式

场景: 规则来源优先级说明
  测试: verify_rule_source_priority
  假设 读者追问企业管控规则和用户自定义规则冲突时谁赢
  那么 章节解释 managed > global > local 的优先级

场景: shadowedRule 检测说明
  测试: verify_shadowed_rule_detection
  假设 用户添加了一条规则被更高优先级规则覆盖
  当 读者读完 shadowed rule 检测
  那么 能理解 detectUnreachableRules 如何发现被遮蔽的规则

场景: 通配符匹配规则说明
  测试: verify_wildcard_matching_explained
  假设 读者想写一条匹配所有 git 子命令的规则
  那么 章节说明通配符语法及匹配规则

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 permissionRuleParser.ts 中的 permissionRuleValueFromString
  那么 约第93行存在该函数

场景: 无效规则格式处理
  测试: verify_invalid_rule_format_handling
  假设 用户配置了格式错误的权限规则
  那么 章节说明解析失败时的行为

## 排除范围

- 不重复三层决策架构（第 15 章）
- 不深入 YOLO 分类器（第 16 章）
