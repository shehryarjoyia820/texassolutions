/* Texas Solutions Truck Dispatch: nav, reveal, rate board, estimator, forms. */
(function () {
  'use strict';
  var WEB3FORMS_ACCESS_KEY = 'c66393e0-d742-483a-b9d0-a923d09baa97';
  var ENDPOINT = 'https://api.web3forms.com/submit';
  document.documentElement.classList.remove('no-js');

  /* header shadow + mobile nav */
  var header = document.querySelector('.header');
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  var burger = document.querySelector('.burger');
  var mnav = document.getElementById('mnav');
  if (burger && mnav) {
    burger.addEventListener('click', function () {
      var open = mnav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    mnav.addEventListener('click', function (e) { if (e.target.tagName === 'A') { mnav.classList.remove('open'); document.body.style.overflow = ''; } });
  }
  Array.prototype.forEach.call(document.querySelectorAll('.dd > button'), function (b) {
    b.addEventListener('click', function () {
      var dd = b.parentNode; var open = dd.classList.toggle('open');
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  document.addEventListener('click', function (e) {
    Array.prototype.forEach.call(document.querySelectorAll('.dd.open'), function (dd) { if (!dd.contains(e.target)) dd.classList.remove('open'); });
  });

  /* reveal on scroll */
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    Array.prototype.forEach.call(rv, function (el) { io.observe(el); });
  } else { Array.prototype.forEach.call(rv, function (el) { el.classList.add('in'); }); }

  /* rate board: rotate highlighted row so the board feels live */
  var rows = document.querySelectorAll('.board-table tbody tr');
  if (rows.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var i = 0;
    setInterval(function () {
      Array.prototype.forEach.call(rows, function (r) { r.classList.remove('flash'); });
      rows[i % rows.length].classList.add('flash'); i++;
    }, 1800);
  }
  var clock = document.getElementById('boardTime');
  if (clock) {
    var tick = function () { clock.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }); };
    tick(); setInterval(tick, 30000);
  }

  /* estimator */
  var est = document.getElementById('estimator');
  var money = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };
  if (est) {
    var cfg = JSON.parse(est.getAttribute('data-pricing'));
    var trucks = est.querySelector('#estTrucks'), gross = est.querySelector('#estGross');
    var outT = est.querySelector('#estTrucksOut'), outG = est.querySelector('#estGrossOut');
    function kind() { var c = est.querySelector('input[name=estType]:checked'); return c ? c.value : 'semi'; }
    function syncGross(reset) {
      var p = cfg[kind()];
      if (reset) gross.value = Math.round((p.gross[0] + p.gross[1]) / 2);
      est.querySelector('#estTypical').textContent = money(p.gross[0]) + ' - ' + money(p.gross[1]);
    }
    function calc() {
      var p = cfg[kind()], n = +trucks.value, g = +gross.value;
      var lo = g * p.pct[0] / 100, hi = g * p.pct[1] / 100;
      outT.textContent = n + (n === 1 ? ' truck' : ' trucks');
      outG.textContent = money(g);
      est.querySelector('#estPct').textContent = p.pct[0] + '-' + p.pct[1] + '%';
      est.querySelector('#estWeekly').textContent = money(lo * n) + ' - ' + money(hi * n);
      est.querySelector('#estPerTruck').textContent = money(lo) + ' - ' + money(hi);
      est.querySelector('#estMonthly').textContent = money(lo * n * 52 / 12) + ' - ' + money(hi * n * 52 / 12);
      est.querySelector('#estKeep').textContent = money((g - hi) * n) + ' - ' + money((g - lo) * n);
      est.querySelector('#estBig').innerHTML = money(lo * n) + '<small> - ' + money(hi * n) + ' / week</small>';
      var summary = p.label + ', ' + n + ' truck(s), ' + money(g) + ' weekly gross per truck, ' + p.pct[0] + '-' + p.pct[1] + '% = ' + money(lo * n) + ' - ' + money(hi * n) + ' per week (OTR)';
      Array.prototype.forEach.call(document.querySelectorAll('input[name=estimate_summary]'), function (h) { h.value = summary; });
      var eqSel = document.getElementById('qEquip');
      if (eqSel && !eqSel.dataset.touched) eqSel.value = p.defaultEq;
      var qt = document.getElementById('qTrucks'); if (qt && !qt.dataset.touched) qt.value = n;
    }
    Array.prototype.forEach.call(est.querySelectorAll('input[name=estType]'), function (r) { r.addEventListener('change', function () { syncGross(true); calc(); }); });
    trucks.addEventListener('input', calc); gross.addEventListener('input', calc);
    ['qEquip', 'qTrucks'].forEach(function (id) { var el = document.getElementById(id); if (el) el.addEventListener('change', function () { el.dataset.touched = '1'; }); });
    var pre = new URLSearchParams(location.search).get('type');
    if (pre && cfg[pre]) { var r = est.querySelector('input[value=' + pre + ']'); if (r) r.checked = true; }
    syncGross(true); calc();
  }

  /* forms: plain written fields only, sent through Web3Forms */
  Array.prototype.forEach.call(document.querySelectorAll('form[data-web3]'), function (form) {
    var status = form.querySelector('.form-status');
    var btn = form.querySelector('button[type=submit]');
    function show(msg, ok) { status.textContent = msg; status.className = 'form-status ' + (ok ? 'ok' : 'err'); }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.botcheck && form.botcheck.checked) return;
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = new FormData(form);
      data.append('access_key', WEB3FORMS_ACCESS_KEY);
      data.append('subject', form.getAttribute('data-subject') || 'New dispatch inquiry');
      data.append('from_name', 'Texas Solutions Dispatch Website');
      data.append('page', location.href);
      data.set('sms_consent', form.querySelector('input[name=sms_consent]') && form.querySelector('input[name=sms_consent]').checked ? 'Yes - agreed to SMS' : 'No');
      var label = btn.textContent; btn.disabled = true; btn.textContent = 'Sending...';
      fetch(ENDPOINT, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
        .then(function (r) { return r.json().catch(function () { return { success: r.ok }; }); })
        .then(function (res) {
          if (res && res.success) {
            form.reset();
            show('Thank you. A Texas Solutions dispatcher will contact you shortly. For a faster reply, message us on WhatsApp.', true);
          } else { throw new Error((res && res.message) || 'failed'); }
        })
        .catch(function () { show('Sorry, the form could not be sent. Please call (838) 910-3147 or message us on WhatsApp.', false); })
        .then(function () { btn.disabled = false; btn.textContent = label; });
    });
  });

  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
})();
