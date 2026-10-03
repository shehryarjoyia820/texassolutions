/* Texas Solutions Truck Dispatch: nav, reveal, analytics, calculator framework, estimator, fuel, forms. */
(function () {
  'use strict';
  var WEB3FORMS_ACCESS_KEY = 'c66393e0-d742-483a-b9d0-a923d09baa97';
  var ENDPOINT = 'https://api.web3forms.com/submit';
  document.documentElement.classList.remove('no-js');
  var TS = window.TS = {};
  var each = function (list, fn) { Array.prototype.forEach.call(list, fn); };
  var store = {
    get: function (s, k) { try { return JSON.parse(window[s].getItem(k)); } catch (e) { return null; } },
    set: function (s, k, v) { try { window[s].setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } },
    del: function (s, k) { try { window[s].removeItem(k); } catch (e) { /* storage blocked */ } }
  };

  /* ---------------------------------------------------------------- analytics
     GA4 events (see docs/HANDOVER.md, "Analytics events"). Payloads never carry names, phone
     numbers, emails or MC/DOT numbers: only tool, equipment, page and campaign. */
  var qs0 = new URLSearchParams(location.search);
  var ATTR_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  (function captureAttribution() {
    if (store.get('sessionStorage', 'ts:attr')) return;
    var a = { landing_page: location.pathname };
    ATTR_KEYS.forEach(function (k) { if (qs0.get(k)) a[k] = qs0.get(k).slice(0, 100); });
    if (qs0.get('gclid')) a.gclid = 'yes';
    try { if (document.referrer) { var r = new URL(document.referrer); if (r.host !== location.host) a.referrer = r.host; } } catch (e) { /* ignore */ }
    store.set('sessionStorage', 'ts:attr', a);
  })();
  TS.attribution = function () { return store.get('sessionStorage', 'ts:attr') || {}; };
  TS.track = function (name, params) {
    var p = {}, a = TS.attribution();
    Object.keys(params || {}).forEach(function (k) { if (params[k] !== undefined && params[k] !== '') p[k] = params[k]; });
    p.page_path = location.pathname;
    ATTR_KEYS.slice(0, 3).forEach(function (k) { if (a[k]) p['campaign_' + k.slice(4)] = a[k]; });
    if (window.TS_DEBUG) { console.log('[ga4]', name, JSON.stringify(p)); (TS.events = TS.events || []).push([name, p]); return; }
    if (window.gtag) window.gtag('event', name, p);
  };
  function linkLocation(el) {
    if (el.closest('.mbar')) return 'mobile_bar';
    if (el.closest('.wa-float')) return 'floating_button';
    if (el.closest('.topbar') || el.closest('.header') || el.closest('.mnav')) return 'header';
    if (el.closest('.footer')) return 'footer';
    if (el.closest('.cside')) return 'contact_panel';
    if (el.closest('.est, .calc-cta')) return 'calculator';
    return 'page';
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var h = a.getAttribute('href');
    var ev = /^tel:/.test(h) ? 'click_call' : /^sms:/.test(h) ? 'click_text' : /wa\.me\//.test(h) ? 'click_whatsapp' : null;
    if (ev) TS.track(ev, { link_location: linkLocation(a), tool_name: (a.closest('[data-tool]') || {}).getAttribute ? a.closest('[data-tool]').getAttribute('data-tool') : undefined });
  });

  /* ---------------------------------------------------------------- header + mobile nav */
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
  each(document.querySelectorAll('.dd > button'), function (b) {
    b.addEventListener('click', function () {
      var dd = b.parentNode; var open = dd.classList.toggle('open');
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  document.addEventListener('click', function (e) {
    each(document.querySelectorAll('.dd.open'), function (dd) { if (!dd.contains(e.target)) dd.classList.remove('open'); });
  });

  /* reveal on scroll */
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    each(rv, function (el) { io.observe(el); });
  } else { each(rv, function (el) { el.classList.add('in'); }); }
  // Safety net: never leave content hidden (slow devices, print, crawlers).
  setTimeout(function () { each(rv, function (el) { el.classList.add('in'); }); }, 2500);

  /* ---------------------------------------------------------------- number helpers */
  TS.money = function (n, d) {
    if (!isFinite(n)) n = 0;
    var neg = n < 0; n = Math.abs(n);
    return (neg ? '-$' : '$') + n.toLocaleString('en-US', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 });
  };
  TS.num = function (id) { var el = document.getElementById(id); if (!el) return 0; var x = parseFloat(el.value); return isFinite(x) ? x : 0; };

  /* ---------------------------------------------------------------- calculator framework
     TS.tool(root, {run, validate, positive, noSave, blank}) gives every calculator:
     - input checks (empty, negative, zero denominators, max) with "Enter your details"
       instead of a misleading $0,
     - Reset, Print, Save on this device (localStorage only) and Share link,
     - GA4 tool_start / tool_calculate / tool_export, each fired once at the right moment. */
  function labelFor(el) {
    var l = el.id && document.querySelector('label[for="' + el.id + '"]');
    var t = l ? l.textContent : (el.getAttribute('aria-label') || 'this field');
    return t.replace(/\s*\(optional\)\s*/i, '').replace(/\s+/g, ' ').trim();
  }
  function fields(root) {
    return Array.prototype.filter.call(root.querySelectorAll('input, select'), function (el) {
      return el.type !== 'hidden' && !el.closest('.tool-bar') && !el.closest('.compare');
    });
  }
  function visible(el) { return el.offsetParent !== null || el.type === 'radio'; }
  function readState(root) {
    var s = {};
    fields(root).forEach(function (el) {
      if (el.type === 'radio') { if (el.checked) s['r:' + el.name] = el.value; }
      else if (el.type === 'checkbox') { if (el.id) s[el.id] = el.checked; }
      else if (el.id) s[el.id] = el.value;
    });
    return s;
  }
  function writeState(root, s) {
    fields(root).forEach(function (el) {
      if (el.type === 'radio') { if (s['r:' + el.name] !== undefined) el.checked = el.value === s['r:' + el.name]; }
      else if (el.type === 'checkbox') { if (el.id in s) el.checked = !!s[el.id]; }
      else if (el.id && el.id in s) el.value = s[el.id];
    });
  }
  TS.tool = function (root, o) {
    if (!root) return null;
    var name = root.getAttribute('data-tool') || root.id;
    var big = root.querySelector('.est-big');
    var started = false, timer = null, lastSig = null, defaults = null, ok = false;
    var positive = o.positive || [];
    var msgEl = document.createElement('p');
    msgEl.className = 'calc-msg'; msgEl.setAttribute('role', 'status'); msgEl.hidden = true;
    if (big) big.parentNode.insertBefore(msgEl, big.nextSibling);

    function check() {
      var bad = null;
      fields(root).forEach(function (el) {
        el.classList.remove('bad'); el.removeAttribute('aria-invalid');
        if (bad || !visible(el)) return;
        var v = el.value.trim(), lab = labelFor(el), m = null;
        var optional = el.hasAttribute('placeholder') || el.hasAttribute('data-optional');
        if (el.type === 'number') {
          var x = parseFloat(v);
          if (v === '') { if (!optional) m = 'Enter ' + lab.toLowerCase() + '.'; }
          else if (!isFinite(x)) m = lab + ' must be a number.';
          else if (x < 0) m = lab + ' can\'t be negative.';
          else if ((positive.indexOf(el.id) >= 0 || el.hasAttribute('data-positive')) && x <= 0) m = lab + ' must be more than 0.';
          else if (el.max !== '' && x > parseFloat(el.max)) m = lab + ' can\'t be more than ' + el.max + '.';
        } else if (el.required && v === '') m = 'Enter ' + lab.toLowerCase() + '.';
        if (m) { bad = m; el.classList.add('bad'); el.setAttribute('aria-invalid', 'true'); }
      });
      if (!bad && o.validate) bad = o.validate() || null;
      return bad;
    }
    function blank(msg) {
      ok = false;
      if (big) big.innerHTML = 'Enter your details<small>' + (msg ? 'see the note below' : '') + '</small>';
      each(root.querySelectorAll('.est-lines b'), function (b) { b.textContent = '-'; });
      msgEl.textContent = msg || ''; msgEl.hidden = !msg;
      if (o.blank) o.blank();
    }
    function run(user) {
      var msg = check();
      if (msg) { blank(msg); return false; }
      msgEl.hidden = true;
      ok = o.run() !== false;
      if (!ok) { blank(); return false; }
      if (user) {
        clearTimeout(timer);
        timer = setTimeout(function () {
          var sig = JSON.stringify(readState(root));
          if (ok && sig !== lastSig) { lastSig = sig; TS.track('tool_calculate', { tool_name: name, equipment: o.equipment ? o.equipment() : undefined }); }
        }, 1500);
      }
      return true;
    }
    function onUser(e) {
      if (e.target.closest('.tool-bar') || e.target.closest('.compare')) return;
      if (!started && e.isTrusted !== false) { started = true; TS.track('tool_start', { tool_name: name }); }
      run(true);
    }
    root.addEventListener('input', onUser);
    root.addEventListener('change', onUser);

    // Toolbar: reset, print, save (this device only), share.
    var key = 'ts:tool:' + name;
    var bar = document.createElement('div');
    bar.className = 'tool-bar';
    bar.innerHTML = '<button type="button" data-a="reset">Reset</button><button type="button" data-a="print">Print</button>' +
      (o.noSave ? '' : '<button type="button" data-a="save">Save on this device</button><button type="button" data-a="load" hidden>Use my saved numbers</button>') +
      '<button type="button" data-a="share">Share tool</button><span class="tool-bar-note" role="status"></span>';
    var out = root.querySelector('.est-out');
    var smallNote = out && out.querySelector(':scope > small:last-of-type');
    if (out) out.insertBefore(bar, smallNote || null);
    var note = bar.querySelector('.tool-bar-note');
    var loadBtn = bar.querySelector('[data-a=load]');
    if (loadBtn && store.get('localStorage', key)) loadBtn.hidden = false;
    function say(t) { note.textContent = t; clearTimeout(say.t); say.t = setTimeout(function () { note.textContent = ''; }, 5000); }
    bar.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      var a = b.getAttribute('data-a');
      if (a === 'reset') {
        writeState(root, defaults); if (o.afterRestore) o.afterRestore(); run(false); say('Reset to the example values.');
      } else if (a === 'print') {
        if (!ok) { say('Enter your details first.'); return; }
        TS.track('tool_export', { tool_name: name, method: 'print' });
        var sec = root.closest('section');
        document.body.classList.add('print-tool'); if (sec) sec.classList.add('print-target');
        var done = function () { document.body.classList.remove('print-tool'); if (sec) sec.classList.remove('print-target'); window.removeEventListener('afterprint', done); };
        window.addEventListener('afterprint', done);
        window.print(); setTimeout(done, 1000);
      } else if (a === 'save') {
        if (store.set('localStorage', key, { at: new Date().toISOString(), v: readState(root) })) {
          if (loadBtn) loadBtn.hidden = false;
          TS.track('tool_export', { tool_name: name, method: 'save_device' });
          say('Saved in this browser only. Nothing was sent to us.');
        } else say('This browser blocks saving (private mode or storage off).');
      } else if (a === 'load') {
        var s = store.get('localStorage', key);
        if (s && s.v) { writeState(root, s.v); if (o.afterRestore) o.afterRestore(); run(true); say('Loaded your numbers saved on ' + new Date(s.at).toLocaleDateString() + '.'); }
      } else if (a === 'share') {
        var url = location.origin + location.pathname + '?utm_source=share&utm_medium=tool_link&utm_campaign=' + encodeURIComponent(name);
        var fin = function (m) { TS.track('share', { method: m, content_type: 'tool', item_id: name }); };
        if (navigator.share) { navigator.share({ title: document.title, url: url }).then(function () { fin('native'); }).catch(function () { /* cancelled */ }); }
        else if (navigator.clipboard) { navigator.clipboard.writeText(url).then(function () { fin('copy'); say('Link copied. It opens the tool, not your numbers.'); }); }
        else { window.prompt('Copy this link:', url); fin('prompt'); }
      }
    });

    var ctl = { run: run, root: root, ok: function () { return ok; }, setDefaults: function () { defaults = readState(root); } };
    ctl.setDefaults();
    return ctl;
  };

  /* ---------------------------------------------------------------- dispatch fee estimator */
  var est = document.getElementById('estimator');
  var money = TS.money;
  var pctTxt = function (p) { return p[0] === p[1] ? p[0] + '%' : p[0] + '-' + p[1] + '%'; };
  var cfg = est ? JSON.parse(est.getAttribute('data-pricing')) : null;
  function truckById(id) { for (var k = 0; k < cfg.trucks.length; k++) if (cfg.trucks[k].id === id) return cfg.trucks[k]; return cfg.trucks[0]; }
  if (est) {
    var trucks = est.querySelector('#estTrucks'), gross = est.querySelector('#estGross');
    var outT = est.querySelector('#estTrucksOut'), outG = est.querySelector('#estGrossOut');
    var custom = est.querySelector('#estCustom');
    var $ = function (id) { return document.getElementById(id); };
    var current = function () { var c = est.querySelector('input[name=estTruck]:checked'); return truckById(c ? c.value : ''); };
    var lastTruck = null;
    var pick = function (reset) {
      var tr = current();
      if (reset) gross.value = Math.round((tr.gross[0] + tr.gross[1]) / 2);
      $('estTypical').textContent = money(tr.gross[0]) + ' - ' + money(tr.gross[1]);
      $('estTruckName').textContent = tr.name; $('estTruckName2').textContent = tr.name;
      var wt = $('wqTruck'); if (wt && !wt.dataset.touched) { wt.value = tr.id; wt.dispatchEvent(new Event('sync')); }
    };
    var estCalc = function () {
      var tr = current();
      if (tr !== lastTruck) { pick(lastTruck !== null); lastTruck = tr; }
      var n = +trucks.value, g = +gross.value;
      var cp = parseFloat(custom.value), useCustom = cp > 0 && cp <= 100;
      var pLo = useCustom ? cp : tr.pct[0], pHi = useCustom ? cp : tr.pct[1];
      var lo = g * pLo / 100, hi = g * pHi / 100;
      var rng = function (a, b) { return a === b ? money(a) : money(a) + ' - ' + money(b); };
      outT.textContent = n + (n === 1 ? ' truck' : ' trucks');
      outG.textContent = money(g);
      $('estPct').textContent = useCustom ? cp + '% (your rate)' : pctTxt(tr.pct);
      $('estRpm').textContent = tr.rpm + ' /mi';
      $('estWeekly').textContent = rng(lo * n, hi * n);
      $('estPerTruck').textContent = rng(lo, hi);
      $('estMonthly').textContent = rng(lo * n * 52 / 12, hi * n * 52 / 12);
      $('estKeep').textContent = rng((g - hi) * n, (g - lo) * n);
      $('estBig').innerHTML = (useCustom || lo === hi) ? money(lo * n) + '<small>per week at ' + (useCustom ? cp : pLo) + '%</small>' : money(lo * n) + '<small> - ' + money(hi * n) + ' / week</small>';
      var wp = $('wqPct'); if (wp && !wp.dataset.touched) wp.value = useCustom ? cp : '';
      var wq = $('wqTrucks'); if (wq && !wq.dataset.touched) wq.value = n;
      var wg = $('wqGross'); if (wg && !wg.dataset.touched) wg.value = g;
    };
    var qs = new URLSearchParams(location.search), want = qs.get('truck') || { semi: 'dry-van', small: 'box-truck' }[qs.get('type')];
    if (want) { var r0 = est.querySelector('input[name=estTruck][value="' + want + '"]'); if (r0) r0.checked = true; }
    pick(true); lastTruck = current();
    TS.tool(est, { run: estCalc, equipment: function () { return current().name; } }).run(false);
  }

  /* free quote: opens WhatsApp with the carrier's details filled in (nothing is stored by us) */
  var wa = document.getElementById('waQuote');
  if (wa && cfg) {
    var wt = document.getElementById('wqTruck'), hint = document.getElementById('wqPctHint');
    var syncHint = function () { var tr = truckById(wt.value); hint.textContent = 'Our rate for a ' + tr.name + ': ' + pctTxt(tr.pct) + ' of weekly gross (OTR)'; };
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
      TS.track('click_whatsapp', { link_location: 'estimate_quote', equipment: tr.name });
      window.open(url, '_blank', 'noopener');
    });
  }

  /* ---------------------------------------------------------------- inquiry + callback forms
     Web3Forms emails each submission to the dispatch inbox. lead_form_submit /
     callback_request fire only after Web3Forms confirms success. Duplicate
     sends in the same session are blocked; failures are shown to the visitor
     with a WhatsApp fallback and reported to GA4 as lead_form_error. */
  each(document.querySelectorAll('form[data-web3]'), function (form) {
    var status = form.querySelector('.form-status');
    var btn = form.querySelector('button[type=submit]');
    var kind = form.getAttribute('data-kind') || 'lead';
    var busy = false;
    function show(msg, ok, htmlMsg) { if (htmlMsg) status.innerHTML = msg; else status.textContent = msg; status.className = 'form-status ' + (ok ? 'ok' : 'err'); }
    function val(n) { var el = form.querySelector('[name="' + n + '"]'); return el ? el.value.trim() : ''; }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (busy) return;
      if (form.botcheck && form.botcheck.checked) return;
      var oneof = form.querySelectorAll('[data-oneof]');
      var hasContact = !oneof.length || Array.prototype.some.call(oneof, function (el) { return el.value.trim(); });
      each(oneof, function (el) { el.setCustomValidity(hasContact ? '' : 'Enter a phone number or an email address.'); });
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var sig = [kind, val('name'), val('phone'), val('email')].join('|').toLowerCase();
      var sent = store.get('sessionStorage', 'ts:sent') || {};
      if (sent[sig] && Date.now() - sent[sig] < 30 * 60 * 1000) {
        show('We already received this request at ' + new Date(sent[sig]).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + '. A dispatcher will contact you; no need to send it again.', true);
        return;
      }
      var data = new FormData(form);
      var consent = form.querySelector('input[name=sms_consent]');
      var agreed = consent && consent.checked;
      data.append('access_key', WEB3FORMS_ACCESS_KEY);
      data.append('subject', form.getAttribute('data-subject') || 'New dispatch inquiry');
      data.append('from_name', 'Texas Solutions Dispatch Website');
      data.append('form_type', kind === 'callback' ? 'Callback request' : 'Carrier inquiry');
      data.append('page', location.href.split('?')[0]);
      data.append('submission_id', Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 8));
      data.append('submitted_at', new Date().toISOString());
      var a = TS.attribution();
      Object.keys(a).forEach(function (k) { data.append('attribution_' + k, a[k]); });
      data.set('sms_consent', agreed ? 'Yes - agreed to SMS' : 'No');
      if (!agreed) { data.set('sms_consent_text', 'not given'); data.set('sms_consent_version', 'not given'); }
      data.delete('botcheck');
      busy = true;
      var label = btn.textContent; btn.disabled = true; btn.textContent = 'Sending...';
      fetch(ENDPOINT, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
        .then(function (r) { return r.json().catch(function () { return { success: r.ok }; }); })
        .then(function (res) {
          if (!(res && res.success)) throw new Error('rejected');
          sent[sig] = Date.now(); store.set('sessionStorage', 'ts:sent', sent);
          TS.track(kind === 'callback' ? 'callback_request' : 'lead_form_submit', {
            form_id: form.id, equipment: val('equipment') || undefined, trucks: val('trucks') || undefined,
            mc_status: val('mc_status') || undefined, contact_method: val('contact_method') || undefined, sms_consent: agreed ? 'yes' : 'no'
          });
          form.reset();
          show(kind === 'callback' ? 'Thank you. A dispatcher will call you back. For a faster reply, message us on WhatsApp.' : 'Thank you. A Texas Solutions dispatcher will contact you shortly. For a faster reply, message us on WhatsApp.', true);
        })
        .catch(function (err) {
          TS.track('lead_form_error', { form_id: form.id, error_type: err && err.message === 'rejected' ? 'rejected' : 'network' });
          var txt = encodeURIComponent((kind === 'callback' ? 'CALLBACK REQUEST' : 'DISPATCH INQUIRY') + '\nName: ' + val('name') + '\nPhone: ' + (val('phone') || '-') +
            '\nEmail: ' + (val('email') || '-') + '\nEquipment: ' + (val('equipment') || '-') + '\nHome state: ' + (val('home_state') || '-') +
            '\nTrucks: ' + (val('trucks') || '-') + '\nMC status: ' + (val('mc_status') || '-') + '\nBest time: ' + (val('best_time') || '-'));
          show('Sorry, your details could not be sent. Nothing was saved. Please <a href="tel:+18389103147">call (838) 910-3147</a> or <a href="https://wa.me/18389103147?text=' + txt + '" target="_blank" rel="noopener">send them on WhatsApp</a>.', false, true);
        })
        .then(function () { busy = false; btn.disabled = false; btn.textContent = label; });
    });
  });

  /* ---------------------------------------------------------------- fuel data (mirror of tools/fuel_data.py) */
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  TS.human = function (iso) { if (!iso) return ''; var p = iso.split('-'); return MONTHS[+p[1] - 1] + ' ' + (+p[2]) + ', ' + p[0]; };
  TS.fuelStatus = function (observed, cadence, maxAge) {
    if (!observed) return 'unavailable';
    var p = observed.split('-'), now = new Date();
    var age = Math.floor((Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()) - Date.UTC(+p[0], +p[1] - 1, +p[2])) / 864e5);
    return age <= (maxAge || { daily: 2, weekly: 9 })[cadence] ? 'fresh' : 'stale';
  };
  TS.fuelLabel = function (r) {
    if (!r || r.status === 'unavailable') return 'No current price available; enter your pump price';
    var what = r.source + (r.fallback ? ' for the ' + r.regionName + ' region (no daily ' + r.name + ' value)' : '');
    return what + ', ' + (r.cadence === 'weekly' ? 'week of ' : '') + TS.human(r.observed) + (r.status === 'stale' ? ' (stale: the source has not updated since)' : '');
  };
  TS.fuelResolve = function (data, states, code, fuel, maxAge) {
    var f = data && data.fuels && data.fuels[fuel], st = states[code];
    var mk = function (raw, src, level, extra) {
      var r = { geo: code, name: st.name, fuel: fuel, price: raw ? raw.price : null, level: level, source: src.name, sourceUrl: src.url,
        cadence: src.cadence, observed: raw ? raw.observed : null, fallback: level === 'regional' };
      r.status = raw ? TS.fuelStatus(r.observed, r.cadence, maxAge) : 'unavailable';
      for (var k in extra || {}) r[k] = extra[k];
      return r;
    };
    if (!f || !st) return { status: 'unavailable', price: null };
    if (f.states[code]) return mk(f.states[code], f.sources.state, 'state');
    var reg = f.regions[st.region];
    if (reg) return mk(reg, f.sources.region, 'regional', { regionName: reg.name });
    return mk(null, f.sources.state, 'state');
  };

  /* ---------------------------------------------------------------- fuel cost calculator */
  var fc = document.getElementById('fuelCalc');
  if (fc) {
    var F = JSON.parse(fc.getAttribute('data-fuel'));
    var g = function (id) { return document.getElementById(id); };
    var usd = function (n, d) { return TS.money(n, d); };
    var num = TS.num;
    var weight = g('fuelWeight'), priceIn = g('fuelPrice'), stateSel = g('fuelState'), typeSel = g('fuelType');
    var data = F.fuel, lastTruckId = null, rec = null;
    var truck = function () { var c = fc.querySelector('input[name=fuelTruck]:checked'); for (var i = 0; i < F.trucks.length; i++) if (c && F.trucks[i].id === c.value) return F.trucks[i]; return F.trucks[0]; };
    var fuelKind = function () { return F.gasTrucks.indexOf(truck().id) >= 0 ? typeSel.value : 'diesel'; };
    var fillPrice = function () {
      rec = TS.fuelResolve(data, F.states, stateSel.value, fuelKind(), F.maxAge);
      priceIn.value = rec.price ? rec.price.toFixed(3) : '';
      priceIn.dataset.auto = '1';
      var nm = fuelKind() === 'gasoline' ? 'Gasoline' : 'Diesel';
      g('fuelPriceLabel').textContent = nm;
      g('fuelPriceNote').textContent = rec.price ? F.states[stateSel.value].name + ' ' + nm.toLowerCase() + ': $' + rec.price.toFixed(3) + '/gal (' + TS.fuelLabel(rec) + '). Type your pump price to override it.'
        : 'No current ' + nm.toLowerCase() + ' price for ' + F.states[stateSel.value].name + '. Type your pump price.';
      g('fuelPriceNote').className = 'hint' + (rec.status === 'stale' ? ' stale' : '');
    };
    var pickTruck = function (reset) {
      var tr = truck();
      weight.max = tr.max; if (reset) weight.value = tr.def;
      g('fuelMax').textContent = tr.max.toLocaleString('en-US') + ' lbs';
      g('fuelReeferWrap').hidden = tr.id !== 'reefer';
      g('fuelTypeWrap').hidden = F.gasTrucks.indexOf(tr.id) < 0;
    };
    var fuelRun = function () {
      var tr = truck();
      if (tr.id !== lastTruckId) { pickTruck(lastTruckId !== null); if (lastTruckId !== null && priceIn.dataset.auto) fillPrice(); lastTruckId = tr.id; }
      var w = +weight.value;
      g('fuelWeightOut').textContent = w.toLocaleString('en-US') + ' lbs';
      // gallons per mile rise linearly with cargo weight (calibrated to FHWA / NACFE data)
      var baseMpg = tr.empty / (1 + tr.k * w / 1000);
      var over = Math.max(0, num('fuelSpeed') - 62);
      var auto = Math.max(baseMpg * 0.6, baseMpg - tr.spd * over);
      var mpg = num('fuelMpg') > 0 ? num('fuelMpg') : auto;
      var miles = num('fuelMiles') + num('fuelDead');
      var driveGal = miles / mpg;
      var idleGal = num('fuelIdle') * tr.idle;
      var reeferGal = tr.id === 'reefer' ? num('fuelReefer') * F.reeferGph : 0;
      var gal = driveGal + idleGal + reeferGal;
      var price = num('fuelPrice');
      var cost = gal * price;
      g('fuelMpgOut').textContent = mpg.toFixed(1) + ' mpg' + (num('fuelMpg') > 0 ? ' (yours)' : '');
      g('fuelTotalMi').textContent = miles.toLocaleString('en-US') + ' mi';
      g('fuelGal').textContent = gal.toLocaleString('en-US', { maximumFractionDigits: 1 }) + ' gal';
      g('fuelSplit').textContent = [driveGal, idleGal, reeferGal].map(function (x) { return x.toFixed(1); }).join(' / ') + ' gal';
      g('fuelCpm').textContent = usd(cost / miles, 2) + ' /mi';
      g('fuelPriceUsed').textContent = usd(price, 3) + ' /gal (' + fuelKind() + ')';
      g('fuelPriceSrc').textContent = priceIn.dataset.auto && rec && rec.price ? TS.fuelLabel(rec) : 'Your price (entered manually)';
      g('fuelBig').innerHTML = usd(cost) + '<small>for ' + miles.toLocaleString('en-US') + ' miles</small>';
      var rate = num('fuelRate'), rev = rate * num('fuelMiles');
      g('fuelRevRow').hidden = g('fuelShareRow').hidden = !(rate > 0);
      if (rate > 0) { g('fuelNet').textContent = usd(rev - cost) + ' of ' + usd(rev); g('fuelShare').textContent = rev ? (cost / rev * 100).toFixed(1) + '%' : '-'; }
    };
    priceIn.addEventListener('input', function () { delete priceIn.dataset.auto; });
    stateSel.addEventListener('change', fillPrice);
    typeSel.addEventListener('change', fillPrice);
    var qsF = new URLSearchParams(location.search), wantT = qsF.get('truck'), wantS = (qsF.get('state') || '').toUpperCase();
    if (wantS && F.states[wantS]) stateSel.value = wantS;
    if (wantT) { var rt = fc.querySelector('input[name=fuelTruck][value="' + wantT + '"]'); if (rt) rt.checked = true; }
    pickTruck(true); lastTruckId = truck().id; fillPrice();
    var fuelTool = TS.tool(fc, {
      run: fuelRun, positive: ['fuelMiles', 'fuelPrice'], equipment: function () { return truck().name; },
      validate: function () { return priceIn.value === '' ? 'Enter your fuel price: there is no current state average to fill in.' : null; },
      afterRestore: function () { pickTruck(false); lastTruckId = truck().id; if (priceIn.dataset.auto) fillPrice(); }
    });
    fuelTool.run(false);
    // Pick up newer prices if this page was served from a cache.
    fetch('data/fuel-prices.json', { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
      if (d && d.fuels && JSON.stringify(d) !== JSON.stringify(data)) {
        data = d; if (priceIn.dataset.auto) fillPrice(); fuelTool.run(false);
      }
    }).catch(function () { /* keep the prices built into the page */ });
  }

  /* expandable lists (home FAQ: "See all FAQs") */
  each(document.querySelectorAll('[data-expand]'), function (b) {
    b.addEventListener('click', function () {
      var box = document.getElementById(b.getAttribute('data-expand'));
      if (!box) return;
      var opening = box.hasAttribute('hidden');
      if (opening) { box.removeAttribute('hidden'); each(box.querySelectorAll('.rv'), function (el) { el.classList.add('in'); }); }
      else box.setAttribute('hidden', '');
      b.setAttribute('aria-expanded', opening ? 'true' : 'false');
      b.textContent = b.getAttribute(opening ? 'data-less' : 'data-more');
    });
  });

  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
})();
