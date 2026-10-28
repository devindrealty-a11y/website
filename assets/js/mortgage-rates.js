/*
 * Mortgage rate explorer. Numbers come from assets/data/mortgage-rates.json.
 * Edit that file to refresh rates. This script does not call FormSubmit.
 * The intro form is a normal data-form-key form handled by site.js.
 *
 * monthlyPayment uses Canadian semi-annual compounding, the same convention
 * as the affordability calculator. It is principal and interest only.
 */
(function () {
  var DEFAULT_TERM = "5y-fixed";
  var DEFAULT_BANK = "rbc";

  function monthlyPayment(principal, annualRatePct, years) {
    if (!(principal > 0) || !(years > 0) || !isFinite(principal) || !isFinite(annualRatePct)) return null;
    if (annualRatePct <= 0) return principal / (years * 12);
    var monthly = Math.pow(1 + annualRatePct / 200, 1 / 6) - 1;
    var n = years * 12;
    var growth = Math.pow(1 + monthly, n);
    return principal * (monthly * growth) / (growth - 1);
  }

  function formatRate(n) {
    return (Math.round(n * 100) / 100).toFixed(2);
  }

  function formatMoney(n) {
    return n.toLocaleString("en-CA", { style: "currency", currency: "CAD" });
  }

  function boot() {
    var root = document.getElementById("rate-explorer");
    if (!root) return;
    var embedded = document.getElementById("mortgage-rates-data");
    var data = null;
    if (embedded) {
      try { data = JSON.parse(embedded.textContent); } catch (err) { data = null; }
    }
    if (data) apply(root, data);

    var url = root.getAttribute("data-rates-url");
    if (!url || !window.fetch) return;
    fetch(url, { credentials: "same-origin" })
      .then(function (res) {
        if (!res.ok) throw new Error("rates");
        return res.json();
      })
      .then(function (fresh) {
        if (!fresh || !fresh.banks || !fresh.terms) return;
        if (!data || fresh.updated !== data.updated) apply(root, fresh);
      })
      .catch(function () { /* baked-in rates stay on the page */ });
  }

  function apply(root, data) {
    var terms = data.terms || [];
    var banks = data.banks || [];
    var termById = {};
    var bankById = {};
    terms.forEach(function (term) { termById[term.id] = term; });
    banks.forEach(function (bank) { bankById[bank.id] = bank; });

    var termInputs = root.querySelectorAll('input[name="rate-term"]');
    var bankInputs = root.querySelectorAll('input[name="rate-bank"]');
    var cards = root.querySelectorAll("[data-bank-card]");
    var asofNodes = document.querySelectorAll("[data-rates-asof]");
    var figure = root.querySelector("[data-panel-figure]");
    var kickerBank = root.querySelector("[data-panel-bank]");
    var kickerTerm = root.querySelector("[data-panel-term]");
    var spread = root.querySelector("[data-panel-spread]");
    var sourceLink = root.querySelector("[data-panel-source]");
    var payForm = root.querySelector("[data-pay-form]");
    var payOut = root.querySelector("[data-pay-out]");
    var payNote = root.querySelector("[data-pay-note]");
    var typeRate = document.querySelectorAll("[data-type-rate]");
    var selection = document.getElementById("intro-selection");
    var selectionLabel = document.getElementById("intro-selection-label");
    var calcLinks = root.querySelectorAll("[data-calc-link]");

    var params = new URLSearchParams(window.location.search);
    var initialTerm = params.get("term");
    var initialBank = params.get("bank");
    if (!termById[initialTerm]) initialTerm = checkedValue(termInputs) || DEFAULT_TERM;
    if (!bankById[initialBank]) initialBank = DEFAULT_BANK;
    setChecked(termInputs, initialTerm);
    setChecked(bankInputs, "all");
    var interacted = Boolean(params.get("term") || params.get("bank"));

    function selectedTerm() {
      return termById[checkedValue(termInputs)] || terms[0];
    }

    function selectedBankId() {
      var pressed = root.querySelector("[data-bank-card][aria-pressed='true']");
      var id = pressed && pressed.getAttribute("data-bank-card");
      if (bankById[id] && !pressed.hidden) return id;
      var visible = null;
      cards.forEach(function (card) {
        if (!visible && !card.hidden) visible = card.getAttribute("data-bank-card");
      });
      return visible || (banks[0] && banks[0].id);
    }

    function rateFor(bank, term) {
      if (!bank || !term || !bank.rates) return null;
      return bank.rates[term.id] || null;
    }

    function paint() {
      var term = selectedTerm();
      var filter = checkedValue(bankInputs) || "all";
      cards.forEach(function (card) {
        var id = card.getAttribute("data-bank-card");
        var bank = bankById[id];
        var cell = rateFor(bank, term);
        card.hidden = filter !== "all" && id !== filter;
        var value = card.querySelector("[data-card-rate]");
        var meta = card.querySelector("[data-card-meta]");
        if (value) value.textContent = cell ? formatRate(cell.rate) : "—";
        if (meta) meta.textContent = cell && cell.spread ? cell.spread : (term ? term.label : "");
      });

      var bankId = filter !== "all" ? filter : selectedBankId();
      if (filter !== "all") bankId = filter;
      cards.forEach(function (card) {
        var on = card.getAttribute("data-bank-card") === bankId && !card.hidden;
        card.setAttribute("aria-pressed", on ? "true" : "false");
      });
      if (filter === "all" && !root.querySelector("[data-bank-card][aria-pressed='true']:not([hidden])")) {
        var first = root.querySelector("[data-bank-card]:not([hidden])");
        if (first) {
          first.setAttribute("aria-pressed", "true");
          bankId = first.getAttribute("data-bank-card");
        }
      }

      var bank = bankById[bankId];
      var cell = rateFor(bank, term);
      if (kickerBank) kickerBank.textContent = bank ? bank.name : "";
      if (kickerTerm) kickerTerm.textContent = term ? term.label : "";
      if (figure) figure.innerHTML = cell ? formatRate(cell.rate) + '<span class="rate-unit">%</span>' : "—";
      if (spread) {
        if (cell && cell.spread) {
          spread.hidden = false;
          spread.textContent = cell.spread + " as labeled by Ratehub.ca";
        } else {
          spread.hidden = true;
          spread.textContent = "";
        }
      }
      var sourceKey = term && term.source;
      var source = sourceKey && data.source && data.source[sourceKey];
      if (sourceLink && source) {
        sourceLink.href = source.url;
        sourceLink.textContent = source.label;
      }
      asofNodes.forEach(function (node) {
        node.textContent = data.updatedLabel || "";
      });

      var selectionText = bank && term && cell
        ? bank.legalName + ", " + term.label + ", " + formatRate(cell.rate) + "% illustrative (rates as of " + (data.updatedLabel || "") + ")"
        : "";
      if (selection) selection.value = selectionText;
      if (selectionLabel) {
        selectionLabel.textContent = selectionText
          ? "Your note will mention " + selectionText + "."
          : "";
      }
      typeRate.forEach(function (node) {
        node.textContent = cell ? formatRate(cell.rate) : "";
      });
      calcLinks.forEach(function (link) {
        var base = link.getAttribute("data-calc-base") || link.getAttribute("href");
        if (!link.getAttribute("data-calc-base") && base) link.setAttribute("data-calc-base", base.split("?")[0]);
        var clean = link.getAttribute("data-calc-base") || base;
        link.href = clean;
      });

      paintPayment();
      if (interacted) writeUrl(term && term.id, bankId);
    }

    function paintPayment() {
      if (!payOut) return;
      var term = selectedTerm();
      var bank = bankById[selectedBankId()];
      var cell = rateFor(bank, term);
      var price = numberValue("[data-pay-price]");
      var down = numberValue("[data-pay-down]");
      var years = numberValue("[data-pay-years]");
      if (!cell || price === null || down === null || years === null) {
        payOut.textContent = "—";
        if (payNote) payNote.textContent = "Enter an example price and down payment.";
        return;
      }
      if (down > price) {
        payOut.textContent = "—";
        if (payNote) payNote.textContent = "The down payment is higher than the example price.";
        return;
      }
      var principal = price - down;
      var payment = monthlyPayment(principal, cell.rate, years);
      if (payment === null) {
        payOut.textContent = "—";
        if (payNote) payNote.textContent = "Enter an example price above the down payment.";
        return;
      }
      payOut.textContent = formatMoney(payment);
      if (payNote) {
        payNote.textContent = "Principal and interest only, at " + formatRate(cell.rate) + "% on " + formatMoney(principal) + " over " + years + " years. Taxes, strata, heat, insurance, and mortgage default insurance are not included.";
      }
    }

    function numberValue(selector) {
      var input = root.querySelector(selector);
      if (!input) return null;
      if (input.value === "") return null;
      var n = Number(input.value);
      if (!isFinite(n) || n < 0) return null;
      return n;
    }

    function writeUrl(termId, bankId) {
      if (!window.history || !history.replaceState) return;
      var url = new URL(window.location.href);
      if (termId) url.searchParams.set("term", termId);
      if (bankId) url.searchParams.set("bank", bankId);
      history.replaceState(null, "", url.pathname + url.search + url.hash);
    }

    function onChoice() {
      interacted = true;
      paint();
    }
    termInputs.forEach(function (input) {
      input.addEventListener("change", onChoice);
    });
    bankInputs.forEach(function (input) {
      input.addEventListener("change", onChoice);
    });
    cards.forEach(function (card) {
      card.addEventListener("click", function () {
        cards.forEach(function (other) { other.setAttribute("aria-pressed", "false"); });
        card.setAttribute("aria-pressed", "true");
        onChoice();
      });
    });
    if (payForm) {
      payForm.addEventListener("submit", function (event) { event.preventDefault(); });
      payForm.addEventListener("input", paintPayment);
    }

    if (initialBank && bankById[initialBank]) {
      cards.forEach(function (card) {
        card.setAttribute("aria-pressed", card.getAttribute("data-bank-card") === initialBank ? "true" : "false");
      });
    }
    paint();
  }

  function checkedValue(nodes) {
    var value = "";
    nodes.forEach(function (node) { if (node.checked) value = node.value; });
    return value;
  }

  function setChecked(nodes, value) {
    nodes.forEach(function (node) { node.checked = node.value === value; });
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { monthlyPayment: monthlyPayment, formatRate: formatRate };
  }
  if (typeof document !== "undefined") {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
    else boot();
  }
})();
