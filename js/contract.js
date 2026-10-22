/* Sign Contract page: fill, e-sign, download the signed PDF, and send a copy to the dispatch team.
   Agreement text comes from #contractData (tools/content.py CONTRACT), so the page and the PDF always match. */
(function () {
  var form = document.getElementById('contractForm');
  var dataEl = document.getElementById('contractData');
  if (!form || !dataEl) return;
  var K = JSON.parse(dataEl.textContent);
  var $ = function (id) { return document.getElementById(id); };
  var val = function (n) { var el = form.querySelector('[name="' + n + '"]'); return el ? el.value.trim() : ''; };
  var status = $('k-status');
  var show = function (msg, ok) { status.textContent = msg; status.className = 'form-status ' + (ok ? 'ok' : 'err'); };

  var now = new Date();
  var dateText = now.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  $('k-date').textContent = dateText;
  Array.prototype.forEach.call(document.querySelectorAll('.k-date-copy'), function (el) { el.textContent = dateText; });

  /* fee and payment method shown inside the agreement text */
  /* fee: our standard rate for the equipment fills the field; the carrier may change it */
  var standardFee = function () { var f = K.fees[val('equipment')]; return f ? String(f) : ''; };
  var fee = function () { var n = parseFloat(val('fee')); return isFinite(n) && n > 0 ? String(n) : ''; };
  $('k-equipment').addEventListener('change', function () { $('k-fee').value = standardFee(); syncTerms(); });
  var payment = function () { return val('payment') === 'Other' ? (val('payment_other') || 'Other') : val('payment'); };
  var syncTerms = function () {
    Array.prototype.forEach.call(document.querySelectorAll('.k-fee'), function (el) { el.textContent = fee() || '__'; });
    Array.prototype.forEach.call(document.querySelectorAll('.k-pay'), function (el) { el.textContent = payment() || '__'; });
    var other = val('payment') === 'Other';
    $('k-other-wrap').hidden = !other;
    $('k-payment_other').required = other;
  };
  ['k-equipment', 'k-fee', 'k-payment', 'k-payment_other'].forEach(function (id) { $(id).addEventListener('input', syncTerms); $(id).addEventListener('change', syncTerms); });
  syncTerms();

  /* ---------------------------------------------------------------- signature: draw or type */
  var canvas = $('k-canvas'), ctx = canvas.getContext('2d'), drawn = false, drawing = false, mode = 'draw';
  ctx.lineWidth = 3.2; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.strokeStyle = '#0a0a0a';
  var pt = function (e) {
    var r = canvas.getBoundingClientRect();
    return [(e.clientX - r.left) * canvas.width / r.width, (e.clientY - r.top) * canvas.height / r.height];
  };
  canvas.addEventListener('pointerdown', function (e) {
    drawing = true; canvas.setPointerCapture(e.pointerId);
    var p = pt(e); ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(p[0] + 0.1, p[1] + 0.1); ctx.stroke();
    drawn = true; canvas.parentNode.classList.add('signed');
  });
  canvas.addEventListener('pointermove', function (e) { if (!drawing) return; var p = pt(e); ctx.lineTo(p[0], p[1]); ctx.stroke(); });
  ['pointerup', 'pointercancel', 'pointerleave'].forEach(function (t) { canvas.addEventListener(t, function () { drawing = false; }); });
  $('k-clear').addEventListener('click', function () { ctx.clearRect(0, 0, canvas.width, canvas.height); drawn = false; canvas.parentNode.classList.remove('signed'); });

  var typed = $('k-typed'), preview = $('k-typed-preview');
  typed.addEventListener('input', function () { preview.textContent = typed.value; });
  Array.prototype.forEach.call(document.querySelectorAll('.k-pad-tabs button'), function (b) {
    b.addEventListener('click', function () {
      mode = b.getAttribute('data-mode');
      Array.prototype.forEach.call(document.querySelectorAll('.k-pad-tabs button'), function (o) {
        o.classList.toggle('on', o === b); o.setAttribute('aria-selected', o === b ? 'true' : 'false');
      });
      $('k-pad-draw').hidden = mode !== 'draw';
      $('k-pad-type').hidden = mode !== 'type';
      if (mode === 'type' && !typed.value) { typed.value = val('rep_name'); preview.textContent = typed.value; }
    });
  });

  /* signatures as JPEG images on white; typed names and the dispatcher's signature use a script font */
  function scriptSignature(name, stamp) {
    /* stamp: the dispatcher's signature, larger in Great Vibes, slightly tilted, with an orange flourish */
    var c = document.createElement('canvas'); c.width = 900; c.height = 260;
    var x = c.getContext('2d');
    var face = stamp ? '400 SIZEpx "Great Vibes", "Dancing Script", cursive' : '600 SIZEpx "Dancing Script", cursive';
    x.fillStyle = '#fff'; x.fillRect(0, 0, c.width, c.height);
    x.fillStyle = '#0a0a0a'; x.textBaseline = 'middle';
    var size = stamp ? 170 : 120; x.font = face.replace('SIZE', size);
    while (x.measureText(name).width > 820 && size > 40) { size -= 6; x.font = face.replace('SIZE', size); }
    if (stamp) {
      x.save(); x.translate(30, 128); x.rotate(-0.05); x.fillText(name, 0, 0); x.restore();
      var w = x.measureText(name).width;
      x.strokeStyle = '#f97316'; x.lineWidth = 5; x.lineCap = 'round';
      x.beginPath(); x.moveTo(60, 214); x.bezierCurveTo(260, 236, 520, 226, Math.min(870, w + 70), 186); x.stroke();
    } else {
      x.fillText(name, 20, 140);
    }
    return c.toDataURL('image/jpeg', 0.92);
  }
  function signatureImage() {
    if (mode === 'type') return typed.value.trim() ? scriptSignature(typed.value.trim()) : null;
    if (!drawn) return null;
    var c = document.createElement('canvas'); c.width = 900; c.height = 260;
    var x = c.getContext('2d');
    x.fillStyle = '#fff'; x.fillRect(0, 0, c.width, c.height);
    x.drawImage(canvas, 0, 0);
    return c.toDataURL('image/jpeg', 0.92);
  }

  /* ---------------------------------------------------------------- PDF */
  function loadImage(src) {
    return new Promise(function (res) {
      var img = new Image();
      img.onload = function () {
        /* downscale onto white and embed as JPEG so the PDF stays small */
        var k = Math.min(1, 640 / img.naturalWidth), c = document.createElement('canvas');
        c.width = Math.round(img.naturalWidth * k); c.height = Math.round(img.naturalHeight * k);
        var g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height); g.drawImage(img, 0, 0, c.width, c.height);
        res({ data: c.toDataURL('image/jpeg', 0.9), w: c.width, h: c.height });
      };
      img.onerror = function () { res(null); };
      img.src = src;
    });
  }

  function buildPdf(info, sig, logo) {
    var jsPDF = window.jspdf.jsPDF;
    var doc = new jsPDF({ unit: 'pt', format: 'letter' });
    var W = doc.internal.pageSize.getWidth(), H = doc.internal.pageSize.getHeight(), M = 54, y = 0;
    var ORANGE = [249, 115, 22], INK = [10, 10, 10], MUTED = [92, 87, 82], GREEN = [21, 128, 61];
    var setC = function (c) { doc.setTextColor(c[0], c[1], c[2]); };
    var need = function (h) { if (y + h > H - 60) { doc.addPage(); y = 64; } };
    var text = function (t, size, style, color, gap) {
      doc.setFont('helvetica', style || 'normal'); doc.setFontSize(size); setC(color || INK);
      var lines = doc.splitTextToSize(t, W - 2 * M), lh = size * 1.38;
      lines.forEach(function (l) { need(lh); doc.text(l, M, y); y += lh; });
      y += gap == null ? 6 : gap;
    };
    var bullets = function (items) {
      doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5); setC(INK);
      items.forEach(function (it) {
        var lines = doc.splitTextToSize(it, W - 2 * M - 16);
        lines.forEach(function (l, i) { need(15); if (!i) { doc.setFillColor(ORANGE[0], ORANGE[1], ORANGE[2]); doc.circle(M + 4, y - 3.5, 2, 'F'); } doc.text(l, M + 16, y); y += 15; });
      });
      y += 6;
    };
    var heading = function (t) { need(34); y += 8; doc.setFont('helvetica', 'bold'); doc.setFontSize(12.5); setC(INK); doc.text(t.toUpperCase(), M, y); y += 8; doc.setDrawColor(ORANGE[0], ORANGE[1], ORANGE[2]); doc.setLineWidth(1.5); doc.line(M, y, M + 36, y); y += 16; };
    var fieldRow = function (label, value) {
      need(20); doc.setFont('helvetica', 'normal'); doc.setFontSize(10); setC(MUTED); doc.text(label, M, y);
      doc.setFont('helvetica', 'bold'); setC(INK); doc.text(String(value || '-'), M + 110, y);
      doc.setDrawColor(220, 216, 210); doc.setLineWidth(0.6); doc.line(M + 108, y + 4, W - M, y + 4); y += 20;
    };

    /* header: logo left, black and orange bars right */
    /* slanted black bar with an orange bar under it, as on the web page */
    doc.setFillColor(INK[0], INK[1], INK[2]); doc.rect(W - 250, 0, 250, 52, 'F'); doc.triangle(W - 250, 0, W - 250, 52, W - 290, 52, 'F');
    doc.setFillColor(ORANGE[0], ORANGE[1], ORANGE[2]); doc.rect(W - 170, 56, 170, 10, 'F'); doc.triangle(W - 170, 56, W - 170, 66, W - 180, 66, 'F');
    if (logo) { var lw = 160, lh = lw * logo.h / logo.w; doc.addImage(logo.data, 'JPEG', M, 28, lw, lh); }
    y = 128;
    text(K.title, 24, 'bold', INK, 4);
    text('This Dispatch Services Agreement ("Agreement") is entered into on ' + info.date + ', by and between:', 11, 'normal', INK, 10);

    heading('Dispatch company');
    fieldRow('Company', K.dispatcher.name); fieldRow('Address', K.dispatcher.address); fieldRow('Email', K.dispatcher.email); fieldRow('Phone', K.dispatcher.phone);
    heading('Carrier');
    fieldRow('Company name', info.company); fieldRow('MC number', info.mc); fieldRow('USDOT number', info.usdot);
    fieldRow('Address', info.address); fieldRow('Phone', info.phone); fieldRow('Email', info.email); fieldRow('Equipment', info.equipment);

    K.sections.forEach(function (s, i) {
      heading((i + 1) + '. ' + s[0]);
      s[1].forEach(function (p) {
        if (Array.isArray(p)) bullets(p);
        else text(p.replace('{fee}', info.fee).replace('{payment}', info.payment), 10.5, 'normal', INK, 6);
      });
    });
    heading('Required documents from the Carrier');
    text('Before dispatch services begin, the Carrier should provide:', 10.5, 'normal', INK, 4);
    bullets(K.documents);
    text(K.attorney_note, 9.5, 'italic', MUTED, 6);

    /* signatures */
    need(250); heading('Signatures');
    var col = (W - 2 * M - 24) / 2;
    doc.setFont('helvetica', 'bold'); doc.setFontSize(11); setC(INK); doc.text('DISPATCHER', M, y); doc.text('CARRIER', M + col + 24, y); y += 18;
    doc.setFont('helvetica', 'normal'); doc.setFontSize(10);
    doc.text('Company: ' + K.dispatcher.name, M, y); doc.text('Company: ' + info.company, M + col + 24, y, { maxWidth: col }); y += 16;
    doc.text('Signed by: ' + K.dispatcher_signature, M, y); doc.text('Representative: ' + info.rep, M + col + 24, y, { maxWidth: col }); y += 10;
    var sigTop = y + 6;
    doc.setDrawColor(200, 196, 190); doc.setLineWidth(0.8);
    doc.roundedRect(M, sigTop, col, 70, 6, 6); doc.roundedRect(M + col + 24, sigTop, col, 70, 6, 6);
    if (info.dispatcherSig) doc.addImage(info.dispatcherSig, 'JPEG', M + 10, sigTop + 6, col - 20, (col - 20) * 260 / 900);
    if (sig) doc.addImage(sig, 'JPEG', M + col + 34, sigTop + 6, col - 20, (col - 20) * 260 / 900);
    y = sigTop + 88; setC(INK); doc.setFontSize(10);
    doc.text('Date: ' + info.date, M, y); doc.text('Date: ' + info.date, M + col + 24, y); y += 22;
    doc.setFontSize(8.5); setC(MUTED);
    var es = doc.splitTextToSize(K.esign, col); doc.text(es, M + col + 24, y); y += es.length * 11 + 10;

    /* signature certificate */
    doc.addPage(); y = 70;
    text('Electronic signature certificate', 18, 'bold', INK, 8);
    heading('Document');
    fieldRow('Agreement', K.title); fieldRow('Version', K.version); fieldRow('Document ID', info.docId);
    heading('Signer');
    fieldRow('Name', info.rep); fieldRow('Company', info.company); fieldRow('Email', info.email); fieldRow('Phone', info.phone);
    fieldRow('Signature type', info.mode === 'type' ? 'Typed name' : 'Drawn by hand');
    fieldRow('Signed at', info.signedLocal); fieldRow('Signed (UTC)', info.signedUtc);
    heading('Device');
    text(info.ua, 8.5, 'normal', MUTED, 4);
    text('Signed on ' + info.page, 8.5, 'normal', MUTED, 10);
    doc.setDrawColor(GREEN[0], GREEN[1], GREEN[2]); doc.setFillColor(234, 247, 238);
    need(40); doc.roundedRect(M, y, W - 2 * M, 34, 6, 6, 'FD'); doc.setFont('helvetica', 'bold'); doc.setFontSize(10); setC(GREEN);
    doc.text('Signed electronically by the Carrier and by ' + K.dispatcher_signature + '.', M + 12, y + 21);

    /* page footers */
    var n = doc.getNumberOfPages();
    for (var i = 1; i <= n; i++) {
      doc.setPage(i); doc.setFont('helvetica', 'normal'); doc.setFontSize(8); setC(MUTED);
      doc.text('Document ID: ' + info.docId + '  |  ' + K.version, M, H - 28);
      doc.text('Page ' + i + ' of ' + n, W - M, H - 28, { align: 'right' });
      doc.setDrawColor(ORANGE[0], ORANGE[1], ORANGE[2]); doc.setLineWidth(2); doc.line(0, H - 4, W, H - 4);
    }
    return doc;
  }

  /* ---------------------------------------------------------------- document uploads
     One field per document (Web3Forms Pro sends each as an attachment, 5 MB max per file).
     Photos are resized to 2000 px JPEG in the browser; PDFs are sent as they are. */
  var MAX_BYTES = 5 * 1024 * 1024;
  var docs = {};
  var kb = function (n) { return n > 1048576 ? (n / 1048576).toFixed(1) + ' MB' : Math.max(1, Math.round(n / 1024)) + ' KB'; };
  var shrinkImage = function (f) {
    return new Promise(function (res) {
      var url = URL.createObjectURL(f), img = new Image();
      img.onload = function () {
        var k = Math.min(1, 2000 / Math.max(img.naturalWidth, img.naturalHeight)), c = document.createElement('canvas');
        c.width = Math.round(img.naturalWidth * k); c.height = Math.round(img.naturalHeight * k);
        var g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height); g.drawImage(img, 0, 0, c.width, c.height);
        URL.revokeObjectURL(url);
        c.toBlob(function (b) { res(b ? new File([b], f.name.replace(/\.[^.]+$/, '') + '.jpg', { type: 'image/jpeg' }) : f); }, 'image/jpeg', 0.82);
      };
      img.onerror = function () { URL.revokeObjectURL(url); res(f); };  /* e.g. HEIC the browser cannot draw: send as is */
      img.src = url;
    });
  };
  Array.prototype.forEach.call(form.querySelectorAll('.k-up input[type=file]'), function (input) {
    var box = input.closest('.k-up'), state = box.querySelector('.k-up-state'), label = box.querySelector('.k-up-label').firstChild.textContent.trim();
    var reset = function (msg, err) { delete docs[input.name]; box.classList.remove('has-file'); box.classList.toggle('bad', !!err); state.textContent = msg || 'Choose file or take a photo'; };
    input.addEventListener('change', function () {
      var f = input.files && input.files[0];
      if (!f) { reset(); return; }
      var isImg = /^image\//.test(f.type), isPdf = f.type === 'application/pdf' || /\.pdf$/i.test(f.name);
      if (!isImg && !isPdf) { input.value = ''; reset('Please choose a photo or a PDF.', true); return; }
      state.textContent = 'Preparing ' + f.name + '...';
      (isImg ? shrinkImage(f) : Promise.resolve(f)).then(function (out) {
        if (out.size > MAX_BYTES) { input.value = ''; reset(f.name + ' is ' + kb(out.size) + '. The limit is 5 MB.', true); return; }
        docs[input.name] = { file: out, label: label };
        box.classList.add('has-file'); box.classList.remove('bad');
        state.textContent = out.name + ' · ' + kb(out.size);
      });
    });
  });
  var fileName = function (label, company, file) {
    var ext = (file.name.match(/\.[a-z0-9]+$/i) || ['.pdf'])[0].toLowerCase();
    return (label.replace(/\(.*?\)/g, '') + ' ' + company).trim().replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '') + ext;
  };

  /* ---------------------------------------------------------------- submit */
  var lastDoc = null, lastName = '', busy = false;
  $('k-again').addEventListener('click', function () { if (lastDoc) lastDoc.save(lastName); });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (busy) return;
    syncTerms();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    var sig = signatureImage();
    if (!sig) { show(mode === 'type' ? 'Type your name to sign.' : 'Draw your signature in the box to sign.', false); return; }
    if (!window.jspdf) { show('The PDF tool is still loading. Please wait a moment and press the button again.', false); return; }
    busy = true; show('Preparing your signed agreement...', true);
    var signed = new Date();
    var info = {
      company: val('company'), mc: val('mc'), usdot: val('usdot'), address: val('address'), phone: val('phone'), email: val('email'),
      equipment: val('equipment'), fee: fee(), standardFee: standardFee(), payment: payment(), rep: val('rep_name'), mode: mode, date: dateText,
      docId: (window.crypto && crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36) + Math.random().toString(36).slice(2)).toUpperCase(),
      signedLocal: signed.toString(), signedUtc: signed.toISOString(), ua: navigator.userAgent, page: location.href.split('?')[0]
    };
    (document.fonts && document.fonts.load ? Promise.all([document.fonts.load('600 40px "Dancing Script"'), document.fonts.load('400 40px "Great Vibes"')]) : Promise.resolve())
      .then(function () { sig = signatureImage(); info.dispatcherSig = scriptSignature(K.dispatcher_signature, true); return loadImage(K.logo); })
      .then(function (logo) {
        lastDoc = buildPdf(info, sig, logo);
        lastName = 'Texas-Solutions-Dispatch-Agreement-' + (info.company || 'carrier').replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '') + '.pdf';
        lastDoc.save(lastName);
        /* copy for the dispatch team: every field, the signature image and the document ID */
        var small = document.createElement('canvas'); small.width = 450; small.height = 130;
        var img = new Image();
        /* white background so the attachment is not black where the pad is transparent */
        return new Promise(function (res) { img.onload = function () { var c = small.getContext('2d'); c.fillStyle = '#fff'; c.fillRect(0, 0, 450, 130); c.drawImage(img, 0, 0, 450, 130); small.toBlob(res, 'image/png'); }; img.src = sig; })
          .then(function (sigSmall) {
            var fd = new FormData();
            fd.append('access_key', TS.form.key);
            fd.append('subject', 'Signed dispatch agreement: ' + info.company + ' (' + info.equipment + ', ' + info.fee + '%)');
            fd.append('from_name', 'Texas Solutions Dispatch Website');
            fd.append('form_type', 'Signed dispatch agreement');
            fd.append('agreement_version', K.version);
            fd.append('document_id', info.docId);
            fd.append('carrier_company', info.company); fd.append('mc_number', info.mc); fd.append('usdot_number', info.usdot);
            fd.append('address', info.address); fd.append('phone', info.phone); fd.append('email', info.email);
            fd.append('equipment', info.equipment); fd.append('dispatch_fee_percent', info.fee);
            fd.append('standard_fee_percent', info.standardFee);
            fd.append('fee_changed_by_carrier', info.fee !== info.standardFee ? 'YES - carrier entered ' + info.fee + '% (standard ' + info.standardFee + '%)' : 'No'); fd.append('payment_method', info.payment);
            fd.append('representative', info.rep); fd.append('name', info.rep);
            fd.append('signature_type', info.mode === 'type' ? 'Typed name' : 'Drawn by hand');
            fd.append('dispatcher_signature', 'Auto-signed: ' + K.dispatcher_signature);
            fd.append('signed_at_utc', info.signedUtc); fd.append('signed_at_local', info.signedLocal);
            fd.append('agreement_date', info.date); fd.append('user_agent', info.ua); fd.append('page', info.page);
            fd.append('signature_image', 'Attached as a PNG file (also printed in the signed PDF)');
            /* attachments: the signed PDF plus any documents the carrier uploaded */
            var names = Object.keys(docs);
            fd.append('documents_attached', names.length ? names.map(function (n) { return docs[n].label; }).join(', ') : 'None uploaded');
            var withFiles = new FormData();
            fd.forEach(function (v, k) { withFiles.append(k, v); });
            withFiles.append('contract_pdf', new File([lastDoc.output('blob')], lastName, { type: 'application/pdf' }));
            if (sigSmall) withFiles.append('signature', new File([sigSmall], 'Signature-' + (info.company || 'carrier').replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '') + '.png', { type: 'image/png' }));
            names.forEach(function (n) { withFiles.append(n, docs[n].file, fileName(docs[n].label, info.company, docs[n].file)); });
            show(names.length ? 'Sending your signed agreement and ' + names.length + ' document' + (names.length > 1 ? 's' : '') + '...' : 'Sending your signed agreement...', true);
            var send = function (body) {
              /* no Content-Type header: the browser sets the multipart boundary */
              return fetch(TS.form.endpoint, { method: 'POST', body: body, headers: { Accept: 'application/json' } })
                .then(function (r) { return r.json().catch(function () { return { success: r.ok }; }); });
            };
            return send(withFiles).then(function (res) {
              if (res && res.success) return res;
              /* attachments refused: still deliver the agreement details, and ask for the files another way */
              info.filesFailed = true;
              fd.set('documents_attached', 'Attachments could not be sent: ' + (res && res.message ? res.message : 'rejected'));
              fd.set('signature_image', 'Not attached (attachments were refused); it is printed in the PDF the carrier downloaded');
              return send(fd);
            });
          });
      })
      .then(function (res) {
        if (!(res && res.success)) throw new Error('rejected');
        if (info.filesFailed) $('k-done').querySelector('p').textContent = 'Your signed PDF has downloaded and your agreement details reached our team, but the attachments could not be sent. Please email the PDF and your documents to ' + K.notify_email + ' or WhatsApp them to (838) 910-3147.';
        if (TS.track) TS.track('contract_signed', { equipment: info.equipment, fee: info.fee });
        status.className = 'form-status'; status.textContent = '';
        $('k-done').hidden = false; $('k-done').scrollIntoView({ behavior: 'smooth', block: 'center' });
        form.querySelector('.k-submit').hidden = true;
      })
      .catch(function () {
        if (lastDoc) show('Your PDF downloaded, but the copy could not reach our team. Please email the PDF to ' + K.notify_email + ' or WhatsApp it to (838) 910-3147.', false);
        else show('Something went wrong while creating the PDF. Please try again, or call (838) 910-3147.', false);
      })
      .then(function () { busy = false; });
  });
})();
