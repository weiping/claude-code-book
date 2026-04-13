spec: task
name: "第6章：用户输入的三条分叉路"
tags: [book-chapter, part-2]
---

## 意图

本章解析用户每次按下回车后的第一段旅程：输入如何被分类、分流。核心问题：Claude Code 怎么判断这条输入该交给 LLM、该本地执行、还是触发内置命令？优先级队列如何保证正确的调度顺序？

## 约束

必须：
- 引用 src/utils/processUserInput/processUserInput.ts 中的 processUserInput 函数（约第85行）
- 引用 processSlashCommand.tsx、processBashCommand.tsx、processTextPrompt.ts 各至少一处
- 绘制 Mermaid flowchart 展示三条分叉路的判断逻辑
- 解释优先级队列（getCommandsByMaxPriority）在多消息并发时的作用

禁止：
- 不得深入 slash 命令的注册机制（详见第 7 章）
- 不得深入 LLM 调用循环（详见第 8、9 章）
- 不得分析工具执行细节（详见第 10-14 章）

## 已定决策

- 开篇问题："你输入 /clear、!ls、还是普通问题——Claude Code 怎么知道该怎么处理？"
- Mermaid flowchart 展示判断逻辑
- 源码引用格式：`src/utils/processUserInput/processUserInput.ts:行号`

## 边界

### 允许修改
- book/src/part2/ch06.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 slash 命令注册（第 7 章）
- 不深入 LLM 调用（第 8、9 章）

## 验收标准

场景: 三条分叉路判断逻辑图正确
  测试: verify_three_paths_flowchart
  假设 读者阅读 Mermaid 流程图
  当 读者追踪 /clear、!ls、普通文本三种输入
  那么 图中三条路径分别指向：processSlashCommand、processBashCommand、processTextPrompt，判断条件清晰

场景: 分流判断依据说清
  测试: verify_routing_criteria_explained
  假设 读者想知道"以 / 开头就是 slash 命令吗"
  当 读者读完判断逻辑一节
  那么 章节给出实际的判断依据（isSlashCommand 检查、! 前缀检查等）并引用源码

场景: 优先级队列作用说明
  测试: verify_priority_queue_explained
  假设 读者追问"用户快速连续输入时会怎样"
  那么 章节说明 getCommandsByMaxPriority 如何处理队列中多条消息的调度

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 src/utils/processUserInput/processUserInput.ts:85 附近
  那么 存在 processUserInput 函数定义，且函数内有分叉逻辑

场景: 不越界进入后续章节范围
  测试: verify_no_chapter_boundary_violation
  假设 读者检查 slash 命令注册机制的描述
  当 读者搜索 getCommands 的内部实现分析
  那么 最多一句提及并有"详见第 7 章"指引，不展开注册逻辑

场景: 异常输入处理说明
  测试: verify_error_input_handling
  假设 读者输入空字符串或仅空白字符
  当 读者检查章节的边界情况说明
  那么 章节说明空输入或无效 slash 命令的处理路径

## 排除范围

- 不深入 slash 命令的目录注册机制（第 7 章）
- 不分析 LLM streaming 响应（第 8 章）
- 不覆盖工具执行权限检查（第 15 章）
