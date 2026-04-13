spec: task
name: "第12章：BashTool 解剖——最复杂工具的实现"
tags: [book-chapter, part-3]
---

## 意图

本章深度解剖 BashTool——代码库中最复杂的单个工具。核心问题：一条 bash 命令从输入到输出经历了哪些处理阶段？命令语义分类如何影响 UI 展示？沙箱路由如何决定？输出超长时如何截断？

## 约束

必须：
- 引用 src/tools/BashTool/BashTool.tsx 中的 BASH_SEARCH_COMMANDS、BASH_READ_COMMANDS 集合定义（约第60-72行）
- 引用 shouldUseSandbox（src/tools/BashTool/shouldUseSandbox.ts）的路由逻辑
- 引用 parseSedEditCommand（src/tools/BashTool/sedEditParser.ts）说明 sed 命令的特殊处理
- 绘制 BashTool 处理流程的 Mermaid 图

禁止：
- 不得重复第 11 章的 Tool 接口概念
- 不得深入沙箱的底层实现
- 不得覆盖权限检查逻辑（第 15 章范围）

## 已定决策

- 开篇问题："同样是执行命令，为什么 cat file.txt 在 UI 里折叠显示，而 rm -rf 触发警告？"
- Mermaid flowchart 展示完整处理流程
- 源码引用格式：`src/tools/BashTool/BashTool.tsx:行号`

## 边界

### 允许修改
- book/src/part3/ch12.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 SandboxManager 内部实现

## 验收标准

场景: 命令语义分类覆盖三类
  测试: verify_semantic_classification_three_types
  假设 读者阅读语义分类一节
  当 读者查看三类命令集合
  那么 章节展示 BASH_SEARCH_COMMANDS、BASH_READ_COMMANDS、BASH_LIST_COMMANDS 三个集合

场景: 沙箱路由逻辑说清
  测试: verify_sandbox_routing_explained
  假设 读者追问"哪些命令会进沙箱"
  那么 章节引用 shouldUseSandbox 并说明触发条件

场景: sed 命令特殊处理说明
  测试: verify_sed_special_handling
  假设 读者追问"为什么 sed 命令有单独的解析器"
  那么 章节解释 parseSedEditCommand 的原因

场景: 输出截断机制说明
  测试: verify_output_truncation_explained
  假设 命令输出超过大小限制
  当 读者追踪超长输出的处理路径
  那么 章节说明输出被持久化到磁盘并返回预览路径的机制

场景: 处理流程图完整
  测试: verify_processing_flowchart_complete
  假设 读者阅读 Mermaid 流程图
  当 读者追踪一条命令的完整路径
  那么 图中包含语义分类、沙箱路由、执行、输出处理

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 BashTool.tsx 中的 BASH_SEARCH_COMMANDS 定义
  那么 约第60行存在该 Set 定义

## 排除范围

- 不深入 SandboxManager 的沙箱隔离实现
- 不分析权限检查流程（第 15 章）
- 不覆盖后台任务化机制（第 30 章 Swarm Task 范围）
