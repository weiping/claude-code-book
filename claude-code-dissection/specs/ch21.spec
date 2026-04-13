spec: task
name: "第21章：上下文组装——git 状态、工具描述与用户上下文的构建"
tags: [book-chapter, part-5]
---

## 意图

本章解析 Claude Code 如何将运行环境信息编织进 API 请求。核心问题：getUserContext 和 getSystemContext 分别包含什么？git status 如何被采集并截断？这些上下文为什么是 API cache-key 的一部分？

## 约束

必须：
- 引用 src/context.ts 中的 getGitStatus（约第36行）、getSystemContext（约第116行）、getUserContext（约第155行）
- 引用 src/utils/queryContext.ts 中的 fetchSystemPromptParts，展示其如何组合三部分（systemPrompt/userContext/systemContext）
- 说明 MAX_STATUS_CHARS（约第20行）对 git status 的截断限制
- 解释"cache-key 前缀"的含义：相同前缀的请求可复用 Anthropic prompt cache

禁止：
- 不得深入 CLAUDE.md 发现逻辑（第 20 章范围）
- 不得深入 prompt cache 的技术实现（第 24 章范围）
- 不得深入工具描述的生成方式（第 11 章范围）

## 已定决策

- 开篇问题："Claude 为什么知道你在哪个 git 分支、当前目录是什么？这些信息怎么进入对话？"
- ASCII 流程图展示 fetchSystemPromptParts 的三路并发采集
- 源码引用格式：`src/context.ts:行号`

## 边界

### 允许修改
- book/src/part5/ch21.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 prompt cache 技术（第 24 章）

## 验收标准

场景: getUserContext 与 getSystemContext 分工说清
  测试: verify_context_separation
  假设 读者追问"这两个 context 有什么区别"
  当 读者读完分工说明
  那么 章节清楚描述：getUserContext 包含用户相关信息（工作目录、git 状态），getSystemContext 包含系统级信息（平台、版本），并引用源码

场景: git status 采集和截断说明
  测试: verify_git_status_collection
  假设 读者追问"git status 输出很长怎么处理"
  那么 章节说明 MAX_STATUS_CHARS 的截断限制值，以及截断后如何标注（不引起 Claude 误解）

场景: cache-key 前缀概念说明
  测试: verify_cache_key_prefix_explained
  假设 读者追问"为什么要把 git 状态放进 cache-key"
  那么 章节解释：systemPrompt + userContext + systemContext 构成 cache-key 前缀，相同前缀的请求可复用 Anthropic 侧的 prompt cache，降低 token 成本

场景: memoize 缓存机制说明
  测试: verify_context_memoize
  假设 读者追问"每次对话都重新采集 git status 吗"
  那么 章节说明 getGitStatus 使用 memoize 缓存，并解释缓存失效的触发条件

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 context.ts 中的 getGitStatus
  那么 约第36行存在 export const getGitStatus = memoize(async () => ...) 定义

场景: git 不可用时的降级
  测试: verify_non_git_repo_handling
  假设 当前目录不是 git 仓库
  当 读者检查非 git 场景的处理
  那么 章节说明 getIsGit() 返回 false 时 getGitStatus 返回 null，上下文中省略 git 相关信息

## 排除范围

- 不深入 CLAUDE.md 文件的发现（第 20 章）
- 不深入 prompt cache 的 API 实现（第 24 章）
- 不覆盖工具描述的 description() 生成（第 11 章）
