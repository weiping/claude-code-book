spec: task
name: "第35章：Plugin 系统——DXT 包的生命周期"
tags: [book-chapter, part-9]
---

## 意图

本章解析 Claude Code 的 Plugin 系统。核心问题：DXT 插件包格式是什么？PluginInstallationManager 如何处理安装/升级/卸载？bundled plugins 与 marketplace plugins 有何不同？插件如何向运行时注入 hook？

## 约束

必须：
- 引用 src/plugins/PluginInstallationManager.ts 中的 install/uninstall 相关函数
- 引用 src/plugins/bundled/index.ts 中的 initBuiltinPlugins（约第20行）说明内置插件的初始化
- 引用 src/plugins/builtinPlugins.ts 说明 built-in 与 marketplace 插件的区分原则
- 解释 DXT（Desktop Extension）包格式：manifest.json + 代码文件的标准结构

禁止：
- 不得深入 Skill 系统（第 36 章范围，注释中明确说明两者分工）
- 不得深入 Hook 系统的触发机制（第 18 章范围）
- 不得分析具体 marketplace 插件的业务逻辑

## 已定决策

- 开篇问题："Plugin 和 Skill 都是扩展机制，为什么要有两套？DXT 格式解决什么问题？"
- 流程图展示 DXT 包安装生命周期：下载 → 校验 → 解压 → 注册 → hook 注入
- 源码引用格式：`src/plugins/PluginInstallationManager.ts:行号`

## 边界

### 允许修改
- book/src/part9/ch35.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 Skill 系统实现（第 36 章）

## 验收标准

场景: Plugin 与 Skill 的分工说清
  测试: verify_plugin_skill_separation
  假设 读者追问"为什么有了 Skill 还需要 Plugin"
  那么 章节引用 builtinPlugins.ts 的注释（"Not all bundled features should be built-in plugins"），解释 Plugin 用于用户可切换的功能扩展，Skill 用于 AI 能力注入

场景: DXT 包格式说明
  测试: verify_dxt_package_format
  假设 读者想创建一个 DXT 插件
  当 读者读完格式说明
  那么 章节描述 DXT 包的必要组成（manifest.json 的关键字段、代码入口），并说明安装时的校验要求

场景: 安装生命周期流程完整
  测试: verify_installation_lifecycle
  假设 读者追踪一个插件从下载到可用的完整流程
  当 读者阅读生命周期流程图
  那么 图中覆盖：下载/获取 → 包格式校验 → 文件解压到插件目录 → 注册到插件列表 → hook 注入五个阶段

场景: bundled 与 marketplace 区分说明
  测试: verify_bundled_vs_marketplace
  假设 读者追问"内置插件和从 marketplace 安装的有什么区别"
  那么 章节说明 bundled（代码在 src/plugins/bundled/ 中随二进制发布）vs marketplace（运行时下载安装）的差异

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 src/plugins/bundled/index.ts 中的 initBuiltinPlugins
  那么 约第20行存在该函数导出

场景: 插件安装失败时的处理
  测试: verify_install_failure_handling
  假设 DXT 包格式校验失败或网络下载中断
  当 读者检查错误处理说明
  那么 章节说明安装失败时的回滚策略（保留原有插件状态）和用户提示方式

## 排除范围

- 不深入 Skill 系统实现（第 36 章）
- 不覆盖 Hook 触发机制的底层实现（第 18 章）
- 不分析具体 marketplace 插件的业务功能
