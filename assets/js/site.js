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

  // Forms: wire to endpoint from config.js, or show placeholder notice (never sends anything)
  var cfg = (window.SITE_CONFIG && window.SITE_CONFIG.forms) || {};
  document.querySelectorAll('form[data-form-key]').forEach(function (form) {
    var key = form.getAttribute('data-form-key');
    var endpoint = (cfg[key] || '').trim();
    var status = form.querySelector('.form-status');
    if (endpoint) {
      form.setAttribute('action', endpoint);
      form.setAttribute('method', 'POST');
      return; // normal submission to the configured service
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      if (status) {
        status.className = 'form-status show placeholder';
        status.innerHTML = '[PLACEHOLDER] This draft form is not connected yet, so nothing was sent. ' +
          'In the meantime, please email <a href="mailto:devin@axfordrealestate.ca">devin@axfordrealestate.ca</a>.';
        status.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
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
