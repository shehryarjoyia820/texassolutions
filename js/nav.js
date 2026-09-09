// Mobile nav toggle — works for any header on the page that follows the
// .nav-burger / .nav-mobile pattern.
(function () {
  function init() {
    document.querySelectorAll('[data-nav-toggle]').forEach(function (btn) {
      var targetId = btn.getAttribute('data-nav-toggle');
      var menu = document.getElementById(targetId);
      if (!menu) return;
      btn.addEventListener('click', function () {
        var open = menu.classList.toggle('is-open');
        btn.textContent = open ? '×' : '☰';
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      menu.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', function () {
          menu.classList.remove('is-open');
          btn.textContent = '☰';
          btn.setAttribute('aria-expanded', 'false');
        });
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
