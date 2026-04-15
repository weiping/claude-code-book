spec: task
name: "第4章：CLI 入口与模式分叉——从 main.tsx 到 REPL / Headless / SDK"
tags: [book-chapter, part-2]
---

## 意图

追踪 Claude Code 从进程启动到模式分叉的完整路径：main.tsx 的三路并行启动序列（MDM 配置读取 / Keychain 预读取 / import 求值重叠）、Commander.js 命令解析树的结构，以及交互模式 / Headless（-p/--print）/ SDK / Assistant（feature('KAIROS') 门控）四种运行模式的分叉逻辑。读者读完后能在自己的 Agent CLI 项目中复用这一"并行启动 + 模式分叉"模式。

## 已定决策

- 写作语言：中文正文，英文技术术语保留原文
- ⛔ 写作风格：hunter（模式猎人）（从 DESIGN.md 读取，写作时必须遵循 writing-styles.md 中 hunter 风格的全部专属规则）
- ⛔ 章节结构：`## [模式预告开篇]` → `## 问题` → `## 源码实例 1` → `## 源码实例 2（变体）` → `## 模式剖析` → `## 适用范围` → `## 权衡与局限` → `## 与已知模式的对话` → `## 你能做什么`
- 源码引用格式：`src/相对路径:行号`
- 核心文件：src/main.tsx（入口文件，4683 行）
- 关联文件：src/setup.ts、src/cli/print.ts、src/entrypoints/sdk/、src/bootstrap/state.ts

## 约束

### 必须
- 每个核心概念有至少一处 `相对路径:行号` 格式的源码引用
- 包含至少一个可渲染的 Mermaid 流程图或 ASCII 架构图
- ⛔ 每节开篇格式与 hunter 风格匹配（模式预告，不引用源码）
- 跨章节引用使用"详见第 X 章"格式，不重复解释
- ⛔ 展示至少 2 处源码实例，证明模式的普遍性
- 包含适用范围表（什么场景用/不用该模式）
- 包含权衡与局限分析
- 包含与已知业界模式的对话（至少引用一个 GoF/POSA/EIP 模式）
- 使用"我们"而非"用户"/"读者"建立对话感

### 禁止
- ⛔ 开篇不得直接引用源码路径或行号（开篇是问题场景+模式预告+价值承诺，150-200字）
- 不得引用排除范围中的 stub 或未实现模块（特别是 src/assistant/）
- 不得出现"介绍了…"、"描述了…"、"讲解了…"等空洞表述
- 不得对源码中没有依据的设计意图做无标注的猜测（必须标注「（推断）」）
- 不得重复已在其他章节详细讲解的内容（用交叉引用代替）
- 不展开 REPL 界面细节（详见第 5 章）
- 不展开 processUserInput 路由逻辑（详见第 6 章）
- 不展开 bootstrap/state.ts 实现细节（详见第 2 章）

## 边界

### 允许修改
- book/src/part2/ch04-NEW.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不分析 src/assistant/、src/ssh/、src/server/、src/proactive/（排除范围 stub）

## 完成条件

场景: hunter 风格开篇
  测试: ch04_hunter_style_opening
  假设 读者打开第 4 章
  当 读者阅读章节第一屏内容
  那么 ⛔ 开篇不直接引用任何源码路径或行号，而是以问题场景+模式预告+价值承诺三要素切入（150-200字）

场景: 并行启动序列有图表
  测试: ch04_startup_diagram
  假设 读者阅读启动序列节
  当 读者检查图表区域
  那么 包含一个 Mermaid 序列图或 ASCII 图展示三路并行启动（MDM/Keychain/import 求值）
  那么 图表上方有 **图 4-X：[标题]** 标注

场景: 四种模式分叉有流程图
  测试: ch04_mode_fork_diagram
  假设 读者阅读模式分叉节
  当 读者检查图表区域
  那么 包含一个 Mermaid flowchart 展示交互/Headless/SDK/Assistant 四种模式的分叉判断
  那么 图表上方有 **图 4-X：[标题]** 标注

