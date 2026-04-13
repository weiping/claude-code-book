spec: task
name: "第38章：Ink 的自建 Reconciler"
tags: [book-chapter, part-10]
---

## 意图

本章解析 Ink 如何在没有 DOM 的终端中运行 React。核心问题：react-reconciler 的 host config 如何将 React 虚拟 DOM 映射到终端字符网格？Yoga layout 引擎如何在终端中实现 Flexbox？render-node-to-output.ts 如何将节点树合成为字符输出？

## 约束

必须：
- 引用 src/ink/reconciler.ts 中的 createReconciler 调用（约第224行）、commitMount（约第401行）和 dispatcher 定义（约第187行）
- 引用 src/ink/renderer.ts 中的 createRenderer 函数和 RenderOptions 类型（约第15行）
- 引用 src/ink/render-node-to-output.ts 说明节点树到字符输出的转换
- 解释 react-reconciler 的 host config 核心概念：createInstance/appendChildToContainer/commitUpdate 的用途

禁止：
- 不得深入 termio 原语层的解析（第 39 章范围）
- 不得深入 React 内部 Fiber 算法（只在接口层描述 reconciler 的 host config）
- 不得重复第 2 章的技术选型分析

## 已定决策

- 开篇问题："React 用 reconciler 操作 DOM，Ink 没有 DOM——它的 reconciler 操作什么？"
- ASCII 图展示：React Fiber → Ink reconciler → Yoga 节点树 → 字符网格输出 的转换链
- 源码引用格式：`src/ink/reconciler.ts:行号`

## 边界

### 允许修改
- book/src/part10/ch38.md

### 禁止做
- 不修改 DESIGN.md 或其他章节文件
- 不深入 React Fiber 内部调度算法

## 验收标准

场景: host config 核心方法说明
  测试: verify_host_config_methods
  假设 读者想了解 Ink reconciler 如何接管 React 的 DOM 操作
  当 读者查看 host config 方法说明
  那么 章节覆盖至少三个核心方法：createInstance（创建终端节点）、commitUpdate（更新节点属性）、appendChildToContainer（挂载节点），每个有用途说明

场景: Yoga layout 在终端中的作用说明
  测试: verify_yoga_layout_in_terminal
  假设 读者追问"Box 组件的 flexDirection 在终端里怎么生效"
  那么 章节解释 Yoga 的 Flexbox 计算如何产生字符列/行的布局数值，以及这些数值如何被 render-node-to-output 使用

场景: 字符输出合成流程说明
  测试: verify_character_output_synthesis
  假设 读者追踪一个 Text 组件从 React 渲染到终端显示的完整路径
  那么 章节说明：React render → reconciler commitMount → Yoga 计算 → renderNodeToOutput → Screen 输出字符网格的关键步骤

场景: 帧率控制和重绘优化说明
  测试: verify_frame_rate_control
  假设 读者追问"Ink 是每次状态变化都重新渲染整个终端吗"
  那么 章节说明 Ink 的帧率控制机制（记录 lastYogaMs、lastCommitMs）和增量更新策略，避免频繁全屏重绘

场景: 源码引用可验证
  测试: verify_source_citations_exist
  假设 读者查找 reconciler.ts 中的 createReconciler 调用
  那么 约第224行存在 const reconciler = createReconciler<...>({...}) 调用

场景: reconciler 初始化失败时的处理
  测试: verify_reconciler_init_failure
  假设 Yoga 布局引擎初始化失败（如 WASM 加载失败）
  当 读者检查错误处理说明
  那么 章节说明 Yoga 初始化失败时 Ink 的降级行为（如使用简单列布局）或直接抛出错误

## 排除范围

- 不深入 termio ANSI 解析（第 39 章）
- 不深入 React Fiber 的 Concurrent Mode 调度算法
- 不覆盖 Ink 的 devtools 集成（src/ink/devtools.ts）
