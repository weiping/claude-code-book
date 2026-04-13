(() => {
    // 将 mdbook 输出的 <pre><code class="language-mermaid"> 转换为 mermaid 可识别的 <div class="mermaid">
    document.querySelectorAll('pre code.language-mermaid').forEach(code => {
        const pre = code.parentElement;
        const div = document.createElement('div');
        div.className = 'mermaid';
        div.textContent = code.textContent;
        pre.replaceWith(div);
    });

    const darkThemes = ['ayu', 'navy', 'coal'];
    const lightThemes = ['light', 'rust'];

    const classList = document.getElementsByTagName('html')[0].classList;
    let lastThemeWasLight = true;
    for (const cssClass of classList) {
        if (darkThemes.includes(cssClass)) {
            lastThemeWasLight = false;
            break;
        }
    }

    const theme = lastThemeWasLight ? 'default' : 'dark';
    mermaid.initialize({
        startOnLoad: true,
        theme,
        securityLevel: 'loose',
        fontFamily: '"PingFang SC", "Heiti SC", "Microsoft YaHei", sans-serif'
    });

    for (const darkTheme of darkThemes) {
        const el = document.getElementById(darkTheme);
        if (el) el.addEventListener('click', () => {
            if (lastThemeWasLight) window.location.reload();
        });
    }
    for (const lightTheme of lightThemes) {
        const el = document.getElementById(lightTheme);
        if (el) el.addEventListener('click', () => {
            if (!lastThemeWasLight) window.location.reload();
        });
    }
})();
