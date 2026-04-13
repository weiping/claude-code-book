spec: task
name: "第2章：技术栈选型——React/Ink + Bun + TypeScript 的工程逻辑"
tags: [book-chapter, part-1]
---

## 意图

本章回答"为什么这样选技术栈"——不是罗列技术，而是还原每个选型背后的工程约束和权衡。核心问题：在终端里跑 React 是认真的吗？Bun 替代 Node 带来了什么？`bun:bundle` 的 `feature()` API 为什么是架构级别的决策？

## 约束

必须：
- 引用 src/ink/reconciler.ts、src/replLauncher.tsx、src/main.tsx 中的 feature() 调用各至少一处
- 解释 bun:bundle feature() 与 webpack process.env.NODE_ENV 的本质差异：编译期物理删除分支 vs 运行期跳过
- 说明 Ink 的自定义 reconciler 为什么不能直接用 React DOM（终端无 DOM，只有字符网格）
- 包含至少一个对比表或 ASCII 图展示 Bun target vs Node target 的产物差异

禁止：
- 不得深入 reconciler 实现算法细节（详见第 38 章）
- 不得深入 feature flag 双层运行时体系（详见第 4 章）
- 不得重复第 1 章的模块关系图内容

## 已定决策

- 开篇问题："如果让你设计一个 AI Coding Agent 的 CLI，你会选什么渲染方案？"
- 每个技术选型配"为什么不选 X"的分析
- 源码引用格式：`相对路径:行号`

## 边界

### 允许修改
- book/src/part1/ch02.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 reconciler Yoga layout 算法（第 38 章范围）
- 不深入 GrowthBook 运行期 A/B（第 4 章范围）

## 验收标准

场景: 编译期消除机制说清
  测试: verify_compile_time_elimination_explained
  假设 读者熟悉 webpack tree-shaking
  当 读者读完 bun:bundle feature() 一节
  那么 读者能解释 feature('KAIROS') 返回 false 时 require('./assistant/index.js') 分支在产物中物理消失，而非运行时跳过

场景: Ink 选型有两个以上工程理由
  测试: verify_ink_rationale_has_two_reasons
  假设 读者怀疑"用 React 写 CLI 是过度设计"
  当 读者读完 Ink 选型分析
  那么 章节给出至少两个明确的工程理由，每个理由有对应的"不选 X 是因为 Y"结构

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者检查 src/ink/reconciler.ts
  那么 文件存在，且章节引用的行号在文件中对应到真实代码

场景: Bun vs Node 对比清晰
  测试: verify_bun_node_comparison_present
  假设 读者阅读对比图表
  当 读者对比两者的构建产物
  那么 表格或图中明确包含：feature() 支持、产物体积、运行时依赖三个维度

场景: 不越界深入 reconciler
  测试: verify_reconciler_not_deep_dived
  假设 读者检查 reconciler 相关段落
  当 读者统计该段落对 reconciler 内部算法的描述
  那么 不出现 Yoga layout 节点计算、diff 算法等实现细节，有"详见第 38 章"的指引

## 排除范围

- 不深入 reconciler 的 Yoga layout 算法（第 38 章）
- 不覆盖 GrowthBook 运行期 A/B 配置（第 4 章）
- 不分析 Ink 的 termio 原语层（第 39 章）
