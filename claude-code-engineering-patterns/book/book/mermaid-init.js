// Initialize mermaid for mdbook
document.addEventListener('DOMContentLoaded', function() {
  if (typeof mermaid !== 'undefined') {
    mermaid.initialize({
      startOnLoad: true,
      theme: 'default',
      securityLevel: 'loose'
    });
    // Convert code blocks with class "language-mermaid" to mermaid divs
    document.querySelectorAll('code.language-mermaid').forEach(function(el) {
      const div = document.createElement('div');
      div.className = 'mermaid';
      div.textContent = el.textContent;
      el.parentNode.replaceWith(div);
    });
    mermaid.init(undefined, document.querySelectorAll('.mermaid'));
  }
});
