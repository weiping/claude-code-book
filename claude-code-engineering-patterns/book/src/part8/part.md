# 第八篇：Task 系统——后台执行的基础设施

> *目的：理解 Harness·任务编排子系统——7 种后台任务的生命周期管理*

本篇从 7 种任务类型的统一状态机出发，经过子进程 Agent 隔离、远程任务通信架构，到达自主执行的 DreamTask。

---

## 本章导航

- [第 29 章：7 种任务类型的状态机——Task 系统设计](ch29.md)
- [第 30 章：LocalAgentTask——子 Agent 的进程模型与 I/O 协议](ch30.md)
- [第 31 章：RemoteAgentTask——远程任务的通信架构](ch31.md)
- [第 32 章：DreamTask——后台自主执行的设计意图](ch32.md)
