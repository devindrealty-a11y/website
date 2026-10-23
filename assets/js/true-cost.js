/*
 * True-cost estimator. Rates are the published 2026 figures cited on
 * true-cost-of-owning-a-home-bc.html. Dollars are integer cents.
 * This file does not call FormSubmit by itself; the sign-up
 * handler is boot() and only runs in the browser after the visitor submits.
 */
(function () {
  var CITIES = {
    coquitlam: { taxNumer: 38520, taxDenom: 100000, name: "Coquitlam" },
    "port-coquitlam": { taxNumer: 37754, taxDenom: 100000, name: "Port Coquitlam" },
    "port-moody": { taxNumer: 429125, taxDenom: 1000000, name: "Port Moody" }
  };

  // Annual city utility bills, in cents. Property-tax lines are separate.
  var UTILITY = {
    coquitlam: {
      detached: { small: 166100, medium: 175300, large: 190800 },
      townhouse: 108800,
      apartment: 108800
    },
    "port-coquitlam": {
      detached: 129400,
      townhouse: 118300,
      apartment: 91400,
      solidWaste: 33300
    },
    "port-moody": {
      detached: 189200,
      townhouse: 166200,
      apartment: 86400,
      apartmentCollection: 111600
    }
  };

  var STRATA_START = {
    coquitlam: 432,
    "port-coquitlam": 423,
    "port-moody": 450
  };

  function roundDiv(numer, denom) {
    return Math.round(numer / denom);
  }

  function money(cents) {
    var sign = cents < 0 ? "-" : "";
    var n = Math.abs(Math.round(cents));
    var dollars = Math.floor(n / 100);
    var rem = n % 100;
    var grouped = String(dollars).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return sign + "$" + grouped + "." + (rem < 10 ? "0" : "") + rem;
  }

  function additionalSchoolCents(assessed) {
    var between = Math.min(Math.max(assessed - 3000000, 0), 1000000);
    var over = Math.max(assessed - 4000000, 0);
    return Math.round(between / 5) + Math.round(over * 2 / 5);
  }

  function grantCents(assessed, kind, taxCents) {
    if (kind !== "basic" && kind !== "additional") return { cents: 0, floor: 0 };
    var full = kind === "additional" ? 84500 : 57000;
    var floor = kind === "additional" ? 10000 : 35000;
    var over = assessed - 2075000;
    var reduction = over > 0 ? Math.floor(over / 1000) * 500 : 0;
    var grant = Math.max(0, full - reduction);
    return { cents: Math.min(grant, Math.max(0, taxCents - floor)), floor: floor };
  }

  function utilityAnnual(input) {
    var city = input.city;
    var type = input.type;
    if (city === "coquitlam") {
      if (type === "detached") {
        var cart = input.cart === "small" || input.cart === "large" ? input.cart : "medium";
        return { cents: UTILITY.coquitlam.detached[cart], cart: cart };
      }
      return { cents: UTILITY.coquitlam[type] || UTILITY.coquitlam.townhouse, cart: "" };
    }
    if (city === "port-coquitlam") {
      return { cents: UTILITY["port-coquitlam"][type] || 0, cart: "" };
    }
    if (type === "apartment" && input.pmCollection) {
      return { cents: UTILITY["port-moody"].apartmentCollection, cart: "" };
    }
    return { cents: UTILITY["port-moody"][type] || 0, cart: "" };
  }

  function gasCents(gjTenths) {
    if (!(gjTenths > 0)) return 0;
    var basic = roundDiv(4216 * 365, 1200);
    var variable = Math.round(gjTenths * 12601 / 100);
    return basic + variable;
  }

  function electricCents(kwh) {
    if (!(kwh > 0)) return 0;
    var step1 = Math.min(kwh, 675);
    var step2 = Math.max(kwh - 675, 0);
    var basic = Math.round(2344 * 30 / 100);
    var energy = Math.round((step1 * 1187 + step2 * 1408) / 100);
    return basic + energy;
  }

  function estimate(input) {
    var city = CITIES[input.city] ? input.city : "coquitlam";
    var type = input.type === "detached" || input.type === "apartment" ? input.type : "townhouse";
    var homeValue = Math.max(0, Math.round(Number(input.homeValue) || 0));
    var assessed = Math.max(0, Math.round(Number(input.assessed) || 0));
    var spec = CITIES[city];
    var taxBefore = roundDiv(assessed * spec.taxNumer, spec.taxDenom);
    var schoolExtra = additionalSchoolCents(assessed);
    if (city === "port-coquitlam" && type === "detached") taxBefore += UTILITY["port-coquitlam"].solidWaste;
    taxBefore += schoolExtra;
    var grantResult = grantCents(assessed, input.grant, taxBefore);
    var grant = grantResult.cents;
    var taxNet = taxBefore - grant;
    var util = utilityAnnual({ city: city, type: type, cart: input.cart, pmCollection: !!input.pmCollection });
    var strata = Math.max(0, Math.round(Number(input.strataMonthly) || 0)) * 100;
    var insuranceAnnual = Math.max(0, Math.round(Number(input.insuranceAnnual) || 0)) * 100;
    var insurance = roundDiv(insuranceAnnual, 12);
    var pct = Math.max(0, Number(input.maintenancePercent) || 0);
    var maintenanceAnnual = Math.round(homeValue * pct);
    var maintenance = roundDiv(maintenanceAnnual, 12);
    var gas = gasCents(Math.max(0, Math.round(Number(input.gjTenths) || 0)));
    var electric = electricCents(Math.max(0, Math.round(Number(input.kwh) || 0)));
    var taxMonthly = roundDiv(taxNet, 12);
    var utilMonthly = roundDiv(util.cents, 12);
    var lines = [
      { key: "tax", label: "Property tax", monthly: taxMonthly, annual: taxNet },
      { key: "strata", label: "Strata fee", monthly: strata, annual: strata * 12 },
      { key: "insurance", label: "Home insurance", monthly: insurance, annual: insuranceAnnual },
      { key: "maintenance", label: "Maintenance", monthly: maintenance, annual: maintenanceAnnual },
      { key: "utilities", label: "City water, sewer and waste", monthly: utilMonthly, annual: util.cents },
      { key: "gas", label: "Natural gas", monthly: gas, annual: gas * 12 },
      { key: "electric", label: "Electricity", monthly: electric, annual: electric * 12 }
    ];
    var monthly = 0;
    var annual = 0;
    lines.forEach(function (line) {
      monthly += line.monthly;
      annual += line.annual;
    });
    return {
      city: city,
      cityName: spec.name,
      type: type,
      homeValue: homeValue,
      assessed: assessed,
      taxBefore: taxBefore,
      schoolExtra: schoolExtra,
      grant: grant,
      grantFloor: grantResult.floor,
      cart: util.cart,
      lines: lines,
      monthly: monthly,
      annual: annual
    };
  }

  function boot() {
    var form = document.getElementById("tc-estimator");
    var out = document.getElementById("tc-body");
    if (!form || !out) return;

    var cityEl = document.getElementById("tc-city");
    var typeEl = document.getElementById("tc-type");
    var valueEl = document.getElementById("tc-value");
    var assessedEl = document.getElementById("tc-assessed");
    var sameEl = document.getElementById("tc-same");
    var grantEl = document.getElementById("tc-grant");
    var strataEl = document.getElementById("tc-strata");
    var insuranceEl = document.getElementById("tc-insurance");
    var maintEl = document.getElementById("tc-maint");
    var kwhEl = document.getElementById("tc-kwh");
    var gjEl = document.getElementById("tc-gj");
    var cartEl = document.getElementById("tc-cart");
    var cartWrap = document.getElementById("tc-cart-wrap");
    var pmEl = document.getElementById("tc-pm-collection");
    var pmWrap = document.getElementById("tc-pm-wrap");
    var strataHint = document.getElementById("tc-strata-hint");
    var errorEl = document.getElementById("tc-error");
    var strataDirty = false;

    function digits(el) {
      return Math.round(Number(String(el.value).replace(/,/g, "")) || 0);
    }

    function suggestedStrata() {
      if (typeEl.value === "detached") return 0;
      return STRATA_START[cityEl.value] || 0;
    }

    function syncStrataHint() {
      if (!strataHint) return;
      if (typeEl.value === "detached") {
        strataHint.textContent = "Most detached houses have no strata fee. If the house is in a strata, type the monthly fee from the Form B.";
        return;
      }
      var n = STRATA_START[cityEl.value] || 0;
      strataHint.textContent = "Starting point: $" + n + " a month, the figure Relta calls typical among listed strata homes in this city that publish a fee. Condos and townhouses are mixed together in that sample. Replace it with the fee on the listing or the Form B.";
    }

    function syncExtras() {
      if (cartWrap) cartWrap.hidden = !(cityEl.value === "coquitlam" && typeEl.value === "detached");
      if (pmWrap) pmWrap.hidden = !(cityEl.value === "port-moody" && typeEl.value === "apartment");
      if (!strataDirty) strataEl.value = String(suggestedStrata());
      syncStrataHint();
    }

    function render() {
      syncExtras();
      if (sameEl && sameEl.checked) assessedEl.value = valueEl.value;
      var homeValue = digits(valueEl);
      var assessed = digits(assessedEl);
      if (!(homeValue > 0) || !(assessed > 0)) {
        errorEl.hidden = false;
        errorEl.textContent = "Enter a home value and an assessed value above zero. Property tax uses the assessed value.";
        out.hidden = true;
        return;
      }
      errorEl.hidden = true;
      out.hidden = false;
      var result = estimate({
        city: cityEl.value,
        type: typeEl.value,
        homeValue: homeValue,
        assessed: assessed,
        grant: grantEl.value,
        cart: cartEl ? cartEl.value : "medium",
        pmCollection: pmEl ? pmEl.checked : false,
        strataMonthly: digits(strataEl),
        insuranceAnnual: digits(insuranceEl),
        maintenancePercent: Number(maintEl.value) || 0,
        gjTenths: Math.round((Number(gjEl.value) || 0) * 10),
        kwh: digits(kwhEl)
      });
      var max = 0;
      result.lines.forEach(function (line) { if (line.monthly > max) max = line.monthly; });
      var rows = result.lines.map(function (line) {
        var width = max > 0 ? Math.max(0, Math.round(line.monthly / max * 100)) : 0;
        return '<div class="tc-line"><div class="tc-line-label"><span>' + line.label + '</span><span class="tc-bar" style="width:' + width + '%"></span></div><strong>' + money(line.monthly) + '</strong></div>';
      }).join("");
      var grantNote = result.grant > 0
        ? " Home owner grant applied: " + money(result.grant) + " a year. At least " + money(result.grantFloor) + " of tax stays on the bill."
        : " No home owner grant applied.";
      var schoolNote = result.schoolExtra > 0
        ? " Includes additional school tax of " + money(result.schoolExtra) + " a year on the value over $3 million."
        : "";
      out.innerHTML =
        '<p class="tc-total-label">Estimated monthly total, besides the mortgage</p>' +
        '<p class="tc-total">' + money(result.monthly) + '</p>' +
        '<p class="tc-annual">About ' + money(result.annual) + ' a year. ' + result.cityName + ", " + result.type.replace("-", " ") + "." + grantNote + schoolNote + "</p>" +
        '<div class="tc-lines">' + rows + "</div>" +
        '<p class="tc-overlap">Lines can overlap. A strata fee often already includes the building\'s insurance, some utilities, and common-property repairs. Natural gas and electricity here are before GST. This is not a quote and not a tax bill.</p>';
    }

    form.addEventListener("input", function (e) {
      if (e.target === strataEl) strataDirty = true;
      if (e.target === valueEl && sameEl && sameEl.checked) assessedEl.value = valueEl.value;
      render();
    });
    form.addEventListener("change", function (e) {
      if (e.target === cityEl || e.target === typeEl) strataDirty = false;
      render();
    });
    render();
    wireSignup();
  }

  function wireSignup() {
    var form = document.getElementById("tc-signup");
    if (!form) return;
    var status = form.querySelector(".form-status");
    var btn = form.querySelector('button[type="submit"]');
    var cfg = (window.SITE_CONFIG && window.SITE_CONFIG.forms) || {};

    function show(cls, html) {
      if (!status) return;
      status.className = "form-status show " + cls;
      status.innerHTML = html;
    }

    function track() {
      if (!window.goatcounter || typeof window.goatcounter.count !== "function") return;
      try { window.goatcounter.count({ path: "true-cost-signup", title: "true-cost-signup", event: true }); } catch (err) {}
    }

    function postCopy(name, email) {
      var endpoint = String(cfg.trueCostSignup || "").trim();
      if (!endpoint) return Promise.resolve("skipped");
      var payload = {
        name: name,
        email: email,
        consent: "yes",
        form: "True cost guide sign-up",
        page: (window.location.origin || "") + (window.location.pathname || ""),
        _subject: "True cost guide sign-up: " + name,
        _template: "table",
        _replyto: email
      };
      return fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(payload)
      }).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (j) {
          return (r.ok && String(j.success) !== "false") ? "sent" : "error";
        });
      }).catch(function () { return "error"; });
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var data = new FormData(form);
      if (data.get("_honey")) {
        form.reset();
        show("success", "<strong>Thanks. Devin has your request.</strong>");
        return;
      }
      var name = String(data.get("name") || "").trim();
      var email = String(data.get("email") || "").trim();
      var fallback = 'Please email <a href="mailto:devin@axfordrealestate.ca">devin@axfordrealestate.ca</a> or call <a href="tel:+16048091032">604-809-1032</a>.';
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = "Sending…"; }
      postCopy(name, email).then(function (copy) {
        if (copy === "sent") {
          track();
          form.reset();
          show("success", "<strong>Thanks. Devin has your request.</strong> He will email you about the guide.");
        } else {
          show("error", "Sorry, the signup did not go through. " + fallback);
        }
      }).then(function () {
        if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label || "Send me updates"; }
      });
    });
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = {
      estimate: estimate,
      money: money,
      gasCents: gasCents,
      electricCents: electricCents,
      STRATA_START: STRATA_START
    };
  }
  if (typeof document !== "undefined") {
    document.addEventListener("DOMContentLoaded", boot);
  }
})();
