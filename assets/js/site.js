(function () {
  document.documentElement.classList.add('js');
  var root = document.documentElement;
  var header = document.querySelector('.site-header');

  // Header height drives the mobile menu offset and anchor scroll margin
  function setHeaderHeight() {
    if (header) root.style.setProperty('--hdr-h', header.offsetHeight + 'px');
  }
  setHeaderHeight();
  window.addEventListener('load', setHeaderHeight);
  window.addEventListener('resize', setHeaderHeight);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(setHeaderHeight);

  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    var main = document.getElementById('main');
    var footer = document.querySelector('.site-footer');
    var setOpen = function (open, returnFocus) {
      nav.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Menu');
      root.classList.toggle('nav-open', open);
      [main, footer].forEach(function (el) {
        if (!el) return;
        if (open) el.setAttribute('inert', ''); else el.removeAttribute('inert');
      });
      if (open) {
        setHeaderHeight();
        var first = nav.querySelector('a');
        if (first) first.focus({ preventScroll: true });
      } else if (returnFocus) {
        toggle.focus({ preventScroll: true });
      }
    };
    toggle.addEventListener('click', function () {
      setOpen(!nav.classList.contains('open'), false);
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setOpen(false, false); });
    });
    document.addEventListener('keydown', function (e) {
      if ((e.key === 'Escape' || e.key === 'Esc') && nav.classList.contains('open')) setOpen(false, true);
    });
    window.addEventListener('resize', function () {
      if (nav.classList.contains('open') && window.getComputedStyle(toggle).display === 'none') setOpen(false, false);
    });
  }

  // YouTube tours: load the player only after a click
  document.querySelectorAll('[data-yt]').forEach(function (btn) {
    var id = btn.getAttribute('data-yt') || '';
    if (!/^[A-Za-z0-9_-]{11}$/.test(id)) return;
    btn.addEventListener('click', function () {
      var iframe = document.createElement('iframe');
      iframe.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
      iframe.title = btn.getAttribute('data-yt-title') || 'YouTube video';
      iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      iframe.allowFullscreen = true;
      iframe.referrerPolicy = 'strict-origin-when-cross-origin';
      btn.replaceWith(iframe);
      iframe.focus();
    });
  });

  // Year
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Forms: AJAX submit to the endpoint in config.js (FormSubmit), with on-page success message
  var cfg = (window.SITE_CONFIG && window.SITE_CONFIG.forms) || {};
  document.querySelectorAll('form[data-form-key]').forEach(function (form) {
    var endpoint = (cfg[form.getAttribute('data-form-key')] || '').trim();
    var status = form.querySelector('.form-status');
    var btn = form.querySelector('button[type="submit"]');
    function show(cls, html) {
      if (!status) return;
      status.className = 'form-status show ' + cls;
      status.innerHTML = html;
      status.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    function revealThanks() {
      var fields = form.querySelector('[data-offer-fields]');
      var thanks = form.querySelector('[data-offer-thanks]');
      if (!fields || !thanks) return false;
      fields.hidden = true;
      thanks.hidden = false;
      thanks.focus({ preventScroll: true });
      thanks.scrollIntoView({ behavior: 'smooth', block: 'center' });
      return true;
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var fallback = 'Please email <a href="mailto:devin@axfordrealestate.ca">devin@axfordrealestate.ca</a> or call <a href="tel:+16048091032">604-809-1032</a>.';
      if (!endpoint) { show('error', 'This form is not connected right now, so nothing was sent. ' + fallback); return; }
      var fd = new FormData(form);
      if (fd.get('_honey')) { form.reset(); if (!revealThanks()) show('success', 'Thanks! Your message has been sent.'); return; } // bot trap
      var data = {};
      fd.forEach(function (v, k) { data[k] = data[k] ? data[k] + ', ' + v : v; });
      if (data.email) data._replyto = data.email;
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = 'Sending…'; }
      fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          var ok = res.ok && String(res.j.success) !== 'false';
          if (ok) {
            form.reset();
            if (!revealThanks()) show('success', '<strong>Thanks — your request has been sent!</strong> Devin will be in touch soon. If it\'s urgent, call <a href="tel:+16048091032">604-809-1032</a>.');
          } else {
            show('error', 'Sorry, something went wrong and your request may not have been sent. ' + fallback);
          }
        })
        .catch(function () { show('error', 'Sorry, we couldn\'t send your request (network error). ' + fallback); })
        .then(function () { if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label || 'Send'; } });
    });
  });

  // Two-step intake (tenant landing page)
  document.querySelectorAll('[data-next-step]').forEach(function (btn) {
    var form = btn.closest('form');
    var wrap = form.querySelector('[data-step2-wrap]');
    btn.addEventListener('click', function () {
      var fields = btn.parentElement.querySelectorAll('input,select,textarea');
      for (var i = 0; i < fields.length; i++) { if (!fields[i].reportValidity()) return; }
      wrap.classList.add('open');
      btn.style.display = 'none';
      var first = wrap.querySelector('select,input,textarea');
      if (first) first.focus({ preventScroll: true });
      wrap.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  // Sticky mobile CTA: hide while the hero or the intake form is on screen
  var sticky = document.querySelector('[data-sticky-cta]');
  var intake = document.getElementById('intake');
  if (sticky && intake && 'IntersectionObserver' in window) {
    var onScreen = [];
    var stickyObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var i = onScreen.indexOf(e.target);
        if (e.isIntersecting && i < 0) onScreen.push(e.target);
        if (!e.isIntersecting && i > -1) onScreen.splice(i, 1);
      });
      sticky.classList.toggle('hide', onScreen.length > 0);
    }, { threshold: 0.15 });
    stickyObserver.observe(intake);
    document.querySelectorAll('[data-sticky-hide]').forEach(function (el) { stickyObserver.observe(el); });
  }
})();
