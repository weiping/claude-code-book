# 第七篇：Hooks 引擎——Harness 的核心

> *目的：深入理解 Harness·Hooks 引擎子系统——独立的用户扩展接口，贯穿工具执行、会话生命周期和智能体协作全流程*

本篇从 Hook 事件全景出发，经过多态执行器设计、异步注册表实现、配置快照隔离，到达声明式钩子注册。

---

## 本章导航

- [第 24 章：20+ 事件的生命周期地图——Hooks 全景](ch24.md)
- [第 25 章：四种执行器——`command/prompt/agent/http` 的多态设计](ch25.md)
- [第 26 章：AsyncHookRegistry——异步钩子的注册、超时与并发控制](ch26.md)
- [第 27 章：hooksConfigSnapshot——配置快照隔离模式](ch27.md)
- [第 28 章：Frontmatter Hooks——Skill 与 Agent 的声明式钩子注册](ch28.md)
