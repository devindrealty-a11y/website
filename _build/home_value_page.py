"""Home value and nearby sales for the Tri-Cities, BC.

A visual request page. No automated price, no invented market numbers.
Copy rules: write "Tri-Cities, BC", and do not use "best", "top", or "expert".
"""
import json
import re

from partials import (
    BROKERAGE_ADDR,
    EMAIL,
    ICONS,
    PHONE,
    SITE,
    TEL,
    consent,
    foot,
    head,
)

PAGE = "home-value-tri-cities.html"
URL = SITE + PAGE
I = ICONS

TITLE = "What Is My Home Worth in Coquitlam? | Recent Sales, Tri-Cities, BC"
DESC = (
    "What is my home worth in Coquitlam, Port Coquitlam or Port Moody? "
    "Recent home sales in the Tri-Cities, BC, walked through on a free 15-minute call "
    "with Devin Desaulniers at Axford Real Estate."
)

_BARE_TRI = re.compile(r"Tri-Cities(?!\s*,\s*BC)")
_BANNED = re.compile(r"\b(?:best|top|expert)\b", re.I)
_CHECK = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
    '<path d="M20 6L9 17l-5-5"/></svg>'
)


def _skyline(paths):
    return (
        '<svg class="hv-sky" viewBox="0 0 120 48" fill="none" aria-hidden="true" focusable="false">'
        + paths
        + "</svg>"
    )


_COQ = _skyline(
    '<path d="M8 40V22h10v18M22 40V14h8v26M34 40V18h14v22" stroke="currentColor" stroke-width="2"/>'
    '<path d="M52 40V10h6v30M62 40V16h16v24M82 40V20h10v20M96 40V12h12v28" stroke="currentColor" stroke-width="2"/>'
    '<path d="M4 40h112" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
)
_POCO = _skyline(
    '<path d="M6 40V24l14-10 14 10v16M38 40V26l12-8 12 8v14M68 40V22l16-12 16 12v18" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>'
    '<path d="M4 40h112" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
)
_POMO = _skyline(
    '<path d="M4 30c10 4 18-2 28 0s16 6 26 2 18-6 28-2 16 4 30 0" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
    '<path d="M18 40V24h12v16M36 40V18h10v22M52 40V22h18v18M76 40V16h14v24" stroke="currentColor" stroke-width="2"/>'
    '<path d="M4 40h112" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
)


def _webpage_jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "@id": URL + "#webpage",
        "url": URL,
        "name": TITLE,
        "description": DESC,
        "inLanguage": "en-CA",
        "isPartOf": {"@type": "WebSite", "name": "Devin Desaulniers", "url": SITE},
        "about": [
            {"@id": SITE + "#devin-desaulniers"},
            {"@type": "Place", "name": "Tri-Cities, BC"},
            {"@type": "Place", "name": "Coquitlam"},
            {"@type": "Place", "name": "Port Coquitlam"},
            {"@type": "Place", "name": "Port Moody"},
        ],
        "publisher": {
            "@type": "RealEstateAgent",
            "name": "Axford Real Estate",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "2326 Clarke St",
                "addressLocality": "Port Moody",
                "addressRegion": "BC",
                "postalCode": "V3H 1Y8",
                "addressCountry": "CA",
            },
        },
    }
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(data, indent=2, ensure_ascii=False)
        + "\n</script>\n"
    )


def _assert_copy(*parts):
    blob = "\n".join(parts)
    bare = _BARE_TRI.search(blob)
    if bare:
        raise SystemExit("home value page uses bare 'Tri-Cities' at: " + bare.group(0))
    hit = _BANNED.search(re.sub(r"<[^>]+>", " ", blob))
    if hit:
        raise SystemExit("home value page uses a banned word: " + hit.group(0))


