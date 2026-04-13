spec: task
name: "第18章：Hooks 系统——生命周期拦截点"
tags: [book-chapter, part-4]
---

## 意图

本章解析 Hooks 系统。核心问题：AsyncHookRegistry 如何注册和轮询异步 Hook？pre/post sampling hooks 在哪个时机触发？ssrfGuard 如何防止恶意 HTTP 请求？

## 约束

必须：
- 引用 src/utils/hooks/AsyncHookRegistry.ts 中的 registerPendingAsyncHook（约第30行）和 checkForAsyncHookResponses（约第113行）
- 引用 src/utils/hooks/postSamplingHooks.ts 展示 post-sampling hook 触发时机
- 引用 src/utils/hooks/ssrfGuard.ts 中的 isBlockedAddress（约第42行）
- 用表格列出主要 Hook 事件类型及其触发时机

禁止：
- 不得深入 Plugin hook 的注入（第 35 章范围）
- 不得深入 Skill hook 的注入（第 36 章范围）
- 不得重复第 15 章的权限决策流程

## 已定决策

- 开篇："Claude 执行完一个工具后，有没有机会'钩住'这个结果做后处理？"
- 源码引用格式：`src/utils/hooks/AsyncHookRegistry.ts:行号`

## 边界

### 允许修改
- book/src/part4/ch18.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件

## 验收标准

场景: Hook 事件类型表格完整
  测试: verify_hook_event_types_table
  假设 读者想了解有哪些拦截点可用
  那么 表格覆盖至少 4 种 Hook 类型，每种有触发时机说明

场景: 异步 Hook 注册流程说明
  测试: verify_async_hook_registration
  假设 读者想注册一个在工具调用后触发的 Hook
  那么 能理解 registerPendingAsyncHook 的参数和 checkForAsyncHookResponses 的轮询机制

场景: ssrfGuard 防护说明
  测试: verify_ssrf_guard_explained
  假设 读者追问 Hook 向外部服务发请求有没有安全限制
  那么 章节引用 ssrfGuard.ts，解释它如何检测并阻止 SSRF 攻击

场景: post-sampling hook 触发时机说明
  测试: verify_post_sampling_timing
  假设 读者追问 post-sampling hook 在什么时候触发
  那么 章节说明在 LLM 响应接收完毕后触发

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 AsyncHookRegistry.ts 中的 registerPendingAsyncHook
  那么 约第30行存在该函数定义

场景: Hook 超时处理
  测试: verify_hook_timeout_handling
  假设 注册的 Hook 执行超时
  那么 章节说明超时后的行为

## 排除范围

- 不深入 Plugin hook 注入机制（第 35 章）
- 不深入 Skill hook 注入（第 36 章）
- 不重复权限决策流程（第 15 章）
