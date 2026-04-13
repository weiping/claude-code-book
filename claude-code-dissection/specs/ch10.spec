spec: task
name: "第10章：运行模式状态机——Plan、Auto、Worktree 等模式的实现"
tags: [book-chapter, part-2]
---

## 意图

本章解析 Claude Code 的运行模式体系。核心问题：PermissionMode 的完整枚举、handlePlanModeTransition 的状态转移逻辑、Plan V2 多 Agent 并行计数策略，以及 Worktree 模式的隔离机制。

## 约束

必须：
- 引用 src/types/permissions.ts 中的 EXTERNAL_PERMISSION_MODES 和 InternalPermissionMode 枚举（约第16-36行）
- 引用 src/bootstrap/state.ts 中的 handlePlanModeTransition（约第1349行）
- 引用 src/utils/planModeV2.ts 中的 getPlanModeV2AgentCount 展示订阅级别差异
- 绘制 Mermaid stateDiagram 展示六种模式的合法转移

禁止：
- 不得深入权限规则引擎（第 15-17 章范围）
- 不得深入 YOLO/AI 分类器的实现（第 16 章范围）

## 已定决策

- 开篇问题："PermissionMode 类型里有 6 种模式，但用户从 UI 只能设置 5 种——第六种 bubble 为什么只能被代码内部使用？"
- Mermaid stateDiagram-v2 展示模式状态机
- 源码引用格式：`src/types/permissions.ts:行号`

## 边界

### 允许修改
- book/src/part2/ch10.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入权限规则引擎实现

## 验收标准

场景: 六种模式枚举完整
  测试: verify_six_modes_enumerated
  假设 读者想知道 Claude Code 有哪些运行模式
  当 读者查看模式枚举说明
  那么 章节覆盖全部 6 种模式，每种有 1-2 句用途说明

场景: 状态转移图正确
  测试: verify_state_diagram_transitions
  假设 读者阅读 Mermaid 状态图
  当 读者检查转移箭头
  那么 图中包含常见合法转移和 bubble 的特殊说明

场景: Plan V2 多 Agent 计数说明
  测试: verify_plan_v2_agent_count
  假设 读者追问"Plan V2 和 Plan V1 有什么区别"
  那么 章节解释 getPlanModeV2AgentCount 按订阅级别返回并行 Agent 数

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 src/types/permissions.ts 中的 EXTERNAL_PERMISSION_MODES
  那么 约第16-21行存在该常量定义

场景: auto 模式的条件编译说明
  测试: verify_auto_mode_feature_gate
  假设 读者追问"为什么 auto 不在 EXTERNAL_PERMISSION_MODES 里"
  那么 章节解释 auto 模式由 TRANSCRIPT_CLASSIFIER feature flag 门控

场景: Worktree 模式隔离机制说明
  测试: verify_worktree_isolation_explained
  假设 读者追问"Worktree 模式和普通模式有什么不同"
  那么 章节说明 isWorktreeModeEnabled() 的当前实现和历史原因

## 排除范围

- 不深入权限规则引擎（第 15-17 章）
- 不深入 YOLO 分类器实现（第 16 章）
- 不分析 coordinator 模式（stub）
