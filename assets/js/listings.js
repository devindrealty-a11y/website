(function () {
  var PAGE_WIDE = 24;
  var PAGE_NARROW = 12;
  var SHARD_COUNT = 48;
  var BADGE_SRC = "https://www.realtor.ca/images/en-ca/powered_by_realtor.svg";
  var tag = document.currentScript || document.querySelector("script[data-feed]");
  var mode = (tag && tag.getAttribute("data-mode")) || "sale";
  var feedPath = (tag && tag.getAttribute("data-feed")) || "listings/data.json";
  var samplePath = (tag && tag.getAttribute("data-sample")) || "_fixtures/listings-sample.json";
  var state = { listings: [], byId: {}, cities: {}, sample: false, destinationId: null, shown: PAGE_WIDE, photo: 0, current: null, lightbox: false };
  var shardCache = {};
  var shardWait = {};
  var baseTitle = document.title;
  var searchEl = document.getElementById("ls-search");
  var detailEl = document.getElementById("ls-detail");
  var resultsEl = document.getElementById("ls-results");
  var countEl = document.getElementById("ls-count");
  var moreEl = document.getElementById("ls-more");
  var filtersEl = document.getElementById("ls-filters");
  var sampleEl = document.getElementById("ls-sample");
  var emptyEl = document.getElementById("ls-empty");
  var toggleEl = document.getElementById("ls-filter-toggle");
  var moreFiltersEl = document.getElementById("ls-more-filters");
  var desktopFilters = window.matchMedia("(min-width: 900px)");
  if (!searchEl || !filtersEl) return;

  function pageSize() {
    return window.matchMedia("(max-width: 699px)").matches ? PAGE_NARROW : PAGE_WIDE;
  }

  function dataUrl() {
    var params = new URLSearchParams(location.search);
    var local = location.hostname === "localhost" || location.hostname === "127.0.0.1" || location.hostname === "::1";
    state.sample = params.get("preview") === "1" || (local && params.get("live") !== "1");
    return state.sample ? samplePath : feedPath;
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
        state.cities = {};
        state.listings.forEach(function (item) {
          if (item && item.id) state.byId[String(item.id)] = item;
          if (item && item.city) state.cities[String(item.city).toLowerCase()] = item.city;
        });
        fillCities();
        if (sampleEl) sampleEl.hidden = !state.sample;
        state.shown = pageSize();
        route();
      })
      .catch(function () {
        countEl.textContent = state.sample
          ? "Sample data could not be loaded."
          : "The listing feed could not be loaded.";
      });
  }

  function fillCities() {
    var list = document.getElementById("ls-cities");
    if (!list) return;
    var names = Object.keys(state.cities).map(function (key) { return state.cities[key]; });
    names.sort(function (a, b) { return a.localeCompare(b, "en"); });
    var frag = document.createDocumentFragment();
    names.forEach(function (city) {
      var opt = document.createElement("option");
      opt.value = city;
      frag.appendChild(opt);
    });
    list.replaceChildren(frag);
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
    if (f.q) {
      var city = (item.city || "").toLowerCase();
      var area = (item.area || "").toLowerCase();
      var address = (item.address || "").toLowerCase();
      if (state.cities[f.q]) {
        if (city !== f.q && area !== f.q) return false;
      } else if ((city + " " + area + " " + address).indexOf(f.q) === -1) {
        return false;
      }
    }
    if (f.min != null && (item.price == null || item.price < f.min)) return false;
    if (f.max != null && (item.price == null || item.price > f.max)) return false;
    if (f.beds != null && (item.beds == null || item.beds < f.beds)) return false;
    if (f.baths != null && (item.baths == null || item.baths < f.baths)) return false;
    if (f.type && item.type !== f.type) return false;
    return true;
  }

  function sorted(list, how) {
    var copy = list.slice();
    copy.sort(function (a, b) {
      if (how === "price-asc" || how === "price-desc") {
        var dir = how === "price-asc" ? 1 : -1;
        if (a.price == null && b.price == null) return 0;
        if (a.price == null) return 1;
        if (b.price == null) return -1;
        return dir * (a.price - b.price);
      }
      if (how === "city") return String(a.city || "").localeCompare(String(b.city || ""), "en");
      return String(b.updated || "").localeCompare(String(a.updated || ""));
    });
    return copy;
  }

  function renderResults() {
    var f = filters();
    var list = sorted(state.listings.filter(function (item) { return matches(item, f); }), f.sort);
    var page = pageSize();
    if (state.shown < page) state.shown = page;
    var visible = list.slice(0, state.shown);
    resultsEl.replaceChildren();
    if (!list.length) {
      countEl.textContent = countLabel(0);
      moreEl.hidden = true;
      paintEmpty(state.listings.length ? "filters" : (mode === "rent" ? "feed-rent" : "feed-sale"));
      return;
    }
    if (emptyEl) {
      emptyEl.hidden = true;
      emptyEl.replaceChildren();
    }
    countEl.textContent = countLabel(list.length);
    var frag = document.createDocumentFragment();
    visible.forEach(function (item, index) { frag.appendChild(card(item, index)); });
    resultsEl.appendChild(frag);
    moreEl.hidden = visible.length >= list.length;
  }

  function paintEmpty(kind) {
    if (!emptyEl) return;
    emptyEl.hidden = false;
    var box = document.createElement("div");
    box.className = "ls-empty";
    var heading = document.createElement("h2");
    var copy = document.createElement("p");
    var actions = document.createElement("div");
    actions.className = "btn-row";
    if (kind === "feed-rent") {
      heading.textContent = "Nothing for rent in this refresh";
      copy.textContent = "This update of the REALTOR.ca feed has no active residential rentals in Greater Vancouver or the Fraser Valley. Devin still helps people find a place to rent, and the homes for sale are one page away.";
      actions.appendChild(pageLink("Talk with Devin about a rental", "tenants.html", true));
      actions.appendChild(pageLink("See homes for sale", "listings.html", false));
    } else if (kind === "feed-sale") {
      heading.textContent = "No homes for sale in this refresh";
      copy.textContent = "This update did not include active residential listings. Send Devin a note and he can help you look.";
      actions.appendChild(pageLink("Contact Devin", "buyers.html", true));
    } else {
      heading.textContent = mode === "rent" ? "No rentals match" : "No homes match";
      copy.textContent = "Try another city, a wider price, or clear the filters.";
      var clear = document.createElement("button");
      clear.type = "button";
      clear.className = "btn btn-outline";
      clear.textContent = "Clear filters";
      clear.addEventListener("click", clearFilters);
      actions.appendChild(clear);
    }
    box.appendChild(heading);
    box.appendChild(copy);
    box.appendChild(actions);
    emptyEl.replaceChildren(box);
  }

  function pageLink(text, href, primary) {
    var a = document.createElement("a");
    a.className = primary ? "btn btn-primary" : "btn btn-outline";
    a.href = href;
    a.textContent = text;
    return a;
  }

  function card(item, index) {
    var article = document.createElement("article");
    article.className = "ls-card";
    var media = document.createElement("a");
    media.className = "ls-media";
    media.href = "#" + encodeURIComponent(item.id);
    media.appendChild(photoEl(item, 0, index > 1));
    var total = photoTotal(item);
    if (total > 1) {
      var badgeCount = document.createElement("span");
      badgeCount.className = "ls-photocount";
      badgeCount.textContent = total + " photos";
      media.appendChild(badgeCount);
    }
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
    var foot = document.createElement("div");
    foot.className = "ls-card-foot";
    var link = realtorLink(item, true);
    link.classList.add("ls-realtor");
    foot.appendChild(link);
    foot.appendChild(badge(item));
    body.appendChild(price);
    body.appendChild(h);
    body.appendChild(meta);
    body.appendChild(broker);
    body.appendChild(foot);
    article.appendChild(media);
    article.appendChild(body);
    return article;
  }

  function photoEl(item, index, lazy) {
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
    if (lazy) img.loading = "lazy";
    else if (index === 0) img.setAttribute("fetchpriority", "high");
    img.decoding = "async";
    img.addEventListener("load", function () {
      var box = img.parentElement;
      if (!box || !img.naturalWidth || !box.clientWidth) return;
      var dpr = window.devicePixelRatio || 1;
      if (img.naturalWidth < box.clientWidth * dpr && img.naturalHeight < box.clientHeight * dpr) img.classList.add("is-native");
    });
    img.addEventListener("error", function () {
      var missing = document.createElement("div");
      missing.className = "ls-nophoto";
      missing.textContent = "Photo unavailable";
      img.replaceWith(missing);
    });
    return img;
  }

  function httpsPhotos(item) {
    var list = item.photos;
    if (!list || !list.length) list = item.photo ? [item.photo] : [];
    return list.filter(function (url) { return typeof url === "string" && url.indexOf("https://") === 0; });
  }

  function photoTotal(item) {
    if (item.photos && item.photos.length) return item.photos.length;
    if (item.photoCount) return item.photoCount;
    return item.photo ? 1 : 0;
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
    if (item.area && item.area !== item.city) bits.push(item.area);
    return bits.join(" · ");
  }

  function formatBaths(n) {
    var num = Number(n);
    return num % 1 === 0 ? String(num) : String(num);
  }

  function countLabel(n) {
    if (mode === "rent") return n === 1 ? "1 rental" : n + " rentals";
    return n === 1 ? "1 home" : n + " homes";
  }

  function money(n) {
    if (n == null || n === "") return mode === "rent" ? "Rent on request" : "Price on request";
    var text = "$" + Number(n).toLocaleString("en-CA");
    return mode === "rent" ? text + "/month" : text;
  }

  function brokerageLine(item) {
    return "Listing brokerage: " + (item.brokerage || "not supplied in the feed");
  }

  function realtorLink(item, compact) {
    var a = document.createElement("a");
    a.target = "_blank";
    a.rel = "noopener";
    a.href = safeHttp(item.realtorUrl) || "https://www.realtor.ca/";
    a.textContent = safeHttp(item.realtorUrl)
      ? (compact ? "View on REALTOR.ca" : "View this listing on REALTOR.ca")
      : "REALTOR.ca";
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
    closeLightbox();
    document.body.classList.remove("is-listing-open");
    detailEl.hidden = true;
    searchEl.hidden = false;
    document.title = baseTitle;
    renderResults();
  }

  function showDetail(item) {
    state.current = item;
    state.photo = 0;
    document.body.classList.add("is-listing-open");
    searchEl.hidden = true;
    detailEl.hidden = false;
    var inquiry = document.querySelector(".ls-inquiry");
    if (inquiry) inquiry.hidden = false;
    document.title = titleFor(item) + " | " + baseTitle;
    paintDetail();
    ensureDetail(item, function () {
      if (state.current === item) paintDetail();
    });
    var heading = document.getElementById("ls-heading");
    if (heading) heading.focus();
    window.scrollTo(0, 0);
    track(item);
  }

  function shardUrl(id) {
    var text = String(id || "");
    var n = /^\d+$/.test(text) ? (Number(text) % SHARD_COUNT) : 0;
    return "listings/" + (mode === "rent" ? "rent" : "sale") + "/" + n + ".json";
  }

  function ensureDetail(item, done) {
    if (!item || state.sample || item._detailLoaded || item.photos) {
      if (item) item._detailLoaded = true;
      done(item);
      return;
    }
    loadShard(shardUrl(item.id), function (payload) {
      var detail = (payload && payload[String(item.id)]) || {};
      if (detail.photos && detail.photos.length) item.photos = detail.photos;
      if (detail.remarks) item.remarks = detail.remarks;
      item._detailLoaded = true;
      done(item);
    });
  }

  function loadShard(url, cb) {
    if (Object.prototype.hasOwnProperty.call(shardCache, url)) {
      cb(shardCache[url]);
      return;
    }
    if (shardWait[url]) {
      shardWait[url].push(cb);
      return;
    }
    shardWait[url] = [cb];
    fetch(url, { headers: { "Accept": "application/json" } })
      .then(function (r) { if (!r.ok) throw new Error(String(r.status)); return r.json(); })
      .then(function (data) { finishShard(url, data || {}); })
      .catch(function () { finishShard(url, {}); });
  }

  function finishShard(url, data) {
    shardCache[url] = data;
    var waiters = shardWait[url] || [];
    delete shardWait[url];
    waiters.forEach(function (fn) { fn(data); });
  }

  function showMissing() {
    closeLightbox();
    document.body.classList.add("is-listing-open");
    searchEl.hidden = true;
    detailEl.hidden = false;
    document.getElementById("ls-price").textContent = "";
    document.getElementById("ls-heading").textContent = "This listing is no longer in the feed";
    document.getElementById("ls-meta").textContent = "";
    document.getElementById("ls-broker").textContent = "";
    document.getElementById("ls-agent").textContent = "";
    document.getElementById("ls-photo").replaceChildren();
    document.getElementById("ls-photo-count").textContent = "";
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
    var total = photoTotal(item);
    document.getElementById("ls-price").textContent = money(item.price);
    document.getElementById("ls-heading").textContent = titleFor(item);
    document.getElementById("ls-meta").textContent = metaLine(item);
    document.getElementById("ls-broker").textContent = brokerageLine(item);
    var agent = document.getElementById("ls-agent");
    agent.textContent = item.agent ? "Listing REALTOR®: " + item.agent : "";
    var frame = document.getElementById("ls-photo");
    frame.replaceChildren(photoEl(item, state.photo, false));
    var photoCountEl = document.getElementById("ls-photo-count");
    if (!item._detailLoaded && !state.sample && total > photos.length) {
      photoCountEl.textContent = "Loading " + total + " photos…";
    } else if (photos.length > 1) {
      photoCountEl.textContent = "Photo " + (state.photo + 1) + " of " + photos.length;
    } else {
      photoCountEl.textContent = "";
    }
    var thumbs = document.getElementById("ls-thumbs");
    thumbs.replaceChildren();
    photos.forEach(function (_url, i) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "ls-thumb" + (i === state.photo ? " is-on" : "");
      btn.setAttribute("aria-label", "Photo " + (i + 1));
      btn.appendChild(photoEl(item, i, true));
      btn.addEventListener("click", function () { state.photo = i; paintDetail(); });
      thumbs.appendChild(btn);
    });
    var multi = photos.length > 1;
    document.getElementById("ls-prev").hidden = !multi;
    document.getElementById("ls-next").hidden = !multi;
    var linkSlot = document.getElementById("ls-realtor-link");
    linkSlot.replaceChildren(realtorLink(item, false));
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
    } else if (!item._detailLoaded && !state.sample) {
      var waiting = document.createElement("p");
      waiting.textContent = "Loading the description…";
      remarks.appendChild(waiting);
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
    paintLightbox();
  }

  function ensureLightbox() {
    var root = document.getElementById("ls-lightbox");
    if (root) return root;
    root = document.createElement("div");
    root.id = "ls-lightbox";
    root.className = "ls-lightbox";
    root.hidden = true;
    root.setAttribute("role", "dialog");
    root.setAttribute("aria-modal", "true");
    root.setAttribute("aria-label", "Listing photo");
    var close = document.createElement("button");
    close.type = "button";
    close.className = "ls-lightbox-close";
    close.textContent = "Close";
    close.addEventListener("click", closeLightbox);
    var stage = document.createElement("div");
    stage.className = "ls-lightbox-stage";
    stage.id = "ls-lightbox-stage";
    var count = document.createElement("p");
    count.className = "ls-lightbox-count";
    count.id = "ls-lightbox-count";
    root.appendChild(close);
    root.appendChild(stage);
    root.appendChild(count);
    root.addEventListener("click", function (e) {
      if (e.target === root) closeLightbox();
    });
    var startX = null;
    stage.addEventListener("touchstart", function (e) {
      startX = e.changedTouches && e.changedTouches[0] ? e.changedTouches[0].clientX : null;
    }, { passive: true });
    stage.addEventListener("touchend", function (e) {
      if (startX == null || !e.changedTouches || !e.changedTouches[0]) return;
      var dx = e.changedTouches[0].clientX - startX;
      startX = null;
      if (Math.abs(dx) > 40) step(dx < 0 ? 1 : -1);
    }, { passive: true });
    document.body.appendChild(root);
    return root;
  }

  function openLightbox() {
    var photos = state.current ? httpsPhotos(state.current) : [];
    if (!photos.length || !detailEl || detailEl.hidden) return;
    state.lightbox = true;
    var root = ensureLightbox();
    root.hidden = false;
    document.body.classList.add("is-lightbox");
    paintLightbox();
    var close = root.querySelector(".ls-lightbox-close");
    if (close) close.focus();
  }

  function closeLightbox() {
    if (!state.lightbox && !document.getElementById("ls-lightbox")) return;
    state.lightbox = false;
    var root = document.getElementById("ls-lightbox");
    if (root) root.hidden = true;
    document.body.classList.remove("is-lightbox");
  }

  function paintLightbox() {
    if (!state.lightbox) return;
    var stage = document.getElementById("ls-lightbox-stage");
    var count = document.getElementById("ls-lightbox-count");
    var item = state.current;
    if (!stage || !item) return;
    var photos = httpsPhotos(item);
    stage.replaceChildren(photoEl(item, state.photo, false));
    var img = stage.querySelector("img");
    if (img) img.alt = photos.length > 1 ? "Photo " + (state.photo + 1) + " of " + photos.length : "Listing photo";
    if (count) count.textContent = photos.length > 1 ? "Photo " + (state.photo + 1) + " of " + photos.length : "";
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

  // CREA DDF Analytics Web Service (analytics.crea.ca), required on listing views
  // by the June 2026 DDF rules. Sample rows and rows without a numeric ListingID
  // are not logged. One view per listing per browser session.
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
    var referral = "";
    try { referral = location.href || ""; } catch (e) { referral = ""; }
    var img = new Image();
    img.src = "https://analytics.crea.ca/LogEvents.svc/LogEvents?ListingID=" + encodeURIComponent(item.analyticsId)
      + "&DestinationID=" + encodeURIComponent(state.destinationId)
      + "&EventType=view&UUID=" + encodeURIComponent(uuid + "-" + state.destinationId)
      + (referral ? "&ReferralURL=" + encodeURIComponent(referral) : "");
  }

  function markChips() {
    var min = document.getElementById("ls-min").value;
    var max = document.getElementById("ls-max").value;
    document.querySelectorAll(".ls-chip").forEach(function (btn) {
      var on = (btn.getAttribute("data-min") || "") === min && (btn.getAttribute("data-max") || "") === max;
      btn.classList.toggle("is-on", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  function syncFilterButton() {
    if (!toggleEl) return;
    var n = 0;
    if (document.getElementById("ls-beds").value) n += 1;
    if (document.getElementById("ls-baths").value) n += 1;
    if (document.getElementById("ls-type").value) n += 1;
    var min = document.getElementById("ls-min").value;
    var max = document.getElementById("ls-max").value;
    var chipOn = false;
    document.querySelectorAll(".ls-chip").forEach(function (btn) {
      if ((btn.getAttribute("data-min") || "") === min && (btn.getAttribute("data-max") || "") === max) chipOn = true;
    });
    if ((min || max) && !chipOn) n += 1;
    toggleEl.textContent = n ? "Filters (" + n + ")" : "Filters";
    if (desktopFilters.matches) toggleEl.setAttribute("aria-expanded", "true");
    else toggleEl.setAttribute("aria-expanded", moreFiltersEl && !moreFiltersEl.classList.contains("is-collapsed") ? "true" : "false");
  }

  function applyFilters() {
    markChips();
    syncFilterButton();
    state.shown = pageSize();
    renderResults();
  }

  function clearFilters() {
    filtersEl.reset();
    applyFilters();
  }

  var timer = null;
  filtersEl.addEventListener("submit", function (e) { e.preventDefault(); applyFilters(); });
  filtersEl.addEventListener("input", function () {
    clearTimeout(timer);
    timer = setTimeout(applyFilters, 150);
  });
  filtersEl.addEventListener("change", applyFilters);
  document.getElementById("ls-clear").addEventListener("click", clearFilters);
  document.querySelectorAll(".ls-chip").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.getElementById("ls-min").value = btn.getAttribute("data-min") || "";
      document.getElementById("ls-max").value = btn.getAttribute("data-max") || "";
      applyFilters();
    });
  });
  if (toggleEl && moreFiltersEl) {
    toggleEl.addEventListener("click", function () {
      moreFiltersEl.classList.toggle("is-collapsed");
      syncFilterButton();
    });
    if (desktopFilters.addEventListener) desktopFilters.addEventListener("change", syncFilterButton);
  }
  moreEl.addEventListener("click", function () { state.shown += pageSize(); renderResults(); });
  document.getElementById("ls-prev").addEventListener("click", function () { step(-1); });
  document.getElementById("ls-next").addEventListener("click", function () { step(1); });
  var frame = document.getElementById("ls-photo");
  var touchX = null;
  var gesture = "";
  if (frame) {
    frame.addEventListener("touchstart", function (e) {
      gesture = "";
      touchX = e.changedTouches && e.changedTouches[0] ? e.changedTouches[0].clientX : null;
    }, { passive: true });
    frame.addEventListener("touchend", function (e) {
      if (touchX == null || !e.changedTouches || !e.changedTouches[0]) return;
      var dx = e.changedTouches[0].clientX - touchX;
      touchX = null;
      if (Math.abs(dx) > 40) {
        gesture = "swipe";
        step(dx < 0 ? 1 : -1);
      }
    }, { passive: true });
    frame.addEventListener("click", function () {
      if (gesture === "swipe") { gesture = ""; return; }
      openLightbox();
    });
    frame.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        openLightbox();
      }
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && state.lightbox) {
      closeLightbox();
      if (frame) frame.focus();
      return;
    }
    if (!detailEl || detailEl.hidden) return;
    var name = e.target && e.target.tagName;
    if (name === "INPUT" || name === "TEXTAREA" || name === "SELECT") return;
    if (e.key === "ArrowLeft") step(-1);
    if (e.key === "ArrowRight") step(1);
  });
  document.getElementById("ls-back").addEventListener("click", function (e) {
    e.preventDefault();
    history.pushState(null, "", location.pathname + location.search);
    showSearch();
  });
  window.addEventListener("hashchange", route);
  window.addEventListener("popstate", route);
  syncFilterButton();
  load();
})();
