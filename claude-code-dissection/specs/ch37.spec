spec: task
name: "第37章：未发布的功能总线——Feature Flag 背后的实验特性"
tags: [book-chapter, part-9]
---

## 意图

本章从 feature flag 分布反推 Claude Code 的产品演进方向。核心问题：ULTRAPLAN、DAEMON、BG_SESSIONS、COORDINATOR_MODE、BYOC_ENVIRONMENT_RUNNER 等实验 flag 背后有怎样的代码骨架？从这些 flag 能读出什么产品信号？

## 约束

必须：
- 引用 src/utils/ultraplan/keyword.ts 和 src/utils/ultraplan/ccrSession.ts 展示 ULTRAPLAN 的关键词检测和远程 Plan 会话机制
- 引用 src/utils/concurrentSessions.ts 中的 SessionKind 枚举（daemon/bg 类型）说明 DAEMON/BG_SESSIONS 的基础设施
- 引用 src/coordinator/coordinatorMode.ts 中的 COORDINATOR_MODE 使用，说明 coordinator 的骨架
- 用分类表展示 60+ flag 中有代表性的实验特性及其推断的产品方向

禁止：
- 不得分析已排除的 stub 模块内部实现（KAIROS、SSH、coordinator 等）
- 不得深入 feature flag 双层架构（第 4 章范围）
- 不得泄露未公开的产品路线图（所有推断标注「推断」）

## 已定决策

- 开篇问题："从源码里能看出 Claude Code 下一步想做什么吗？feature flag 是最好的线索。"
- 分类表：flag 名称 → 实验阶段（草图/骨架/接近完成） → 推断的产品方向
- 源码引用格式：`src/utils/ultraplan/keyword.ts:行号`

## 边界

### 允许修改
- book/src/part9/ch37.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入已排除 stub 模块的实现

## 验收标准

场景: 实验 flag 分类表有代表性
  测试: verify_experimental_flags_table
  假设 读者阅读分类表
  当 读者统计覆盖的 flag 数量
  那么 表格覆盖至少 8 个有代表性的实验 flag，每个标注实验阶段和推断产品方向，并注明「推断」

场景: ULTRAPLAN 代码骨架说明
  测试: verify_ultraplan_skeleton
  假设 读者追问"ULTRAPLAN 是什么功能"
  那么 章节引用 keyword.ts 的关键词检测和 ccrSession.ts 的远程 Plan 会话，说明 ULTRAPLAN 触发用户输入关键词后发起远程协作 Plan 的骨架，并标注「推断」

场景: DAEMON/BG_SESSIONS 基础设施说明
  测试: verify_daemon_bg_infrastructure
  假设 读者追问"BG_SESSIONS 和普通会话有什么不同"
  那么 章节引用 SessionKind 枚举中的 daemon/bg 类型，说明后台会话的基础设施已就绪，功能尚未完全发布

场景: 产品方向推断有标注
  测试: verify_inference_annotations
  假设 读者检查章节中的产品方向判断
  当 读者搜索"推断"字样
  那么 所有无源码直接证明的产品方向判断都标注了「推断」，未标注的结论有直接源码证据

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 src/utils/ultraplan/keyword.ts
  那么 文件存在，且章节引用的关键词检测函数在文件中真实存在

场景: flag 骨架代码不完整时的说明
  测试: verify_incomplete_skeleton_noted
  假设 某个实验 flag 对应的代码只有接口没有实现
  当 读者检查该 flag 的说明
  那么 章节明确标注该功能处于"仅有接口骨架，实现未完成"状态，不过度推断其功能细节

## 排除范围

- 不分析 KAIROS/SSH/coordinator 等已排除 stub 模块的实现
- 不重复 feature flag 双层架构（第 4 章）
- 不泄露任何未公开的产品路线图承诺
