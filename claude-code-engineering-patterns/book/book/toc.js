// Populate the sidebar
//
// This is a script, and not included directly in the page, to control the total size of the book.
// The TOC contains an entry for each page, so if each page includes a copy of the TOC,
// the total size of the page becomes O(n**2).
class MDBookSidebarScrollbox extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        this.innerHTML = '<ol class="chapter"><li class="chapter-item expanded affix "><a href="preface.html">前言</a></li><li class="chapter-item expanded affix "><li class="part-title">第一篇：地图与地基</li><li class="chapter-item expanded "><a href="part1/part.html"><strong aria-hidden="true">1.</strong> 篇章导览</a></li><li class="chapter-item expanded "><a href="part1/ch01.html"><strong aria-hidden="true">2.</strong> 第 1 章：系统总体架构与技术栈——Claude Code 的结构地图</a></li><li class="chapter-item expanded "><a href="part1/ch02.html"><strong aria-hidden="true">3.</strong> 第 2 章：Bootstrap 与全局状态——50+ 函数背后的单例设计</a></li><li class="chapter-item expanded "><a href="part1/ch03.html"><strong aria-hidden="true">4.</strong> 第 3 章：构建时特性开关——bun:bundle feature() 的死代码消除</a></li><li class="chapter-item expanded affix "><li class="part-title">第二篇：查询引擎——从用户输入到 AI 响应</li><li class="chapter-item expanded "><a href="part2/part.html"><strong aria-hidden="true">5.</strong> 篇章导览</a></li><li class="chapter-item expanded "><a href="part2/ch04.html"><strong aria-hidden="true">6.</strong> 第 4 章：用户输入分流——processUserInput 的路由决策树</a></li><li class="chapter-item expanded "><a href="part2/ch05.html"><strong aria-hidden="true">7.</strong> 第 5 章：斜杠命令系统——103 个命令的注册、加载与执行</a></li><li class="chapter-item expanded "><a href="part2/ch06.html"><strong aria-hidden="true">8.</strong> 第 6 章：模型自动选择——Opus、Sonnet 与 Haiku 的路由逻辑</a></li><li class="chapter-item expanded "><a href="part2/ch07.html"><strong aria-hidden="true">9.</strong> 第 7 章：Effort、Fast Mode 与 Thinking——推理深度控制的三轴</a></li><li class="chapter-item expanded "><a href="part2/ch08.html"><strong aria-hidden="true">10.</strong> 第 8 章：QueryEngine 主循环——工具调用的编排逻辑</a></li><li class="chapter-item expanded "><a href="part2/ch09.html"><strong aria-hidden="true">11.</strong> 第 9 章：流式响应管道——异步生成器的工程应用</a></li><li class="chapter-item expanded affix "><li class="part-title">第三篇：Tool 系统——可扩展的工具协议</li><li class="chapter-item expanded "><a href="part3/part.html"><strong aria-hidden="true">12.</strong> 篇章导览</a></li><li class="chapter-item expanded "><a href="part3/ch10.html"><strong aria-hidden="true">13.</strong> 第 10 章：Tool 接口契约——buildTool() 工厂与 Zod 输入验证</a></li><li class="chapter-item expanded "><a href="part3/ch11.html"><strong aria-hidden="true">14.</strong> 第 11 章：权限决策树——PermissionMode 的四层设计</a></li><li class="chapter-item expanded "><a href="part3/ch12.html"><strong aria-hidden="true">15.</strong> 第 12 章：AI 分类器替代规则引擎——yolo-classifier 的设计哲学</a></li><li class="chapter-item expanded "><a href="part3/ch13.html"><strong aria-hidden="true">16.</strong> 第 13 章：MCP 工具协议——把第三方工具变成一等公民</a></li><li class="chapter-item expanded "><a href="part3/ch14.html"><strong aria-hidden="true">17.</strong> 第 14 章：Skill 系统——声明式能力包的加载与执行</a></li><li class="chapter-item expanded affix "><li class="part-title">第四篇：上下文工程——控制 AI 的信息视野</li><li class="chapter-item expanded "><a href="part4/part.html"><strong aria-hidden="true">18.</strong> 篇章导览</a></li><li class="chapter-item expanded "><a href="part4/ch15.html"><strong aria-hidden="true">19.</strong> 第 15 章：提示词装配——fetchSystemPromptParts() 的分层组装</a></li><li class="chapter-item expanded "><a href="part4/ch16.html"><strong aria-hidden="true">20.</strong> 第 16 章：CLAUDE.md 注入——层级化指令的加载与优先级</a></li><li class="chapter-item expanded "><a href="part4/ch17.html"><strong aria-hidden="true">21.</strong> 第 17 章：会话持久化——转录、快照与断点续写</a></li><li class="chapter-item expanded "><a href="part4/ch18.html"><strong aria-hidden="true">22.</strong> 第 18 章：AutoCompact 与上下文折叠——窗口压缩的触发机制</a></li><li class="chapter-item expanded "><a href="part4/ch19.html"><strong aria-hidden="true">23.</strong> 第 19 章：记忆系统——本地、跨会话与团队记忆的三层架构</a></li><li class="chapter-item expanded affix "><li class="part-title">第五篇：Hooks 引擎——Harness 的核心</li><li class="chapter-item expanded "><a href="part5/part.html"><strong aria-hidden="true">24.</strong> 篇章导览</a></li><li class="chapter-item expanded "><a href="part5/ch20.html"><strong aria-hidden="true">25.</strong> 第 20 章：20+ 事件的生命周期地图——Hooks 全景</a></li><li class="chapter-item expanded "><a href="part5/ch21.html"><strong aria-hidden="true">26.</strong> 第 21 章：四种执行器——command/prompt/agent/http 的多态设计</a></li><li class="chapter-item expanded "><a href="part5/ch22.html"><strong aria-hidden="true">27.</strong> 第 22 章：AsyncHookRegistry——异步钩子的注册、超时与并发控制</a></li><li class="chapter-item expanded "><a href="part5/ch23.html"><strong aria-hidden="true">28.</strong> 第 23 章：配置快照隔离——会话内行为一致性保证</a></li><li class="chapter-item expanded "><a href="part5/ch24.html"><strong aria-hidden="true">29.</strong> 第 24 章：声明式钩子注册——从 CLAUDE.md 到执行器的绑定链路</a></li><li class="chapter-item expanded affix "><li class="part-title">第六篇：Task 系统——后台执行的基础设施</li><li class="chapter-item expanded "><a href="part6/part.html"><strong aria-hidden="true">30.</strong> 篇章导览</a></li><li class="chapter-item expanded "><a href="part6/ch25.html"><strong aria-hidden="true">31.</strong> 第 25 章：7 种任务类型的状态机——Task 系统设计</a></li><li class="chapter-item expanded "><a href="part6/ch26.html"><strong aria-hidden="true">32.</strong> 第 26 章：LocalAgentTask——子 Agent 的进程模型与 I/O 协议</a></li><li class="chapter-item expanded "><a href="part6/ch27.html"><strong aria-hidden="true">33.</strong> 第 27 章：RemoteAgentTask——远程任务的通信架构</a></li><li class="chapter-item expanded "><a href="part6/ch28.html"><strong aria-hidden="true">34.</strong> 第 28 章：DreamTask——后台自主执行的设计意图</a></li><li class="chapter-item expanded affix "><li class="part-title">第七篇：Swarm——多智能体协作架构</li><li class="chapter-item expanded "><a href="part7/part.html"><strong aria-hidden="true">35.</strong> 篇章导览</a></li><li class="chapter-item expanded "><a href="part7/ch29.html"><strong aria-hidden="true">36.</strong> 第 29 章：Teammate 生命周期——Swarm 架构总览</a></li><li class="chapter-item expanded "><a href="part7/ch30.html"><strong aria-hidden="true">37.</strong> 第 30 章：leaderPermissionBridge——跨进程权限协商模式</a></li><li class="chapter-item expanded "><a href="part7/ch31.html"><strong aria-hidden="true">38.</strong> 第 31 章：三种 Teammate 后端——in-process/tmux/auto 的选型逻辑</a></li><li class="chapter-item expanded "><a href="part7/ch32.html"><strong aria-hidden="true">39.</strong> 第 32 章：permissionSync——多智能体间的权限同步协议</a></li><li class="chapter-item expanded affix "><li class="part-title">第八篇：安全和权限系统——Agent 行为的边界工程</li><li class="chapter-item expanded "><a href="part8/part.html"><strong aria-hidden="true">40.</strong> 篇章导览</a></li><li class="chapter-item expanded "><a href="part8/ch33.html"><strong aria-hidden="true">41.</strong> 第 33 章：权限系统全景——拦截→规则→确认的三层防线</a></li><li class="chapter-item expanded "><a href="part8/ch34.html"><strong aria-hidden="true">42.</strong> 第 34 章：PermissionRule 规则引擎——allowedTools 的 glob 匹配与优先级链</a></li><li class="chapter-item expanded "><a href="part8/ch35.html"><strong aria-hidden="true">43.</strong> 第 35 章：权限处理器三态——interactive/coordinator/swarmWorker 的策略差异</a></li><li class="chapter-item expanded "><a href="part8/ch36.html"><strong aria-hidden="true">44.</strong> 第 36 章：信任对话与拒绝追踪——用户决策的持久化与安全审计</a></li><li class="chapter-item expanded affix "><li class="part-title">第九篇：Marketplace 与 Plugins——生态扩展架构</li><li class="chapter-item expanded "><a href="part9/part.html"><strong aria-hidden="true">45.</strong> 篇章导览</a></li><li class="chapter-item expanded "><a href="part9/ch37.html"><strong aria-hidden="true">46.</strong> 第 37 章：Plugin 生命周期——发现、安装、更新与卸载</a></li><li class="chapter-item expanded "><a href="part9/ch38.html"><strong aria-hidden="true">47.</strong> 第 38 章：Marketplace 协议——官方注册表与第三方源</a></li><li class="chapter-item expanded "><a href="part9/ch39.html"><strong aria-hidden="true">48.</strong> 第 39 章：Plugin 包结构——目录约定、package.json 契约与沙箱边界</a></li><li class="chapter-item expanded affix "><li class="part-title">第十篇：模式提炼——工程启示录</li><li class="chapter-item expanded "><a href="part10/part.html"><strong aria-hidden="true">49.</strong> 篇章导览</a></li><li class="chapter-item expanded "><a href="part10/ch40.html"><strong aria-hidden="true">50.</strong> 第 40 章：Harness 工程模式图谱——12 个可复用设计模式</a></li><li class="chapter-item expanded "><a href="part10/ch41.html"><strong aria-hidden="true">51.</strong> 第 41 章：从 CLI 到 Agent 平台——架构跃迁的路线图</a></li><li class="chapter-item expanded affix "><li class="part-title">附录</li><li class="chapter-item expanded "><a href="appendix-a.html"><strong aria-hidden="true">52.</strong> 附录 A：Hook 事件速查表</a></li><li class="chapter-item expanded "><a href="appendix-b.html"><strong aria-hidden="true">53.</strong> 附录 B：工具权限矩阵</a></li><li class="chapter-item expanded "><a href="appendix-c.html"><strong aria-hidden="true">54.</strong> 附录 C：关键类型索引</a></li><li class="chapter-item expanded "><a href="appendix-d.html"><strong aria-hidden="true">55.</strong> 附录 D：环境变量参考</a></li><li class="chapter-item expanded "><a href="appendix-e.html"><strong aria-hidden="true">56.</strong> 附录 E：Feature Flag 完整清单</a></li><li class="chapter-item expanded "><a href="appendix-f.html"><strong aria-hidden="true">57.</strong> 附录 F：术语表</a></li></ol>';
        // Set the current, active page, and reveal it if it's hidden
        let current_page = document.location.href.toString().split("#")[0].split("?")[0];
        if (current_page.endsWith("/")) {
            current_page += "index.html";
        }
        var links = Array.prototype.slice.call(this.querySelectorAll("a"));
        var l = links.length;
        for (var i = 0; i < l; ++i) {
            var link = links[i];
            var href = link.getAttribute("href");
            if (href && !href.startsWith("#") && !/^(?:[a-z+]+:)?\/\//.test(href)) {
                link.href = path_to_root + href;
            }
            // The "index" page is supposed to alias the first chapter in the book.
            if (link.href === current_page || (i === 0 && path_to_root === "" && current_page.endsWith("/index.html"))) {
                link.classList.add("active");
                var parent = link.parentElement;
                if (parent && parent.classList.contains("chapter-item")) {
                    parent.classList.add("expanded");
                }
                while (parent) {
                    if (parent.tagName === "LI" && parent.previousElementSibling) {
                        if (parent.previousElementSibling.classList.contains("chapter-item")) {
                            parent.previousElementSibling.classList.add("expanded");
                        }
                    }
                    parent = parent.parentElement;
                }
            }
        }
        // Track and set sidebar scroll position
        this.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') {
                sessionStorage.setItem('sidebar-scroll', this.scrollTop);
            }
        }, { passive: true });
        var sidebarScrollTop = sessionStorage.getItem('sidebar-scroll');
        sessionStorage.removeItem('sidebar-scroll');
        if (sidebarScrollTop) {
            // preserve sidebar scroll position when navigating via links within sidebar
            this.scrollTop = sidebarScrollTop;
        } else {
            // scroll sidebar to current active section when navigating via "next/previous chapter" buttons
            var activeSection = document.querySelector('#sidebar .active');
            if (activeSection) {
                activeSection.scrollIntoView({ block: 'center' });
            }
        }
        // Toggle buttons
        var sidebarAnchorToggles = document.querySelectorAll('#sidebar a.toggle');
        function toggleSection(ev) {
            ev.currentTarget.parentElement.classList.toggle('expanded');
        }
        Array.from(sidebarAnchorToggles).forEach(function (el) {
            el.addEventListener('click', toggleSection);
        });
    }
}
window.customElements.define("mdbook-sidebar-scrollbox", MDBookSidebarScrollbox);
