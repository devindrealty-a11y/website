/* Market-report PDF gate. Posts to FormSubmit, then reveals the file.
   Do not test-submit this form: the first real submission emails devin@axfordrealestate.ca.
   GoatCounter event "report-download" fires only after FormSubmit accepts the request.
   The event name does not include the visitor's name or email. */
(function () {
  var form = document.querySelector("form[data-market-report]");
  if (!form) return;
  var cfg = (window.SITE_CONFIG && window.SITE_CONFIG.forms) || {};
  var endpoint = (cfg.marketReport || form.getAttribute("action") || "").trim();
  var status = form.querySelector(".form-status");
  var btn = form.querySelector('button[type="submit"]');
  var thanks = form.querySelector("[data-report-thanks]");
  var download = form.querySelector("[data-report-download]");

  function show(cls, html) {
    if (!status) return;
    status.className = "form-status show " + cls;
    status.innerHTML = html;
  }

  function reveal() {
    var fields = form.querySelector(".form-grid");
    if (fields) fields.hidden = true;
    if (thanks) {
      thanks.hidden = false;
      if (thanks.focus) thanks.focus({ preventScroll: true });
    }
    if (download) download.click();
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    var fallback = 'Please email <a href="mailto:devin@axfordrealestate.ca">devin@axfordrealestate.ca</a> or call <a href="tel:+16048091032">604-809-1032</a>.';
    var fd = new FormData(form);
    if (fd.get("_honey")) {
      form.reset();
      show("success", "Thanks.");
      return;
    }
    if (!endpoint) {
      show("error", "This form is not connected right now, so nothing was sent. " + fallback);
      return;
    }
    var name = String(fd.get("name") || "").trim();
    var data = {};
    fd.forEach(function (v, k) {
      data[k] = data[k] ? data[k] + ", " + v : v;
    });
    data._subject = "Market report download: " + name;
    if (data.email) data._replyto = data.email;
    data.page = (window.location.origin || "") + (window.location.pathname || "");
    if (btn) {
      btn.disabled = true;
      btn.dataset.label = btn.textContent;
      btn.textContent = "Sending…";
    }
    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(data)
    })
      .then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; });
      })
      .then(function (res) {
        var ok = res.ok && String(res.j.success) !== "false";
        if (!ok) {
          show("error", "Sorry, something went wrong and your request may not have been sent. " + fallback);
          return;
        }
        if (window.goatcounter && typeof window.goatcounter.count === "function") {
          try { window.goatcounter.count({ path: "report-download", title: "report-download", event: true }); } catch (err) {}
        }
        form.reset();
        show("success", "<strong>Thanks.</strong> Your download should start now. If it does not, use the link below.");
        reveal();
      })
      .catch(function () {
        show("error", "Sorry, we could not send your request (network error). " + fallback);
      })
      .then(function () {
        if (btn) {
          btn.disabled = false;
          btn.textContent = btn.dataset.label || "Send me the PDF";
        }
      });
  });
})();
