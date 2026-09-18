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
  // Safety net: never leave content hidden (slow devices, print, crawlers).
  setTimeout(function () { Array.prototype.forEach.call(rv, function (el) { el.classList.add('in'); }); }, 2500);

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

  /* estimator: per-truck pricing */
  var est = document.getElementById('estimator');
  var money = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };
  var cfg = est ? JSON.parse(est.getAttribute('data-pricing')) : null;
  function truckById(id) { for (var k = 0; k < cfg.trucks.length; k++) if (cfg.trucks[k].id === id) return cfg.trucks[k]; return cfg.trucks[0]; }
  if (est) {
    var trucks = est.querySelector('#estTrucks'), gross = est.querySelector('#estGross');
    var outT = est.querySelector('#estTrucksOut'), outG = est.querySelector('#estGrossOut');
    var custom = est.querySelector('#estCustom');
    var $ = function (id) { return document.getElementById(id); };
    function current() { var c = est.querySelector('input[name=estTruck]:checked'); return truckById(c ? c.value : ''); }
    function pick(reset) {
      var tr = current();
      if (reset) gross.value = Math.round((tr.gross[0] + tr.gross[1]) / 2);
      $('estTypical').textContent = money(tr.gross[0]) + ' - ' + money(tr.gross[1]);
      $('estTruckName').textContent = tr.name; $('estTruckName2').textContent = tr.name;
      var wt = $('wqTruck'); if (wt && !wt.dataset.touched) { wt.value = tr.id; wt.dispatchEvent(new Event('sync')); }
    }
    function calc() {
      var tr = current(), n = +trucks.value, g = +gross.value;
      var cp = parseFloat(custom.value), useCustom = cp > 0 && cp <= 100;
      var pLo = useCustom ? cp : tr.pct[0], pHi = useCustom ? cp : tr.pct[1];
      var lo = g * pLo / 100, hi = g * pHi / 100;
      var rng = function (a, b) { return a === b ? money(a) : money(a) + ' - ' + money(b); };
      outT.textContent = n + (n === 1 ? ' truck' : ' trucks');
      outG.textContent = money(g);
      $('estPct').textContent = useCustom ? cp + '% (your rate)' : tr.pct[0] + '-' + tr.pct[1] + '%';
      $('estRpm').textContent = tr.rpm + ' /mi';
      $('estWeekly').textContent = rng(lo * n, hi * n);
      $('estPerTruck').textContent = rng(lo, hi);
      $('estMonthly').textContent = rng(lo * n * 52 / 12, hi * n * 52 / 12);
      $('estKeep').textContent = rng((g - hi) * n, (g - lo) * n);
      $('estBig').innerHTML = useCustom ? money(lo * n) + '<small>per week at ' + cp + '%</small>' : money(lo * n) + '<small> - ' + money(hi * n) + ' / week</small>';
      var wp = $('wqPct'); if (wp && !wp.dataset.touched) wp.value = useCustom ? cp : '';
      var wq = $('wqTrucks'); if (wq && !wq.dataset.touched) wq.value = n;
      var wg = $('wqGross'); if (wg && !wg.dataset.touched) wg.value = g;
    }
    Array.prototype.forEach.call(est.querySelectorAll('input[name=estTruck]'), function (r) { r.addEventListener('change', function () { pick(true); calc(); }); });
    trucks.addEventListener('input', calc); gross.addEventListener('input', calc); custom.addEventListener('input', calc);
    var qs = new URLSearchParams(location.search), want = qs.get('truck') || { semi: 'dry-van', small: 'box-truck' }[qs.get('type')];
    if (want) { var r0 = est.querySelector('input[name=estTruck][value="' + want + '"]'); if (r0) r0.checked = true; }
    pick(true); calc();
  }

  /* free quote: opens WhatsApp with the carrier's details filled in */
  var wa = document.getElementById('waQuote');
  if (wa && cfg) {
    var wt = document.getElementById('wqTruck'), hint = document.getElementById('wqPctHint');
    var syncHint = function () { var tr = truckById(wt.value); hint.textContent = 'Our rate for a ' + tr.name + ': ' + tr.pct[0] + '-' + tr.pct[1] + '% of weekly gross (OTR)'; };
    wt.addEventListener('change', function () { wt.dataset.touched = '1'; syncHint(); });
    wt.addEventListener('sync', syncHint); syncHint();
    ['wqTrucks', 'wqGross', 'wqPct'].forEach(function (id) { var el = document.getElementById(id); el.addEventListener('input', function () { el.dataset.touched = '1'; }); });
    wa.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!wa.checkValidity()) { wa.reportValidity(); return; }
      var v = function (id) { return document.getElementById(id).value.trim(); };
      var tr = truckById(wt.value);
      var lines = [
        'FREE DISPATCH QUOTE REQUEST',
        'Name: ' + v('wqName'),
        'Phone: ' + v('wqPhone'),
        'Truck type: ' + tr.name,
        'Number of trucks: ' + (v('wqTrucks') || '1'),
        'Desired percentage: ' + v('wqPct') + '%',
        'Weekly gross per truck: ' + (v('wqGross') ? money(+v('wqGross')) : '-'),
        'MC number: ' + (v('wqMc') || '-'),
        'Home base / lanes: ' + (v('wqLanes') || '-'),
        'Message: ' + (v('wqMsg') || '-'),
        '(Sent from dispatch.texassolutions.co/estimate)'
      ];
      var url = 'https://wa.me/' + cfg.wa + '?text=' + encodeURIComponent(lines.join('\n'));
      var st = wa.querySelector('.form-status');
      st.className = 'form-status ok';
      st.innerHTML = 'Opening WhatsApp... If it does not open, <a href="' + url + '" target="_blank" rel="noopener">tap here</a>.';
      window.open(url, '_blank', 'noopener');
    });
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
