spec: task
name: "第1章：运行时 Harness 全景——总体架构解析"
tags: [book-chapter, part-1]
---

## 意图

本章建立全书的结构地图。读者读完后能用一张模块关系图说清楚 Claude Code 由哪些子系统构成、它们的依赖方向是什么，为后续所有章节提供定位锚点。核心问题：Claude Code 不只是一个 CLI wrapper，它是什么？

## 约束

必须：
- 包含一张 Mermaid 模块关系图，覆盖全书 11 篇对应的主要子系统（不少于 8 个节点）
- 引用 src/main.tsx 中的 launchRepl 调用、src/tools.ts 和 src/commands.ts 的导入
- 说明 Harness 的工程含义：组织各子系统协同工作的运行时骨架，而非功能集合
- 标注哪些子系统有完整分析、哪些因 stub 而排除，指向附录 B

禁止：
- 不得深入任何单一子系统的实现（每个子系统最多 2-3 句描述）
- 不得引用 src/assistant/、src/ssh/、src/proactive/、src/coordinator/ 中的 stub 内容
- 不得重复 DESIGN.md 核心主张的原文

## 已定决策

- 写作风格：autopsy 工程师解剖
- 开篇：以"当你运行 claude，进程里到底跑着什么？"作为认知冲突问题
- 图表：Mermaid flowchart，从 main.tsx 出发展开
- 源码引用格式：`相对路径:行号`

## 边界

### 允许修改
- book/src/part1/ch01.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 stub 模块：src/assistant/、src/ssh/、src/proactive/、src/coordinator/

## 验收标准

场景: 模块关系图覆盖完整
  测试: verify_architecture_diagram_nodes
  假设 读者阅读 Mermaid 图表
  当 读者统计图中节点
  那么 节点数不少于 8 个，覆盖 main.tsx 入口、REPL、QueryEngine、Tool 系统、Permission 系统、MCP、Swarm、TUI 层

场景: Harness 概念可提炼
  测试: verify_harness_definition_extractable
  假设 读者读完"什么是 Harness"一节
  当 读者被问到"Harness 与普通 CLI 的区别"
  那么 能从正文中直接提炼出一句定义，且定义不涉及具体功能

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者在项目目录中跟随引用
  当 读者检查 src/main.tsx 中 launchRepl 的调用行
  那么 引用行号存在且内容与描述一致

场景: stub 模块排除标注存在
  测试: verify_stub_exclusion_noted
  假设 读者想了解 KAIROS 或 SSH 功能
  当 读者在模块说明中搜索相关内容
  那么 章节明确标注这些模块为 stub 并指向附录 B

场景: 设计权衡存在
  测试: verify_tradeoff_present
  假设 读者追问"为什么用 React 写 CLI"
  那么 章节有简短权衡说明（不超过 1 段），详细展开指向第 2 章

场景: 无实现细节越界
  测试: verify_no_deep_dive
  假设 读者检查任意一个子系统的描述段落
  当 读者统计该段落字数
  那么 每个子系统的描述不超过 3 句，不出现具体函数名列表或代码块

## 排除范围

- 不分析 src/assistant/（KAIROS 模式，stub）
- 不分析 src/ssh/（最小实现）
- 不分析 src/proactive/（最小实现）
- 不分析 src/coordinator/（stub）
- 不包含启动时序细节（详见第 3 章）
