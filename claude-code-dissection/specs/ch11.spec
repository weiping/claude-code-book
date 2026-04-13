spec: task
name: "第11章：Tool 接口与 buildTool 工厂"
tags: [book-chapter, part-3]
---

## 意图

本章解析 Claude Code 工具系统的核心抽象。核心问题：Tool 接口定义了哪些职责？buildTool 工厂填充了什么默认实现？isReadOnly/isDestructive/interruptBehavior 三元安全模型如何保护用户？

## 约束

必须：
- 引用 src/Tool.ts 中的 Tool 类型定义（约第362行）和 buildTool 函数（约第783行）
- 引用 TOOL_DEFAULTS（约第757行）展示工厂默认填充的方法
- 解释安全三元模型：isReadOnly/isDestructive/interruptBehavior
- 用代码片段（不超过 25 行）展示一个最小 ToolDef 示例

禁止：
- 不得深入具体工具实现（第 12-14 章范围）
- 不得深入权限决策流程（第 15 章范围）

## 已定决策

- 开篇问题："BashTool、FileReadTool、MCPTool——它们形态各异，是什么让它们都能被 query.ts 统一调用？"
- 用表格展示 Tool 接口的核心方法分组
- 源码引用格式：`src/Tool.ts:行号`

## 边界

### 允许修改
- book/src/part3/ch11.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入具体工具实现

## 验收标准

场景: Tool 接口方法分组清晰
  测试: verify_tool_interface_grouped
  假设 读者想实现一个新工具
  当 读者查看 Tool 接口方法表格
  那么 表格将方法分为核心必须实现和可选覆盖两组

场景: 安全三元模型解释正确
  测试: verify_safety_triad_explained
  假设 读者追问"为什么不是简单的 allowed/denied 两态"
  那么 章节解释三元模型中每个维度的语义

场景: buildTool 工厂作用说清
  测试: verify_build_tool_factory_role
  假设 读者追问"ToolDef 和 Tool 有什么区别"
  那么 章节解释 buildTool 将 ToolDef 转换为完整 Tool

场景: 最小 ToolDef 示例可运行
  测试: verify_minimal_tooldef_example
  假设 读者按照示例实现一个最小工具
  当 读者检查示例代码
  那么 示例包含 name/description/inputSchema/call 四个必须字段，不超过 25 行

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 src/Tool.ts 中的 buildTool 函数
  那么 约第783行存在 export function buildTool 定义

场景: 越界到具体工具时有指引
  测试: verify_cross_chapter_references
  假设 读者在阅读时想了解 BashTool 的具体实现
  那么 章节有"详见第 12 章"指引，不展开 BashTool 内部逻辑

## 排除范围

- 不深入 BashTool、AgentTool 等具体工具实现（第 12-13 章）
- 不覆盖 MCP 工具的特殊处理（第 27 章）
- 不分析权限决策流程（第 15 章）
