// mermaid 自动初始化：将 <code class="language-mermaid"> 转为 SVG
(function() {
  // 动态加载 mermaid.js（CDN）
  var script = document.createElement('script');
  script.src = 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js';
  script.onload = function() {
    mermaid.initialize({
      startOnLoad: false,
      theme: 'default',
      themeVariables: {
        primaryColor: '#2563eb',
        primaryTextColor: '#1a1a1a',
        primaryBorderColor: '#1e3a5f',
        lineColor: '#475569',
        fontFamily: '"PingFang SC", "Microsoft YaHei", sans-serif',
        fontSize: '14px'
      },
      flowchart: { htmlLabels: true, curve: 'linear' },
      sequence: { actorMargin: 50 },
      er: { diagramPadding: 20 }
    });

    // 找所有 mermaid 代码块并替换为图表
    var codeBlocks = document.querySelectorAll('code.language-mermaid');
    var promises = [];
    codeBlocks.forEach(function(block, i) {
      var pre = block.parentElement;
      var def = block.textContent.trim();
      var id = 'mermaid-diagram-' + i;
      
      // 创建容器
      var container = document.createElement('div');
      container.className = 'mermaid-container';
      container.style.cssText = [
        'background: #f8fafc',
        'border: 1px solid #e2e8f0',
        'border-radius: 6px',
        'padding: 16px',
        'margin: 16px 0',
        'overflow-x: auto',
        'text-align: center'
      ].join(';');
      pre.parentNode.replaceChild(container, pre);
      
      promises.push(
        mermaid.render(id, def).then(function(result) {
          container.innerHTML = result.svg;
          // 让 SVG 宽度自适应
          var svg = container.querySelector('svg');
          if (svg) {
            svg.style.maxWidth = '100%';
            svg.style.height = 'auto';
          }
        }).catch(function(err) {
          // 渲染失败时恢复代码块
          var fallback = document.createElement('pre');
          fallback.innerHTML = '<code class="language-mermaid">' + 
            def.replace(/&/g,'&amp;').replace(/</g,'&lt;') + '</code>';
          container.parentNode.replaceChild(fallback, container);
        })
      );
    });
    return Promise.all(promises);
  };
  document.head.appendChild(script);
})();
