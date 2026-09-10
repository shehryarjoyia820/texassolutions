// Home page only: top scroll-progress bar, the rotating sample load board,
// and the dispatch assistant chat widget.
(function () {
  function initScrollProgress() {
    var bar = document.querySelector('[data-scroll-progress]');
    if (!bar) return;
    function onScroll() {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      var pct = max > 0 ? (h.scrollTop / max) * 100 : 0;
      bar.style.width = pct.toFixed(1) + '%';
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  var LANES = [
    ['Midland, TX → Phoenix, AZ', 'Dry Van', '872', '$2.41'],
    ['Laredo, TX → Atlanta, GA', 'Reefer', '1,142', '$2.68'],
    ['Dallas, TX → Denver, CO', 'Flatbed', '793', '$2.55'],
    ['Houston, TX → Memphis, TN', 'Dry Van', '587', '$2.33'],
    ['Odessa, TX → Oklahoma City, OK', 'Hotshot', '412', '$2.90'],
    ['El Paso, TX → Los Angeles, CA', 'Power Only', '801', '$2.22'],
    ['San Antonio, TX → Nashville, TN', 'Step Deck', '1,024', '$2.61'],
    ['Fort Worth, TX → Kansas City, MO', 'Reefer', '520', '$2.47'],
    ['Amarillo, TX → Salt Lake City, UT', 'Flatbed', '906', '$2.72'],
    ['Midland, TX → New Orleans, LA', 'Box Truck', '634', '$2.18']
  ];

  function initBoard() {
    var body = document.querySelector('[data-board-body]');
    if (!body) return;
    var tick = 0;
    function render() {
      body.innerHTML = '';
      for (var i = 0; i < 5; i++) {
        var r = LANES[(tick + i) % LANES.length];
        var row = document.createElement('div');
        row.className = 'board-cols board-row';
        row.innerHTML =
          '<div class="board-lane">' + r[0] + '</div>' +
          '<div style="font-size:14px">' + r[1] + '</div>' +
          '<div style="font-size:14px">' + r[2] + '</div>' +
          '<div class="board-rate">' + r[3] + '</div>';
        body.appendChild(row);
      }
    }
    render();
    setInterval(function () { tick = (tick + 1) % LANES.length; render(); }, 3200);
  }

  var QA = {
    'How is the dispatch fee charged?': 'Service is percentage-based under your signed agreement. There is no setup fee and no monthly subscription.',
    'What equipment do you dispatch?': 'Dry van, reefer, flatbed, step deck, power only, hotshot, box truck and straight truck. Tell us what you run and we will match lanes to it.',
    'Do you force loads?': 'No. You approve every load, lane and rate before anything is booked.',
    'How do I start?': 'Fill in the carrier application on this page, or call (838) 910-3147. Onboarding is four steps: apply, speak with us, sign the agreement, start dispatching.',
    'What does it cost?': 'No setup fee and no monthly subscription. Percentage-based pricing is discussed directly with you before paid service begins.'
  };

  function initChat() {
    var toggleBtn = document.querySelector('[data-chat-toggle]');
    var panel = document.querySelector('[data-chat-panel]');
    var closeBtn = document.querySelector('[data-chat-close]');
    var body = document.querySelector('[data-chat-body]');
    var quick = document.querySelector('[data-chat-quick]');
    if (!toggleBtn || !panel || !body || !quick) return;

    function addMsg(who, text) {
      var el = document.createElement('div');
      el.className = 'chat-msg ' + (who === 'me' ? 'me' : 'bot');
      el.textContent = text;
      body.appendChild(el);
      body.scrollTop = body.scrollHeight;
    }

    function setOpen(open) {
      panel.classList.toggle('is-open', open);
      toggleBtn.textContent = open ? 'Close' : 'Ask a dispatcher';
    }

    toggleBtn.addEventListener('click', function () {
      setOpen(!panel.classList.contains('is-open'));
    });
    if (closeBtn) closeBtn.addEventListener('click', function () { setOpen(false); });

    Object.keys(QA).forEach(function (q) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'btn btn-secondary';
      btn.textContent = q;
      btn.addEventListener('click', function () {
        addMsg('me', q);
        setTimeout(function () { addMsg('bot', QA[q]); }, 550);
      });
      quick.appendChild(btn);
    });
  }

  function initHeroVideo() {
    var video = document.querySelector('[data-hero-video]');
    if (!video) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      video.pause();
      video.removeAttribute('autoplay');
    }
  }

  function init() {
    initScrollProgress();
    initBoard();
    initChat();
    initHeroVideo();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
