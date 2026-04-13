spec: task
name: "第7章：斜杠命令系统——内置命令的注册与执行"
tags: [book-chapter, part-2]
---

## 意图

本章解析 Claude Code 的斜杠命令体系。核心问题：100+ 个命令是怎么注册的？getCommands() 如何动态加载、过滤？一条斜杠命令是如何绕过 LLM 直接执行的？

## 约束

必须：
- 引用 src/commands.ts 中的 getCommands 函数（约第476行）和 filterCommandsForRemoteMode
- 引用至少 2 个具体命令目录（如 src/commands/clear/、src/commands/help/）的入口文件
- 解释 SystemLocalCommandMessage 类型的作用：标记该消息不发给 LLM
- 说明 isCommandEnabled 的过滤逻辑：feature flag、用户类型、远程模式的多重过滤

禁止：
- 不得逐一分析所有 100+ 个命令（附录 A 的关键文件索引范围）
- 不得深入具体命令的业务逻辑
- 不得重复第 6 章的分流判断内容

## 已定决策

- 开篇问题："/help、/clear、/model——这些命令是怎么被 Claude Code 知道的？"
- ASCII 目录树展示 commands/ 下的约定结构
- 源码引用格式：`src/commands.ts:行号`

## 边界

### 允许修改
- book/src/part2/ch07.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入具体命令业务逻辑

## 验收标准

场景: 目录约定注册机制说清
  测试: verify_directory_convention_explained
  假设 读者想添加一个新斜杠命令
  当 读者读完注册机制一节
  那么 能理解需要在 src/commands/ 下创建子目录并导出特定结构，getCommands() 会自动发现它

场景: SystemLocalCommandMessage 作用说清
  测试: verify_local_command_message_role
  假设 读者追问"斜杠命令的结果怎么不触发 LLM 调用"
  那么 章节解释 SystemLocalCommandMessage 类型标记这类消息走本地执行路径，不进入 query.ts

场景: isCommandEnabled 过滤链说明
  测试: verify_command_filter_chain
  假设 读者追问"为什么某些命令只有内部用户才看得到"
  那么 章节说明 isCommandEnabled 的过滤维度：feature flag、USER_TYPE、远程模式，并有源码引用

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 src/commands.ts 中 getCommands 函数
  那么 引用行号对应真实函数定义

场景: 执行路径有说明
  测试: verify_execution_path_explained
  假设 读者想追踪 /clear 命令的完整执行路径
  那么 章节给出从用户输入到命令执行完成的路径（不需要跟进具体清除逻辑）

场景: 命令不存在时的处理
  测试: verify_unknown_command_handling
  假设 用户输入了一个不存在的斜杠命令
  当 读者检查错误处理说明
  那么 章节说明未知命令的反馈机制（错误提示或忽略）

## 排除范围

- 不逐一分析 100+ 个命令（见附录 A）
- 不分析 MCP 命令的注册（第 27 章）
- 不覆盖 Skill 命令的动态注册（第 36 章）
