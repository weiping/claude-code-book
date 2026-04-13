spec: task
name: "第30章：Task 类型体系——三种执行模式的实现"
tags: [book-chapter, part-8]
---

## 意图

本章深入三种 Task 类型的内部实现差异。核心问题：InProcessTeammateTask 如何在同一进程内运行子 Agent？LocalAgentTask 如何管理独立进程的生命周期？LocalShellTask 如何将后台 Shell 进程前台化？

## 约束

必须：
- 引用 src/tasks/InProcessTeammateTask/InProcessTeammateTask.ts 中的 injectUserMessageToTeammate 或 getAllInProcessTeammateTasks
- 引用 src/tasks/LocalAgentTask/LocalAgentTask.ts 中的 registerAsyncAgent、isLocalAgentTask、LocalAgentTaskState
- 引用 src/tasks/LocalShellTask/LocalShellTask.tsx 中的 backgroundExistingForegroundTask 或 registerForeground
- 解释三种 Task 的核心差异：进程隔离级别、通信方式、适用场景

禁止：
- 不得重复第 29 章的架构总览
- 不得深入 forkSubagent/runAgent 的对话循环（第 31 章范围）
- 不得深入 Swarm 权限同步（第 32 章范围）

## 已定决策

- 开篇问题："InProcess Task 和 LocalAgent Task 都能运行子 Agent——它们有什么本质区别？"
- 对比表展示三种 Task 的进程隔离、通信方式、内存共享情况
- 源码引用格式：`src/tasks/LocalAgentTask/LocalAgentTask.ts:行号`

## 边界

### 允许修改
- book/src/part8/ch30.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 runAgent 对话循环（第 31 章）

## 验收标准

场景: 三种 Task 对比表完整
  测试: verify_three_task_comparison
  假设 读者想选择合适的 Task 类型
  当 读者查看对比表
  那么 表格包含：进程隔离（同进程/独立进程/远程）、通信方式（函数调用/IPC/HTTP）、内存共享（是/否）、适用场景四个维度

场景: InProcessTeammateTask 通信机制说明
  测试: verify_inprocess_communication
  假设 读者追问"InProcess Task 怎么和主 Agent 通信"
  那么 章节解释 injectUserMessageToTeammate 的直接函数调用机制，无序列化开销

场景: LocalAgentTask 注册机制说明
  测试: verify_local_agent_registration
  假设 读者追问"LocalAgentTask 如何注册和追踪异步 Agent"
  那么 章节引用 registerAsyncAgent 和 LocalAgentTaskState 说明 Agent 注册和状态追踪机制

场景: LocalShellTask 前台化机制说明
  测试: verify_shell_task_foreground
  假设 读者追问"后台 Shell 任务怎么切换到前台"
  那么 章节引用 backgroundExistingForegroundTask 或 registerForeground 说明前后台切换逻辑

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 LocalAgentTask.ts 中的 registerAsyncAgent
  那么 文件存在，且 registerAsyncAgent 函数可在文件中找到

场景: Task 生命周期结束时的清理
  测试: verify_task_cleanup
  假设 子 Agent 任务异常终止
  当 读者检查清理机制
  那么 章节说明 Task 结束时的资源释放（进程终止、状态清理），并引用 stopTask.ts 或 killShellTasksForAgent

## 排除范围

- 不重复 Swarm 架构总览（第 29 章）
- 不深入 runAgent 的对话循环（第 31 章）
- 不覆盖 RemoteAgentTask 的远程调度（需要 Bridge 层支持，见排除范围）
