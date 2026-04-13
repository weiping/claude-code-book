spec: task
name: "第40章：并发优先的启动哲学"
tags: [book-chapter, part-11]
---

## 意图

本章从第3章的具体实现出发，提炼"并发优先"的设计原则。核心问题：Claude Code 冷启动中哪些决策体现了"能并行就不串行"？如何用 profileCheckpoint 量化并驱动优化？这个原则能推广到哪些 CLI 工具场景？

## 约束

必须：
- 引用 src/utils/startupProfiler.ts 中的 profileCheckpoint（约第65行）、profileReport（约第123行）和 checkpoint 数据结构
- 提炼第3章的三路并发（MDM/Keychain/Bootstrap）背后的通用原则，不重复第3章的实现细节
- 列出至少三个"可并行但被串行化"的常见 CLI 反模式及其改进方案
- 给出一个可量化的优化方法：如何用 profileCheckpoint 埋点识别串行瓶颈

禁止：
- 不得重复第3章的具体代码实现细节
- 不得深入 MDM/Keychain 的业务逻辑
- 不得引入第3章未提及的新启动优化技术

## 已定决策

- 本章为工程原则提炼章，代码密度低于前面章节，重在归纳和类比
- 开篇以 profileReport 的输出示例开场，让读者看到数字化的启动时间分布
- 源码引用格式：`src/utils/startupProfiler.ts:行号`

## 边界

### 允许修改
- book/src/part11/ch40.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不重复第3章的实现细节

## 验收标准

场景: 并发优先原则可提炼为一条规则
  测试: verify_principle_extractable
  假设 读者读完本章
  当 读者被要求用一句话总结原则
  那么 能从正文中直接提炼出"将所有独立的 I/O 操作并行化，推迟到首次使用时才等待结果"或等价表述

场景: 三路并发抽象为通用模式
  测试: verify_parallel_pattern_generalized
  假设 读者想将此模式应用到自己的 CLI
  当 读者读完模式说明
  那么 章节给出通用模式：识别独立 I/O 操作 → 在模块加载时触发 → 在首次使用前 await，不依赖 Claude Code 的具体实现

场景: profileCheckpoint 量化方法可操作
  测试: verify_profiling_method_actionable
  假设 读者想优化自己的 CLI 启动时间
  当 读者读完量化方法说明
  那么 章节给出可操作的步骤：在关键路径添加 checkpoint 埋点 → 运行 profileReport → 识别最长串行段 → 评估是否可并行

场景: 常见反模式列举
  测试: verify_antipatterns_listed
  假设 读者检查自己的 CLI 代码
  当 读者对照反模式列表
  那么 章节给出至少三个具体反模式（如：顺序读取多个配置文件、启动时同步验证 API key、串行初始化多个服务），每个有改进建议

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 startupProfiler.ts 中的 profileCheckpoint
  那么 约第65行存在该函数的 export function 定义

场景: 并发引入的风险说明
  测试: verify_concurrency_risks_acknowledged
  假设 读者问"并发化所有初始化会有什么风险"
  那么 章节说明并发的已知风险（初始化顺序依赖、错误处理复杂化）及 Claude Code 如何应对（顺序依赖的模块仍串行，错误仍前台报告）

## 排除范围

- 不重复第3章的 MDM/Keychain 并发实现细节
- 不覆盖 Node.js 事件循环的底层原理
- 不分析 async/await 与 Promise.all 的实现区别
