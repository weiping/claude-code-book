# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个技术书籍写作仓库，包含三本关于 Claude Code 架构分析的电子书，均使用 **mdBook** 格式。

| 目录 | 书名 | 内容定位 |
|------|------|---------|
| `claude-code-dissection/` | 《深度解剖 Claude Code 的源码》 | 源码追踪线 + 工程模式提炼，11篇 42章 + 6篇附录 |
| `claude-code-harness-engineering/` | 《从 Claude Code 源码提炼的 Harness 工程模式》 | Harness 工程原则，8篇多章 |
| `claude-code-engineering-patterns/` | 《Claude Code 工程模式》 | Harness 工程模式总结，10篇 41章 + 6篇附录 |

## 每本书的目录结构

```
<book-dir>/
├── DESIGN.md          # 全局不变量：书的核心主张、结构规划（不得随意修改）
├── book/              # mdBook 项目根目录
│   ├── book.toml      # mdBook 配置
│   └── src/           # 书稿源文件
│       ├── SUMMARY.md # 目录（mdBook 必须文件）
│       ├── preface.md
│       ├── part1/     # 按篇分目录
│       │   └── ch01.md
│       └── ...
├── plans/             # 各章写作计划（ch01.plan 等）
└── specs/             # 各章内容规格（ch01.spec 等）
```

## 构建命令

```bash
# 在某本书的 book/ 目录下构建 HTML
cd claude-code-dissection/book && mdbook build

# 本地预览（带热重载）
cd claude-code-dissection/book && mdbook serve

# 检查书稿结构
cd claude-code-dissection/book && mdbook test
```

## 写作规范

### DESIGN.md 的地位
每本书的 `DESIGN.md` 是**全局不变量**，记录书的核心主张和结构规划，一旦确认不得修改。写作新章节前务必对照 DESIGN.md 确认方向。

### 文件命名
- 书稿：`src/partN/chNN.md`
- 计划：`plans/chNN.plan`（含章节骨架、前置阅读清单、场景列表）
- 规格：`specs/chNN.spec`（frontmatter 含 `spec: task`、`name:`、`tags:`，正文含意图和约束）
- 批次计划：`plans/batch.md`（全书工作量估算、分批执行顺序）

### 写作风格（按书区分）
每本书在 `plans/batch.md` 中指定全书统一的 `STYLE_ID`：

| 书 | 风格名 | 特征 |
|----|-------|------|
| `claude-code-dissection` | **autopsy**（解剖） | 以源码行号为证据，逐层拆解实现决策 |
| `claude-code-engineering-patterns` | **hunter**（猎手） | 跨文件多实例引用，聚焦工程模式的规律性 |
| `claude-code-harness-engineering` | 无固定 STYLE_ID | 原则提炼为主，论证为辅 |

通用约束（三本书均适用）：
- 正文不展示代码片段（"实证"类节除外）；源码仅作为隐含锚点
- 不使用括号内的源码路径；表格和 Mermaid 图内也不含源码路径
- 每章结尾提炼 2-3 条工程原则，格式：`原则 N.N：[原则名] — [一句话阐述]`
- 每章开头用"一句话主张"描述读完该章的收获

### SUMMARY.md 维护
新增章节必须同步更新 `book/src/SUMMARY.md`，否则 mdBook 不会渲染该章节。

### Mermaid 图表
`claude-code-dissection` 和 `claude-code-engineering-patterns` 通过 `book/src/theme/mermaid-init.js` 加载本地 `mermaid.min.js`，非 mdBook 原生支持。`claude-code-harness-engineering` 同样使用此方案。

## 构建脚本

`claude-code-engineering-patterns/` 和 `claude-code-dissection/` 下有辅助脚本（`claude-code-harness-engineering/` 无此脚本）：

```bash
build_pdf.py       # 将 mdBook HTML 输出合并渲染为 PDF
generate_cover.py  # 生成封面图片
```

## 核心参考资料

- `claude-code-harness-engineering/ARCHITECTURE_ANALYSIS.md`：Claude Code 技术架构完整分析（含 mermaid 架构图）
- `claude-code-harness-engineering/DESIGN.md`：Harness 工程书的完整章节规划
- `claude-code-engineering-patterns/HARNESS_ARCHITECTURE.md`：Harness 架构分析报告
- `claude-code-engineering-patterns/DESIGN.md`：工程模式书的完整章节规划
