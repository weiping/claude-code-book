spec: task
name: "第36章：Skill 系统——Markdown 封装的 AI 能力"
tags: [book-chapter, part-9]
---

## 意图

本章解析 Claude Code 的 Skill 系统。核心问题：Skill 如何将 Markdown 文档打包为可调用的 AI 能力单元？SkillTool 的执行路径是什么？EXPERIMENTAL_SKILL_SEARCH flag 开启时语义检索如何工作？

## 约束

必须：
- 引用 src/skills/loadSkillsDir.ts 中的 createSkillCommand（约第270行）、parseSkillFrontmatterFields（约第185行）、getSkillDirCommands（约第638行）
- 引用 src/tools/SkillTool/SkillTool.ts 中的 SkillTool 定义和 recordSkillUsage 调用
- 引用 src/services/skillSearch/ 目录中的 localSearch.ts 或 featureCheck.ts 说明语义检索
- 解释 Skill frontmatter 的关键字段（name、description、trigger 等）及其在发现机制中的作用

禁止：
- 不得重复第 35 章的 Plugin 安装生命周期
- 不得深入 MCP Skills 的协议层（第 27 章范围）
- 不得分析 bundled Skills 的具体内容（src/skills/bundled/）

## 已定决策

- 开篇问题："Skill 和 slash 命令（/xxx）有什么区别？Skill 里的 Markdown 是怎么变成 Claude 能执行的指令的？"
- ASCII 示例展示一个最小 Skill 的 Markdown 结构（frontmatter + 指令正文）
- 源码引用格式：`src/skills/loadSkillsDir.ts:行号`

## 边界

### 允许修改
- book/src/part9/ch36.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 MCP Skills 协议（第 27 章）

## 验收标准

场景: Skill frontmatter 字段说明
  测试: verify_skill_frontmatter_fields
  假设 读者想创建一个 Skill
  当 读者读完 frontmatter 字段说明
  那么 章节展示 parseSkillFrontmatterFields 解析的关键字段（name/description/trigger 等），有 ASCII 示例说明每个字段用途

场景: createSkillCommand 转换机制说明
  测试: verify_skill_to_command_conversion
  假设 读者追问"Markdown 文件怎么变成可执行的命令"
  那么 章节解释 createSkillCommand 将 Skill 文件转换为 Command 对象的过程，包括 description 注入和 execute 函数绑定

场景: EXPERIMENTAL_SKILL_SEARCH 语义检索说明
  测试: verify_skill_search_mechanism
  假设 读者追问"有几百个 Skill 时模型如何找到正确的"
  那么 章节说明 feature('EXPERIMENTAL_SKILL_SEARCH') 开启时的语义检索路径（localSearch 或远程检索），与关键词匹配的区别

场景: Skill 使用追踪说明
  测试: verify_skill_usage_tracking
  假设 读者追问"Claude Code 怎么知道哪些 Skill 被频繁使用"
  那么 章节解释 recordSkillUsage 的调用时机和数据用途（改进推荐排序）

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 loadSkillsDir.ts 中的 createSkillCommand
  那么 约第270行存在该函数，将 Skill 文件转换为 Command 对象

场景: Skill 文件语法错误时的处理
  测试: verify_skill_parse_error_handling
  假设 Skill 的 Markdown frontmatter 格式错误
  当 读者检查错误处理说明
  那么 章节说明解析失败时的行为（跳过该 Skill，记录警告），不影响其他 Skill 的加载

## 排除范围

- 不重复 Plugin 安装生命周期（第 35 章）
- 不深入 MCP Skills 的协议包装（第 27 章）
- 不分析 bundled Skills 的具体指令内容（src/skills/bundled/）
