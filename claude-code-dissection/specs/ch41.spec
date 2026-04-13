spec: task
name: "第41章：安全性的三道防线"
tags: [book-chapter, part-11]
---

## 意图

本章系统提炼 Claude Code 的安全防御架构。核心问题：从工具三元安全模型、权限三层决策、到 SSRF 防护和沙箱隔离——这些防线在架构上如何互补？"纵深防御"原则在 AI Agent 场景下的独特挑战是什么？

## 约束

必须：
- 引用 src/Tool.ts 中的 isReadOnly/isDestructive/interruptBehavior 三元安全模型（约第404-416行）作为第一道防线的代表
- 引用 src/utils/hooks/ssrfGuard.ts 中的 ssrfGuardedLookup（约第216行）说明 SSRF 防护
- 引用 src/utils/sandbox/sandbox-adapter.ts 说明沙箱隔离层
- 绘制三道防线的层次图：工具层（三元模型）→ 权限层（三层决策）→ 运行时层（SSRF/沙箱）

禁止：
- 不得重复各章节的实现细节（用交叉引用代替）
- 不得分析 secretScanner 的具体检测规则（安全敏感）
- 不得给出绕过任何防线的方法

## 已定决策

- 本章为工程原则提炼章，每道防线用一节，每节有"设计动机 → 实现 → 局限性"三段式
- 开篇问题："为什么 AI Agent 的安全问题比普通程序更难？三道防线各解决什么威胁？"
- 源码引用格式：`src/Tool.ts:行号`（每道防线引用代表性文件）

## 边界

### 允许修改
- book/src/part11/ch41.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不给出安全绕过路径

## 验收标准

场景: 三道防线层次图正确
  测试: verify_three_defense_layers_diagram
  假设 读者阅读层次图
  当 读者追踪一个危险操作的拦截路径
  那么 图中展示：第一道（工具层：isDestructive 触发警告）→ 第二道（权限层：三层决策拦截）→ 第三道（运行时层：沙箱隔离/SSRF 防护），每层有代表性源码引用

场景: AI Agent 独特安全挑战说明
  测试: verify_ai_agent_security_challenges
  假设 读者追问"AI Agent 的安全问题和普通程序有什么不同"
  那么 章节给出至少两个 AI Agent 特有的安全挑战（如：prompt injection 可绕过工具层规则、Agent 行为不可完全预测）

场景: SSRF 防护的必要性说明
  测试: verify_ssrf_protection_rationale
  假设 读者追问"为什么需要 SSRF 防护"
  那么 章节解释恶意 MCP 服务器或 Hook 可能发起内网请求，ssrfGuardedLookup 如何阻止对私有 IP 的访问，引用源码行号

场景: 每道防线的局限性说明
  测试: verify_each_layer_limitations
  假设 读者追问"这三道防线能防住所有攻击吗"
  那么 章节对每道防线都有一句局限性说明（不可完全防止的威胁），体现诚实的安全观

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 Tool.ts 中的 isDestructive 定义
  那么 约第406行存在 isDestructive? 可选方法定义，标注"不可逆操作"语义

场景: 防线失效时的降级行为
  测试: verify_defense_failure_degradation
  假设 其中一道防线（如沙箱）无法启动
  当 读者检查降级行为
  那么 章节说明防线失效时系统的降级策略（保守拒绝 vs 允许用户知情选择继续），引用相关代码

## 排除范围

- 不重复各防线的实现细节（用"详见第 X 章"代替）
- 不展示 secretScanner 的具体检测规则（安全敏感）
- 不提供任何绕过防线的方法或路径
