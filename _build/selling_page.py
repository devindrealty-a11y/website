"""Selling page: short intro, seasonal maintenance cards, guide request form.

Rendered by _build/build.py. The form posts through assets/js/config.js
(maintenanceGuide) and the shared handler in assets/js/site.js.
"""
import json
import re

from partials import EMAIL, PHONE, SITE, TEL, consent, foot, head, picture

PAGE = "selling.html"

_CHECK = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
    '<path d="M20 6L9 17l-5-5"/></svg>'
)


def _icon(paths):
    return (
        '<span class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
        f'focusable="false">{paths}</svg></span>'
    )


IC = {
    "rain": _icon('<path d="M12 3v3"/><path d="M7 8a5 5 0 0 1 10 0 4 4 0 0 1 1 8H6a4 4 0 0 1 1-8z"/><path d="M8 20l-1 2M12 20l-1 2M16 20l-1 2"/>'),
    "roof": _icon('<path d="M3 11l9-7 9 7"/><path d="M5 10v9h14v-9"/>'),
    "tap": _icon('<path d="M8 3v6"/><path d="M8 9h8a3 3 0 0 1 0 6H8"/><path d="M8 21v-6"/><path d="M5 21h6"/>'),
    "filter": _icon('<path d="M4 4h16l-6 8v6l-4 2v-8z"/>'),
    "alarm": _icon('<path d="M6 16V10a6 6 0 0 1 12 0v6"/><path d="M4 16h16"/><path d="M10 19a2 2 0 0 0 4 0"/>'),
    "drop": _icon('<path d="M12 3s6 6.2 6 10a6 6 0 0 1-12 0c0-3.8 6-10 6-10z"/>'),
    "ground": _icon('<path d="M3 18c2-3 4-3 6 0s4 3 6 0 4-3 6 0"/><path d="M4 10l8-6 8 6"/><path d="M7 10v4M17 10v4"/>'),
    "deck": _icon('<path d="M4 10h16"/><path d="M6 10v8M10 10v8M14 10v8M18 10v8"/><path d="M4 18h16"/>'),
    "tank": _icon('<path d="M8 6h8a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2z"/><path d="M9 3h6"/><path d="M12 11v4"/>'),
    "quake": _icon('<path d="M3 12h3l2-5 4 10 2-5h7"/>'),
}

TIPS = [
    ("Fall", "rain", "Clear the gutters",
     "Debris in the eavestroughs lets rain overflow against the walls. BC Housing says to look at the roof and gutters in spring and in fall, and after a hard wind or a heavy rain."),
    ("Fall", "roof", "Moss on the roof",
     "Moss holds moisture on shingles and shakes and speeds up wear. Have a roofer look. Walking a wet roof is their job."),
    ("Fall", "tap", "Hoses and sprinklers",
     "Take hoses off outdoor taps before a freeze so water is not trapped in the line. If you have in-ground sprinklers, have a contractor clear the lines with air before a freezing night."),
    ("Winter", "filter", "Furnace and heat pump filters",
     "FortisBC says to check a gas furnace filter at least every three months, and more often with pets or smokers. BC Hydro says to clean heat-pump filters several times a year and to follow the manual."),
    ("Winter", "alarm", "Smoke and CO alarms",
     "Test smoke alarms every month. The B.C. fire-safety toolkit says to replace the alarm at 10 years, or when the maker says. FortisBC says a carbon monoxide alarm belongs on each level, especially near bedrooms."),
    ("Winter", "drop", "Condensation and the attic",
     "Fog on the glass is a moisture clue. CMHC says a wet attic is often warm air leaking up from the house. Adding vents alone can pull more of that air in."),
    ("Spring", "ground", "Slope, drains, and the sump",
     "Ground, walks, and beds that slope toward the house keep a basement damp. Know where the footing drain and the sump are, and whether the pump runs when you can reach the float."),
    ("Spring", "deck", "Decks, siding, and sealant",
     "Keep balcony drains free of leaves. Failed sealant at windows and vents is where a lot of wall leaks start. BC Housing says a contractor should replace it, and should leave weep holes open."),
    ("Any month", "tank", "The hot water tank",
     "Health Canada: 60°C at the tank, and a mixing valve so the tap is 49°C. Strap the tank to the wall. FortisBC says the B.C. codes now require that strap."),
    ("Any month", "quake", "Pests, and a shake",
     "Carpenter ants tunnel in damp wood. They do not eat it. Keep wood dry and off the soil. In an earthquake: Drop, Cover, and Hold On. Know the shut-offs. Do not turn the gas meter back on yourself."),
]

