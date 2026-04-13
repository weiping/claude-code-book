spec: task
name: "第29章：多智能体架构总览——Swarm 的层次模型"
tags: [book-chapter, part-8]
---

## 意图

本章建立多智能体系统的心智模型。核心问题：Swarm、Task、Agent 三层如何分工？InProcess/Local/Remote 三种拓扑各适合什么场景？多智能体系统的协作触发点在哪里？

## 约束

必须：
- 引用 src/tasks/ 目录下的 Task 类型体系（InProcessTeammateTask、LocalAgentTask、RemoteAgentTask、LocalShellTask）
- 引用 src/utils/swarm/teamHelpers.ts 中的 SpawnTeamOutput 和 TeamAllowedPath 说明团队结构
- 引用 src/tools/AgentTool/AgentTool.tsx 的 Progress 类型展示 AgentTool 与 Task 的连接点
- 绘制三层架构的 Mermaid 图：Swarm 层（策略）→ Task 层（执行载体）→ Agent 层（对话循环）

禁止：
- 不得深入 Task 类型的内部实现（第 30 章范围）
- 不得深入 forkSubagent/runAgent（第 31 章范围）
- 不得深入 Swarm 权限同步（第 32 章范围）

## 已定决策

- 开篇问题："当 Claude Code 说'我会让另一个 Agent 来处理这个'，后台发生了什么？"
- Mermaid 三层架构图：Swarm → Task → Agent
- 源码引用格式：`src/tasks/types.ts` 或 `src/utils/swarm/teamHelpers.ts:行号`

## 边界

### 允许修改
- book/src/part8/ch29.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 Task 内部实现（第 30 章）
- 不深入 forkSubagent（第 31 章）

## 验收标准

场景: 三层架构职责划分清晰
  测试: verify_three_layer_responsibilities
  假设 读者阅读三层架构图
  当 读者查看 Swarm/Task/Agent 三层的职责说明
  那么 每层有明确的职责描述：Swarm（协调策略、权限同步）、Task（执行载体、进程/线程管理）、Agent（对话循环、工具调用）

场景: 三种拓扑适用场景说明
  测试: verify_three_topology_use_cases
  假设 读者想选择合适的多智能体拓扑
  当 读者读完三种拓扑说明
  那么 章节给出 InProcess（同进程、低开销）、Local（独立进程、隔离）、Remote（跨机器、云端）各自的适用场景和成本差异

场景: AgentTool 与 Task 连接点说明
  测试: verify_agenttool_task_connection
  假设 读者追问"AgentTool 调用后怎么创建 Task"
  那么 章节说明 AgentTool.call() 根据配置选择创建哪种 Task 类型，并指向第 30 章的详细实现

场景: 协作触发点说明
  测试: verify_collaboration_trigger_points
  假设 读者追问"什么情况下会触发多智能体协作"
  那么 章节列出触发场景（如 AgentTool 被调用、/fork 命令、Plan V2 并行）并说明每种场景对应的架构路径

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 src/tasks/ 目录下的 Task 类型
  那么 章节引用的文件（如 InProcessTeammateTask/、LocalAgentTask/）在该目录下真实存在

场景: 多智能体失败时的隔离
  测试: verify_agent_failure_isolation
  假设 一个子 Agent 任务失败或超时
  当 读者检查隔离机制说明
  那么 章节说明子 Agent 失败不影响主 Agent 的继续运行（如有），以及失败结果如何返回给父 Agent

## 排除范围

- 不深入 Task 类型的内部实现（第 30 章）
- 不分析 forkSubagent/runAgent 执行循环（第 31 章）
- 不覆盖 Swarm 权限 Mailbox（第 32 章）
