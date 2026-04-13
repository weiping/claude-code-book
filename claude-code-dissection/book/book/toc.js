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
        this.innerHTML = '<ol class="chapter"><li class="chapter-item expanded "><a href="preface.html"><strong aria-hidden="true">1.</strong> 序：为什么要解剖 Claude Code</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded "><a href="part1/ch01.html"><strong aria-hidden="true">2.</strong> 第 1 章：运行时 Harness 全景——总体架构解析</a></li><li class="chapter-item expanded "><a href="part1/ch02.html"><strong aria-hidden="true">3.</strong> 第 2 章：技术栈选型——React/Ink + Bun + TypeScript 的工程逻辑</a></li><li class="chapter-item expanded "><a href="part1/ch03.html"><strong aria-hidden="true">4.</strong> 第 3 章：启动流水线的并发艺术</a></li><li class="chapter-item expanded "><a href="part1/ch04.html"><strong aria-hidden="true">5.</strong> 第 4 章：Feature Flag 的双层架构</a></li><li class="chapter-item expanded "><a href="part1/ch05.html"><strong aria-hidden="true">6.</strong> 第 5 章：Bootstrap 全局状态——进程的状态脊梁</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded "><a href="part2/ch06.html"><strong aria-hidden="true">7.</strong> 第 6 章：用户输入的三条分叉路</a></li><li class="chapter-item expanded "><a href="part2/ch07.html"><strong aria-hidden="true">8.</strong> 第 7 章：斜杠命令系统——内置命令的注册与执行</a></li><li class="chapter-item expanded "><a href="part2/ch08.html"><strong aria-hidden="true">9.</strong> 第 8 章：query.ts——单轮对话的原子循环</a></li><li class="chapter-item expanded "><a href="part2/ch09.html"><strong aria-hidden="true">10.</strong> 第 9 章：Query Engine——多轮编排与状态管理</a></li><li class="chapter-item expanded "><a href="part2/ch10.html"><strong aria-hidden="true">11.</strong> 第 10 章：运行模式状态机——Plan、Auto、Worktree 等模式的实现</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded "><a href="part3/ch11.html"><strong aria-hidden="true">12.</strong> 第 11 章：Tool 接口与 buildTool 工厂</a></li><li class="chapter-item expanded "><a href="part3/ch12.html"><strong aria-hidden="true">13.</strong> 第 12 章：BashTool 解剖——最复杂工具的实现</a></li><li class="chapter-item expanded "><a href="part3/ch13.html"><strong aria-hidden="true">14.</strong> 第 13 章：AgentTool——递归智能体的工具接口</a></li><li class="chapter-item expanded "><a href="part3/ch14.html"><strong aria-hidden="true">15.</strong> 第 14 章：工具注册与条件加载</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded "><a href="part4/ch15.html"><strong aria-hidden="true">16.</strong> 第 15 章：权限系统的三层决策架构</a></li><li class="chapter-item expanded "><a href="part4/ch16.html"><strong aria-hidden="true">17.</strong> 第 16 章：YOLO 模式与 AI 分类器</a></li><li class="chapter-item expanded "><a href="part4/ch17.html"><strong aria-hidden="true">18.</strong> 第 17 章：PermissionRule 与规则引擎</a></li><li class="chapter-item expanded "><a href="part4/ch18.html"><strong aria-hidden="true">19.</strong> 第 18 章：Hooks 系统——生命周期拦截点</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded "><a href="part5/ch19.html"><strong aria-hidden="true">20.</strong> 第 19 章：系统提示的优先级堆叠与组装</a></li><li class="chapter-item expanded "><a href="part5/ch20.html"><strong aria-hidden="true">21.</strong> 第 20 章：CLAUDE.md 的发现、解析与注入</a></li><li class="chapter-item expanded "><a href="part5/ch21.html"><strong aria-hidden="true">22.</strong> 第 21 章：上下文组装——git 状态、工具描述与用户上下文的构建</a></li><li class="chapter-item expanded "><a href="part5/ch22.html"><strong aria-hidden="true">23.</strong> 第 22 章：模型自动选择——Opus、Sonnet 与 Haiku 的路由逻辑</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded "><a href="part6/ch23.html"><strong aria-hidden="true">24.</strong> 第 23 章：会话系统——标识、持久化与恢复</a></li><li class="chapter-item expanded "><a href="part6/ch24.html"><strong aria-hidden="true">25.</strong> 第 24 章：缓存系统——Prompt Cache 与 Context 压缩四策略</a></li><li class="chapter-item expanded "><a href="part6/ch25.html"><strong aria-hidden="true">26.</strong> 第 25 章：AutoCompact 与边界标记的实现</a></li><li class="chapter-item expanded "><a href="part6/ch26.html"><strong aria-hidden="true">27.</strong> 第 26 章：本地记忆系统——memdir 与 SessionMemory</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded "><a href="part7/ch27.html"><strong aria-hidden="true">28.</strong> 第 27 章：MCP 客户端的三协议实现</a></li><li class="chapter-item expanded "><a href="part7/ch28.html"><strong aria-hidden="true">29.</strong> 第 28 章：MCP 认证——OAuth、JWT 与 xaa</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded "><a href="part8/ch29.html"><strong aria-hidden="true">30.</strong> 第 29 章：多智能体架构总览——Swarm 的层次模型</a></li><li class="chapter-item expanded "><a href="part8/ch30.html"><strong aria-hidden="true">31.</strong> 第 30 章：Task 类型体系——三种执行模式的实现</a></li><li class="chapter-item expanded "><a href="part8/ch31.html"><strong aria-hidden="true">32.</strong> 第 31 章：Subagent 的生命周期——forkSubagent、runAgent 与内存隔离</a></li><li class="chapter-item expanded "><a href="part8/ch32.html"><strong aria-hidden="true">33.</strong> 第 32 章：Swarm 权限同步——沙箱中的信任传递</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded "><a href="part9/ch33.html"><strong aria-hidden="true">34.</strong> 第 33 章：Effort、Fast Mode 与 Thinking——推理深度控制</a></li><li class="chapter-item expanded "><a href="part9/ch34.html"><strong aria-hidden="true">35.</strong> 第 34 章：跨会话记忆——extractMemories 与 teamMemorySync</a></li><li class="chapter-item expanded "><a href="part9/ch35.html"><strong aria-hidden="true">36.</strong> 第 35 章：Plugin 系统——DXT 包的生命周期</a></li><li class="chapter-item expanded "><a href="part9/ch36.html"><strong aria-hidden="true">37.</strong> 第 36 章：Skill 系统——Markdown 封装的 AI 能力</a></li><li class="chapter-item expanded "><a href="part9/ch37.html"><strong aria-hidden="true">38.</strong> 第 37 章：未发布的功能总线——Feature Flag 背后的实验特性</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded "><a href="part10/ch38.html"><strong aria-hidden="true">39.</strong> 第 38 章：Ink 的自建 Reconciler</a></li><li class="chapter-item expanded "><a href="part10/ch39.html"><strong aria-hidden="true">40.</strong> 第 39 章：termio——终端原语的解析与发送</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded "><a href="part11/ch40.html"><strong aria-hidden="true">41.</strong> 第 40 章：并发优先的启动哲学</a></li><li class="chapter-item expanded "><a href="part11/ch41.html"><strong aria-hidden="true">42.</strong> 第 41 章：安全性的三道防线</a></li><li class="chapter-item expanded "><a href="part11/ch42.html"><strong aria-hidden="true">43.</strong> 第 42 章：可扩展性的四种机制</a></li></ol>';
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