FAQS = [
    ("What does selling with you include?",
     "I help you set a price from recent sales nearby, prepare the home, and market it. A written market evaluation is free, and asking for one does not mean you have to list. I am a Real Estate Associate with Axford Real Estate, working with sellers in Greater Vancouver and the Tri-Cities, BC."),
    ("Who looks after the roof on a townhouse or a condo?",
     "It depends on the strata plan and the bylaws. The Province of British Columbia says those documents, not a guess, decide the split. Under the standard bylaws in the Strata Property Act, the strata maintains the exterior, the structure, and things attached to the outside, including balconies. Owners maintain their own strata lot except where the bylaws give that job to the strata. Read your bylaws before you repair a roof or a deck."),
    ("How often should a roof here be looked at?",
     "BC Housing's roof bulletin says twice a year: in the spring, and in the fall before winter rain, plus after high wind, heavy rain, or hail. Hire a roofing professional for the inspection and for moss. The same bulletin says a roof's life can range from 10 years to over 30, depending on design, exposure, construction, and materials. That is a range, not a date for your roof."),
    ("Is this guide a home inspection?",
     "No. It is general information for owners in Greater Vancouver and the Tri-Cities, BC. It is not a substitute for a professional home inspection. In B.C., home inspectors are licensed through Consumer Protection BC. A home inspection is a visual look at the home on that day. It is not a prediction, and it is not a code inspection."),
]


def _plain(html):
    return re.sub(r"<[^>]+>", "", html)


def _check(fragment):
    bare = re.search(r"Tri-Cities(?!\s*,\s*BC)", fragment)
    if bare:
        raise SystemExit("selling page: bare Tri-Cities")
    hit = re.search(r"\b(?:best|top|expert)\b", fragment, re.I)
    if hit:
        raise SystemExit(f"selling page: do not use {hit.group(0)!r}")


def _schema():
    address = {
        "@type": "PostalAddress",
        "streetAddress": "2326 Clarke St",
        "addressLocality": "Port Moody",
        "addressRegion": "BC",
        "postalCode": "V3H 1Y8",
        "addressCountry": "CA",
    }
    agent = {
        "@type": ["RealEstateAgent", "LocalBusiness"],
        "@id": SITE + "selling.html#agent",
        "name": "Devin Desaulniers",
        "jobTitle": "Real Estate Associate",
        "url": SITE + "selling.html",
        "image": SITE + "assets/img/devin-kitchen-800.jpg",
        "telephone": "604-809-1032",
        "email": EMAIL,
        "address": address,
        "areaServed": [
            {"@type": "Place", "name": "Greater Vancouver"},
            {"@type": "Place", "name": "Tri-Cities, BC"},
        ],
        "parentOrganization": {"@type": "RealEstateAgent", "name": "Axford Real Estate", "address": address},
    }
    howto = {
        "@type": "HowTo",
        "name": "Seasonal home maintenance in Greater Vancouver",
        "description": "Ten short maintenance checks for a house in Greater Vancouver and the Tri-Cities, BC, drawn from BC Housing, CMHC, FortisBC, BC Hydro, and provincial safety pages.",
        "step": [
            {"@type": "HowToStep", "position": i + 1, "name": f"{season}: {title}", "text": text}
            for i, (season, _icon_key, title, text) in enumerate(TIPS)
        ],
    }
    faq = {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQS
        ],
    }
    data = {"@context": "https://schema.org", "@graph": [agent, howto, faq]}
    return '<script type="application/ld+json">\n' + json.dumps(data, indent=2, ensure_ascii=False) + "\n</script>"


