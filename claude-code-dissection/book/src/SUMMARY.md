# 目录

- [序：为什么要解剖 Claude Code](preface.md)

---

## 第一篇：地基——总体架构与技术栈

- [第 1 章：运行时 Harness 全景——总体架构解析](part1/ch01.md)
- [第 2 章：技术栈选型——React/Ink + Bun + TypeScript 的工程逻辑](part1/ch02.md)
- [第 3 章：启动流水线的并发艺术](part1/ch03.md)
- [第 4 章：Feature Flag 的双层架构](part1/ch04.md)
- [第 5 章：Bootstrap 全局状态——进程的状态脊梁](part1/ch05.md)

---

## 第二篇：Agent 主循环

- [第 6 章：用户输入的三条分叉路](part2/ch06.md)
- [第 7 章：斜杠命令系统——内置命令的注册与执行](part2/ch07.md)
- [第 8 章：query.ts——单轮对话的原子循环](part2/ch08.md)
- [第 9 章：Query Engine——多轮编排与状态管理](part2/ch09.md)
- [第 10 章：运行模式状态机——Plan、Auto、Worktree 等模式的实现](part2/ch10.md)

---

## 第三篇：工具系统——AI 的手

- [第 11 章：Tool 接口与 buildTool 工厂](part3/ch11.md)
- [第 12 章：BashTool 解剖——最复杂工具的实现](part3/ch12.md)
- [第 13 章：AgentTool——递归智能体的工具接口](part3/ch13.md)
- [第 14 章：工具注册与条件加载](part3/ch14.md)

---

## 第四篇：安全和权限系统

- [第 15 章：权限系统的三层决策架构](part4/ch15.md)
- [第 16 章：YOLO 模式与 AI 分类器](part4/ch16.md)
- [第 17 章：PermissionRule 与规则引擎](part4/ch17.md)
- [第 18 章：Hooks 系统——生命周期拦截点](part4/ch18.md)

---

## 第五篇：提示词工程

- [第 19 章：系统提示的优先级堆叠与组装](part5/ch19.md)
- [第 20 章：CLAUDE.md 的发现、解析与注入](part5/ch20.md)
- [第 21 章：上下文组装——git 状态、工具描述与用户上下文的构建](part5/ch21.md)
- [第 22 章：模型自动选择——Opus、Sonnet 与 Haiku 的路由逻辑](part5/ch22.md)

---

## 第六篇：上下文工程

- [第 23 章：会话系统——标识、持久化与恢复](part6/ch23.md)
- [第 24 章：缓存系统——Prompt Cache 与 Context 压缩四策略](part6/ch24.md)
- [第 25 章：AutoCompact 与边界标记的实现](part6/ch25.md)
- [第 26 章：本地记忆系统——memdir 与 SessionMemory](part6/ch26.md)

---

## 第七篇：MCP 集成——可插拔的外部能力

- [第 27 章：MCP 客户端的三协议实现](part7/ch27.md)
- [第 28 章：MCP 认证——OAuth、JWT 与 xaa](part7/ch28.md)

---

## 第八篇：多智能体系统

- [第 29 章：多智能体架构总览——Swarm 的层次模型](part8/ch29.md)
- [第 30 章：Task 类型体系——三种执行模式的实现](part8/ch30.md)
- [第 31 章：Subagent 的生命周期——forkSubagent、runAgent 与内存隔离](part8/ch31.md)
- [第 32 章：Swarm 权限同步——沙箱中的信任传递](part8/ch32.md)

---

## 第九篇：高级功能

- [第 33 章：Effort、Fast Mode 与 Thinking——推理深度控制](part9/ch33.md)
- [第 34 章：跨会话记忆——extractMemories 与 teamMemorySync](part9/ch34.md)
- [第 35 章：Plugin 系统——DXT 包的生命周期](part9/ch35.md)
- [第 36 章：Skill 系统——Markdown 封装的 AI 能力](part9/ch36.md)
- [第 37 章：未发布的功能总线——Feature Flag 背后的实验特性](part9/ch37.md)

---

## 第十篇：TUI 层——在终端里渲染 React

- [第 38 章：Ink 的自建 Reconciler](part10/ch38.md)
- [第 39 章：termio——终端原语的解析与发送](part10/ch39.md)

---

## 第十一篇：工程原则——从实现提炼的设计智慧

- [第 40 章：并发优先的启动哲学](part11/ch40.md)
- [第 41 章：安全性的三道防线](part11/ch41.md)
- [第 42 章：可扩展性的四种机制](part11/ch42.md)
