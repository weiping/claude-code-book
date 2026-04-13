spec: task
name: "第19章：系统提示的优先级堆叠与组装"
tags: [book-chapter, part-5]
---

## 意图

本章解析 Claude Code 系统提示的构建逻辑。核心问题：多种系统提示来源如何按优先级合并？Override 模式何时完全替换默认提示？Agent 系统提示在 proactive 模式下为什么是追加而非替换？

## 约束

必须：
- 引用 src/utils/systemPrompt.ts 中的 buildEffectiveSystemPrompt 函数（约第41行）
- 引用函数上方的注释（约第30-38行）展示五级优先级列表（Override/Coordinator/Agent/Custom/Default）
- 解释 Override（loop mode）优先级0：完全替换所有其他提示的语义
- 解释 Agent 提示在 proactive 模式下追加而非替换的设计原因

禁止：
- 不得深入 CLAUDE.md 的发现机制（第 20 章范围）
- 不得深入上下文组装的 git status 部分（第 21 章范围）
- 不得深入 Coordinator 模式（stub，见第 37 章）

## 已定决策

- 开篇问题："--system-prompt 参数和 CLAUDE.md 文件都能设置系统提示，谁说了算？"
- 用优先级堆栈图（ASCII 或 Mermaid）展示五级覆盖关系
- 源码引用格式：`src/utils/systemPrompt.ts:行号`

## 边界

### 允许修改
- book/src/part5/ch19.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 CLAUDE.md 发现逻辑（第 20 章）
- 不深入 Coordinator 模式实现

## 验收标准

场景: 五级优先级顺序正确
  测试: verify_five_level_priority_order
  假设 读者阅读优先级堆栈图
  当 读者按优先级从高到低排列
  那么 顺序为：Override（0）→ Coordinator（1）→ Agent（2）→ Custom（3）→ Default（4），每级有触发条件说明

场景: Override 语义说清
  测试: verify_override_semantics
  假设 读者追问"Override 和 Custom 有什么区别"
  那么 章节解释 Override 完全替换所有提示（包括 appendSystemPrompt 也被跳过），而 Custom 只替换 Default

场景: Agent proactive 模式追加逻辑说明
  测试: verify_agent_proactive_append
  假设 读者追问"Agent 的系统提示为什么有时追加、有时替换"
  那么 章节解释 isProactiveActive 时 Agent 提示追加到 Default 上，非 proactive 时 Agent 提示替换 Default，并引用源码

场景: appendSystemPrompt 的位置说明
  测试: verify_append_system_prompt_position
  假设 读者追问"--append-system-prompt 的内容加在哪里"
  那么 章节说明 appendSystemPrompt 始终追加在最末尾（除 Override 模式外），引用源码

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 systemPrompt.ts 中的 buildEffectiveSystemPrompt
  那么 约第41行存在该函数，上方有五级优先级注释

场景: 自定义提示与默认提示冲突时的行为
  测试: verify_custom_vs_default_conflict
  假设 用户同时设置了 --system-prompt 和 CLAUDE.md 中有自定义提示
  当 读者检查合并行为
  那么 章节说明 Custom 替换 Default，CLAUDE.md 内容通过 appendSystemPrompt 或单独注入（指向第 20 章）

## 排除范围

- 不深入 CLAUDE.md 的发现机制（第 20 章）
- 不深入上下文组装（git status、工具描述，第 21 章）
- 不分析 Coordinator 模式提示（stub）
