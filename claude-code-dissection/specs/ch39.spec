spec: task
name: "第39章：termio——终端原语的解析与发送"
tags: [book-chapter, part-10]
---

## 意图

本章解析 Ink 的终端控制序列层。核心问题：ANSI escape 序列（CSI/OSC/DEC/SGR）是如何被解析的？光标控制、颜色渲染、选区管理的底层实现是什么？tokenizer 和 parser 的职责如何分工？

## 约束

必须：
- 引用 src/ink/termio/parser.ts 中的 parseCSI（约第87行）、parseCSIParams（约第81行）和顶部注释（约第4-6行）说明 parser 的职责
- 引用 src/ink/termio/tokenize.ts 中的 createTokenizer 说明 tokenizer 与 parser 的分工
- 引用 src/ink/termio/csi.ts 中的 CSI 常量和 src/ink/termio/sgr.ts 中的 applySGR 说明颜色处理
- 引用 src/ink/termio/dec.ts 或 src/ink/termio/osc.ts 各一处展示不同类型的控制序列

禁止：
- 不得深入 Ink reconciler 的节点树（第 38 章范围）
- 不得深入终端特定功能（如鼠标事件、复杂键盘映射）的完整实现
- 不得重复第 2 章的 Ink 技术选型分析

## 已定决策

- 开篇问题："终端里的颜色、光标移动、标题栏更新——这些是怎么实现的？为什么需要自己写解析器？"
- ASCII 图展示 tokenizer → parser → action 的处理流水线
- 源码引用格式：`src/ink/termio/parser.ts:行号`

## 边界

### 允许修改
- book/src/part10/ch39.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 reconciler 节点树（第 38 章）

## 验收标准

场景: tokenizer 与 parser 职责分工说清
  测试: verify_tokenizer_parser_separation
  假设 读者追问"为什么要分 tokenizer 和 parser 两层"
  那么 章节解释 tokenizer 负责边界检测（识别 escape 序列的起止），parser 负责语义解释（"\x1b[31m" → SGR 红色），两层分工使各自保持简单

场景: CSI/OSC/DEC/SGR 四类序列各有示例
  测试: verify_four_sequence_types
  假设 读者想了解不同类型 escape 序列的用途
  当 读者查看四类序列说明
  那么 章节给出每类至少一个具体示例：CSI（光标移动/清屏）、SGR（颜色属性）、OSC（标题栏/链接）、DEC（备用屏幕/光标可见性）

场景: parseCSI 解析示例说明
  测试: verify_parse_csi_example
  假设 读者阅读 parseCSI 函数说明
  当 读者查看解析示例
  那么 章节展示 "\x1b[31m" 的解析过程：提取 CSI 参数 [31] → 识别为 SGR → 调用 applySGR 设置前景色红色

场景: 颜色渲染机制说明
  测试: verify_color_rendering_mechanism
  假设 读者追问"256 色和 true color 怎么处理"
  那么 章节说明 applySGR 对不同颜色模式（基础 16 色、256 色、24 位 true color）的处理差异，引用 sgr.ts

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 termio/parser.ts 中的 parseCSI
  那么 约第87行存在 function parseCSI(rawSequence: string): Action | null 的函数定义

场景: 未知或损坏 escape 序列的处理
  测试: verify_unknown_sequence_handling
  假设 终端输出了一个非标准或损坏的 escape 序列
  当 读者检查错误处理
  那么 章节说明 parseCSI 返回 null 时的处理：忽略未知序列，不影响后续序列的解析

## 排除范围

- 不深入 Ink reconciler 的布局计算（第 38 章）
- 不覆盖完整的鼠标事件处理
- 不分析键盘原始输入的 keypress 解析（src/ink/parse-keypress.ts）
