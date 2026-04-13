spec: task
name: "第25章：AutoCompact 与边界标记的实现"
tags: [book-chapter, part-6]
---

## 意图

本章深入 AutoCompact 的具体实现。核心问题：token 警告状态如何计算？compact boundary message 如何在对话历史中标记压缩边界？PROMPT_CACHE_BREAK_DETECTION 如何检测 prompt cache 被意外破坏？

## 约束

必须：
- 引用 src/services/compact/autoCompact.ts 中的 calculateTokenWarningState（约第93行）、WARNING_THRESHOLD_BUFFER_TOKENS（约第63行）、getAutoCompactThreshold（约第72行）
- 引用 src/utils/messages.ts 中的 createMicrocompactBoundaryMessage（约第4557行）和 SystemCompactBoundaryMessage 类型
- 解释 compact boundary 的作用：标记历史被截断的位置，防止 Claude 对截断前的内容产生幻觉
- 说明 PROMPT_CACHE_BREAK_DETECTION flag 下的检测机制

禁止：
- 不得重复第 24 章的四种策略总览
- 不得深入 MicroCompact 和 SnipCompact 的实现细节（本章聚焦 AutoCompact）
- 不得深入 compact 的 prompt 设计（只分析触发和标记机制）

## 已定决策

- 开篇问题："AutoCompact 触发时，Claude 是怎么'知道'历史被压缩了的？有没有可能误以为历史完整？"
- Mermaid 状态图展示 token 使用量 → 警告阈值 → 压缩阈值的状态转换
- 源码引用格式：`src/services/compact/autoCompact.ts:行号`

## 边界

### 允许修改
- book/src/part6/ch25.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 MicroCompact/SnipCompact 算法

## 验收标准

场景: token 警告状态三级说明
  测试: verify_three_warning_levels
  假设 读者追问"超过多少 token 会触发压缩"
  那么 章节展示三个阈值：正常区间、警告区间（WARNING_THRESHOLD_BUFFER_TOKENS）、压缩触发阈值（getAutoCompactThreshold），并给出各阈值的具体数值

场景: compact boundary 标记机制说清
  测试: verify_compact_boundary_marker
  假设 读者追问"压缩后 Claude 怎么知道历史被截断了"
  那么 章节解释 SystemCompactBoundaryMessage 被插入到对话历史中标记截断位置，Claude 能识别该标记并调整行为

场景: PROMPT_CACHE_BREAK_DETECTION 说明
  测试: verify_cache_break_detection
  假设 读者追问"prompt cache 被意外破坏时会怎样"
  那么 章节说明该 feature flag 开启后如何检测 cache 破坏（通过比对 cache 读写 token 计数），以及检测到异常时的告警行为

场景: calculateTokenWarningState 返回值说明
  测试: verify_warning_state_return_value
  假设 读者阅读 calculateTokenWarningState 的函数签名
  当 读者查看返回值类型
  那么 章节解释返回对象的关键字段（isAboveWarningThreshold/isAboveAutoCompactThreshold）及其下游使用方式

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 autoCompact.ts 中的 WARNING_THRESHOLD_BUFFER_TOKENS
  那么 约第63行存在该常量，值为 20000

场景: 压缩触发但压缩失败的处理
  测试: verify_compact_trigger_failure
  假设 token 超过阈值但压缩 API 调用失败
  当 读者检查失败处理说明
  那么 章节说明失败时是继续对话（可能溢出）还是中断，引用相关错误处理代码

## 排除范围

- 不重复四种压缩策略总览（第 24 章）
- 不深入 MicroCompact 的单工具结果摘要算法
- 不深入 SnipCompact 的 snip projection 逻辑
- 不覆盖 compact 的 LLM prompt 设计（src/services/compact/prompt.ts 范围）
