/* Self-hosted chat widget. Guided answers stay in the browser.
   The message form posts to SITE_CONFIG.forms.chatLead (same FormSubmit URL as the other forms).
   GoatCounter events use fixed names only. chat-message-sent is counted only after
   FormSubmit accepts the message. count.js is async, so an event that happens before
   window.goatcounter.count exists is queued and sent when the script loads.
   A counter that never loads or throws is ignored. */
(function () {
  if (document.querySelector(".dd-chat")) return;

  var EMAIL = "devin@axfordrealestate.ca";
  var PHONE = "604-809-1032";
  var TEL = "tel:+16048091032";
  var CALC = "https://devindrealty-a11y.github.io/mortgage-calculator/";
  var HEADER = "Devin Desaulniers, REALTOR®, Axford Real Estate";

  var cfg = (window.SITE_CONFIG && window.SITE_CONFIG.forms) || {};
  var endpoint = (cfg.chatLead || "").trim();

  function siteBase() {
    var scripts = document.getElementsByTagName("script");
    for (var i = scripts.length - 1; i >= 0; i--) {
      var src = scripts[i].getAttribute("src") || "";
      if (src.indexOf("assets/js/chat.js") !== -1) {
        return new URL(src, window.location.href).href.replace(/assets\/js\/chat\.js(?:\?.*)?$/, "");
      }
    }
    return "";
  }
  var base = siteBase();

  var PATHS = [
    {
      id: "buy",
      event: "chat-buying",
      label: "Buying a home",
      answers: [
        {
          text: "Active homes for sale in Greater Vancouver and the Fraser Valley are on the listings page.",
          links: [{ href: "listings.html", label: "Homes for sale" }]
        },
        {
          text: "Neighbourhood guides cover communities in the Tri-Cities, BC, including Burquitlam, Port Moody, and Port Coquitlam.",
          links: [
            { href: "buyers.html#neighbourhoods", label: "Neighbourhood guides" },
            { href: "burquitlam-neighbourhood-guide.html", label: "Burquitlam guide" },
            { href: "port-moody.html", label: "Port Moody guide" },
            { href: "port-coquitlam.html", label: "Port Coquitlam guide" }
          ]
        },
        {
          text: "The mortgage affordability calculator is free. Results are estimates only. They are not a mortgage approval or financial advice.",
          links: [{ href: CALC, label: "Mortgage calculator", external: true }]
        }
      ]
    },
    {
      id: "rent",
      event: "chat-renting",
      label: "Renting — tenant relocation service, $1,500 + GST, paid by the tenant",
      answers: [
        {
          text: "The tenant relocation service is $1,500 + GST, paid by the tenant. It includes a consultation, a rental search, showings in person or by live video, and lease review and negotiation.",
          links: [{ href: "tenants.html", label: "Tenant relocation service" }]
        },
        {
          text: "Homes for rent in Greater Vancouver and the Fraser Valley are on the rentals page.",
          links: [{ href: "rentals.html", label: "Homes for rent" }]
        },
        {
          text: "If you are moving to Greater Vancouver, the relocating guide is a place to start. It includes the Tri-Cities, BC.",
          links: [{ href: "relocating-to-greater-vancouver.html", label: "Relocating to Greater Vancouver" }]
        }
      ]
    },
    {
      id: "move",
      event: "chat-relocating",
      label: "Relocating to Greater Vancouver",
      answers: [
        {
          text: "The relocating guide is written for people moving to Greater Vancouver, including the Tri-Cities, BC.",
          links: [{ href: "relocating-to-greater-vancouver.html", label: "Relocating to Greater Vancouver" }]
        },
        {
          text: "If you need a rental before you arrive, the tenant relocation service is $1,500 + GST, paid by the tenant. Homes for rent are listed separately.",
          links: [
            { href: "tenants.html", label: "Tenant relocation service" },
            { href: "rentals.html", label: "Homes for rent" }
          ]
        },
        {
          text: "If you are buying, start with homes for sale and the neighbourhood guides. The mortgage calculator gives an estimate only. It is not a mortgage approval.",
          links: [
            { href: "listings.html", label: "Homes for sale" },
            { href: "buyers.html#neighbourhoods", label: "Neighbourhood guides" },
            { href: CALC, label: "Mortgage calculator", external: true }
          ]
        }
      ]
    },
    {
      id: "sell",
      event: "chat-selling",
      label: "Selling a home",
      answers: [
        {
          text: "You can ask for a free market evaluation. Send the address on that page and Devin emails you recent sales nearby and what he would expect the home to bring. There is no cost, and asking does not mean you have to list.",
          links: [{ href: "home-evaluation.html", label: "Free home evaluation" }]
        },
        {
          text: "The evaluation is his opinion from recent sales. It is not an appraisal, and it is not a promise of a sale price.",
          links: []
        }
      ]
    }
  ];

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var topic = null;
  var step = "menu";
  var leadNoted = false;
  var inerted = [];

  var root = document.createElement("div");
  root.className = "dd-chat";

  var scrim = document.createElement("div");
  scrim.className = "dd-chat-scrim";
  scrim.hidden = true;
  scrim.setAttribute("aria-hidden", "true");

  var panel = document.createElement("div");
  panel.className = "dd-chat-panel";
  panel.id = "dd-chat-panel";
  panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-modal", "true");
  panel.setAttribute("aria-labelledby", "dd-chat-title");
  panel.hidden = true;
  panel.tabIndex = -1;

  var head = document.createElement("div");
  head.className = "dd-chat-head";
  var headText = document.createElement("div");
  var title = document.createElement("h2");
  title.className = "dd-chat-title";
  title.id = "dd-chat-title";
  title.textContent = HEADER;
  headText.appendChild(title);
  var closeBtn = document.createElement("button");
  closeBtn.type = "button";
  closeBtn.className = "dd-chat-close";
  closeBtn.setAttribute("aria-label", "Close chat");
  closeBtn.innerHTML = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6L6 18"/></svg>';
  head.appendChild(headText);
  head.appendChild(closeBtn);

  var body = document.createElement("div");
  body.className = "dd-chat-body";
  var log = document.createElement("div");
  log.className = "dd-chat-log";
  log.setAttribute("role", "log");
  log.setAttribute("aria-live", "polite");
  log.setAttribute("aria-relevant", "additions");
  var actions = document.createElement("div");
  actions.className = "dd-chat-actions";
  body.appendChild(log);
  body.appendChild(actions);
  panel.appendChild(head);
  panel.appendChild(body);

  var launch = document.createElement("button");
  launch.type = "button";
  launch.className = "dd-chat-launch";
  launch.setAttribute("aria-expanded", "false");
  launch.setAttribute("aria-controls", "dd-chat-panel");
  launch.setAttribute("aria-haspopup", "dialog");
  launch.innerHTML = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M5 6.5A2.5 2.5 0 0 1 7.5 4h9A2.5 2.5 0 0 1 19 6.5v7A2.5 2.5 0 0 1 16.5 16H12l-4.2 3.2c-.6.45-1.4.02-1.4-.7V16H7.5A2.5 2.5 0 0 1 5 13.5z"/></svg><span>Chat</span>';

  root.appendChild(panel);
  root.appendChild(launch);
  document.body.appendChild(scrim);
  document.body.appendChild(root);

  var pendingCounts = [];
  var countWatching = false;

  function goatcountReady() {
    return !!(window.goatcounter && typeof window.goatcounter.count === "function");
  }

  function flushCounts() {
    if (!goatcountReady() || !pendingCounts.length) return;
    var batch = pendingCounts.splice(0, pendingCounts.length);
    batch.forEach(function (payload) {
      try { window.goatcounter.count(payload); } catch (err) {}
    });
  }

  function watchGoatcounter() {
    if (countWatching) return;
    countWatching = true;
    var script = document.querySelector("script[data-goatcounter]");
    if (script) script.addEventListener("load", flushCounts);
    window.addEventListener("load", flushCounts);
    var tries = 0;
    var timer = setInterval(function () {
      tries += 1;
      flushCounts();
      if (!pendingCounts.length || tries >= 50) clearInterval(timer);
    }, 200);
  }

  function countEvent(name) {
    if (!name) return;
    // event must be boolean true. The path is the event name and does not start with "/".
    pendingCounts.push({ path: name, title: name, event: true });
    if (goatcountReady()) flushCounts();
    else watchGoatcounter();
  }

  function pageElts() {
    return Array.prototype.filter.call(document.body.children, function (el) {
      return el !== root && el !== scrim && el.tagName !== "SCRIPT";
    });
  }

  function setInert(on) {
    if (on) {
      inerted = [];
      pageElts().forEach(function (el) {
        if (el.hasAttribute("inert")) return;
        el.setAttribute("inert", "");
        inerted.push(el);
      });
      document.documentElement.classList.add("dd-chat-open");
    } else {
      inerted.forEach(function (el) { el.removeAttribute("inert"); });
      inerted = [];
      document.documentElement.classList.remove("dd-chat-open");
    }
  }

  function scrollToEnd() {
    body.scrollTo({ top: body.scrollHeight, behavior: reduceMotion ? "auto" : "smooth" });
  }

  function makeLink(item) {
    var a = document.createElement("a");
    a.className = "dd-chat-link";
    if (item.external) {
      a.href = item.href;
      a.target = "_blank";
      a.rel = "noopener";
    } else {
      a.href = base + item.href;
    }
    a.textContent = item.label;
    if (item.external) {
      var note = document.createElement("span");
      note.className = "dd-sr";
      note.textContent = " (opens in a new tab)";
      a.appendChild(note);
    }
    return a;
  }

  function addMessage(kind, text, links) {
    var row = document.createElement("div");
    row.className = "dd-msg dd-msg--" + kind;
    var bubble = document.createElement("div");
    bubble.className = "dd-bubble";
    var p = document.createElement("p");
    p.textContent = text;
    bubble.appendChild(p);
    if (links && links.length) {
      var list = document.createElement("div");
      list.className = "dd-chat-links";
      links.forEach(function (item) { list.appendChild(makeLink(item)); });
      bubble.appendChild(list);
    }
    row.appendChild(bubble);
    log.appendChild(row);
    return bubble;
  }

  function talkLine() {
    var p = document.createElement("p");
    p.className = "dd-chat-talk";
    p.appendChild(document.createTextNode("Prefer to talk? Call or text "));
    var a = document.createElement("a");
    a.href = TEL;
    a.textContent = PHONE;
    p.appendChild(a);
    p.appendChild(document.createTextNode("."));
    return p;
  }

  function choiceButton(label, primary, onClick) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "dd-choice" + (primary ? " dd-choice--primary" : "");
    b.textContent = label;
    b.addEventListener("click", onClick);
    return b;
  }

  function showMenu(moveFocus) {
    step = "menu";
    topic = null;
    leadNoted = false;
    log.textContent = "";
    actions.textContent = "";
    addMessage("bot", "Hi. I can point you to the right page on this site. If you want Devin to follow up, you can leave a message at the end.");
    addMessage("bot", "Are you buying, renting, relocating to Greater Vancouver, or selling? Renting here means the tenant relocation service: $1,500 + GST, paid by the tenant.");
    PATHS.forEach(function (path) {
      actions.appendChild(choiceButton(path.label, false, function () { choose(path); }));
    });
    actions.appendChild(talkLine());
    if (moveFocus) {
      var first = actions.querySelector(".dd-choice");
      if (first) first.focus({ preventScroll: true });
    }
  }

  function choose(path) {
    topic = path;
    step = "answers";
    leadNoted = false;
    countEvent(path.event);
    addMessage("user", path.label);
    path.answers.forEach(function (ans) {
      addMessage("bot", ans.text, ans.links);
    });
    actions.textContent = "";
    actions.appendChild(choiceButton("Send a message", true, showLead));
    actions.appendChild(choiceButton("Choose a different topic", false, function () { showMenu(true); }));
    actions.appendChild(talkLine());
    var sendBtn = actions.querySelector(".dd-choice--primary");
    if (sendBtn) sendBtn.focus({ preventScroll: true });
    scrollToEnd();
  }

  function field(id, labelText, opts) {
    var wrap = document.createElement("div");
    wrap.className = "field";
    var label = document.createElement("label");
    label.htmlFor = id;
    label.appendChild(document.createTextNode(labelText + " "));
    if (opts.required) {
      var req = document.createElement("span");
      req.className = "req";
      req.textContent = "*";
      label.appendChild(req);
    } else if (opts.hint) {
      var hint = document.createElement("span");
      hint.className = "hint";
      hint.textContent = opts.hint;
      label.appendChild(hint);
    }
    var input;
    if (opts.tag === "textarea") {
      input = document.createElement("textarea");
      input.rows = 4;
    } else {
      input = document.createElement("input");
      input.type = opts.type || "text";
    }
    input.id = id;
    input.name = opts.name;
    if (opts.required) input.required = true;
    if (opts.autocomplete) input.autocomplete = opts.autocomplete;
    if (opts.inputmode) input.inputMode = opts.inputmode;
    wrap.appendChild(label);
    wrap.appendChild(input);
    return wrap;
  }

  function showLead() {
    step = "lead";
    countEvent("chat-lead-shown");
    if (!leadNoted) {
      addMessage("bot", "Leave your name and email, and a short message. Phone is optional.");
      leadNoted = true;
    }
    actions.textContent = "";
    var form = document.createElement("form");
    form.className = "dd-chat-form";
    form.action = "#";
    form.method = "post";
    form.noValidate = false;

    function hidden(name, value) {
      var input = document.createElement("input");
      input.type = "hidden";
      input.name = name;
      input.value = value;
      form.appendChild(input);
    }
    hidden("_subject", "New chat widget message");
    hidden("_template", "table");
    hidden("form", "Chat widget");
    hidden("topic", topic ? topic.label : "");
    hidden("page", window.location.href);

    var honey = document.createElement("div");
    honey.className = "hp";
    honey.setAttribute("aria-hidden", "true");
    var honeyLabel = document.createElement("label");
    honeyLabel.textContent = "Leave this field empty ";
    var honeyInput = document.createElement("input");
    honeyInput.type = "text";
    honeyInput.name = "_honey";
    honeyInput.tabIndex = -1;
    honeyInput.autocomplete = "off";
    honeyLabel.appendChild(honeyInput);
    honey.appendChild(honeyLabel);
    form.appendChild(honey);

    var grid = document.createElement("div");
    grid.className = "form-grid";
    grid.appendChild(field("dd-chat-name", "Name", { name: "name", required: true, autocomplete: "name" }));
    grid.appendChild(field("dd-chat-email", "Email", { name: "email", type: "email", required: true, autocomplete: "email", inputmode: "email" }));
    grid.appendChild(field("dd-chat-phone", "Phone", { name: "phone", type: "tel", autocomplete: "tel", hint: "(optional)" }));
    grid.appendChild(field("dd-chat-message", "Message", { name: "message", tag: "textarea", required: true }));

    var consentWrap = document.createElement("div");
    consentWrap.className = "field";
    var consentLabel = document.createElement("label");
    consentLabel.className = "consent";
    var consentInput = document.createElement("input");
    consentInput.type = "checkbox";
    consentInput.name = "consent";
    consentInput.value = "yes";
    consentInput.required = true;
    var consentText = document.createElement("span");
    consentText.appendChild(document.createTextNode("I agree to be contacted by Devin Desaulniers (Axford Real Estate) by email or phone about my request. I can opt out at any time. "));
    var req = document.createElement("span");
    req.className = "req";
    req.textContent = "*";
    consentText.appendChild(req);
    consentLabel.appendChild(consentInput);
    consentLabel.appendChild(consentText);
    consentWrap.appendChild(consentLabel);
    grid.appendChild(consentWrap);

    var submit = document.createElement("button");
    submit.type = "submit";
    submit.className = "btn btn-primary";
    submit.textContent = "Send";
    grid.appendChild(submit);

    var status = document.createElement("div");
    status.className = "form-status";
    status.setAttribute("role", "status");
    status.setAttribute("aria-live", "polite");
    grid.appendChild(status);
    form.appendChild(grid);

    var back = choiceButton("Back", false, function () {
      step = "answers";
      actions.textContent = "";
      actions.appendChild(choiceButton("Send a message", true, showLead));
      actions.appendChild(choiceButton("Choose a different topic", false, function () { showMenu(true); }));
      actions.appendChild(talkLine());
      var again = actions.querySelector(".dd-choice--primary");
      if (again) again.focus();
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      sendForm(form, submit, status);
    });

    actions.appendChild(form);
    actions.appendChild(back);
    var nameInput = form.querySelector("#dd-chat-name");
    if (nameInput) {
      nameInput.focus({ preventScroll: true });
      var delta = nameInput.getBoundingClientRect().top - body.getBoundingClientRect().top;
      body.scrollTo({ top: Math.max(0, body.scrollTop + delta - 8), behavior: reduceMotion ? "auto" : "smooth" });
    }
  }

  function showStatus(status, cls, html) {
    status.className = "form-status show " + cls;
    status.innerHTML = html;
  }

  function showThanks() {
    actions.textContent = "";
    var box = document.createElement("div");
    box.className = "dd-thanks";
    box.tabIndex = -1;
    box.setAttribute("role", "status");
    var strong = document.createElement("p");
    strong.className = "dd-thanks-title";
    strong.textContent = "Thanks — your message has been sent.";
    var p = document.createElement("p");
    p.textContent = "Devin will be in touch soon. If it's urgent, call or text " + PHONE + ".";
    var a = document.createElement("a");
    a.className = "btn btn-outline";
    a.href = TEL;
    a.textContent = "Call or text " + PHONE;
    box.appendChild(strong);
    box.appendChild(p);
    box.appendChild(a);
    actions.appendChild(box);
    step = "thanks";
    box.focus();
  }

  function sendForm(form, btn, status) {
    var fallback = 'Please email <a href="mailto:' + EMAIL + '">' + EMAIL + '</a> or call <a href="' + TEL + '">' + PHONE + '</a>.';
    if (!endpoint) {
      showStatus(status, "error", "This form is not connected right now, so nothing was sent. " + fallback);
      return;
    }
    var fd = new FormData(form);
    if (fd.get("_honey")) {
      form.reset();
      showThanks();
      return;
    }
    var data = {};
    fd.forEach(function (v, k) { data[k] = data[k] ? data[k] + ", " + v : v; });
    if (data.email) data._replyto = data.email;
    btn.disabled = true;
    var label = btn.textContent;
    btn.textContent = "Sending…";
    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(data)
    })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        var ok = res.ok && String(res.j.success) !== "false";
        if (ok) {
          countEvent("chat-message-sent");
          showThanks();
        } else showStatus(status, "error", "Sorry, something went wrong and your message may not have been sent. " + fallback);
      })
      .catch(function () {
        showStatus(status, "error", "Sorry, we couldn't send your message (network error). " + fallback);
      })
      .then(function () {
        if (step !== "thanks" && btn.isConnected) {
          btn.disabled = false;
          btn.textContent = label;
        }
      });
  }

  function focusable(container) {
    return Array.prototype.filter.call(
      container.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), textarea:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'),
      function (el) {
        if (el.closest("[hidden]")) return false;
        if (el.tabIndex < 0) return false;
        return true;
      }
    );
  }

  function openChat() {
    if (!panel.hidden) return;
    panel.hidden = false;
    scrim.hidden = false;
    root.classList.add("is-open");
    countEvent("chat-opened");
    launch.setAttribute("aria-expanded", "true");
    setInert(true);
    var nodes = actions.querySelectorAll("button, input, textarea, a[href]");
    var target = null;
    for (var i = 0; i < nodes.length; i++) {
      if (nodes[i].tabIndex < 0 || nodes[i].name === "_honey") continue;
      target = nodes[i];
      break;
    }
    (target || closeBtn).focus({ preventScroll: true });
  }

  function closeChat() {
    if (panel.hidden) return;
    panel.hidden = true;
    scrim.hidden = true;
    root.classList.remove("is-open");
    launch.setAttribute("aria-expanded", "false");
    setInert(false);
    launch.focus({ preventScroll: true });
  }

  launch.addEventListener("click", function () {
    if (panel.hidden) openChat();
    else closeChat();
  });
  closeBtn.addEventListener("click", closeChat);
  scrim.addEventListener("click", closeChat);

  document.addEventListener("keydown", function (e) {
    if (panel.hidden) return;
    if (e.key === "Escape" || e.key === "Esc") {
      e.preventDefault();
      closeChat();
      return;
    }
    if (e.key !== "Tab") return;
    var items = focusable(panel);
    if (!items.length) return;
    var first = items[0];
    var last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });

  showMenu();
})();