场景: 源码引用有效性
  测试: ch04_source_anchors
  层级: 集成
  假设 读者跟随本章中的源码引用
  当 读者在项目目录查找每处路径和行号
  那么 每处引用都实际存在于对应文件的对应行

场景: feature flag 条件导入有分析
  测试: ch04_feature_flag_imports
  假设 本章讨论 feature('KAIROS') 等条件导入
  当 读者检查相关内容
  那么 有源码引用指向 main.tsx 中的条件导入代码
  那么 分析了为什么使用构建时 DCE 而非运行时 if/else（详见第 3 章的交叉引用）

场景: deferred prefetches 有说明
  测试: ch04_deferred_prefetches
  假设 本章讨论启动优化
  当 读者检查 startDeferredPrefetches 的内容
  那么 说明了哪些预取被延迟到首次渲染后执行，以及为什么

场景: 不引用排除范围
  测试: ch04_no_excluded_refs
  层级: 集成
  假设 DESIGN.md 列出了排除范围
  当 读者检查本章所有源码路径
  那么 没有任何路径落在 src/assistant/、src/ssh/、src/server/、src/proactive/ 中

场景: 模式命名框格式规范
  测试: ch04_pattern_box_format
  假设 本章使用 hunter 风格
  当 读者检查模式剖析节或章末
  那么 存在至少 1 个模式命名框，包含中英文模式名、问题、解决方案、源码锚点

场景: 章末行动建议
  测试: ch04_action_items
  假设 读者读完本章
  当 读者检查"你能做什么"节
  那么 包含 5-8 条以行动动词开头的可操作建议

场景: ⛔ hunter 开篇格式（最高优先级）
  测试: ch04_hunter_opening_format
  假设 读者打开本章
  当 读者阅读第一屏内容（开篇节）
  那么 ⛔ 开篇不直接引用任何源码路径或行号
  那么 开篇包含三要素：问题场景+模式预告+价值承诺
  那么 全章未混用其他风格的写作手法

场景: 多实例证明模式普遍性
  测试: ch04_multi_instance_proof
  假设 本章提炼了一个工程模式
  当 读者检查源码实例节
  那么 存在至少 2 处不同位置（不同文件或不同函数）的源码实例，证明该模式在代码库中反复出现
  那么 每个实例说明与第一个实例的关键区别

场景: 适用范围表存在
  测试: ch04_applicability_table
  假设 本章提炼了一个工程模式
  当 读者检查"适用范围"节
  那么 存在一个表格，列出该模式适用（✓）和不适用（✗）的场景，每行附理由和替代方案

场景: 权衡与局限分析
  测试: ch04_tradeoffs_and_limits
  假设 本章提炼了一个工程模式
  当 读者检查"权衡与局限"节
  那么 章节说明了该模式的适用边界、潜在失败风险、性能影响和替代方案

场景: 与已知模式的对话
  测试: ch04_known_pattern_dialogue
  假设 本章提炼了一个工程模式
  当 读者检查"与已知模式的对话"节
  那么 章节将本章模式与至少一个业界已知模式（如 GoF 设计模式、POSA 架构模式、EIP 集成模式）做了对比
  那么 对比说明了相同点和不同点

场景: 读者对话感
  测试: ch04_reader_voice
  假设 本章使用 hunter 风格
  当 读者检查章节中的代词和叙述方式
  那么 使用"我们"而非"用户"或"读者"
  那么 关键结论前有设问句（如"为什么不用……？"）
  那么 复杂逻辑前有预告性文字

场景: 关键信息突出
  测试: ch04_key_info_highlight
  假设 本章有关键结论或重要设计决策
  当 读者快速扫读本章
  那么 关键结论用 **加粗** 标注，不埋在段落中间
  那么 对比信息用表格展示，而非散文逐条列举

## 排除范围

- src/assistant/（Assistant 模式，stub 未实现）
- src/ssh/（SSH 功能，stub 未实现）
- src/server/（服务端组件，stub 未实现）
- src/proactive/（主动建议，stub 未实现）
- src/buddy/、src/voice/（UI 细节）
- TypeScript 语法讲解、React 基础、Bun 运行时基础