def render():
    types = ["Detached", "Townhouse", "Condo / apartment", "Half duplex", "Other"]
    timelines = ["Just curious", "0-3 months", "3-6 months", "6-12 months", "12+ months"]
    type_pills = "".join(
        f'<label><input type="radio" name="Property type" value="{label}" required> {label}</label>'
        for label in types
    )
    time_pills = "".join(
        f'<label><input type="radio" name="Timeline" value="{label}" required> {label}</label>'
        for label in timelines
    )
    cities = [
        ("hv-city--coq", "coquitlam.html", _COQ, "Coquitlam", "Detached homes, townhouses and condo complexes.", "Coquitlam guide"),
        ("hv-city--poco", "port-coquitlam.html", _POCO, "Port Coquitlam", "North side, south side and downtown PoCo.", "Port Coquitlam guide"),
        ("hv-city--pomo", "port-moody.html", _POMO, "Port Moody", "Moody Centre, Inlet Centre and the hillside.", "Port Moody guide"),
    ]
    city_cards = "".join(
        f'''<a class="hv-city {cls}" href="{href}">
        {mark}
        <span class="hv-city-k">Tri-Cities, BC</span>
        <h3>{name}</h3>
        <p>{blurb}</p>
        <span class="card-link">{link} {I["arrow"]}</span>
      </a>'''
        for cls, href, mark, name, blurb, link in cities
    )
    body = f'''
<section class="lp-hero hv-hero">
  <div class="container lp-hero-inner hv-hero-inner">
    <div class="hv-hero-copy">
      <span class="eyebrow">Past clients and sellers · Tri-Cities, BC</span>
      <h1>What's your home worth, and <em>what sold near you?</em></h1>
      <p class="lead">Send me your address. I'll look up recent MLS sales near your home in Coquitlam, Port Coquitlam or Port Moody, then walk you through them.</p>
      <div class="btn-row">
        <a class="btn btn-light" href="{TEL}">{I["phone"]} Book a free 15-minute call</a>
        <a class="btn btn-ghost-light" href="#request">Start with your address {I["arrow"]}</a>
      </div>
      <p class="hero-note">Devin Desaulniers, Real Estate Associate · Axford Real Estate, Port Moody, BC</p>
    </div>
    <aside class="hv-panel" aria-label="What you get">
      <h2>What you get</h2>
      <ol class="hv-gets">
        <li><span class="icon">{I["doc"]}</span><span>Recent sales on your street or in your complex</span></li>
        <li><span class="icon">{I["phone"]}</span><span>A personal walk-through on a 15-minute call</span></li>
        <li><span class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9"/><path d="M8 12h8"/></svg></span><span>I don't calculate a price on this page.</span></li>
      </ol>
    </aside>
  </div>
</section>

<section class="section" id="how">
  <div class="container">
    <div class="sec-head sec-head--center">
      <div>
        <span class="eyebrow">How it works</span>
        <h2>Three short steps</h2>
      </div>
    </div>
    <ol class="hv-steps">
      <li>
        <span class="icon">{I["home"]}</span>
        <span class="hv-n" aria-hidden="true">01</span>
        <h3>You ask</h3>
        <p>Send your address, property type and timeline.</p>
      </li>
      <li>
        <span class="icon">{I["doc"]}</span>
        <span class="hv-n" aria-hidden="true">02</span>
        <h3>Recent MLS sales</h3>
        <p>I pull real recent sales for your street or complex.</p>
      </li>
      <li>
        <span class="icon">{I["phone"]}</span>
        <span class="hv-n" aria-hidden="true">03</span>
        <h3>A 15-minute call</h3>
        <p>I walk you through them. Asking doesn't mean you have to list.</p>
      </li>
    </ol>
  </div>
</section>

<section class="section section--paper" id="request">
  <div class="container hv-request">
    <div class="hv-request-copy">
      <span class="eyebrow">Your home</span>
      <h2>Request a walk-through</h2>
      <p class="lead">Tell me the address, property type and when you might sell. I'll email you back to set up the call.</p>
    </div>
    <form class="offer-form hv-form" id="hv-form" data-form-key="homeValue" data-goat-event="form-home-value" action="#" method="POST">
      <input type="hidden" name="_subject" value="New home value request: Tri-Cities, BC">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="form" value="Home value and nearby sales — Tri-Cities, BC">
      <input type="hidden" name="Page" value="{URL}">
      <div class="hp" aria-hidden="true"><label>Leave this field empty <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
      <div data-offer-fields>
        <div class="form-grid cols-2">
          <div class="field full">
            <label for="hv-address">Property address <span class="req">*</span></label>
            <input id="hv-address" name="Property address" autocomplete="street-address" required>
          </div>
          <fieldset class="field full">
            <legend>Property type <span class="req">*</span></legend>
            <div class="checks">{type_pills}</div>
          </fieldset>
          <fieldset class="field full">
            <legend>Timeline <span class="req">*</span></legend>
            <div class="checks">{time_pills}</div>
          </fieldset>
          <div class="field">
            <label for="hv-name">Your name <span class="req">*</span></label>
            <input id="hv-name" name="name" autocomplete="name" required>
          </div>
          <div class="field">
            <label for="hv-email">Your email <span class="req">*</span></label>
            <input id="hv-email" name="email" type="email" inputmode="email" autocomplete="email" required>
          </div>
          <div class="field full">
            <label for="hv-phone">Phone <span class="req">*</span></label>
            <input id="hv-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required>
          </div>
          <div class="field full">
            <label class="hv-option">
              <input type="checkbox" name="Wider neighbourhood sales" value="Yes">
              <span>
                <strong>Also send recent sales across my wider neighbourhood</strong>
                <span class="hint">Same request. I'll add nearby sales beyond your street or complex.</span>
              </span>
            </label>
          </div>
          {consent("hv")}
          <div class="full">
            <button type="submit" class="btn btn-primary btn-block">Request my walk-through</button>
            <div class="form-status" role="status" aria-live="polite"></div>
          </div>
        </div>
      </div>
      <div class="offer-thanks" data-offer-thanks hidden role="status" tabindex="-1">
        <span class="offer-thanks-mark">{_CHECK}</span>
        <h2>Thanks, I'll take a look.</h2>
        <p>Your request is in. I'll look up recent sales for that address and get back to you to set up the 15-minute call. Want to talk sooner? Call or text me.</p>
        <a class="btn btn-outline" href="{TEL}">{I["phone"]} Call or text {PHONE}</a>
      </div>
      <p class="offer-note">This form is emailed to {EMAIL}. It is a walk-through of recent MLS sales. It is not an appraisal, and it is not a promise of a sale price. Devin Desaulniers, Real Estate Associate, Axford Real Estate.</p>
    </form>
  </div>
</section>

<section class="section" id="sold-near-you">
  <div class="container">
    <div class="sec-head">
      <div>
        <span class="eyebrow">What's sold near you</span>
        <h2>Recent sales in the Tri-Cities, BC</h2>
      </div>
      <div class="sec-head-aside">
        <p class="lead">Ask for recent sales on your street or in your complex, in any of these three cities.</p>
      </div>
    </div>
    <div class="hv-cities">{city_cards}</div>
    <p class="hv-city-note">Use the checkbox in the form, or call or text <a href="{TEL}">{PHONE}</a>.</p>
  </div>
</section>

<section class="section section--night cta-band">
  <div class="container center">
    <span class="eyebrow">Axford Real Estate</span>
    <h2>Ready for a 15-minute call?</h2>
    <p class="lead">I pull the recent MLS sales. Then I explain what they mean for your home.</p>
    <div class="btn-row">
      <a class="btn btn-light" href="{TEL}">{I["phone"]} Book a free 15-minute call</a>
      <a class="btn btn-ghost-light" href="#request">Start with your address {I["arrow"]}</a>
    </div>
    <p class="hv-broker">Devin Desaulniers, Real Estate Associate<br>Brokerage: Axford Real Estate<br>{BROKERAGE_ADDR}</p>
  </div>
</section>
'''
    _assert_copy(TITLE, DESC, body)
    page = head(
        TITLE,
        DESC,
        "home-value",
        og_image="assets/img/devin-headshot-800.jpg",
        page_url=PAGE,
        body_class="hv-page",
        extra_head=_webpage_jsonld(),
    )
    page += body
    page += foot()
    return page