def _tips():
    cards = []
    for season, key, title, text in TIPS:
        cards.append(
            f'<article class="tip-card"><p class="tip-kicker">{IC[key]}<span>{season}</span></p>'
            f"<h3>{title}</h3><p>{text}</p></article>"
        )
    return "".join(cards)


def _faqs():
    rows = []
    for q, a in FAQS:
        rows.append(f'<div class="faq-item"><h3>{q}</h3><div class="ans"><p>{a}</p></div></div>')
    return "".join(rows)


def render():
    photo = picture(
        "assets/img/devin-kitchen",
        (480, 800, 1179),
        1179,
        1550,
        "Devin Desaulniers in a kitchen, Real Estate Associate with Axford Real Estate",
        sizes_attr="(max-width: 699px) 70vw, 220px",
    )
    body = f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Selling · Axford Real Estate</span>
    <h1>Selling a home in Greater Vancouver</h1>
    <p class="lead">I am Devin Desaulniers, a Real Estate Associate with Axford Real Estate. I help sellers in the Tri-Cities, BC and the rest of Greater Vancouver price from recent sales, prepare the home, and bring it to market.</p>
    <div class="btn-row">
      <a class="btn btn-light" href="#guide">Home maintenance tips</a>
      <a class="btn btn-ghost-light" href="#request">Email me the full guide</a>
    </div>
  </div>
</section>
<nav class="page-nav" aria-label="On this page"><div class="container"><span class="pn-label">On this page</span><a href="#guide">Maintenance tips</a><a href="#request">Full guide</a><a href="#questions">Questions</a><a href="home-evaluation.html">Home evaluation</a></div></nav>

<section class="section">
  <div class="container sell-intro">
    <figure class="portrait">{photo}<figcaption><strong>Devin Desaulniers</strong><span>Real Estate Associate · Axford Real Estate</span></figcaption></figure>
    <div>
      <h2>A short list before you list, or if you are staying.</h2>
      <p class="lead">Rain drives most of the work on a West Coast house: gutters, moss, the ground around the foundation, and damp air in the attic and the crawl space. The cards below are the checks I walk through with owners. The longer version is a printable guide.</p>
      <p>A free home evaluation is a separate note: recent sales nearby, and what I would expect your home to bring. Asking does not mean you have to list. <a href="home-evaluation.html">Request a home evaluation</a>.</p>
      <p>Townhouse and condo owners: the strata often looks after the roof and the exterior. You still look after filters, alarms, and whatever your bylaws leave with you. Read the bylaws before you repair something on the outside.</p>
    </div>
  </div>
</section>

<section class="section section--paper" id="guide">
  <div class="container">
    <div class="sec-head">
      <div>
        <span class="eyebrow">Home maintenance tips</span>
        <h2>Ten checks, by season</h2>
      </div>
      <div class="sec-head-aside">
        <p class="lead">Written for detached houses in Greater Vancouver and the Tri-Cities, BC. Each card is a short version of a point in the guide, with the source named there.</p>
      </div>
    </div>
    <div class="sell-photos">
      <figure><img src="assets/img/blog/photos/westwood-greene-port-coquitlam-2025.jpg" width="1200" height="1600" alt="Detached houses on Westwood Street at Greene Street in Port Coquitlam, with the mountains behind them" loading="lazy" decoding="async"><figcaption>Port Coquitlam houses. Neondev1, CC0.</figcaption></figure>
      <figure><img src="assets/img/blog/photos/vancouver-house-roof-west-17th.jpg" width="1400" height="787" alt="Shingled roof and turret of a house on West 17th Avenue in Vancouver" loading="lazy" decoding="async" style="object-position:center 30%"><figcaption>Vancouver roof. Socratic, CC BY-SA 3.0.</figcaption></figure>
      <figure><img src="assets/img/blog/photos/burrard-inlet-port-moody-rain-2014.jpg" width="1000" height="666" alt="Rain on Burrard Inlet at Port Moody, with pilings in the water" loading="lazy" decoding="async"><figcaption>Rain at Port Moody. waferboard, CC BY 2.0.</figcaption></figure>
      <figure><img src="assets/img/blog/photos/kitsilano-house-windows-blossoms.jpg" width="1200" height="675" alt="Wood-sided house in Kitsilano, Vancouver, with spring blossoms in front of the windows" loading="lazy" decoding="async"><figcaption>Kitsilano siding. Adam Jones, CC BY-SA 2.0.</figcaption></figure>
    </div>
    <div class="tip-grid">
      {_tips()}
    </div>
    <p class="sell-credit">Photos are real places, used under the licences named on each picture. The full credit list is in the PDF. This page does not use a rainfall total, a repair price, or a sprinkler-blowout date: I did not find a Metro Vancouver or Tri-Cities, BC page that sets one.</p>
  </div>
