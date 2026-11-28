/* First-time buyer page: property transfer tax estimate and guide request.
   Rates checked against gov.bc.ca on November 28, 2026. This is an estimate. */
(function () {
  var AS_OF = "November 28, 2026";

  function roundMoney(n) {
    return Math.round(n * 100) / 100;
  }

  function basePtt(price) {
    var tax = 0;
    tax += Math.min(price, 200000) * 0.01;
    if (price > 200000) tax += (Math.min(price, 2000000) - 200000) * 0.02;
    if (price > 2000000) tax += (price - 2000000) * 0.03;
    if (price > 3000000) tax += (price - 3000000) * 0.02;
    return roundMoney(tax);
  }

  function fthbExemption(price, base) {
    if (price <= 500000) return base;
    if (price <= 835000) return 8000;
    if (price < 860000) return roundMoney(8000 * (860000 - price) / 25000);
    return 0;
  }

  function newBuildExemption(price, base) {
    if (price <= 1100000) return base;
    if (price < 1150000) return roundMoney(base * ((1150000 - price) / 50000));
    return 0;
  }

  function estimatePtt(price, firstTime, newBuild) {
    var base = basePtt(price);
    var exemption = 0;
    var used = "none";
    var note = "No exemption was applied for the answers you chose.";
    if (newBuild) {
      var built = newBuildExemption(price, base);
      if (built > 0) {
        exemption = built;
        used = "newly-built";
        note = "This uses the newly built home exemption. A qualifying buyer of a new home can use it whether or not this is their first home. When both exemptions could apply, this one removes more of the tax.";
      } else if (price >= 1150000) {
        note = "The newly built home exemption is fully phased out at $1,150,000. The first-time buyers' program ends at $860,000, so it does not apply at this price either.";
      }
    }
    if (exemption === 0 && firstTime) {
      var first = fthbExemption(price, base);
      if (first > 0) {
        exemption = Math.min(first, base);
        used = "first-time";
        note = price <= 500000
          ? "At $500,000 or less, a qualifying first-time buyer can be exempt from the full tax."
          : "On a resale home over $500,000 and up to $835,000, the first-time exemption is $8,000. That is the tax on the first $500,000. It is not a full wipe of the tax. Between $835,000 and $860,000 the $8,000 shrinks to zero.";
      } else if (price >= 860000) {
        note = "The First Time Home Buyers' Program exemption ends at a fair market value of $860,000. At this price the estimate is the full tax.";
      }
    }
    exemption = roundMoney(Math.min(exemption, base));
    return {
      base: base,
      exemption: exemption,
      payable: roundMoney(Math.max(0, base - exemption)),
      used: used,
      note: note,
      further: price > 3000000
    };
  }

  function money(n) {
    return n.toLocaleString("en-CA", { style: "currency", currency: "CAD" });
  }

  function bootEstimator() {
    var form = document.getElementById("ptt-estimator");
    var out = document.getElementById("ptt-result");
    if (!form || !out) return;

    function readYes(name) {
      var picked = form.querySelector('input[name="' + name + '"]:checked');
      return picked ? picked.value === "yes" : false;
    }

    function render() {
      var raw = String(form.price.value || "").replace(/,/g, "").trim();
      var price = Number(raw);
      if (!raw || !isFinite(price) || price <= 0) {
        out.innerHTML = '<p class="ptt-empty">Enter a price to see an estimate.</p>';
        return;
      }
      var result = estimatePtt(price, readYes("first"), readYes("newbuild"));
      var usedLabel = result.used === "newly-built"
        ? "Newly built home exemption"
        : result.used === "first-time"
          ? "First Time Home Buyers' Program"
          : "No exemption applied";
      var further = result.further
        ? '<p class="ptt-note">This price is over $3 million, so the estimate includes the further 2% on the residential value above $3 million. It assumes the whole property is residential.</p>'
        : "";
      out.innerHTML =
        '<p class="ptt-kicker">Estimate only</p>' +
        '<p class="ptt-pay-label">Estimated property transfer tax</p>' +
        '<p class="ptt-pay">' + money(result.payable) + "</p>" +
        '<dl class="ptt-dl">' +
        "<div><dt>Tax before an exemption</dt><dd>" + money(result.base) + "</dd></div>" +
        "<div><dt>" + usedLabel + "</dt><dd>" + (result.exemption ? "− " + money(result.exemption) : money(0)) + "</dd></div>" +
        "</dl>" +
        '<p class="ptt-note">' + result.note + "</p>" +
        further +
        '<p class="ptt-note">Assumes you are buying the whole property, it is 0.5 hectares or smaller, and it is entirely residential. It does not include the additional tax that can apply to some foreign buyers. Checked ' + AS_OF + ". Your lawyer or notary calculates the tax on the registration.</p>";
    }

    form.addEventListener("input", render);
    form.addEventListener("change", render);
    render();
  }

  function bootForm() {
    var form = document.getElementById("ftb-guide");
    if (!form) return;
    var status = form.querySelector(".form-status");
    var btn = form.querySelector('button[type="submit"]');
    var cfg = (window.SITE_CONFIG && window.SITE_CONFIG.forms) || {};
    var pdf = form.getAttribute("data-pdf") || "assets/guides/first-time-home-buyer-guide-bc.pdf";

    function show(cls, html) {
      if (!status) return;
      status.className = "form-status show " + cls;
      status.innerHTML = html;
    }

    function track() {
      if (typeof window.ddCountGoat === "function") {
        window.ddCountGoat("first-time-guide");
        return;
      }
      if (!window.goatcounter || typeof window.goatcounter.count !== "function") return;
      try { window.goatcounter.count({ path: "first-time-guide", title: "first-time-guide", event: true }); } catch (err) {}
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var data = new FormData(form);
      if (data.get("_honey")) {
        form.reset();
        show("success", "<strong>Thanks. Your guide is ready.</strong>");
        return;
      }
      var name = String(data.get("name") || "").trim();
      var email = String(data.get("email") || "").trim();
      var when = String(data.get("when") || "").trim();
      var endpoint = String(cfg.firstTimeGuide || "").trim();
      var fallback = 'Please email <a href="mailto:devin@axfordrealestate.ca">devin@axfordrealestate.ca</a> or call <a href="tel:+16048091032">604-809-1032</a>.';
      if (!endpoint) {
        show("error", "This form is not connected yet. " + fallback);
        return;
      }
      var payload = {
        name: name,
        email: email,
        when: when,
        consent: "yes",
        form: "First-time buyer guide request",
        page: (window.location.origin || "") + (window.location.pathname || ""),
        _subject: "First-time buyer guide request",
        _template: "table",
        _replyto: email
      };
      if (cfg.formCc && endpoint === "https://formsubmit.co/ajax/devin@axfordrealestate.ca") payload._cc = cfg.formCc;
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = "Sending…"; }
      fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(payload)
      }).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (j) {
          return (r.ok && String(j.success) !== "false") ? "sent" : "error";
        });
      }).catch(function () { return "error"; }).then(function (copy) {
        if (copy === "sent") {
          track();
          form.reset();
          show("success", '<strong>Thanks. Devin has your request.</strong> <a href="' + pdf + '">Download the First-Time Buyer guide (PDF)</a>.');
        } else {
          show("error", "Sorry, the request did not go through. " + fallback);
        }
      }).then(function () {
        if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label || "Email me the guide"; }
      });
    });
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { estimatePtt: estimatePtt, basePtt: basePtt };
  }
  if (typeof document !== "undefined") {
    document.addEventListener("DOMContentLoaded", function () {
      bootEstimator();
      bootForm();
    });
  }
})();
