spec: task
name: "第13章：AgentTool——递归智能体的工具接口"
tags: [book-chapter, part-3]
---

## 意图

本章解析 AgentTool 作为工具接口层的职责。核心问题：AgentTool 的输入 schema 如何设计？subagent_type 缺省时发生什么？built-in agents 如何注册和被选择？AgentTool 与第 31 章（Subagent 生命周期）的边界在哪里？

## 约束

必须：
- 引用 src/tools/AgentTool/AgentTool.tsx 中的 AgentTool 定义（约第196行）和 subagent_type schema（约第85行）
- 引用 src/tools/AgentTool/built-in/ 目录，展示内置 Agent 的结构
- 引用 src/tools/AgentTool/builtInAgents.ts 中的 getBuiltInAgents
- 解释 AgentTool 作为"工具接口层"与 runAgent.ts"执行层"的分工

禁止：
- 不得深入 runAgent.ts 的执行循环（第 31 章范围）
- 不得深入 forkSubagent 机制（第 31 章范围）
- 不得重复第 11 章的 buildTool 通用机制

## 已定决策

- 开篇问题："AgentTool 是一个工具，但它启动的是另一个完整的 Claude 实例——这层抽象的边界在哪里？"
- 用对比表展示 AgentTool（接口层）vs runAgent（执行层）的职责划分
- 源码引用格式：`src/tools/AgentTool/AgentTool.tsx:行号`

## 边界

### 允许修改
- book/src/part3/ch13.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 runAgent.ts 执行循环（第 31 章）

## 验收标准

场景: subagent_type 可选设计说清
  测试: verify_subagent_type_optional_design
  假设 读者追问"subagent_type 为什么是可选的"
  那么 章节解释缺省时默认使用 generalPurposeAgent

场景: built-in agents 注册机制说明
  测试: verify_builtin_agents_registration
  假设 读者想添加一个新的内置 Agent 类型
  当 读者读完注册机制
  那么 能理解需要在 built-in/ 目录下添加定义并注册

场景: 接口层与执行层职责对比清晰
  测试: verify_interface_vs_execution_separation
  假设 读者阅读对比表
  那么 表格清晰展示 AgentTool 负责输入验证/权限/调度，runAgent 负责对话循环

场景: 颜色标识分配说明
  测试: verify_color_assignment_explained
  假设 读者追问"多个子 Agent 并行时如何区分"
  那么 章节提及 agentColorManager 的颜色分配机制

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 AgentTool.tsx 中的 AgentTool 定义
  那么 约第196行存在 export const AgentTool = buildTool({...}) 的定义

场景: 不越界进入执行层
  测试: verify_no_execution_layer_deep_dive
  假设 读者检查 runAgent 相关段落
  那么 章节不展开 runAgent 的对话循环实现，有"详见第 31 章"指引

## 排除范围

- 不深入 runAgent.ts 的对话循环（第 31 章）
- 不深入 forkSubagent 的上下文继承机制（第 31 章）
