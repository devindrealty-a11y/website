/*
 * Free lead chat for devindesaulniers.ca.
 * Scripted questions only. No paid widget and no AI model.
 *
 * Switch (assets/js/config.js):
 *   chat: "lead"     this box (default)
 *   chat: "elfsight" Elfsight AI chatbot, same app id as before
 */
(function () {
  if (window.__leadChatInit) return;
  window.__leadChatInit = true;

  var cfg = window.SITE_CONFIG || {};
  var mode = String(cfg.chat || "lead").toLowerCase();
  var root = document.getElementById("lead-chat-root");

  if (mode === "elfsight") {
    showElfsight(cfg.elfsightAppId || "a317cda7-7d35-4984-bea6-2d5efb757691");
    if (root) root.parentNode.removeChild(root);
    return;
  }

  if (!root) return;

  var AREAS = ["Coquitlam", "Port Moody", "Port Coquitlam", "Burquitlam", "Vancouver", "Burnaby", "New Westminster", "Surrey", "Maple Ridge"];
  var BUY_BUDGETS = ["Under $600,000", "$600,000 to $900,000", "$900,000 to $1.2 million", "$1.2 to $1.8 million", "Over $1.8 million", "Not sure yet"];
  var RENT_BUDGETS = ["Under $2,000", "$2,000 to $2,500", "$2,500 to $3,200", "$3,200 to $4,500", "Over $4,500", "Not sure yet"];
  var TIMES = ["As soon as I can", "In the next 3 months", "In 3 to 6 months", "Just looking"];
  var INTENTS = [
    { value: "buy", label: "Buy" },
    { value: "sell", label: "Sell" },
    { value: "rent", label: "Rent" }
  ];

  var answers = { intent: "", intentLabel: "", area: "", budget: "", timeline: "", name: "", phone: "", email: "" };
  var step = 0;
  var areaMode = "choices";
  var busy = false;
  var finished = false;
  var open = false;

  var shell = document.createElement("div");
  shell.className = "lead-chat";
  shell.innerHTML =
    '<div class="lead-chat-panel" id="lead-chat-panel" role="dialog" aria-modal="true" aria-labelledby="lead-chat-title" hidden tabindex="-1">' +
      '<header class="lead-chat-head">' +
        '<img class="lead-chat-avatar" alt="" width="44" height="44">' +
        '<div class="lead-chat-who"><p class="lead-chat-name" id="lead-chat-title">Devin</p><p class="lead-chat-step" id="lead-chat-step">1 of 6</p></div>' +
        '<button type="button" class="lead-chat-textbtn" id="lead-chat-restart" hidden>Start over</button>' +
        '<button type="button" class="lead-chat-close" id="lead-chat-close" aria-label="Close chat">' +
          '<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>' +
        '</button>' +
      '</header>' +
      '<div class="lead-chat-log" id="lead-chat-log"></div>' +
      '<div class="lead-chat-compose" id="lead-chat-compose"></div>' +
      '<p class="lead-chat-privacy" id="lead-chat-privacy"></p>' +
      '<div class="hp" aria-hidden="true"><label>Leave this field empty <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>' +
      '<div class="lead-chat-status" id="lead-chat-status" role="status" aria-live="polite"></div>' +
    '</div>' +
    '<button type="button" class="lead-chat-launch" id="lead-chat-launch" aria-expanded="false" aria-controls="lead-chat-panel">' +
      '<img alt="" width="44" height="44">' +
      '<span>Ask Devin</span>' +
    '</button>';
  root.appendChild(shell);

  var panel = document.getElementById("lead-chat-panel");
  var launch = document.getElementById("lead-chat-launch");
  var log = document.getElementById("lead-chat-log");
  var compose = document.getElementById("lead-chat-compose");
  var stepEl = document.getElementById("lead-chat-step");
  var restart = document.getElementById("lead-chat-restart");
  var closer = document.getElementById("lead-chat-close");
  var statusEl = document.getElementById("lead-chat-status");
  var privacyEl = document.getElementById("lead-chat-privacy");
  var photo = root.getAttribute("data-photo") || "assets/img/devin-headshot-480.webp";
  var privacyHref = root.getAttribute("data-privacy") || "privacy.html";

  shell.querySelectorAll("img").forEach(function (img) { img.src = photo; });
  privacyEl.appendChild(document.createTextNode("I'll use this only to follow up with you. "));
  var privacyLink = document.createElement("a");
  privacyLink.href = privacyHref;
  privacyLink.textContent = "Privacy";
  privacyEl.appendChild(privacyLink);

  var messages = [];

  function say(from, text) {
    messages.push({ from: from, text: text });
    var row = document.createElement("div");
    row.className = "lc-msg" + (from === "user" ? " is-user" : "");
    var bubble = document.createElement("p");
    bubble.className = "lc-bubble";
    bubble.textContent = text;
    row.appendChild(bubble);
    log.appendChild(row);
    log.scrollTop = log.scrollHeight;
    if (from === "bot" && open) statusEl.textContent = text;
  }

  function sayNode(node, spoken) {
    if (spoken) messages.push({ from: "bot", text: spoken });
    var row = document.createElement("div");
    row.className = "lc-msg";
    var bubble = document.createElement("div");
    bubble.className = "lc-bubble";
    bubble.appendChild(node);
    row.appendChild(bubble);
    log.appendChild(row);
    log.scrollTop = log.scrollHeight;
    if (spoken && open) statusEl.textContent = spoken;
  }

  function question(n, intent) {
    if (n === 0) return "What do you want to do?";
    if (n === 1) return "Which area?";
    if (n === 2) {
      if (intent === "sell") return "About what is the home worth?";
      if (intent === "rent") return "What rent are you hoping for, per month?";
      return "What is your budget?";
    }
    if (n === 3) {
      if (intent === "sell") return "When do you want to sell?";
      if (intent === "rent") return "When do you want to move?";
      return "When do you want to buy?";
    }
    if (n === 4) return "What is your name?";
    return "How can I reach you? Phone, email, or both.";
  }

  function clearCompose() {
    while (compose.firstChild) compose.removeChild(compose.firstChild);
  }

  function showError(text) {
    var old = compose.querySelector(".lc-error");
    if (old) old.parentNode.removeChild(old);
    if (!text) return;
    var p = document.createElement("p");
    p.className = "lc-error";
    p.setAttribute("role", "alert");
    p.textContent = text;
    compose.appendChild(p);
  }

  function choiceButtons(items, onPick) {
    var wrap = document.createElement("div");
    wrap.className = "lc-choices";
    items.forEach(function (item) {
      var label = typeof item === "string" ? item : item.label;
      var value = typeof item === "string" ? item : item.value;
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "lc-choice";
      btn.textContent = label;
      btn.addEventListener("click", function () { onPick(value, label); });
      wrap.appendChild(btn);
    });
    return wrap;
  }

  function textRow(input, buttonLabel, onGo) {
    var row = document.createElement("div");
    row.className = "lc-textrow";
    row.appendChild(input);
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "lc-next";
    btn.textContent = buttonLabel;
    btn.addEventListener("click", onGo);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { e.preventDefault(); onGo(); }
    });
    row.appendChild(btn);
    return row;
  }

  function makeInput(opts) {
    var field = document.createElement("label");
    field.className = "lc-field";
    var cap = document.createElement("span");
    cap.textContent = opts.label;
    var input = document.createElement("input");
    input.type = opts.type || "text";
    input.maxLength = opts.max || 80;
    input.autocomplete = opts.auto || "off";
    if (opts.mode) input.inputMode = opts.mode;
    if (opts.spell === false) input.spellcheck = false;
    input.id = opts.id;
    cap.setAttribute("for", opts.id);
    field.appendChild(cap);
    field.appendChild(input);
    return { field: field, input: input };
  }

  function advance(label) {
    say("user", label);
    step += 1;
    if (step < 6) say("bot", question(step, answers.intent));
    render();
  }

  function render() {
    clearCompose();
    restart.hidden = step === 0 && !finished;
    stepEl.textContent = finished ? "Sent" : (Math.min(step, 5) + 1) + " of 6";
    if (finished) return;

    if (step === 0) {
      compose.appendChild(choiceButtons(INTENTS, function (value, label) {
        answers.intent = value;
        answers.intentLabel = label === "Buy" ? "Buy a home" : label === "Sell" ? "Sell a home" : "Rent a home";
        advance(label);
      }));
      return;
    }

    if (step === 1 && areaMode === "choices") {
      var areas = AREAS.map(function (name) { return name; });
      compose.appendChild(choiceButtons(areas.concat(["Other"]), function (value) {
        if (value === "Other") {
          areaMode = "other";
          render();
          return;
        }
        answers.area = value;
        advance(value);
      }));
      return;
    }

    if (step === 1 && areaMode === "other") {
      var back = document.createElement("button");
      back.type = "button";
      back.className = "lc-linkbtn";
      back.textContent = "Show the area list";
      back.addEventListener("click", function () { areaMode = "choices"; render(); });
      compose.appendChild(back);
      var areaInput = document.createElement("input");
      areaInput.type = "text";
      areaInput.className = "lc-input";
      areaInput.maxLength = 80;
      areaInput.placeholder = "Type the area";
      areaInput.setAttribute("aria-label", "Area");
      areaInput.autocomplete = "address-level2";
      compose.appendChild(textRow(areaInput, "Next", function () {
        var value = areaInput.value.replace(/\s+/g, " ").trim();
        if (value.length < 2) { showError("Type the area, then press Next."); areaInput.focus(); return; }
        answers.area = value;
        areaMode = "choices";
        advance(value);
      }));
      areaInput.focus();
      return;
    }

    if (step === 2) {
      var budgets = answers.intent === "rent" ? RENT_BUDGETS : BUY_BUDGETS;
      compose.appendChild(choiceButtons(budgets, function (value) {
        answers.budget = value;
        advance(value);
      }));
      return;
    }

    if (step === 3) {
      compose.appendChild(choiceButtons(TIMES, function (value) {
        answers.timeline = value;
        advance(value);
      }));
      return;
    }

    if (step === 4) {
      var nameBits = makeInput({ label: "Your name", id: "lc-name", auto: "name", max: 80 });
      compose.appendChild(nameBits.field);
      var nameNext = document.createElement("button");
      nameNext.type = "button";
      nameNext.className = "lc-next lc-next-block";
      nameNext.textContent = "Next";
      function goName() {
        var value = nameBits.input.value.replace(/\s+/g, " ").trim();
        if (value.length < 2) { showError("Please tell me your name."); nameBits.input.focus(); return; }
        answers.name = value;
        advance(value);
      }
      nameNext.addEventListener("click", goName);
      nameBits.input.addEventListener("keydown", function (e) {
        if (e.key === "Enter") { e.preventDefault(); goName(); }
      });
      compose.appendChild(nameNext);
      nameBits.input.focus();
      return;
    }

    var phoneBits = makeInput({ label: "Phone", id: "lc-phone", type: "tel", auto: "tel", mode: "tel", max: 40 });
    var emailBits = makeInput({ label: "Email", id: "lc-email", type: "email", auto: "email", mode: "email", max: 160, spell: false });
    compose.appendChild(phoneBits.field);
    compose.appendChild(emailBits.field);

    var consent = document.createElement("label");
    consent.className = "lc-consent";
    var box = document.createElement("input");
    box.type = "checkbox";
    box.id = "lc-consent";
    var consentText = document.createElement("span");
    consentText.textContent = "I agree Devin can contact me by phone or email about this. I can opt out any time.";
    consent.appendChild(box);
    consent.appendChild(consentText);
    compose.appendChild(consent);

    var send = document.createElement("button");
    send.type = "button";
    send.className = "lc-next lc-next-block";
    send.textContent = busy ? "Sending…" : "Send";
    send.disabled = busy;
    function goSend() {
      if (busy) return;
      var phone = phoneBits.input.value.replace(/\s+/g, " ").trim();
      var email = emailBits.input.value.replace(/\s+/g, " ").trim();
      var digits = (phone.match(/\d/g) || []).length;
      if (!phone && !email) { showError("Add a phone number or an email."); phoneBits.input.focus(); return; }
      if (phone && digits < 7) { showError("Please check the phone number."); phoneBits.input.focus(); return; }
      if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { showError("Please check the email address."); emailBits.input.focus(); return; }
      if (!box.checked) { showError("Please agree so I can contact you."); box.focus(); return; }
      answers.phone = phone;
      answers.email = email;
      submitLead(send);
    }
    send.addEventListener("click", goSend);
    emailBits.input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { e.preventDefault(); goSend(); }
    });
    compose.appendChild(send);
    phoneBits.input.focus();
  }

  function honeyValue() {
    var honey = shell.querySelector('[name="_honey"]');
    return honey ? String(honey.value || "") : "";
  }

  function honeyFilled() {
    return honeyValue().replace(/\s+/g, "") !== "";
  }

  function pageUrl() {
    return location.origin + location.pathname;
  }

  function postJson(url, body, extraHeaders) {
    var headers = { "Content-Type": "application/json", "Accept": "application/json" };
    if (extraHeaders) {
      Object.keys(extraHeaders).forEach(function (key) { headers[key] = extraHeaders[key]; });
    }
    var opts = { method: "POST", headers: headers, body: JSON.stringify(body), credentials: "omit" };
    var timer = null;
    if (window.AbortController) {
      var ctrl = new AbortController();
      opts.signal = ctrl.signal;
      timer = setTimeout(function () { ctrl.abort(); }, 20000);
    }
    return fetch(url, opts).then(function (r) {
      if (timer) clearTimeout(timer);
      return r.text().then(function (t) {
        var parsed = {};
        if (t) { try { parsed = JSON.parse(t); } catch (e) { parsed = {}; } }
        return { ok: r.ok, body: parsed };
      });
    }, function (err) {
      if (timer) clearTimeout(timer);
      throw err;
    });
  }

  function settle(promise) {
    return promise.then(function (r) { return r; }, function () { return { ok: false, body: {} }; });
  }

  function submitLead(sendBtn) {
    busy = true;
    sendBtn.disabled = true;
    sendBtn.textContent = "Sending…";
    showError("");

    if (honeyFilled()) {
      finish();
      return;
    }

    var forms = cfg.forms || {};
    var emailUrl = String(forms.leadChat || "").trim();
    var sb = cfg.supabase || {};
    var sbUrl = String(sb.url || "").replace(/\/+$/, "");
    var fn = String(sb.leadFunction || "submit_website_chat_lead");
    if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(fn)) fn = "submit_website_chat_lead";
    var jobs = [];

    if (sbUrl && sb.anonKey) {
      jobs.push(settle(postJson(sbUrl + "/rest/v1/rpc/" + fn, {
        p_intent: answers.intent,
        p_area: answers.area,
        p_budget: answers.budget,
        p_timeline: answers.timeline,
        p_name: answers.name,
        p_phone: answers.phone || null,
        p_email: answers.email || null,
        p_page_url: pageUrl(),
        p_company: honeyValue()
      }, {
        apikey: sb.anonKey,
        Authorization: "Bearer " + sb.anonKey,
        Prefer: "return=minimal"
      })));
    }

    if (emailUrl) {
      var mail = {
        _subject: "New website chat lead",
        _template: "table",
        _honey: "",
        form: "Website chat",
        looking_to: answers.intentLabel,
        area: answers.area,
        budget: answers.budget,
        timeline: answers.timeline,
        name: answers.name,
        phone: answers.phone,
        email: answers.email,
        page: pageUrl()
      };
      if (answers.email) mail._replyto = answers.email;
      jobs.push(settle(postJson(emailUrl, mail)));
    }

    if (!jobs.length) {
      busy = false;
      sendBtn.disabled = false;
      sendBtn.textContent = "Send";
      showError("This chat is not connected right now. Please email devin@axfordrealestate.ca or call 604-809-1032.");
      return;
    }

    Promise.all(jobs).then(function (results) {
      var saved = false;
      var mailed = false;
      results.forEach(function (res, i) {
        var isMail = emailUrl && sbUrl && sb.anonKey ? i === 1 : !!emailUrl && !(sbUrl && sb.anonKey);
        if (sbUrl && sb.anonKey && i === 0) saved = !!res.ok;
        if (isMail) mailed = !!(res.ok && String(res.body && res.body.success) !== "false");
      });
      if (saved || mailed) {
        finish();
        return;
      }
      busy = false;
      sendBtn.disabled = false;
      sendBtn.textContent = "Send";
      showError("Sorry, that didn't go through. Please email devin@axfordrealestate.ca or call 604-809-1032.");
    });
  }

  function finish() {
    busy = false;
    finished = true;
    clearCompose();
    var wrap = document.createElement("div");
    var line = document.createElement("p");
    line.className = "lc-thanks";
    line.appendChild(document.createTextNode("Thanks, " + answers.name + ". I have your note and I'll be in touch soon."));
    var line2 = document.createElement("p");
    line2.className = "lc-thanks";
    line2.appendChild(document.createTextNode("If it's urgent, call or text me at "));
    var tel = document.createElement("a");
    tel.href = "tel:+16048091032";
    tel.textContent = "604-809-1032";
    line2.appendChild(tel);
    line2.appendChild(document.createTextNode("."));
    wrap.appendChild(line);
    wrap.appendChild(line2);
    sayNode(wrap, "Thanks, " + answers.name + ". I have your note and I'll be in touch soon. If it's urgent, call or text 604-809-1032.");
    render();
    restart.hidden = false;
  }

  function reset() {
    answers = { intent: "", intentLabel: "", area: "", budget: "", timeline: "", name: "", phone: "", email: "" };
    step = 0;
    areaMode = "choices";
    busy = false;
    finished = false;
    messages = [];
    while (log.firstChild) log.removeChild(log.firstChild);
    say("bot", "Hi, I'm Devin. I help people buy, sell, and rent homes around Greater Vancouver.");
    say("bot", question(0, ""));
    render();
  }

  function setOpen(next) {
    open = next;
    shell.classList.toggle("is-open", open);
    document.documentElement.classList.toggle("lead-chat-open", open);
    launch.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) {
      panel.hidden = false;
      var lastBot = "";
      messages.forEach(function (msg) { if (msg.from === "bot") lastBot = msg.text; });
      if (lastBot) statusEl.textContent = lastBot;
      panel.focus();
    } else {
      panel.hidden = true;
      launch.focus();
    }
  }

  function focusables() {
    return Array.prototype.slice.call(panel.querySelectorAll("button, a[href], input, textarea, select")).filter(function (el) {
      if (el.disabled || el.tabIndex === -1) return false;
      var node = el;
      while (node && node !== panel) {
        if (node.hidden || (node.classList && node.classList.contains("hp"))) return false;
        node = node.parentNode;
      }
      return true;
    });
  }

  launch.addEventListener("click", function () { setOpen(true); });
  closer.addEventListener("click", function () { setOpen(false); });
  restart.addEventListener("click", function () { if (!busy) reset(); });

  document.addEventListener("keydown", function (e) {
    if (!open) return;
    if (e.key === "Escape" || e.key === "Esc") { setOpen(false); return; }
    if (e.key !== "Tab") return;
    var items = focusables();
    if (!items.length) return;
    var first = items[0];
    var last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  document.addEventListener("pointerdown", function (e) {
    if (!open) return;
    if (window.matchMedia("(max-width: 699px)").matches) return;
    if (!shell.contains(e.target)) setOpen(false);
  });

  function place() {
    var sticky = document.querySelector("[data-sticky-cta]");
    var raised = !!(sticky && window.matchMedia("(max-width: 959px)").matches && !sticky.classList.contains("hide"));
    shell.classList.toggle("is-raised", raised);
  }
  place();
  window.addEventListener("resize", place);
  var stickyEl = document.querySelector("[data-sticky-cta]");
  if (stickyEl && window.MutationObserver) {
    new MutationObserver(place).observe(stickyEl, { attributes: true, attributeFilter: ["class"] });
  }

  reset();

  function showElfsight(appId) {
    var id = String(appId || "").replace(/[^a-z0-9-]/gi, "");
    if (!id) return;
    var script = document.createElement("script");
    script.src = "https://elfsightcdn.com/platform.js";
    script.async = true;
    var holder = document.createElement("div");
    holder.className = "elfsight-app-" + id;
    holder.setAttribute("data-elfsight-app-lazy", "");
    document.body.appendChild(script);
    document.body.appendChild(holder);
  }
})();
