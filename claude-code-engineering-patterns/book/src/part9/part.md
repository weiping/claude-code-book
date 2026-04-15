# 第九篇：Swarm——多智能体协作架构

> *目的：理解 Harness·多智能体子系统——从单 Agent 扩展到多 Agent 协作*

本篇追踪 Swarm 的完整架构：从 Leader/Teammate 生命周期出发，经过跨进程权限协商、三种后端选型，到达权限同步协议。

---

## 本章导航

- [第 33 章：Teammate 生命周期——Swarm 架构总览](ch33.md)
- [第 34 章：leaderPermissionBridge——跨进程权限协商模式](ch34.md)
- [第 35 章：三种 Teammate 后端——`in-process/tmux/auto` 的选型逻辑](ch35.md)
- [第 36 章：permissionSync——多智能体间的权限同步协议](ch36.md)
