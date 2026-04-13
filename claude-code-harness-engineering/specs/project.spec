spec: project
name: "从 Claude Code 源码提炼的 Harness 工程模式"
tags: [book]
---

## 意图

从 Claude Code v2.1.88 的 ~51 万行 TypeScript 源码中提炼可复用的 Harness 工程模式。全书 16 章，8 篇，投影师风格。

## 已定决策

- 写作语言：中文正文 + 英文技术术语保留原文
- 写作风格：projector（零代码展示，源码仅作为隐含锚点）
- 作者：雨杨先生
- 源码引用格式：`相对路径:行号`

## 边界

### 允许修改
- book/src/ 下的所有 .md 文件

### 禁止做
- 不修改 src/ 下的任何源码文件
- 不修改 DESIGN.md

## 排除范围

- assistant/、server/、ssh/、proactive/、bridge/ 中的 stub 文件
- 功能使用教程
- UI 组件渲染逻辑
- 与 Harness 无关的辅助功能
