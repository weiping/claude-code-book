spec: task
name: "第14章：工具注册与条件加载"
tags: [book-chapter, part-3]
---

## 意图

本章解析工具集的动态组装机制。核心问题：getAllBaseTools() 如何根据环境动态决定工具集？MCP 工具何时插入集合？assembleToolPool 如何将基础工具和 MCP 工具合并为最终工具池？

## 约束

必须：
- 引用 src/tools.ts 中的 getAllBaseTools（约第196行）展示条件展开逻辑
- 引用 src/tools.ts 中的 assembleToolPool（约第345行）展示 MCP 工具合并
- 引用条件加载的代表性 feature flag 用法（process.env.USER_TYPE === 'ant'，约第214-215行）
- 绘制工具集四个来源的组装图

禁止：
- 不得深入具体工具实现（第 11-13 章范围）
- 不得深入 MCP 协议层（第 27 章范围）

## 已定决策

- 开篇：揭示"工具集不是静态列表，而是运行时动态组装的"这一核心事实
- 源码引用格式：`src/tools.ts:行号`

## 边界

### 允许修改
- book/src/part3/ch14.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件

## 验收标准

场景: 工具集四个来源说清
  测试: verify_four_tool_sources
  假设 读者阅读工具集组装图
  当 读者查看图中的四个来源
  那么 图中包含静态基础工具、USER_TYPE 条件工具、feature flag 条件工具、MCP 动态工具

场景: 热插入时机说明
  测试: verify_hot_insertion_timing
  假设 读者追问"MCP 工具是启动时加载还是运行中动态加入"
  那么 章节说明 MCP 工具在连接建立后动态插入的时机

场景: USER_TYPE 过滤示例有源码
  测试: verify_user_type_filter_source
  假设 读者查找 USER_TYPE 过滤的源码
  那么 章节引用 src/tools.ts 约第214行的 process.env.USER_TYPE === 'ant' 判断

场景: 工具集大小差异量化
  测试: verify_tool_count_difference
  假设 读者想知道普通用户与 ant 用户的工具集差异
  那么 章节给出大致数量对比，说明差异主要来自哪些条件分支

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 src/tools.ts 中的 getAllBaseTools
  那么 约第196行存在该函数定义

场景: MCP 工具不可用时的降级
  测试: verify_mcp_unavailable_handling
  假设 MCP 服务器连接失败
  当 读者检查工具集的降级策略
  那么 章节说明 MCP 工具不可用时工具集的变化

## 排除范围

- 不深入 MCP 传输协议（第 27 章）
- 不深入具体工具实现（第 11-13 章）
