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
    if (form.hasAttribute('data-lead-form')) return;
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
      // Count the submit as a GoatCounter event, then post. count() does not return a
      // promise and a missing or blocked counter must not stop the FormSubmit request.
      var eventName = form.getAttribute('data-goat-event') || '';
      if (eventName && window.goatcounter && typeof window.goatcounter.count === 'function') {
        try { window.goatcounter.count({ path: eventName, title: eventName, event: true }); } catch (err) {}
      }
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

  // Qualifying lead form. Events are fixed names only: lead-form-start, lead-form-step-N
  // when that step is first shown, and lead-form-sent only after FormSubmit accepts it.
  // Nothing typed into the form is sent to GoatCounter.
  document.querySelectorAll('form[data-lead-form]').forEach(function (form) {
    var endpoint = (cfg[form.getAttribute('data-form-key')] || '').trim();
    var steps = Array.prototype.slice.call(form.querySelectorAll('[data-lead-step]'));
    var progress = form.querySelector('[data-lead-progress]');
    var fill = form.querySelector('[data-lead-fill]');
    var stepNum = form.querySelector('[data-lead-step-num]');
    var backBtn = form.querySelector('[data-lead-back]');
    var nextBtn = form.querySelector('[data-lead-next]');
    var submitBtn = form.querySelector('[data-lead-submit]');
    var status = form.querySelector('.form-status');
    var thanks = form.querySelector('[data-lead-thanks]');
    var body = form.querySelector('[data-lead-body]');
    var subjectInput = form.querySelector('input[name="_subject"]');
    var budgetInput = form.querySelector('input[name="budget"]');
    var budgetQInput = form.querySelector('input[name="budget_question"]');
    var pageInput = form.querySelector('input[name="page"]');
    var legend4 = form.querySelector('[data-lead-budget-legend]');
    var current = 1;
    var started = false;
    var seen = {};
    var sending = false;
    var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (pageInput) {
      pageInput.value = (window.location.origin || '') + (window.location.pathname || '');
    }

    var intentParam = '';
    try {
      intentParam = (new URLSearchParams(window.location.search).get('intent') || '').toLowerCase();
    } catch (err) {}
    var intentMap = { buying: 'Buying', selling: 'Selling', renting: 'Renting' };
    if (intentMap[intentParam]) {
      var preset = form.querySelector('input[name="intent"][value="' + intentMap[intentParam] + '"]');
      if (preset) preset.checked = true;
    }

    function track(name) {
      if (!name || !window.goatcounter || typeof window.goatcounter.count !== 'function') return;
      try { window.goatcounter.count({ path: name, title: name, event: true }); } catch (err) {}
    }

    function selected(name) {
      var el = form.querySelector('input[name="' + name + '"]:checked');
      return el ? el.value : '';
    }

    function fieldValue(name) {
      var el = form.querySelector('[name="' + name + '"]');
      return el ? el.value : '';
    }

    function intent() { return selected('intent'); }

    function budgetQuestion(kind) {
      if (kind === 'Renting') return "What's your monthly rent budget?";
      if (kind === 'Selling') return "What's your home's approximate value?";
      return "What's your budget?";
    }

    function syncBudgetGroups() {
      var rent = intent() === 'Renting';
      var onStep = current === 4;
      form.querySelectorAll('[data-budget-for]').forEach(function (group) {
        var on = (group.getAttribute('data-budget-for') === 'rent') === rent;
        group.hidden = !on;
        group.querySelectorAll('input').forEach(function (input) {
          if (!on) input.checked = false;
          input.disabled = !(on && onStep);
        });
      });
      if (legend4) legend4.textContent = budgetQuestion(intent() || 'Buying');
    }

    function syncSubject() {
      var i = selected('intent');
      var a = selected('area');
      var t = selected('timeline');
      var subject = (i && a && t) ? ('New qualified lead: ' + i + ', ' + a + ', ' + t) : 'New qualified lead';
      if (subjectInput) subjectInput.value = subject;
      var groupName = i === 'Renting' ? 'budget_rent' : 'budget_purchase';
      if (budgetInput) budgetInput.value = selected(groupName);
      if (budgetQInput) budgetQInput.value = i ? budgetQuestion(i) : '';
      return subject;
    }

    function showStatus(cls, html) {
      if (!status) return;
      status.className = 'form-status show ' + cls;
      status.innerHTML = html;
    }

    function markStart() {
      if (started) return;
      started = true;
      seen[1] = true;
      track('lead-form-start');
      track('lead-form-step-1');
    }

    function arrive(n) {
      if (!started || seen[n]) return;
      seen[n] = true;
      track('lead-form-step-' + n);
    }

    function setEnabled(stepEl, on) {
      stepEl.querySelectorAll('input, select, textarea').forEach(function (el) {
        if (el.type === 'hidden') return;
        el.disabled = !on;
      });
    }

    function showStep(n, focusIt) {
      current = n;
      steps.forEach(function (step, index) {
        var on = index + 1 === n;
        step.hidden = !on;
        setEnabled(step, on);
      });
      syncBudgetGroups();
      if (progress) {
        progress.setAttribute('aria-valuenow', String(n));
        progress.setAttribute('aria-valuetext', 'Step ' + n + ' of ' + steps.length);
      }
      if (fill) fill.style.width = ((n / steps.length) * 100) + '%';
      if (stepNum) stepNum.textContent = String(n);
      if (backBtn) backBtn.hidden = n === 1;
      if (nextBtn) nextBtn.hidden = n === steps.length;
      if (submitBtn) {
        submitBtn.hidden = n !== steps.length;
        submitBtn.disabled = sending || n !== steps.length;
      }
      syncSubject();
      if (focusIt) {
        var legend = steps[n - 1].querySelector('legend');
        if (legend) legend.focus({ preventScroll: true });
        steps[n - 1].scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'nearest' });
      }
      arrive(n);
    }

    function validateCurrent() {
      var fields = steps[current - 1].querySelectorAll('input, select, textarea');
      for (var i = 0; i < fields.length; i++) {
        var el = fields[i];
        if (el.disabled || el.type === 'hidden') continue;
        if ((el.type === 'text' || el.type === 'email' || el.tagName === 'TEXTAREA') && el.required && !el.value.trim()) {
          el.setCustomValidity('Please fill in this field.');
        } else {
          el.setCustomValidity('');
        }
        if (!el.checkValidity()) {
          el.reportValidity();
          return false;
        }
      }
      return true;
    }

    function goNext() {
      markStart();
      if (!validateCurrent()) return;
      if (current < steps.length) showStep(current + 1, true);
    }

    function goBack() {
      if (current > 1) showStep(current - 1, true);
    }

    function showThanks() {
      if (body) body.hidden = true;
      if (thanks) {
        thanks.hidden = false;
        thanks.focus({ preventScroll: true });
      }
    }

    form.addEventListener('focusin', markStart);
    if (backBtn) backBtn.addEventListener('click', goBack);
    if (nextBtn) nextBtn.addEventListener('click', goNext);
    form.addEventListener('change', function () {
      syncBudgetGroups();
      syncSubject();
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (current < steps.length) {
        goNext();
        return;
      }
      markStart();
      if (sending || !validateCurrent()) return;
      var honey = form.querySelector('input[name="_honey"]');
      if (honey && honey.value) {
        showThanks();
        return;
      }
      var fallback = 'Please email <a href="mailto:devin@axfordrealestate.ca">devin@axfordrealestate.ca</a> or call <a href="tel:+16048091032">604-809-1032</a>.';
      if (!endpoint) {
        showStatus('error', 'This form is not connected right now, so nothing was sent. ' + fallback);
        return;
      }
      syncSubject();
      var email = fieldValue('email').trim();
      var data = {
        _subject: subjectInput ? subjectInput.value : 'New qualified lead',
        _template: 'table',
        _honey: '',
        _replyto: email,
        form: 'Qualified lead',
        Intent: selected('intent'),
        Area: selected('area'),
        Timeline: selected('timeline'),
        Budget: budgetInput ? budgetInput.value : '',
        'Budget question': budgetQInput ? budgetQInput.value : '',
        'Moving from': selected('moving_from'),
        name: fieldValue('name').trim(),
        email: email,
        phone: fieldValue('phone').trim(),
        message: fieldValue('message').trim(),
        consent: 'yes',
        Page: pageInput ? pageInput.value : ''
      };
      sending = true;
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending…';
      }
      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(data)
      })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          var ok = res.ok && String(res.j.success) !== 'false';
          if (ok) {
            track('lead-form-sent');
            showThanks();
          } else {
            sending = false;
            if (submitBtn) {
              submitBtn.disabled = false;
              submitBtn.textContent = 'Send';
            }
            showStatus('error', 'Sorry, something went wrong and your request may not have been sent. ' + fallback);
          }
        })
        .catch(function () {
          sending = false;
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Send';
          }
          showStatus('error', 'Sorry, we couldn\'t send your request (network error). ' + fallback);
        });
    });

    showStep(1, false);
  });
})();
