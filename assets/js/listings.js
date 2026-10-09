(function () {
  var PAGE = 24;
  var BADGE_SRC = "https://www.realtor.ca/images/en-ca/powered_by_realtor.svg";
  var state = { listings: [], byId: {}, sample: false, destinationId: null, shown: PAGE, photo: 0, current: null };
  var baseTitle = document.title;
  var searchEl = document.getElementById("ls-search");
  var detailEl = document.getElementById("ls-detail");
  var resultsEl = document.getElementById("ls-results");
  var countEl = document.getElementById("ls-count");
  var moreEl = document.getElementById("ls-more");
  var filtersEl = document.getElementById("ls-filters");
  var sampleEl = document.getElementById("ls-sample");
  if (!searchEl || !filtersEl) return;

  function dataUrl() {
    var params = new URLSearchParams(location.search);
    var local = location.hostname === "localhost" || location.hostname === "127.0.0.1" || location.hostname === "::1";
    state.sample = params.get("preview") === "1" || (local && params.get("live") !== "1");
    return state.sample ? "_fixtures/listings-sample.json" : "listings/data.json";
  }

  function load() {
    var url = dataUrl();
    fetch(url, { headers: { "Accept": "application/json" } })
      .then(function (r) { if (!r.ok) throw new Error(String(r.status)); return r.json(); })
      .then(function (data) {
        state.listings = (data && data.listings) || [];
        state.sample = !!(data && data.sample);
        state.destinationId = (data && data.destinationId) || null;
        state.byId = {};
        state.listings.forEach(function (item) { if (item && item.id) state.byId[String(item.id)] = item; });
        if (sampleEl) sampleEl.hidden = !state.sample;
        route();
      })
      .catch(function () {
        countEl.textContent = state.sample
          ? "Sample data could not be loaded."
          : "The listing feed could not be loaded.";
      });
  }

  function filters() {
    var q = document.getElementById("ls-q").value.trim().toLowerCase();
    return {
      q: q,
      min: numOrNull(document.getElementById("ls-min").value),
      max: numOrNull(document.getElementById("ls-max").value),
      beds: numOrNull(document.getElementById("ls-beds").value),
      baths: numOrNull(document.getElementById("ls-baths").value),
      type: document.getElementById("ls-type").value,
      sort: document.getElementById("ls-sort").value
    };
  }

  function numOrNull(value) {
    if (value === "" || value == null) return null;
    var n = Number(value);
    return isFinite(n) ? n : null;
  }

  function matches(item, f) {
    var hay = ((item.city || "") + " " + (item.area || "") + " " + (item.address || "")).toLowerCase();
    if (f.q && hay.indexOf(f.q) === -1) return false;
    if (f.min != null && (item.price == null || item.price < f.min)) return false;
    if (f.max != null && (item.price == null || item.price > f.max)) return false;
    if (f.beds != null && (item.beds == null || item.beds < f.beds)) return false;
    if (f.baths != null && (item.baths == null || item.baths < f.baths)) return false;
    if (f.type && item.type !== f.type) return false;
    return true;
  }

  function sorted(list, mode) {
    var copy = list.slice();
    copy.sort(function (a, b) {
      if (mode === "price-asc" || mode === "price-desc") {
        var dir = mode === "price-asc" ? 1 : -1;
        if (a.price == null && b.price == null) return 0;
        if (a.price == null) return 1;
        if (b.price == null) return -1;
        return dir * (a.price - b.price);
      }
      if (mode === "city") return String(a.city || "").localeCompare(String(b.city || ""), "en");
      return String(b.updated || "").localeCompare(String(a.updated || ""));
    });
    return copy;
  }

  function renderResults() {
    var f = filters();
    var list = sorted(state.listings.filter(function (item) { return matches(item, f); }), f.sort);
    state.shown = Math.min(state.shown, Math.max(list.length, PAGE));
    var visible = list.slice(0, state.shown);
    resultsEl.replaceChildren();
    if (!state.listings.length) {
      countEl.textContent = state.sample
        ? "No sample listings in the preview file."
        : "The listing feed is not connected yet. Homes will show here after it refreshes.";
      moreEl.hidden = true;
      return;
    }
    countEl.textContent = list.length === 1 ? "1 home" : list.length + " homes";
    var frag = document.createDocumentFragment();
    visible.forEach(function (item) { frag.appendChild(card(item)); });
    resultsEl.appendChild(frag);
    moreEl.hidden = visible.length >= list.length;
  }

  function card(item) {
    var article = document.createElement("article");
    article.className = "ls-card";
    var media = document.createElement("a");
    media.className = "ls-media";
    media.href = "#" + encodeURIComponent(item.id);
    media.appendChild(photoEl(item, 0, true));
    var body = document.createElement("div");
    body.className = "ls-card-body";
    var price = document.createElement("p");
    price.className = "ls-price";
    price.textContent = money(item.price);
    var h = document.createElement("h2");
    var titleLink = document.createElement("a");
    titleLink.href = "#" + encodeURIComponent(item.id);
    titleLink.textContent = titleFor(item);
    h.appendChild(titleLink);
    var meta = document.createElement("p");
    meta.className = "ls-meta";
    meta.textContent = metaLine(item);
    var broker = document.createElement("p");
    broker.className = "ls-broker";
    broker.textContent = brokerageLine(item);
    body.appendChild(price);
    body.appendChild(h);
    body.appendChild(meta);
    body.appendChild(broker);
    var linkRow = document.createElement("p");
    linkRow.appendChild(realtorLink(item));
    body.appendChild(linkRow);
    body.appendChild(badge(item));
    article.appendChild(media);
    article.appendChild(body);
    return article;
  }

  function photoEl(item, index, thumb) {
    var photos = httpsPhotos(item);
    if (!photos.length) {
      var empty = document.createElement("div");
      empty.className = "ls-nophoto";
      empty.textContent = "No photo supplied";
      return empty;
    }
    var img = document.createElement("img");
    img.src = photos[index] || photos[0];
    img.alt = "Photo of " + titleFor(item);
    if (thumb) img.loading = "lazy";
    img.decoding = "async";
    img.addEventListener("error", function () {
      var empty = document.createElement("div");
      empty.className = "ls-nophoto";
      empty.textContent = "Photo unavailable";
      img.replaceWith(empty);
    });
    return img;
  }

  function httpsPhotos(item) {
    return (item.photos || []).filter(function (url) { return typeof url === "string" && url.indexOf("https://") === 0; });
  }

  function safeHttp(url) {
    return typeof url === "string" && url.indexOf("https://") === 0 ? url : "";
  }

  function titleFor(item) {
    if (item.address) return item.address + (item.city ? ", " + item.city : "");
    return item.city || "Home";
  }

  function metaLine(item) {
    var bits = [];
    if (item.beds != null) bits.push(item.beds + " bd");
    if (item.baths != null) bits.push(formatBaths(item.baths) + " ba");
    if (item.type) bits.push(item.type);
    if (item.area) bits.push(item.area);
    return bits.join(" · ");
  }

  function formatBaths(n) {
    var num = Number(n);
    return num % 1 === 0 ? String(num) : String(num);
  }

  function money(n) {
    if (n == null || n === "") return "Price on request";
    return "$" + Number(n).toLocaleString("en-CA");
  }

  function brokerageLine(item) {
    return "Listing brokerage: " + (item.brokerage || "not supplied in the feed");
  }

  function realtorLink(item) {
    var a = document.createElement("a");
    a.target = "_blank";
    a.rel = "noopener";
    a.href = safeHttp(item.realtorUrl) || "https://www.realtor.ca/";
    a.textContent = safeHttp(item.realtorUrl) ? "View this listing on REALTOR.ca" : "REALTOR.ca";
    return a;
  }

  function badge(item) {
    var a = document.createElement("a");
    a.className = "powered-by";
    a.target = "_blank";
    a.rel = "noopener";
    a.href = safeHttp(item.realtorUrl) || "https://www.realtor.ca/";
    var img = document.createElement("img");
    img.src = BADGE_SRC;
    img.alt = "";
    img.width = 125;
    img.height = 40;
    img.addEventListener("error", function () { img.remove(); });
    var span = document.createElement("span");
    span.textContent = "Powered by REALTOR.ca";
    a.appendChild(img);
    a.appendChild(span);
    return a;
  }

  function showSearch() {
    detailEl.hidden = true;
    searchEl.hidden = false;
    document.title = baseTitle;
    renderResults();
  }

  function showDetail(item) {
    state.current = item;
    state.photo = 0;
    searchEl.hidden = true;
    detailEl.hidden = false;
    var inquiry = document.querySelector(".ls-inquiry");
    if (inquiry) inquiry.hidden = false;
    document.title = titleFor(item) + " | " + baseTitle;
    paintDetail();
    var heading = document.getElementById("ls-heading");
    if (heading) heading.focus();
    window.scrollTo(0, 0);
    track(item);
  }

  function showMissing() {
    searchEl.hidden = true;
    detailEl.hidden = false;
    document.getElementById("ls-price").textContent = "";
    document.getElementById("ls-heading").textContent = "This listing is no longer in the feed";
    document.getElementById("ls-meta").textContent = "";
    document.getElementById("ls-broker").textContent = "";
    document.getElementById("ls-agent").textContent = "";
    document.getElementById("ls-photo").replaceChildren();
    document.getElementById("ls-thumbs").replaceChildren();
    document.getElementById("ls-remarks").replaceChildren();
    document.getElementById("ls-facts").replaceChildren();
    document.getElementById("ls-badge").replaceChildren();
    document.getElementById("ls-realtor-link").replaceChildren();
    document.getElementById("ls-prev").hidden = true;
    document.getElementById("ls-next").hidden = true;
    var inquiry = document.querySelector(".ls-inquiry");
    if (inquiry) inquiry.hidden = true;
  }

  function paintDetail() {
    var item = state.current;
    if (!item) return;
    var photos = httpsPhotos(item);
    document.getElementById("ls-price").textContent = money(item.price);
    document.getElementById("ls-heading").textContent = titleFor(item);
    document.getElementById("ls-meta").textContent = metaLine(item);
    document.getElementById("ls-broker").textContent = brokerageLine(item);
    var agent = document.getElementById("ls-agent");
    agent.textContent = item.agent ? "Listing REALTOR®: " + item.agent : "";
    var frame = document.getElementById("ls-photo");
    frame.replaceChildren(photoEl(item, state.photo, false));
    var thumbs = document.getElementById("ls-thumbs");
    thumbs.replaceChildren();
    photos.forEach(function (_url, i) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "ls-thumb" + (i === state.photo ? " is-on" : "");
      btn.appendChild(photoEl(item, i, true));
      btn.addEventListener("click", function () { state.photo = i; paintDetail(); });
      thumbs.appendChild(btn);
    });
    var multi = photos.length > 1;
    document.getElementById("ls-prev").hidden = !multi;
    document.getElementById("ls-next").hidden = !multi;
    var linkSlot = document.getElementById("ls-realtor-link");
    linkSlot.replaceChildren(realtorLink(item));
    document.getElementById("ls-badge").replaceChildren(badge(item));
    var facts = document.getElementById("ls-facts");
    facts.replaceChildren();
    [
      ["City", item.city],
      ["Area", item.area],
      ["Postal code", item.postal],
      ["Property type", item.type],
      ["Bedrooms", item.beds],
      ["Bathrooms", item.baths != null ? formatBaths(item.baths) : null],
      ["Interior", item.sqft ? Number(item.sqft).toLocaleString("en-CA") + " sq ft" : null],
      ["Year built", item.year],
      ["Parking", item.parking],
      ["MLS® number", item.mls]
    ].forEach(function (pair) {
      if (pair[1] == null || pair[1] === "") return;
      var row = document.createElement("div");
      var dt = document.createElement("span");
      dt.textContent = pair[0];
      var dd = document.createElement("strong");
      dd.textContent = String(pair[1]);
      row.appendChild(dt);
      row.appendChild(dd);
      facts.appendChild(row);
    });
    var remarks = document.getElementById("ls-remarks");
    remarks.replaceChildren();
    if (item.remarks) {
      var h = document.createElement("h2");
      h.textContent = "Description";
      var p = document.createElement("p");
      p.textContent = item.remarks;
      remarks.appendChild(h);
      remarks.appendChild(p);
    }
    document.getElementById("inq-id").value = item.id || "";
    document.getElementById("inq-mls").value = item.mls || "";
    document.getElementById("inq-address").value = titleFor(item);
    document.getElementById("inq-url").value = safeHttp(item.realtorUrl);
  }

  function step(delta) {
    var photos = state.current ? httpsPhotos(state.current) : [];
    if (photos.length < 2) return;
    state.photo = (state.photo + delta + photos.length) % photos.length;
    paintDetail();
  }

  function currentId() {
    var q = new URLSearchParams(location.search).get("id");
    if (q) return q;
    var hash = location.hash.replace(/^#/, "");
    return hash ? decodeURIComponent(hash) : "";
  }

  function route() {
    var id = currentId();
    if (!id) { showSearch(); return; }
    if (state.byId[id]) showDetail(state.byId[id]);
    else showMissing();
  }

  function track(item) {
    if (state.sample || !state.destinationId || !item.analyticsId) return;
    var key = "ddf-viewed-" + item.analyticsId;
    try { if (sessionStorage.getItem(key)) return; sessionStorage.setItem(key, "1"); } catch (e) {}
    var uuid = "";
    try {
      uuid = localStorage.getItem("ddf-uuid") || "";
      if (!uuid) {
        uuid = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : String(Date.now());
        localStorage.setItem("ddf-uuid", uuid);
      }
    } catch (e) { uuid = "anon"; }
    var img = new Image();
    img.src = "https://analytics.crea.ca/LogEvents.svc/LogEvents?ListingID=" + encodeURIComponent(item.analyticsId)
      + "&DestinationID=" + encodeURIComponent(state.destinationId)
      + "&EventType=view&UUID=" + encodeURIComponent(uuid + "-" + state.destinationId);
  }

  var timer = null;
  filtersEl.addEventListener("submit", function (e) { e.preventDefault(); state.shown = PAGE; renderResults(); });
  filtersEl.addEventListener("input", function () {
    clearTimeout(timer);
    timer = setTimeout(function () { state.shown = PAGE; renderResults(); }, 150);
  });
  filtersEl.addEventListener("change", function () { state.shown = PAGE; renderResults(); });
  document.getElementById("ls-clear").addEventListener("click", function () {
    filtersEl.reset();
    state.shown = PAGE;
    renderResults();
  });
  moreEl.addEventListener("click", function () { state.shown += PAGE; renderResults(); });
  document.getElementById("ls-prev").addEventListener("click", function () { step(-1); });
  document.getElementById("ls-next").addEventListener("click", function () { step(1); });
  document.getElementById("ls-back").addEventListener("click", function (e) {
    e.preventDefault();
    history.pushState(null, "", location.pathname + location.search);
    showSearch();
  });
  window.addEventListener("hashchange", route);
  window.addEventListener("popstate", route);
  load();
})();
