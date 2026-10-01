(function () {
  document.documentElement.classList.add('js');
  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); });
    });
  }

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
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var fallback = 'Please email <a href="mailto:devin@axfordrealestate.ca">devin@axfordrealestate.ca</a> or call <a href="tel:+16048091032">604-809-1032</a>.';
      if (!endpoint) { show('error', 'This form is not connected right now, so nothing was sent. ' + fallback); return; }
      var fd = new FormData(form);
      if (fd.get('_honey')) { show('success', 'Thanks! Your message has been sent.'); form.reset(); return; } // bot trap
      var data = {};
      fd.forEach(function (v, k) { data[k] = data[k] ? data[k] + ', ' + v : v; });
      if (data.email) data._replyto = data.email;
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = 'Sending…'; }
      fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          var ok = res.ok && String(res.j.success) !== 'false';
          if (ok) {
            show('success', '<strong>Thanks — your request has been sent!</strong> Devin will be in touch soon. If it\'s urgent, call <a href="tel:+16048091032">604-809-1032</a>.');
            form.reset();
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

  // Sticky mobile CTA: hide while the intake form is on screen
  var sticky = document.querySelector('[data-sticky-cta]');
  var intake = document.getElementById('intake');
  if (sticky && intake && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { sticky.classList.toggle('hide', e.isIntersecting); });
    }, { threshold: 0.15 }).observe(intake);
  }
})();
