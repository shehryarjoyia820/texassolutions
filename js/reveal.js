// Scroll-triggered reveal animation for [data-reveal] blocks and staggered
// entrance for [data-word] hero lines. Pure CSS classes toggled via IO —
// see .is-visible rules in styles.css.
(function () {
  function init() {
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var words = document.querySelectorAll('[data-word]');
    words.forEach(function (el, i) {
      if (reduce) { el.classList.add('is-visible'); return; }
      el.style.transitionDelay = (i * 0.12) + 's';
      requestAnimationFrame(function () {
        requestAnimationFrame(function () { el.classList.add('is-visible'); });
      });
    });

    var reveals = document.querySelectorAll('[data-reveal]');
    if (reduce) { reveals.forEach(function (el) { el.classList.add('is-visible'); }); return; }

    if (!('IntersectionObserver' in window)) {
      reveals.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.04 });
    reveals.forEach(function (el) { io.observe(el); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
