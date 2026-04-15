# Summary

[前言](preface.md)

# 第一篇：地图与地基

- [篇章导览](part1/part.md)
- [第 1 章：系统总体架构——Claude Code 的结构地图](part1/ch01.md)
- [第 2 章：Bootstrap 与全局状态——50+ 函数背后的单例设计](part1/ch02.md)
- [第 3 章：构建时特性开关——`bun:bundle feature()` 的死代码消除](part1/ch03.md)

# 第二篇：交互层——用户如何与系统对话

- [篇章导览](part2/part.md)
- [第 4 章：CLI 入口与模式分叉——从 main.tsx 到 REPL / Headless / SDK](part2/ch04.md)
- [第 5 章：REPL 界面架构——5000 行组件的交互设计](part2/ch05.md)
- [第 6 章：用户输入分流——`processUserInput` 的路由决策树](part2/ch06.md)
- [第 7 章：斜杠命令系统——103 个命令的注册、加载与执行](part2/ch07.md)
- [第 8 章：IDE 集成——Bridge 协议与 LSP 服务](part2/ch08.md)

# 第三篇：Harness 核心循环——查询引擎

- [篇章导览](part3/part.md)
- [第 9 章：QueryEngine 主循环——工具调用的编排逻辑](part3/ch09.md)
- [第 10 章：流式响应管道——异步生成器的工程应用](part3/ch10.md)

# 第四篇：模型层——API 通信与推理控制

- [篇章导览](part4/part.md)
- [第 11 章：模型自动选择——Opus、Sonnet 与 Haiku 的路由逻辑](part4/ch11.md)
- [第 12 章：推理深度控制——Effort、Fast Mode 与 Thinking 的三轴设计](part4/ch12.md)
- [第 13 章：API 通信层——Anthropic 客户端、重试机制与提示词缓存策略](part4/ch13.md)

# 第五篇：Tool 系统——可扩展的工具协议

- [篇章导览](part5/part.md)
- [第 14 章：Tool 接口契约——`buildTool()` 工厂与 Zod 输入验证](part5/ch14.md)
- [第 15 章：权限决策树——PermissionMode 的四层设计](part5/ch15.md)
- [第 16 章：AI 分类器替代规则引擎——yolo-classifier 的设计哲学](part5/ch16.md)
- [第 17 章：MCP 工具协议——把第三方工具变成一等公民](part5/ch17.md)
- [第 18 章：Skill 系统——声明式能力包的加载与执行](part5/ch18.md)

# 第六篇：上下文工程——控制 AI 的信息视野

- [篇章导览](part6/part.md)
- [第 19 章：提示词装配——`fetchSystemPromptParts()` 的分层组装](part6/ch19.md)
- [第 20 章：CLAUDE.md 注入——层级化指令的加载与优先级](part6/ch20.md)
- [第 21 章：会话持久化——转录、快照与断点续写](part6/ch21.md)
- [第 22 章：AutoCompact 与上下文折叠——窗口压缩的触发机制](part6/ch22.md)
- [第 23 章：记忆系统——本地、跨会话与团队记忆的三层架构](part6/ch23.md)

# 第七篇：Hooks 引擎——Harness 的核心

- [篇章导览](part7/part.md)
- [第 24 章：20+ 事件的生命周期地图——Hooks 全景](part7/ch24.md)
- [第 25 章：四种执行器——`command/prompt/agent/http` 的多态设计](part7/ch25.md)
- [第 26 章：AsyncHookRegistry——异步钩子的注册、超时与并发控制](part7/ch26.md)
- [第 27 章：hooksConfigSnapshot——配置快照隔离模式](part7/ch27.md)
- [第 28 章：Frontmatter Hooks——Skill 与 Agent 的声明式钩子注册](part7/ch28.md)

# 第八篇：Task 系统——后台执行的基础设施

- [篇章导览](part8/part.md)
- [第 29 章：7 种任务类型的状态机——Task 系统设计](part8/ch29.md)
- [第 30 章：LocalAgentTask——子 Agent 的进程模型与 I/O 协议](part8/ch30.md)
- [第 31 章：RemoteAgentTask——远程任务的通信架构](part8/ch31.md)
- [第 32 章：DreamTask——后台自主执行的设计意图](part8/ch32.md)

# 第九篇：Swarm——多智能体协作架构

- [篇章导览](part9/part.md)
- [第 33 章：Teammate 生命周期——Swarm 架构总览](part9/ch33.md)
- [第 34 章：leaderPermissionBridge——跨进程权限协商模式](part9/ch34.md)
- [第 35 章：三种 Teammate 后端——`in-process/tmux/auto` 的选型逻辑](part9/ch35.md)
- [第 36 章：permissionSync——多智能体间的权限同步协议](part9/ch36.md)

# 第十篇：安全权限——Agent 行为的边界工程

- [篇章导览](part10/part.md)
- [第 37 章：权限系统全景——拦截→规则→确认的三层防线](part10/ch37.md)
- [第 38 章：PermissionRule 规则引擎——`allowedTools` 的 glob 匹配与优先级链](part10/ch38.md)
- [第 39 章：权限处理器三态——`interactive/coordinator/swarmWorker` 的策略差异](part10/ch39.md)
- [第 40 章：信任对话与拒绝追踪——用户决策的持久化与安全审计](part10/ch40.md)

# 第十一篇：Marketplace 与 Plugins——生态扩展架构

- [篇章导览](part11/part.md)
- [第 41 章：Plugin 生命周期——发现、安装、更新与卸载](part11/ch41.md)
- [第 42 章：Marketplace 协议——官方注册表与第三方源](part11/ch42.md)
- [第 43 章：Plugin 包结构——目录约定、`package.json` 契约与沙箱边界](part11/ch43.md)

# 第十二篇：模式提炼——工程启示录

- [篇章导览](part12/part.md)
- [第 44 章：Harness 工程模式图谱——12 个可复用设计模式](part12/ch44.md)
- [第 45 章：从 CLI 到 Agent 平台——架构跃迁的路线图](part12/ch45.md)

# 附录

- [附录 A：Hook 事件速查表](appendix-a.md)
- [附录 B：工具权限矩阵](appendix-b.md)
- [附录 C：关键类型索引](appendix-c.md)
- [附录 D：环境变量参考](appendix-d.md)
- [附录 E：Feature Flag 完整清单](appendix-e.md)
- [附录 F：术语表](appendix-f.md)