</section>

<section class="section" id="request">
  <div class="container sell-gate">
    <div>
      <span class="eyebrow">The full guide</span>
      <h2>Want the full guide? I'm happy to email it to you.</h2>
      <p class="lead">It is a short letter-size PDF for homeowners in Greater Vancouver and the Tri-Cities, BC: a season-by-season checklist, what a home inspector looks at, and an earthquake-ready list. Detached houses get the detail. Townhouses and condos get a short note on what the strata usually handles.</p>
      <p>General information only. It is not a substitute for a professional home inspection, and it is not a list of repairs you must finish before you sell.</p>
      <p class="form-note">Devin Desaulniers, Real Estate Associate · Axford Real Estate · <a href="{TEL}">{PHONE}</a></p>
    </div>
    <form class="form-card" id="guide-form" data-form-key="maintenanceGuide" data-goat-event="form-maintenance-guide" action="#" method="POST">
      <input type="hidden" name="_subject" value="Home maintenance guide request">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="form" value="Home maintenance guide request">
      <div class="hp" aria-hidden="true"><label>Leave this field empty <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
      <div data-offer-fields>
        <div class="form-grid">
          <div class="field"><label for="sg-name">Your name <span class="req">*</span></label><input id="sg-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="sg-email">Your email <span class="req">*</span></label><input id="sg-email" name="email" type="email" inputmode="email" autocomplete="email" required></div>
          {consent("sg")}
          <div class="full">
            <button type="submit" class="btn btn-primary">Email me the guide</button>
            <div class="form-status" role="status" aria-live="polite"></div>
          </div>
        </div>
      </div>
      <div class="offer-thanks" data-offer-thanks hidden role="status" tabindex="-1">
        <span class="offer-thanks-mark">{_CHECK}</span>
        <h2>Thanks — the guide is yours.</h2>
        <p>I'll email it to you as well. You can download it here now.</p>
        <a class="btn btn-primary" href="assets/guides/greater-vancouver-home-maintenance-guide.pdf" download>Download the home maintenance guide (PDF)</a>
      </div>
      <noscript><p>This form needs JavaScript. Email <a href="mailto:{EMAIL}">{EMAIL}</a> and ask for the Greater Vancouver home maintenance guide.</p></noscript>
    </form>
  </div>
</section>

<section class="section section--paper" id="questions">
  <div class="container narrow-wide">
    <span class="eyebrow">Questions</span>
    <h2>Selling, strata, and the guide</h2>
    <div class="faq-list">{_faqs()}</div>
  </div>
</section>

<section class="section section--night">
  <div class="container narrow">
    <span class="eyebrow">Next step</span>
    <h2>Want a price, not a maintenance list?</h2>
    <p>Send me the address and I'll email a market evaluation: recent sales nearby, and what I would expect your home to bring. Axford Real Estate, Port Moody.</p>
    <a class="btn btn-light" href="home-evaluation.html">Request a home evaluation</a>
  </div>
</section>
"""
    _check(body)
    _check(_plain(json.dumps([t[3] for t in TIPS] + [a for _, a in FAQS])))
    page = head(
        "Selling a Home in Greater Vancouver | Devin Desaulniers, Axford Real Estate",
        "Selling with Devin Desaulniers at Axford Real Estate, plus seasonal home maintenance tips for Greater Vancouver and the Tri-Cities, BC, and a guide you can have by email.",
        "selling",
        page_url=PAGE,
        extra_head=_schema(),
        agent_knows=["Selling a home in Greater Vancouver", "Home maintenance for the Tri-Cities, BC"],
    )
    page += body
    page += foot()
    return page
