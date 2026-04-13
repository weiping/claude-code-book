spec: task
name: "第31章：Subagent 的生命周期——forkSubagent、runAgent 与内存隔离"
tags: [book-chapter, part-8]
---

## 意图

本章深入 Subagent 的完整执行生命周期。核心问题：forkSubagent 的隐式继承如何让子 Agent 获得父 Agent 的上下文？runAgent 的对话循环与主循环（第 8 章）有何同构与隔离关系？agentMemorySnapshot 如何防止记忆污染？

## 约束

必须：
- 引用 src/tools/AgentTool/forkSubagent.ts 中的 isForkSubagentEnabled（约第32行）、FORK_AGENT（约第60行）、buildForkedMessages（约第107行）
- 引用 src/tools/AgentTool/runAgent.ts 中的 runAgent 函数签名（约第248行）和 killShellTasksForAgent（约第847行）
- 引用 src/tools/AgentTool/resumeAgent.ts 中的 readAgentMetadata 和 reconstructForSubagentResume
- 引用 src/tools/AgentTool/agentMemorySnapshot.ts 中的 SNAPSHOT_BASE 常量和快照目录结构

禁止：
- 不得重复第 30 章的 Task 类型对比
- 不得深入 forkSubagent 的 worktree 细节（只说明隔离目的）
- 不得重复第 8 章的 query.ts 单轮循环细节

## 已定决策

- 开篇问题："forkSubagent 和普通 subagent_type 调用有什么本质区别？'继承父上下文'是什么意思？"
- Mermaid 流程图展示 subagent 从 AgentTool.call() 到执行完成的完整生命周期
- 源码引用格式：`src/tools/AgentTool/runAgent.ts:行号`

## 边界

### 允许修改
- book/src/part8/ch31.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不重复 query.ts 单轮循环（第 8 章）

## 验收标准

场景: forkSubagent 隐式继承说清
  测试: verify_fork_implicit_inheritance
  假设 读者追问"omit subagent_type 时发生了什么"
  那么 章节引用 FORK_AGENT 定义和 buildForkedMessages，解释子 Agent 如何继承父 Agent 的完整对话历史和工具池

场景: runAgent 与主循环同构关系说明
  测试: verify_run_agent_homomorphic
  假设 读者追问"runAgent 和 query.ts 有什么关系"
  那么 章节说明 runAgent 内部同样调用 query.ts 的流式循环（同构），但在独立的 agentId 上下文中运行（隔离），两者无共享状态

场景: agentMemorySnapshot 隔离机制说明
  测试: verify_agent_memory_isolation
  假设 读者追问"两个并行子 Agent 的记忆会互相污染吗"
  那么 章节解释 agentMemorySnapshot 为每个 Agent 创建独立快照目录（agent-memory-snapshots/{agentType}/），实现记忆隔离

场景: resumeAgent 恢复路径说明
  测试: verify_resume_agent_path
  假设 子 Agent 异常中断后需要恢复
  当 读者追踪恢复路径
  那么 章节说明 readAgentMetadata → reconstructForSubagentResume 的恢复链路，以及恢复时对话历史的重建方式

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 forkSubagent.ts 中的 isForkSubagentEnabled
  那么 约第32行存在该函数，内部检查 feature('FORK_SUBAGENT') 和 isCoordinatorMode()

场景: subagent 正常退出与异常退出的处理差异
  测试: verify_subagent_exit_handling
  假设 子 Agent 任务完成（正常退出）vs 被中断（异常退出）
  当 读者检查两种退出路径
  那么 章节说明正常退出返回结果给父 Agent，异常退出触发 killShellTasksForAgent 清理，引用约第847行

## 排除范围

- 不重复 Task 类型的进程隔离对比（第 30 章）
- 不重复 query.ts 单轮原子循环细节（第 8 章）
- 不深入 worktree 文件系统隔离机制（第 10 章 Worktree 模式范围）
