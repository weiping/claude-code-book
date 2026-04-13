// 初始化 Mermaid 渲染，兼容 mdbook 生成的代码块格式
window.addEventListener('load', function() {
  // 配置 mermaid
  mermaid.initialize({
    startOnLoad: false,
    theme: 'default',
    securityLevel: 'loose',
    fontFamily: 'monospace',
  });

  // mdbook 将 ```mermaid 块渲染为 <code class="language-mermaid">
  document.querySelectorAll('code.language-mermaid').forEach(function(el) {
    var pre = el.parentElement; // <pre>
    var container = document.createElement('div');
    container.className = 'mermaid';
    container.textContent = el.textContent;
    pre.parentNode.replaceChild(container, pre);
  });

  // 触发渲染
  mermaid.init(undefined, '.mermaid');
});
