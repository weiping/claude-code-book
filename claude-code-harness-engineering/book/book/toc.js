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
        this.innerHTML = '<ol class="chapter"><li class="chapter-item expanded affix "><a href="preface.html">前言</a></li><li class="chapter-item expanded affix "><li class="part-title">第一篇：全景</li><li class="chapter-item expanded "><a href="part1/part1.html"><strong aria-hidden="true">1.</strong> 篇页：全景</a></li><li class="chapter-item expanded "><a href="part1/ch01.html"><strong aria-hidden="true">2.</strong> 第 1 章：当模型遇见 Harness</a></li><li class="chapter-item expanded affix "><li class="part-title">第二篇：启动与循环</li><li class="chapter-item expanded "><a href="part2/part2.html"><strong aria-hidden="true">3.</strong> 篇页：启动与循环</a></li><li class="chapter-item expanded "><a href="part2/ch02.html"><strong aria-hidden="true">4.</strong> 第 2 章：点火序列</a></li><li class="chapter-item expanded "><a href="part2/ch03.html"><strong aria-hidden="true">5.</strong> 第 3 章：永不停歇的循环</a></li><li class="chapter-item expanded "><a href="part2/ch04.html"><strong aria-hidden="true">6.</strong> 第 4 章：单轮执行的艺术</a></li><li class="chapter-item expanded affix "><li class="part-title">第三篇：上下文工程</li><li class="chapter-item expanded "><a href="part3/part3.html"><strong aria-hidden="true">7.</strong> 篇页：上下文工程</a></li><li class="chapter-item expanded "><a href="part3/ch05.html"><strong aria-hidden="true">8.</strong> 第 5 章：提示词的分层构建</a></li><li class="chapter-item expanded "><a href="part3/ch06.html"><strong aria-hidden="true">9.</strong> 第 6 章：按需加载的智慧</a></li><li class="chapter-item expanded affix "><li class="part-title">第四篇：工具编排</li><li class="chapter-item expanded "><a href="part4/part4.html"><strong aria-hidden="true">10.</strong> 篇页：工具编排</a></li><li class="chapter-item expanded "><a href="part4/ch07.html"><strong aria-hidden="true">11.</strong> 第 7 章：最小工具基座</a></li><li class="chapter-item expanded "><a href="part4/ch08.html"><strong aria-hidden="true">12.</strong> 第 8 章：先规划后执行</a></li><li class="chapter-item expanded affix "><li class="part-title">第五篇：护栏与扩展</li><li class="chapter-item expanded "><a href="part5/part5.html"><strong aria-hidden="true">13.</strong> 篇页：护栏与扩展</a></li><li class="chapter-item expanded "><a href="part5/ch09.html"><strong aria-hidden="true">14.</strong> 第 9 章：渐进式安全</a></li><li class="chapter-item expanded "><a href="part5/ch10.html"><strong aria-hidden="true">15.</strong> 第 10 章：Harness 的神经末梢</a></li><li class="chapter-item expanded affix "><li class="part-title">第六篇：记忆管理</li><li class="chapter-item expanded "><a href="part6/part6.html"><strong aria-hidden="true">16.</strong> 篇页：记忆管理</a></li><li class="chapter-item expanded "><a href="part6/ch11.html"><strong aria-hidden="true">17.</strong> 第 11 章：上下文的五把剪刀</a></li><li class="chapter-item expanded "><a href="part6/ch12.html"><strong aria-hidden="true">18.</strong> 第 12 章：隔离与交接</a></li><li class="chapter-item expanded affix "><li class="part-title">第七篇：多智能体</li><li class="chapter-item expanded "><a href="part7/part7.html"><strong aria-hidden="true">19.</strong> 篇页：多智能体</a></li><li class="chapter-item expanded "><a href="part7/ch13.html"><strong aria-hidden="true">20.</strong> 第 13 章：生成器与评估器</a></li><li class="chapter-item expanded "><a href="part7/ch14.html"><strong aria-hidden="true">21.</strong> 第 14 章：并行世界</a></li><li class="chapter-item expanded affix "><li class="part-title">第八篇：演进</li><li class="chapter-item expanded "><a href="part8/part8.html"><strong aria-hidden="true">22.</strong> 篇页：演进</a></li><li class="chapter-item expanded "><a href="part8/ch15.html"><strong aria-hidden="true">23.</strong> 第 15 章：脚手架会消失</a></li><li class="chapter-item expanded "><a href="part8/ch16.html"><strong aria-hidden="true">24.</strong> 第 16 章：从 Claude Code 到通用原则</a></li><li class="chapter-item expanded affix "><li class="part-title">附录</li><li class="chapter-item expanded "><a href="appendix-a.html"><strong aria-hidden="true">25.</strong> 附录 A：术语表</a></li></ol>';
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
