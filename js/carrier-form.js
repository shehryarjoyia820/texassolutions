// Carrier application form: equipment picker, drag/drop file simulation,
// validation and a success state. Works on every element matching
// [data-carrier-form] so the same markup can appear on the home page and
// the contact page.
(function () {
  function initForm(root) {
    var fields = { name: '', phone: '', email: '', mc: '', lanes: '', consent: false, eq: '' };
    var files = [];
    var uploadTimer = null;

    var formView = root.querySelector('[data-form-view]');
    var doneView = root.querySelector('[data-done-view]');
    var errorEl = root.querySelector('[data-form-error]');
    var progressFill = root.querySelector('[data-progress-fill]');
    var progressLabel = root.querySelector('[data-progress-label]');
    var submitBtn = root.querySelector('[data-submit-btn]');
    var resetBtn = root.querySelector('[data-reset-btn]');
    var dropzone = root.querySelector('[data-dropzone]');
    var fileInput = root.querySelector('[data-file-input]');
    var fileList = root.querySelector('[data-file-list]');
    var eqButtons = root.querySelectorAll('[data-eq]');

    function requiredFilledCount() {
      var keys = ['name', 'phone', 'email', 'mc', 'eq'];
      var n = 0;
      keys.forEach(function (k) { if (String(fields[k]).trim()) n++; });
      return n;
    }

    function updateProgress() {
      var n = requiredFilledCount();
      var pct = Math.round((n / 5) * 100);
      if (progressFill) progressFill.style.width = pct + '%';
      if (progressLabel) progressLabel.textContent = n + '/5 complete';
    }

    function bindInput(name, onValue) {
      var el = root.querySelector('[data-field="' + name + '"]');
      if (!el) return;
      el.addEventListener('input', function () {
        fields[name] = onValue ? onValue(el) : el.value;
        if (errorEl) errorEl.textContent = '';
        updateProgress();
      });
    }
    bindInput('name');
    bindInput('phone');
    bindInput('email');
    bindInput('mc');
    bindInput('lanes');

    var consentEl = root.querySelector('[data-field="consent"]');
    if (consentEl) {
      consentEl.addEventListener('change', function () {
        fields.consent = consentEl.checked;
        if (errorEl) errorEl.textContent = '';
      });
    }

    eqButtons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var key = btn.getAttribute('data-eq');
        fields.eq = fields.eq === key ? '' : key;
        eqButtons.forEach(function (b) {
          b.classList.toggle('is-on', b.getAttribute('data-eq') === fields.eq);
        });
        updateProgress();
      });
    });

    function renderFiles() {
      if (!fileList) return;
      fileList.innerHTML = '';
      files.forEach(function (f) {
        var row = document.createElement('div');
        row.className = 'upload-row';
        var pct = Math.round(f.pct);
        row.innerHTML =
          '<div><div style="font-size:13px">' + escapeHtml(f.name) + '</div>' +
          '<div class="upload-bar"><span style="width:' + pct + '%"></span></div></div>' +
          '<span class="upload-status">' + (pct >= 100 ? 'Received' : 'Uploading') + '</span>';
        fileList.appendChild(row);
      });
    }

    function escapeHtml(s) {
      var div = document.createElement('div');
      div.textContent = s;
      return div.innerHTML;
    }

    function addFiles(list) {
      var added = Array.prototype.slice.call(list || []).slice(0, 6).map(function (f) {
        return { name: f.name, pct: 0 };
      });
      if (!added.length) return;
      files = files.concat(added);
      renderFiles();
      if (uploadTimer) clearInterval(uploadTimer);
      uploadTimer = setInterval(function () {
        var running = false;
        files = files.map(function (f) {
          if (f.pct >= 100) return f;
          running = true;
          return { name: f.name, pct: Math.min(100, f.pct + 12 + Math.random() * 16) };
        });
        renderFiles();
        if (!running) clearInterval(uploadTimer);
      }, 220);
    }

    if (dropzone) {
      dropzone.addEventListener('dragover', function (e) {
        e.preventDefault();
        dropzone.classList.add('is-dragging');
      });
      dropzone.addEventListener('dragleave', function () {
        dropzone.classList.remove('is-dragging');
      });
      dropzone.addEventListener('drop', function (e) {
        e.preventDefault();
        dropzone.classList.remove('is-dragging');
        addFiles(e.dataTransfer.files);
      });
    }
    if (fileInput) {
      fileInput.addEventListener('change', function () { addFiles(fileInput.files); });
    }

    function submit() {
      if (!fields.name.trim() || !fields.phone.trim() || !fields.email.trim()) {
        errorEl.textContent = 'Name, phone, and email are required.';
        return;
      }
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(fields.email)) {
        errorEl.textContent = 'Please enter a valid email address.';
        return;
      }
      if (fields.phone.replace(/\D/g, '').length < 10) {
        errorEl.textContent = 'Please enter a valid 10-digit phone number.';
        return;
      }
      if (!fields.consent) {
        errorEl.textContent = 'Please agree to the SMS terms to request a callback.';
        return;
      }
      errorEl.textContent = '';
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending…';
      setTimeout(function () {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Request a Free Callback';
        formView.style.display = 'none';
        doneView.style.display = 'block';
      }, 1100);
    }

    if (submitBtn) submitBtn.addEventListener('click', submit);

    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        fields = { name: '', phone: '', email: '', mc: '', lanes: '', consent: false, eq: '' };
        files = [];
        if (uploadTimer) clearInterval(uploadTimer);
        renderFiles();
        root.querySelectorAll('[data-field]').forEach(function (el) {
          if (el.type === 'checkbox') el.checked = false; else el.value = '';
        });
        eqButtons.forEach(function (b) { b.classList.remove('is-on'); });
        errorEl.textContent = '';
        updateProgress();
        doneView.style.display = 'none';
        formView.style.display = 'block';
      });
    }

    updateProgress();
  }

  function init() {
    document.querySelectorAll('[data-carrier-form]').forEach(initForm);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
