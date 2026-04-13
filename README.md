# claude-code-book

三本关于 Claude Code 工程架构的技术电子书，以 Claude Code v2.1.88 的 ~51 万行 TypeScript 源码为样本，从不同维度解析其内部设计。

---

## 三本书

### 《深度解剖 Claude Code 源码》
**目录：** `claude-code-dissection/`　**规模：** 11 篇 42 章 + 6 篇附录

官方文档告诉你怎么用 `claude` 命令，但从不解释：为什么启动序列要并行发射三个预热任务？为什么工具系统设计了"三元安全模型"？上下文窗口管理为什么需要四种压缩策略？

本书目标是**逆向还原 Harness 的工程内核**。从 `src/main.tsx` 第一行出发，沿着真实代码路径，逐一解剖每个子系统的数据结构、控制流、并发模型和设计权衡。全书 11 篇 42 章 + 6 篇附录。

---

### 《从 Claude Code 源码提炼的 Harness 工程模式》
**目录：** `claude-code-harness-engineering/`　**规模：** 8 篇

不教你使用 Claude Code，而教你**像 Anthropic 工程师一样思考 Harness 设计**。

每一条工程原则都有源码锚点，但全书不展示代码片段——代码是原材料，原则才是产物。读完这本书，你将理解 Anthropic 工程师在"什么应该由模型管理，什么必须由 Harness 控制"这个问题上的每一个具体作答。

---

### 《Claude Code 工程模式》
**目录：** `claude-code-engineering-patterns/`　**规模：** 10 篇 41 章 + 6 篇附录

这不是一个 CLI。这是一套 **Agent Harness**——把不可控的 AI 行为变成可编排、可拦截、可扩展工程管道的基础设施。

本书从源码提炼可命名的 Harness 工程模式，每章遵循同一结构：先描述一个"猎人发现"，然后展开完整追踪路径，最后提炼可移植的工程模式。全书 10 篇 41 章 + 6 篇附录。

---

## 构建

所有书籍均使用 [mdBook](https://rust-lang.github.io/mdBook/) 格式。

```bash
# 安装 mdBook
cargo install mdbook

# 构建 HTML（在各书的 book/ 目录下执行）
cd claude-code-dissection/book && mdbook build

# 本地预览（带热重载，默认 http://localhost:3000）
cd claude-code-dissection/book && mdbook serve

## 仓库说明

- 每本书的 `DESIGN.md` 是**全局不变量**，记录核心主张和章节规划，写作阶段不得修改
- `book/src/SUMMARY.md` 是 mdBook 必须文件，新增章节必须同步更新
- `plans/batch.md` 是全书写作批次计划，记录各章工作量估算和分批执行顺序


