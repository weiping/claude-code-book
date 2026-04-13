spec: task
name: "第22章：模型自动选择——Opus、Sonnet 与 Haiku 的路由逻辑"
tags: [book-chapter, part-5]
---

## 意图

本章解析 Claude Code 的模型自动选择机制。核心问题：不同订阅级别的用户默认用什么模型？opusplan/sonnetplan 别名如何在 Plan 模式触发模型升级？Haiku 在什么场景被自动切换？用户覆盖和订阅默认的优先级链是什么？

## 约束

必须：
- 引用 src/utils/model/model.ts 中的 getDefaultMainLoopModelSetting（约第178行）展示订阅级别路由（Max/TeamPremium → Opus，其他 → Sonnet）
- 引用 getDefaultOpusModel、getDefaultSonnetModel、getDefaultHaikuModel（约第105-137行）说明各档默认模型
- 引用 opusplan/sonnetplan 别名处理（约第152-163行）展示 Plan 模式模型升级逻辑
- 引用 getSmallFastModel（约第36行）说明 Haiku 的使用场景

禁止：
- 不得深入 Bedrock/Vertex/Foundry 后端路由（提及即可，不展开）
- 不得深入 effort.ts 的四级推理深度（第 33 章范围）
- 不得覆盖模型版本的命名规则（附录 B 范围）

## 已定决策

- 开篇问题："Pro 用户和 Max 用户运行同一条指令，Claude Code 用的是同一个模型吗？"
- 用决策树表展示：订阅级别 × 运行模式 → 默认模型
- 源码引用格式：`src/utils/model/model.ts:行号`

## 边界

### 允许修改
- book/src/part5/ch22.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 effort 四级推理（第 33 章）

## 验收标准

场景: 订阅级别路由表完整
  测试: verify_subscription_routing_table
  假设 读者是 Pro 订阅用户
  当 读者查看订阅级别路由表
  那么 表格涵盖 Max/TeamPremium（→ Opus）、Pro/Enterprise/PAYG（→ Sonnet）、ant 内部（→ 配置或 Opus 1M）三条路由，有源码引用

场景: opusplan 别名说清
  测试: verify_opusplan_alias
  假设 读者追问"为什么设置 /model opusplan 后，只有在 Plan 模式才用 Opus"
  那么 章节引用约第152行的条件判断，解释 opusplan 在 plan 模式返回 Opus、其他模式返回 Sonnet 的逻辑

场景: Haiku 使用场景说明
  测试: verify_haiku_use_cases
  假设 读者追问"Haiku 在什么时候被用到"
  那么 章节说明 getSmallFastModel() 返回 Haiku，并列出调用该函数的典型场景（如快速分类任务、简短判断）

场景: 用户覆盖优先级说明
  测试: verify_user_override_priority
  假设 用户用 --model 参数指定了模型
  当 读者检查覆盖优先级说明
  那么 章节解释 getMainLoopModelOverride() 的优先级高于默认路由，并说明覆盖的生效范围

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 model.ts 中的 getDefaultMainLoopModelSetting
  那么 约第178行存在该函数，包含 isMaxSubscriber() 的条件判断

场景: 无效模型名处理
  测试: verify_invalid_model_name_handling
  假设 用户指定了一个不存在的模型名
  当 读者检查错误处理说明
  那么 章节说明 validateModel 或类似检查的行为，以及用户看到的错误提示

## 排除范围

- 不深入 Bedrock inference profile 的枚举与缓存（附录 C 环境变量范围）
- 不深入 effort 四级推理深度（第 33 章）
- 不覆盖模型版本命名规则（附录 B）
