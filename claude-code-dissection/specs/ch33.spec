spec: task
name: "第33章：Effort、Fast Mode 与 Thinking——推理深度控制"
tags: [book-chapter, part-9]
---

## 意图

本章解析 Claude Code 的推理深度控制机制。核心问题：四级 Effort（low/medium/high/max）如何影响 API 参数？Fast Mode 如何切换到更小的模型？ultrathink 关键词如何触发扩展 thinking token budget？三者如何协同工作？

## 约束

必须：
- 引用 src/utils/effort.ts 中的 EFFORT_LEVELS（约第13行）、modelSupportsEffort（约第23行）、modelSupportsMaxEffort（约第53行）
- 引用 src/utils/thinking.ts 中的 ThinkingConfig 类型、isUltrathinkEnabled、hasUltrathinkKeyword、findThinkingTriggerPositions
- 引用 src/utils/fastMode.ts 中的 isFastModeEnabled 和 prefetchFastModeStatus 说明 Fast Mode 的模型切换
- 解释 Effort 参数如何传递给 Anthropic API（betas 参数或独立字段）

禁止：
- 不得重复第 22 章的模型选择路由
- 不得深入 thinking blocks 在对话历史中的处理（第 8 章 query.ts 范围）
- 不得深入 Effort 的 UI 选择器实现（TUI 层范围）

## 已定决策

- 开篇问题："在提示词里写 'ultrathink' 有魔法吗？它到底改变了什么 API 参数？"
- 对比表展示 Effort 四级 × Fast Mode × ultrathink 的参数组合
- 源码引用格式：`src/utils/effort.ts:行号`

## 边界

### 允许修改
- book/src/part9/ch33.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入模型选择路由（第 22 章）

## 验收标准

场景: Effort 四级与 API 参数映射说清
  测试: verify_effort_api_mapping
  假设 读者追问"设置 --effort max 时 API 请求有什么不同"
  那么 章节说明四级 Effort 如何映射到 API 参数（如 budget_tokens 或 effort 字段），并说明 modelSupportsMaxEffort 的作用（max 仅 Opus 4.6 支持）

场景: ultrathink 关键词触发机制说明
  测试: verify_ultrathink_trigger
  假设 读者在提示词中写了 "ultrathink"
  当 读者追踪触发流程
  那么 章节解释 hasUltrathinkKeyword 检测关键词 → findThinkingTriggerPositions 定位 → 触发扩展 budgetTokens 的完整链路

场景: Fast Mode 模型切换说明
  测试: verify_fast_mode_model_switch
  假设 读者追问"Fast Mode 切换到哪个模型"
  那么 章节引用 isFastModeEnabled 的判断逻辑，说明 Fast Mode 下使用 getSmallFastModel()（Haiku），以及 prefetchFastModeStatus 的预加载策略

场景: ThinkingConfig 三种状态说明
  测试: verify_thinking_config_states
  假设 读者阅读 ThinkingConfig 类型定义
  当 读者查看三种状态
  那么 章节解释 adaptive（自适应）、enabled（指定 budgetTokens）、disabled（禁用）三种状态的含义和触发条件

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 effort.ts 中的 EFFORT_LEVELS
  那么 约第13行存在该数组常量，包含 low/medium/high/max 四个值

场景: 不支持 Effort 的模型的降级处理
  测试: verify_unsupported_model_fallback
  假设 当前模型不支持 Effort 参数（modelSupportsEffort 返回 false）
  当 读者检查降级策略
  那么 章节说明 Effort 参数在不支持的模型上被忽略或报错的行为

## 排除范围

- 不重复模型选择路由（第 22 章）
- 不深入 thinking blocks 在流式 token 中的解析（第 8 章）
- 不覆盖 Effort UI 选择器的 React 组件（TUI 层）
