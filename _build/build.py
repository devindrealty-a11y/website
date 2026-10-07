import os, json
from partials import *
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I = ICONS

MOUNTAINS = '''<svg class="hero-mountains" viewBox="0 0 1440 220" preserveAspectRatio="none" aria-hidden="true">
<path d="M0 150 L120 90 L210 130 L330 50 L450 120 L560 70 L680 135 L800 60 L930 125 L1040 80 L1160 140 L1290 75 L1440 125 L1440 220 L0 220Z" fill="#3474b6" opacity=".10"/>
<path d="M0 175 L150 125 L260 160 L380 105 L520 165 L640 120 L770 170 L900 115 L1030 168 L1170 120 L1300 165 L1440 140 L1440 220 L0 220Z" fill="#808082" opacity=".14"/>
<path d="M0 200 C240 180 480 214 720 196 C960 178 1200 210 1440 192 L1440 220 L0 220Z" fill="#ffffff"/>
</svg>'''

# ---------------- HOME ----------------
# Home-page relocation video ad (web encode of video-bot/grand-tri-cities/grand-tri-cities-final.mp4)
VIDEO_MP4 = "assets/video/greater-vancouver-relocation-ad.mp4"
VIDEO_POSTER = "assets/video/greater-vancouver-relocation-ad-poster.jpg"
VIDEO_NAME = "Moving to Greater Vancouver? | Devin Desaulniers"
VIDEO_DESC = "A short relocation video for people moving to Greater Vancouver, BC (Coquitlam, Port Coquitlam and Port Moody), presented by Devin Desaulniers, Real Estate Associate with Axford Real Estate."
VIDEO_JSONLD = '<script type="application/ld+json">\n' + json.dumps({
    "@context": "https://schema.org",
    "@type": "VideoObject",
    "name": VIDEO_NAME,
    "description": VIDEO_DESC,
    "thumbnailUrl": SITE + VIDEO_POSTER,
    "contentUrl": SITE + VIDEO_MP4,
    "uploadDate": "2026-10-06",
    "duration": "PT32S",
}, indent=2, ensure_ascii=False) + '\n</script>'

home = head("Devin Desaulniers | Real Estate Associate, Axford Real Estate | Tri-Cities, BC",
            "Devin Desaulniers, Real Estate Associate with Axford Real Estate, helping buyers and relocating tenants in Coquitlam, Port Coquitlam, Port Moody and Greater Vancouver.", "home",
            extra_head=VIDEO_JSONLD)
home += f'''
<section class="hero">
  <div class="container hero-inner">
    <div>
      <span class="eyebrow">Coquitlam · Port Coquitlam · Port Moody</span>
      <h1>Your Tri-Cities, BC real estate <span class="accent">neighbour</span>.</h1>
      <p class="lead">I'm Devin Desaulniers, a Real Estate Associate with <strong>Axford Real Estate</strong>. I've lived in the Greater Vancouver area for 28 years, and I help home buyers and relocating tenants across Greater Vancouver — especially here in the Tri-Cities, BC.</p>
      <ul class="chips">
        <li>Licensed since 2020</li>
        <li>28 years living in Greater Vancouver</li>
        <li>Brokerage: Axford Real Estate</li>
      </ul>
      <div class="btn-row">
        <a class="btn btn-primary" href="buyers.html">I'm buying {I["arrow"]}</a>
        <a class="btn btn-outline" href="tenants.html">I'm relocating &amp; renting</a>
      </div>
    </div>
    <div class="hero-card">
      {picture("assets/img/devin-headshot",(480,800),800,1000,"Devin Desaulniers, Real Estate Associate with Axford Real Estate","headshot",eager=True)}
      <div class="who"><strong>Devin Desaulniers</strong><span>Real Estate Associate · Axford Real Estate</span></div>
    </div>
  </div>
  {MOUNTAINS}
</section>

<section class="section video-section" id="video">
  <div class="container">
    <div class="center narrow">
      <span class="eyebrow">Relocation video</span>
      <h2>Moving to Greater Vancouver?</h2>
      <p class="lead">I help people relocating to Greater Vancouver find a rental, with in-person or virtual showings. Watch the video, then see how my relocation rental service works.</p>
    </div>
    <div class="video-frame">
      <video controls playsinline preload="metadata" poster="{VIDEO_POSTER}" width="1280" height="720" aria-label="Moving to Greater Vancouver: relocation video presented by Devin Desaulniers, Real Estate Associate with Axford Real Estate" title="Moving to Greater Vancouver? Relocation video by Devin Desaulniers">
        <source src="{VIDEO_MP4}" type="video/mp4">
        <p>Your browser can't play this video. <a href="{VIDEO_MP4}">Download the relocation video (MP4)</a>.</p>
      </video>
    </div>
    <div class="btn-row" style="justify-content:center;margin-top:28px">
      <a class="btn btn-primary" href="tenants.html">See the relocation rental service {I["arrow"]}</a>
      <a class="btn btn-outline" href="{TEL}">Call or text {PHONE}</a>
    </div>
  </div>
</section>

<section class="section" id="services">
  <div class="container">
    <div class="center narrow">
      <span class="eyebrow">How I can help</span>
      <h2>Services</h2>
      <p class="lead">Whether you're buying your first place or moving to the Lower Mainland and need a rental, I'll make the process clear and manageable.</p>
    </div>
    <div class="grid grid-3" style="margin-top:32px">
      <article class="card service-card">
        <div class="icon">{I["home"]}</div>
        <h3>Buying a home</h3>
        <p>Neighbourhood guidance, listing alerts tailored to you, showings, and support with offers and negotiation from search to completion.</p>
        <a class="btn btn-outline" href="buyers.html">Buyer info &amp; neighbourhoods</a>
      </article>
      <article class="card service-card">
        <div class="icon">{I["key"]}</div>
        <h3>Relocation rental service</h3>
        <p>Moving to Greater Vancouver? I represent tenants through the whole search: consultation, property search, in-person or virtual showings, and lease review &amp; negotiation — <strong>$1,500 + GST, paid by the tenant in two parts</strong>.</p>
        <a class="btn btn-outline" href="tenants.html">See how it works</a>
      </article>
      <article class="card service-card">
        <div class="icon">{I["calc"]}</div>
        <h3>Free mortgage calculator</h3>
        <p>Get a quick estimate of what you might be able to afford before you start shopping — or dig into the details with the full version.</p>
        <a class="btn btn-outline" href="{CALC}" target="_blank" rel="noopener">Open calculator {I["ext"]}</a>
      </article>
    </div>
  </div>
</section>

<section class="section section--grey" id="about">
  <div class="container about-grid">
    <div>
      <span class="eyebrow">About Devin</span>
      <h2>Local roots, Tri-Cities, BC focus</h2>
      <p>I've lived in the Greater Vancouver area for 28 years, I work in Port Moody, and I play soccer on a Port Coquitlam team — so I know the Tri-Cities, BC especially well. I love this area, and I know it as a resident, not just from a map.</p>
      <p>For the last seven years I've been helping people relocate to and from Vancouver, and I've been licensed in real estate since 2020. Today I'm a Real Estate Associate with Axford Real Estate, helping buyers and tenants across Greater Vancouver, with a particular focus on Coquitlam, Port Coquitlam and Port Moody.</p>
      <p>When I'm not working, you'll find me on the soccer pitch or a pickleball court somewhere around town.</p>
      {social_row()}
    </div>
    <div class="facts">
      <div class="fact"><b>2020</b><span>Licensed in real estate</span></div>
      <div class="fact"><b>28 years</b><span>Living in the Greater Vancouver area</span></div>
      <div class="fact"><b>7 years</b><span>Helping people relocate to &amp; from Vancouver</span></div>
      <div class="fact"><b>Port Moody</b><span>Where I work · Tri-Cities, BC focus</span></div>
      <div class="fact" style="grid-column:1/-1"><b>Axford Real Estate</b><span>Brokerage · {BROKERAGE_ADDR}</span></div>
    </div>
  </div>
</section>

{testimonials_section(["thurza","jackie","jordan","florian"], "What clients say", lead="Buyers and sellers I've worked with, in their own words.", sec_id="testimonials", bg="")}

<section class="section section--grey">
  <div class="container">{calc_cta()}</div>
</section>

<section class="section section--blue" id="contact">
  <div class="container">
    <div class="narrow center">
      <span class="eyebrow">Get in touch</span>
      <h2>Let's talk about your move</h2>
      <p style="color:#dbe7f4">Buying, relocating, or just have a question about the Tri-Cities, BC? Reach out — I'm happy to help.</p>
    </div>
    <div class="contact-grid" style="margin-top:32px">
      <div class="contact-item"><div class="icon">{I["mail"]}</div><div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
      <div class="contact-item"><div class="icon">{I["phone"]}</div><div><small>Call or text</small><a href="{TEL}">{PHONE}</a></div></div>
      <div class="contact-item"><div class="icon">{I["pin"]}</div><div><small>Service area</small><span>Greater Vancouver · Tri-Cities, BC</span></div></div>
      <div class="contact-item"><div class="icon">{I["building"]}</div><div><small>Brokerage</small><span>Axford Real Estate</span><br><span>{BROKERAGE_ADDR}</span></div></div>
    </div>
    <div class="btn-row" style="justify-content:center;margin-top:36px">
      <a class="btn btn-light" href="{TEL}">Call {PHONE}</a>
      <a class="btn btn-ghost-light" href="mailto:{EMAIL}">Email Devin</a>
      <a class="btn btn-ghost-light" href="buyers.html#listings">Get listings sent to me</a>
      <a class="btn btn-ghost-light" href="tenants.html#intake">Start a rental search</a>
    </div>
  </div>
</section>
'''
home += foot()

# ---------------- BUYERS ----------------
AREAS = ["Coquitlam","Port Coquitlam","Port Moody","Anmore / Belcarra","Burnaby","New Westminster","Pitt Meadows / Maple Ridge","Other (add in notes)"]
def area_checks(name):
    return "".join(f'<label><input type="checkbox" name="{name}" value="{a}"> {a}</label>' for a in AREAS)
PRICES = ["No minimum","$400,000","$500,000","$600,000","$700,000","$800,000","$900,000","$1,000,000","$1,250,000","$1,500,000","$1,750,000","$2,000,000","$2,500,000","$3,000,000+"]
def opts(lst, first=None):
    o = f'<option value="">{first}</option>' if first else ""
    return o + "".join(f'<option>{x}</option>' for x in lst)

hoods = [
 ("Coquitlam","The largest of the Tri-Cities, BC",
  "A big, varied city stretching from established neighbourhoods near the Fraser River up to newer hillside communities on Burke Mountain and Westwood Plateau. Coquitlam's City Centre has grown into a hub around Coquitlam Centre, Lafarge Lake and Town Centre Park, with SkyTrain's Millennium Line running through the city.",
  ["Burke Mountain","Westwood Plateau","City Centre","Burquitlam","Austin Heights","Maillardville","Ranch Park","Eagle Ridge"],
  "Millennium Line SkyTrain (Burquitlam, Lincoln, Coquitlam Central, Lafarge Lake–Douglas) and West Coast Express at Coquitlam Central; Lougheed Highway and Highway 1 nearby.",
  "Mundy Park, Lafarge Lake & Town Centre Park, Como Lake, and trails on Westwood Plateau and Burke Mountain."),
 ("Port Coquitlam","Riverside community with a small-town feel",
  "“PoCo” sits between the Coquitlam and Pitt rivers, with a walkable downtown, family-friendly residential neighbourhoods and the Traboulay PoCo Trail looping around the city. It's also Terry Fox's hometown — and where I play soccer.",
  ["Downtown PoCo","Citadel Heights","Mary Hill","Oxford Heights","Lincoln Park","Riverwood","Birchland Manor","Glenwood"],
  "West Coast Express at Port Coquitlam station; Lougheed Highway and the Mary Hill Bypass connect to the rest of the region.",
  "Traboulay PoCo Trail, Coquitlam River and Pitt River dikes, and plenty of community sports fields."),
 ("Port Moody","Waterfront “City of the Arts”",
  "Set at the eastern end of Burrard Inlet, Port Moody combines a waterfront lifestyle with forested hillsides. Rocky Point Park, the Shoreline Trail and the craft breweries along Murray Street's “Brewers Row” are local favourites.",
  ["Moody Centre","Inlet Centre / Suter Brook","Newport Village","Heritage Mountain","Heritage Woods","College Park","Glenayre","Ioco"],
  "Millennium Line SkyTrain (Moody Centre, Inlet Centre) and West Coast Express at Moody Centre.",
  "Rocky Point Park, the Shoreline Trail, Old Orchard Park, and quick access to Belcarra and Buntzen Lake."),
 ("Anmore & Belcarra","Quiet villages north of Port Moody",
  "Two small, semi-rural villages tucked into the forest above Port Moody. Homes here tend to sit on larger, treed lots, and residents trade some convenience for privacy and nature on their doorstep.",
  ["Village of Anmore","Village of Belcarra"],
  "Mostly car-dependent; Port Moody's SkyTrain and West Coast Express stations are the nearest rapid transit.",
  "Buntzen Lake, Belcarra Regional Park and Sasamat Lake (White Pine Beach)."),
]
hood_cards = ""
for name,tag,desc,nbhd,transit,outdoors in hoods:
    hood_cards += f'''<article class="card hood">
  <div class="hood-head"><h3>{name}</h3><small>{tag}</small></div>
  <div class="hood-body">
    <p>{desc}</p>
    <h4>Neighbourhoods to know</h4>
    <ul class="tags">{"".join(f"<li>{n}</li>" for n in nbhd)}</ul>
    <h4>Getting around</h4>
    <p>{transit}</p>
    <h4>Outdoors</h4>
    <p>{outdoors}</p>
    <h4>Devin's take</h4>
    <p>{ph(f"Devin's personal insight on {name} — who it suits, favourite spots, what buyers should know")}</p>
  </div>
</article>'''

buyers = head("Buying a Home in the Tri-Cities, BC | Devin Desaulniers, Axford Real Estate",
              "Neighbourhood guides for Coquitlam, Port Coquitlam, Port Moody and nearby areas, a free mortgage affordability calculator, and personalised listing alerts from Devin Desaulniers, Axford Real Estate.", "buyers", page_url="buyers.html")
buyers += f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">For buyers</span>
    <h1>Buying in the Tri-Cities, BC &amp; Greater Vancouver</h1>
    <p class="lead">Local neighbourhood knowledge, listings matched to what you actually want, and a clear plan from your first showing to getting the keys.</p>
    <div class="btn-row" style="margin-top:22px">
      <a class="btn btn-light" href="#listings">Send me listings {I["arrow"]}</a>
      <a class="btn btn-ghost-light" href="{CALC}" target="_blank" rel="noopener">Mortgage calculator {I["ext"]}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">{calc_cta("Start with your budget","Before you fall in love with a listing, get a feel for your price range with my free mortgage affordability calculator. Then talk to a lender about pre-approval.")}</div>
</section>

<section class="section section--grey" style="padding-top:56px">
  <div class="container">
    <div class="grid grid-2" style="align-items:start">
      <div>
        <span class="eyebrow">Working together</span>
        <h2>How I help buyers</h2>
        <div class="buyer-intro">
          {picture("assets/img/devin-bw",(420,720),720,951,"Devin Desaulniers","bw-photo",sizes_attr="(max-width: 639px) 40vw, 200px")}
          <div>
            <p class="lead">Buying is a big decision. My job is to keep you informed and represent your interests at every step.</p>
            <p>Call or text <a href="{TEL}">{PHONE}</a>, or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
          </div>
        </div>
        <p>{ph("Confirm or edit this list of buyer services")}</p>
      </div>
      <ul class="list-check card" style="margin:0">
        <li>Understand your goals, budget and must-haves</li>
        <li>Set up listing alerts for the areas and homes you're interested in</li>
        <li>Book and attend showings, and point out what to look for</li>
        <li>Review comparable sales so you can make an informed offer</li>
        <li>Prepare and negotiate your offer, including subjects like financing and inspection</li>
        <li>Guide you through subject removal, deposits and completion</li>
      </ul>
    </div>
  </div>
</section>

{testimonials_section(["thurza","florian","tyson","kyron"], "What buyers say", lead="Buyers I've helped, in their own words.", sec_id="testimonials", bg="section--tint")}

<section class="section" id="neighbourhoods">
  <div class="container">
    <div class="center narrow">
      <span class="eyebrow">Neighbourhood guides</span>
      <h2>Get to know the Tri-Cities, BC</h2>
      <p class="lead">A quick introduction to the communities I know best. Every street is different — reach out and I'll help you compare areas based on your commute, lifestyle and budget.</p>
    </div>
    <div class="grid grid-2" style="margin-top:32px">{hood_cards}</div>

    <div class="card" style="margin-top:22px">
      <h3>Other nearby areas</h3>
      <p>I also help buyers in neighbouring Greater Vancouver communities, including <strong>Burnaby</strong>, <strong>New Westminster</strong>, and <strong>Pitt Meadows &amp; Maple Ridge</strong>. School District 43 serves Coquitlam, Port Coquitlam, Port Moody, Anmore and Belcarra — always confirm school catchments with the district for a specific address.</p>
      <p>{ph("Any other areas Devin wants to feature, and his notes on them")}</p>
    </div>
  </div>
</section>

<section class="section section--grey" id="listings">
  <div class="container">
    <div class="center narrow">
      <span class="eyebrow">Personalised listing alerts</span>
      <h2>Send me listings</h2>
      <p class="lead">Tell me what you're looking for and I'll send you homes that match — including new listings as they hit the market.</p>
    </div>
    <form class="form-card" style="margin-top:28px" data-form-key="buyerListings" action="#" method="POST">
      <input type="hidden" name="_subject" value="New buyer listings request">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="form" value="Buyer: Send me listings">
      <div class="hp" aria-hidden="true"><label>Leave this field empty <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
      <div class="form-grid cols-2">
        <div class="field"><label for="b-name">Full name <span class="req">*</span></label><input id="b-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="b-email">Email <span class="req">*</span></label><input id="b-email" name="email" type="email" autocomplete="email" required></div>
        <div class="field"><label for="b-phone">Phone</label><input id="b-phone" name="phone" type="tel" autocomplete="tel"></div>
        <div class="field"><label for="b-type">Property type</label><select id="b-type" name="property_type">{opts(["Any","Condo / apartment","Townhouse","Detached house","Half duplex / duplex"],None)}</select></div>
        <fieldset class="field full"><legend>Areas of interest <span class="hint">(choose any)</span></legend><div class="checks">{area_checks("areas")}</div></fieldset>
        <div class="field"><label for="b-min">Price range — minimum</label><select id="b-min" name="price_min">{opts(PRICES[:-1])}</select></div>
        <div class="field"><label for="b-max">Price range — maximum</label><select id="b-max" name="price_max">{opts(["No maximum"]+PRICES[2:])}</select></div>
        <div class="field"><label for="b-beds">Bedrooms (min.)</label><select id="b-beds" name="bedrooms">{opts(["Any","Studio","1+","2+","3+","4+","5+"])}</select></div>
        <div class="field"><label for="b-baths">Bathrooms (min.)</label><select id="b-baths" name="bathrooms">{opts(["Any","1+","1.5+","2+","2.5+","3+"])}</select></div>
        <div class="field"><label for="b-timeline">Timeline</label><select id="b-timeline" name="timeline">{opts(["As soon as possible","Within 3 months","3–6 months","6–12 months","12+ months / just exploring"],"Select…")}</select></div>
        <div class="field"><label for="b-pre">Mortgage pre-approved?</label><select id="b-pre" name="pre_approved">{opts(["Yes","In progress","Not yet","Paying cash / not needed"],"Select…")}</select></div>
        <div class="field full"><label for="b-notes">Anything else? <span class="hint">(must-haves, school catchment, parking, commute…)</span></label><textarea id="b-notes" name="notes"></textarea></div>
        {consent("b")}
        {status_box()}
      </div>
    </form>
  </div>
</section>
'''
buyers += foot()

# ---------------- TENANTS (standalone landing page) ----------------
import html as _html, re as _re, json as _json
TEN_TITLE = "Relocating to Vancouver? Rental Help for Tenants | Devin Desaulniers"
TEN_DESC = "Moving to Vancouver or the Tri-Cities, BC? Get local rental help: consultation, property search with early access, in-person or virtual showings, and lease review & negotiation. $1,500 + GST, paid in two parts."

FAQ_ITEMS = [
 ("Who can help me find a rental in Vancouver if I'm moving from out of province?",
  "<p>I can. I'm Devin Desaulniers, a Real Estate Associate with Axford Real Estate in Port Moody. I help people relocating to Greater Vancouver line up a rental on the <strong>tenant side</strong> before they arrive — in Vancouver, Burnaby, New Westminster and the Tri-Cities, BC (Coquitlam, Port Coquitlam and Port Moody). I search for rentals that fit your budget and commute, arrange and attend showings, do live video walkthroughs and share floor plans when you're not here yet, negotiate on your behalf, and review the lease with you before you sign.</p>"),
 ("Can you help me find a rental before I move?",
  "<p>Yes — you don't have to wait until you land. I shortlist rentals and view them for you. When you can't make it, I do a virtual showing with a live video walkthrough, so you can see the home and ask questions from wherever you are, and I share floor plans for the homes you're seriously considering. If you're in town, I'll attend showings with you and, when practical, drive us between appointments. We also go through the lease together, so you're not wiring money to a scam listing from another province.</p>"),
 ("How much does it cost, and who pays?",
  "<p>The service fee is <strong>$1,500 total + GST</strong>, paid by you, the tenant, in two parts: <strong>$750</strong> at the beginning of our engagement and <strong>$750</strong> once you successfully secure a rental.</p>"),
 ("When do I pay?",
  "<p>$750 (+ GST) at the beginning of the engagement, and the remaining $750 (+ GST) once you successfully secure a rental.</p>"),
 ("What's included?",
  "<p>Four things: a personalized consultation (including green flags and red flags to watch for), a property search with early access to rental opportunities, booking and attending showings (or virtual showings with live video walkthroughs and floor plans when you can't make it), and lease review &amp; negotiation.</p>"),
 ("Where do you find rentals?",
  "<p>I search Facebook Marketplace, Craigslist and other rental sources. Through Axford Real Estate I also have access to our own rental opportunities and firsthand relationships with the property managers in our office.</p>"),
 ("How far ahead of my move should I reach out?",
  "<p>Most Greater Vancouver rentals come on the market only a few weeks before they're available, so the active search usually starts about <strong>4 to 6 weeks</strong> before your move-in date. Use the weeks before that to settle your budget, neighbourhoods, commute needs and documents (ID, proof of income, references). Once you're inside that window, I can move quickly on new listings.</p>"),
 ("What should I have ready to apply for a rental?",
  '<p>Landlords and property managers look for a complete, verifiable application: <strong>photo ID</strong> (a clear, unexpired government-issued ID); <strong>proof of income</strong> (usually 2–3 recent pay stubs, an employment letter, or a contract or offer letter — or, if you\'re self-employed, recent bank statements and/or a Notice of Assessment); <strong>references</strong> from previous landlords and/or employers; sometimes a <strong>credit report</strong>, which you can get yourself (e.g. from Equifax or TransUnion) to speed things up; and a short <strong>renter profile</strong> (who will live there, your move-in date, pets and what you\'re looking for). I can help you organize it. The full checklist is in my free <a href="#resources">Greater Vancouver renter\'s guide</a>.</p>'),
 ("Do you cover the Tri-Cities, BC and the rest of Greater Vancouver, or only Vancouver?",
  '<p>Both — I search across Greater Vancouver. I work in Port Moody, so the Tri-Cities, BC (Coquitlam, Port Coquitlam and Port Moody) are an area I know especially well, but most of my rental searches cover the wider region: Vancouver, Burnaby, New Westminster and beyond. Tell me your commute (SkyTrain, West Coast Express or driving), budget and must-haves, and I\'ll focus the search where it makes sense for you. Moving to Greater Vancouver? Read my <a href="relocating-to-greater-vancouver.html">Relocating to Greater Vancouver guide</a>.</p>'),
 ("How do I avoid rental scams when I'm still out of town?",
  "<p>Never send a deposit before the unit and the landlord (or their licensed agent or property manager) are verified. Be wary of below-market listings that seem too good to be true, landlords who refuse showings, and requests to wire money to “hold” a unit. Get a written tenancy agreement and do a move-in condition inspection. I can view the unit in person, or on a live video walkthrough with you, before you commit.</p>"),
 ("Can you help with pets, parking or commute needs?",
  "<p>Yes. In our consultation we go over your budget, preferred areas, timing, commute, lifestyle and must-haves, and I focus the search on rentals that fit.</p>"),
 ("What if we don't find a place that works?",
  "<p>The first $750 covers the consultation, search and showings, and is non-refundable. The second $750 is only due once you successfully secure a rental, so if no rental is secured, it isn't owed.</p>"),
 ("Do you work for the landlord?",
  f"<p>No — this is a tenant representation service. I represent you, and you pay my fee. {ph('disclosure wording when the rental is one of Axford’s own listings / managed by Axford property managers — confirm with managing broker')}</p>"),
 ("What's the difference between tenant-side rental help and a property management company?",
  "<p>Property managers usually represent the <strong>landlord</strong> and lease out the buildings they manage. I work on the <strong>tenant side</strong>: I represent your search, not a landlord's inventory. Axford also has a separate property management business; my service is different — it's tenant-paid relocation rental help, and I don't manage rental properties myself.</p>"),
]
def _plain(h):
    return _re.sub(r"\s+", " ", _html.unescape(_re.sub(r"<[^>]+>", "", h))).strip()
faq_html = "".join(f'<div class="faq-item"><h3>{q}</h3><div class="ans">{a}</div></div>' for q, a in FAQ_ITEMS)
FAQ_JSONLD = '<script type="application/ld+json">\n' + _json.dumps({
    "@context": "https://schema.org", "@type": "FAQPage",
    "mainEntity": [{"@type": "Question", "name": _plain(q), "acceptedAnswer": {"@type": "Answer", "text": _plain(a)}} for q, a in FAQ_ITEMS]
}, indent=2, ensure_ascii=False) + '\n</script>'
tenants = head(TEN_TITLE, TEN_DESC, "tenants", og_image="assets/img/og-tenants.png", page_url="tenants.html", body_class="has-sticky", extra_head=FAQ_JSONLD)
STEP1 = f"""<div class="form-grid">
  <div class="field"><label for="t-name">Full name <span class="req">*</span></label><input id="t-name" name="name" autocomplete="name" required></div>
  <div class="field"><label for="t-email">Email <span class="req">*</span></label><input id="t-email" name="email" type="email" autocomplete="email" required></div>
  <div class="field"><label for="t-phone">Phone <span class="hint">(incl. country code if outside Canada)</span></label><input id="t-phone" name="phone" type="tel" autocomplete="tel"></div>
  <div class="field"><label for="t-date">Target move-in date <span class="req">*</span></label><input id="t-date" name="move_date" type="date" required></div>
  <button type="button" class="btn btn-primary js-only" data-next-step style="width:100%">Next: your rental needs {I["arrow"]}</button>
</div>"""
STEP2 = f"""<div class="form-grid" data-step2>
  <div class="field"><label for="t-contact">Best way to reach you</label><select id="t-contact" name="preferred_contact">{opts(["Email","Phone call","Text message","Video call"])}</select></div>
  <div class="field"><label for="t-from">Moving from <span class="hint">(city, province/country)</span></label><input id="t-from" name="moving_from"></div>
  <div class="field"><label for="t-budget">Monthly rent budget (CAD)</label><input id="t-budget" name="budget" placeholder="e.g. $2,500–$3,000"></div>
  <div class="field"><label for="t-beds">Bedrooms</label><select id="t-beds" name="bedrooms">{opts(["Studio","1 bedroom","1 bedroom + den","2 bedrooms","3 bedrooms","4+ bedrooms","Flexible"],"Select…")}</select></div>
  <fieldset class="field"><legend>Preferred areas <span class="hint">(choose any)</span></legend><div class="checks">{area_checks("areas")}</div></fieldset>
  <div class="field"><label for="t-pets">Pets?</label><select id="t-pets" name="pets">{opts(["No pets","Cat(s)","Dog(s)","Cat(s) and dog(s)","Other"],"Select…")}</select></div>
  <div class="field"><label for="t-petdetails">Pet details <span class="hint">(number, size, breed)</span></label><input id="t-petdetails" name="pet_details"></div>
  <div class="field"><label for="t-work">Work / school location <span class="hint">(helps plan around your commute)</span></label><input id="t-work" name="work_school_location"></div>
  <div class="field"><label for="t-notes">Notes <span class="hint">(lease length, parking, furnished, must-haves…)</span></label><textarea id="t-notes" name="notes"></textarea></div>
  {consent("t")}
  {status_box()}
</div>"""

tenants += f"""
<section class="lp-hero">
  <div class="container lp-hero-inner">
    <div>
      <span class="eyebrow">Tenant representation<span class="eb-more"> · Greater Vancouver rental guidance</span></span>
      <h1>Relocating to Vancouver? Line up your rental before you arrive.</h1>
      <p class="lead">Moving to Vancouver is a lot to manage from a distance. I'll search, attend showings (or walk you through on live video), and review and negotiate your lease — so you can rent with confidence.</p>
      <div class="price-pill"><b>$1,500</b><span>+ GST · paid in two parts</span></div>
      <ul class="list-check">
        <li>Personalized consultation</li>
        <li>Search + early access</li>
        <li>In-person or virtual showings</li>
        <li>Lease review &amp; negotiation</li>
      </ul>
      <div class="btn-row">
        <a class="btn btn-light" href="#intake">Start your rental search {I["arrow"]}</a>
        <a class="btn btn-ghost-light" href="{TEL}">{I["phone"]} Call {PHONE}</a>
      </div>
      <a class="hero-res-link" href="#resources">{I["doc"]} Free download: my Greater Vancouver renter's guide (PDF)</a>
      <div class="trust-row">
        <span>{I["key"]} Licensed since 2020</span>
        <span>{I["pin"]} 28 years living in Greater Vancouver</span>
        <span>{I["building"]} Axford Real Estate</span>
      </div>
    </div>
    <form class="lp-quick" id="intake" data-form-key="tenantIntake" action="#" method="POST">
      <input type="hidden" name="_subject" value="New relocation rental intake">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="form" value="Tenant: Relocation rental intake">
      <div class="hp" aria-hidden="true"><label>Leave this field empty <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
      <h2>Start your rental search</h2>
      <p>Takes about 2 minutes. No obligation — I'll get back to you to talk next steps. Prefer to talk? <a href="{TEL}">{PHONE}</a></p>
      {STEP1}
      <div class="step2-wrap" data-step2-wrap>
        <hr style="border:0;border-top:1px solid #e6eaef;margin:18px 0">
        <h3 style="margin-bottom:12px">Your rental needs</h3>
        {STEP2}
      </div>
    </form>
  </div>
</section>

<section class="section" id="included">
  <div class="container">
    <div class="center narrow">
      <span class="eyebrow">My services</span>
      <h2>Someone on your side, from first search to move-in</h2>
      <p class="lead">Searching for a rental from out of town is stressful. I represent you, the tenant, so you can make an informed decision without flying in for every viewing.</p>
    </div>
    <div class="grid grid-2" style="margin-top:28px">
      <div class="card"><div class="icon">{I["handshake"]}</div><h3>Personalized consultation</h3><p style="margin:0">I'll help you identify rentals that fit your budget, commute, lifestyle and priorities. I also point out potential green flags and red flags, so you can make a more informed decision and avoid unnecessary uncertainty.</p></div>
      <div class="card"><div class="icon">{I["home"]}</div><h3>Property search &amp; early access</h3><p style="margin:0">I search Facebook Marketplace, Craigslist and other rental sources. Through Axford Real Estate, I also have access to our own rental opportunities and firsthand relationships with the property managers in our office.</p></div>
      <div class="card"><div class="icon">{I["video"]}</div><h3>Showings — in person or virtual</h3><p style="margin:0">I book and coordinate showings and attend with you. When you can't make it, I do virtual showings with a live video walkthrough, plus floor plans for the homes you're seriously considering. When practical, I can also drive us between scheduled appointments.</p></div>
      <div class="card"><div class="icon">{I["doc"]}</div><h3>Lease review &amp; negotiation</h3><p style="margin:0">We review the lease agreement together. I explain the important terms, talk through move-in and move-out expectations, and negotiate rent or other lease terms where appropriate.</p></div>
    </div>
    <div class="fee-block" style="margin-top:28px">
      <div class="fee-main">
        <span class="eyebrow" style="color:#cfe0f3">Service fee</span>
        <div class="fee-total">$1,500 <small>total + GST</small></div>
        <p>Paid by the tenant, in two parts.</p>
      </div>
      <ul class="fee-parts">
        <li><b>$750</b><span>at the beginning of the engagement (non-refundable)</span></li>
        <li><b>$750</b><span>once you successfully secure a rental</span></li>
      </ul>
      <a class="btn btn-light" href="#intake">Start your search {I["arrow"]}</a>
    </div>
    <p class="form-note center" style="margin-top:14px">I help tenants find and lease a home. I do not provide property management services.</p>
  </div>
</section>

{testimonials_section(["susan","hugo","aline"], "What renters say", lead="Tenants I've helped find a home, in their own words.", featured="susan", sec_id="testimonials", bg="section--tint")}

<section class="section section--grey" id="how">
  <div class="container">
    <div class="center narrow">
      <span class="eyebrow">How I can help</span>
      <h2>How it works</h2>
      <p class="lead">Five simple steps, built around your move date.</p>
    </div>
    <ol class="mini-steps five" style="margin-top:28px">
      <li><div><h3>Initial consultation</h3><p>We discuss your budget, preferred areas, timing and must-haves.</p></div></li>
      <li><div><h3>Property search</h3><p>I identify suitable rentals and help you screen opportunities.</p></div></li>
      <li><div><h3>Showings</h3><p>I coordinate and attend showings with you, or provide virtual showings.</p></div></li>
      <li><div><h3>Lease review &amp; negotiation</h3><p>I explain the key terms and negotiate where possible.</p></div></li>
      <li><div><h3>Move in</h3><p>I help you understand the next steps and what to expect at move-in.</p></div></li>
    </ol>
    <div class="center" style="margin-top:28px"><a class="btn btn-primary" href="#intake">Start your rental search {I["arrow"]}</a></div>
  </div>
</section>


<section class="section" id="resources">
  <div class="container">
    <div class="center narrow">
      <span class="eyebrow">Free renter resources</span>
      <h2>Download my renter brochures</h2>
      <p class="lead">Two free PDFs: a practical guide to renting in Greater Vancouver, and a two-page overview of how my tenant representation service works.</p>
    </div>
    <div class="brochures">
      <article class="brochure">
        <a class="cover" href="assets/docs/devin-desaulniers-renter-resources.pdf" target="_blank" rel="noopener" aria-label="Open the Greater Vancouver Renter's Guide (PDF)">{picture("assets/img/brochure-renter-resources",(320,640),640,853,"Cover of Devin Desaulniers' 2026 Greater Vancouver Renter's Guide","",sizes_attr="(max-width: 999px) 120px, 150px")}</a>
        <div>
          <h3>Your Greater Vancouver Renter's Guide (2026)</h3>
          <p>Search smarter, apply stronger and move in with confidence.</p>
          <ul>
            <li>Build the real monthly budget and compare rental types</li>
            <li>Greater Vancouver area snapshot</li>
            <li>Your application package and what to check at a viewing</li>
            <li>B.C. tenancy essentials and protecting yourself after move-in</li>
          </ul>
          <div class="meta">PDF · 4 pages · 0.8 MB</div>
          <a class="btn btn-primary" href="assets/docs/devin-desaulniers-renter-resources.pdf" target="_blank" rel="noopener">View / download PDF {I["arrow"]}</a>
        </div>
      </article>
      <article class="brochure">
        <a class="cover" href="assets/docs/devin-desaulniers-tenant-representation.pdf" target="_blank" rel="noopener" aria-label="Open the Tenant Representation brochure (PDF)">{picture("assets/img/brochure-tenant-representation",(320,640),640,828,"Cover of Devin Desaulniers' Tenant Representation brochure","",sizes_attr="(max-width: 999px) 120px, 150px")}</a>
        <div>
          <h3>Tenant Representation brochure</h3>
          <p>How my tenant-side rental service works, on two pages.</p>
          <ul>
            <li>About me and the 5-step process</li>
            <li>My four services, from consultation to lease review</li>
            <li>The service fee: $1,500 total + GST, in two parts</li>
          </ul>
          <div class="meta">PDF · 2 pages · 0.5 MB</div>
          <a class="btn btn-primary" href="assets/docs/devin-desaulniers-tenant-representation.pdf" target="_blank" rel="noopener">View / download PDF {I["arrow"]}</a>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0;padding-bottom:0">
  <div class="container">
    <a class="guide-callout" href="relocating-to-greater-vancouver.html">
      <span class="gc-icon">{I["pin"]}</span>
      <span><b>Moving to Greater Vancouver?</b> Read my Relocating to Greater Vancouver guide — areas at a glance, commuting, renting basics in B.C., and whether to rent or buy first.</span>
      <span class="gc-arrow">{I["arrow"]}</span>
    </a>
  </div>
</section>

<section class="section">
  <div class="container about-grid" style="align-items:center">
    <div>
      <span class="eyebrow">Your local on the ground</span>
      <h2>Hi, I'm Devin.</h2>
      <p>I've lived in the Greater Vancouver area for 28 years. I work in Port Moody, and I play soccer on a Port Coquitlam team and pickleball around the Tri-Cities, BC. I know this region as a local — so I can tell you what a neighbourhood is actually like, not just what the listing says.</p>
      <p>For the last seven years I've been helping people relocate to and from Vancouver. I've been licensed in real estate since 2020, and today I'm a Real Estate Associate with <strong>Axford Real Estate</strong>.</p>
      <p><a href="{TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="index.html#about">More about me</a> · <a href="relocating-to-greater-vancouver.html">Moving to Greater Vancouver?</a></p>
      {social_row("Look me up")}
    </div>
    <div class="hero-card" style="max-width:320px">
      {picture("assets/img/devin-headshot",(480,800),800,1000,"Devin Desaulniers, Real Estate Associate with Axford Real Estate","headshot",eager="auto",sizes_attr="(max-width: 899px) 80vw, 320px")}
      <div class="who"><strong>Devin Desaulniers</strong><span>Real Estate Associate · Axford Real Estate</span></div>
    </div>
  </div>
</section>

<section class="section section--grey" id="faq">
  <div class="container">
    <div class="center narrow">
      <span class="eyebrow">Questions</span>
      <h2>Frequently asked questions</h2>
    </div>
    <div class="faq-list">{faq_html}</div>
  </div>
</section>

<section class="section trust-badge-section" id="reviews">
  <div class="container center">
    <span class="eyebrow">My brokerage</span>
    <p class="tb-intro">I work with Axford Real Estate, one of Greater Vancouver's top-rated brokerages, based in Port Moody.</p>
    {google_badge()}
  </div>
</section>

<section class="section section--blue">
  <div class="container center narrow">
    <h2>Ready to find your next home?</h2>
    <p style="color:#dbe7f4">Please feel free to reach out at any time.</p>
    <div class="btn-row" style="justify-content:center;margin-top:20px">
      <a class="btn btn-light" href="#intake">Start your rental search {I["arrow"]}</a>
      <a class="btn btn-ghost-light" href="{TEL}">Call {PHONE}</a>
      <a class="btn btn-ghost-light" href="mailto:{EMAIL}?subject=Relocation%20rental%20service">Email Devin</a>
    </div>
  </div>
</section>

<div class="sticky-cta" data-sticky-cta>
  <div class="sc-text"><b>$1,500 + GST</b>Paid in two parts</div>
  <a class="sc-call" href="{TEL}" aria-label="Call Devin at {PHONE}">{I["phone"]}</a>
  <a class="btn btn-primary" href="#intake">Start search</a>
</div>
"""
tenants += foot()

# ---------------- RELOCATING TO GREATER VANCOUVER (guide) ----------------
GV_URL = "relocating-to-greater-vancouver.html"
GV_TITLE = "Relocating to Greater Vancouver | Moving & Rental Guide | Devin Desaulniers"
GV_DESC = "Moving to Greater Vancouver from another province? Areas at a glance, commuting, renting basics in B.C., renting vs buying first, and how Devin Desaulniers of Axford Real Estate helps relocating tenants and buyers."
RTB = "https://www2.gov.bc.ca/gov/content/housing-tenancy/residential-tenancies"
GV_FAQ = [
 ("Who can help me relocate to Greater Vancouver from another province?",
  "<p>I can. I'm Devin Desaulniers, a Real Estate Associate with Axford Real Estate in Port Moody. I've lived in the Greater Vancouver area for 28 years, I've been licensed since 2020, and for the last seven years I've been helping people relocate to and from Vancouver — as tenants who need a rental lined up before they arrive, or as buyers.</p>"),
 ("Should I rent or buy first when moving to Greater Vancouver?",
  "<p>It depends on your timeline, down payment and how sure you are about areas. Some people rent for 6–12 months to learn the commute and the neighbourhoods, then buy. Others buy first if financing and timing are solid. I can help with either path — a tenant-side rental search or buyer representation — and I'll be honest about which fits your dates.</p>"),
 ("Which part of Greater Vancouver should I live in?",
  "<p>Start with your commute, budget and lifestyle. Vancouver suits people who want walkable, transit-rich neighbourhoods; Burnaby and New Westminster offer many condo options near SkyTrain; Richmond has the Canada Line and airport access; the North Shore suits outdoor lovers who can manage a bridge or SeaBus commute; the Tri-Cities, BC and Surrey/Langley offer more space. Tell me where you'll work or study and your hours, and I'll shortlist areas that match.</p>"),
 ("Can you help me find a rental in Greater Vancouver before I move?",
  '<p>Yes. That\'s the core of my tenant-side relocation rental service: I search across Greater Vancouver (in the areas we agree on), attend showings or do live video walkthroughs with floor plans, negotiate on your behalf and review the lease with you — so you\'re not wiring a deposit to a scam listing from out of province. <a href="tenants.html">See how the relocation rental service works</a>.</p>'),
 ("How much does tenant-side relocation rental help cost?",
  "<p><strong>$1,500 total + GST, paid by the tenant</strong>, in two parts: $750 at the beginning of the engagement (non-refundable) and $750 once you successfully secure a rental. It covers a personalized consultation, the property search, showings (in person or virtual), and lease review &amp; negotiation.</p>"),
 ("How far ahead should I contact an agent when relocating to Greater Vancouver?",
  "<p>For <strong>renting</strong>, settle your preferences early, then expect the active search about <strong>4–6 weeks</strong> before move-in, because most listings appear close to availability. For <strong>buying</strong>, reach out as soon as your move date and budget are roughly known — often 2–4+ months out — so we can watch inventory and get you lender-ready.</p>"),
 ("Do you only work in the Tri-Cities, BC?",
  "<p>No. I help tenants and buyers across Greater Vancouver. I work in Port Moody, so the Tri-Cities, BC — Coquitlam, Port Coquitlam and Port Moody — are an area I know especially well, and I regularly search Vancouver, Burnaby, New Westminster and other parts of the region. We'll define your search area up front.</p>"),
 ("How do I start working with Devin Desaulniers on a Greater Vancouver relocation?",
  f'<p>Call or text <a href="{TEL}">{PHONE}</a>, email <a href="mailto:{EMAIL}">{EMAIL}</a>, or message me through my <a href="{SOCIAL[0][1]}" target="_blank" rel="noopener">REALTOR.ca profile</a>. Share your move date, whether you\'re renting or buying, your budget and must-haves (beds, parking, pets, transit). Renting? You can also fill out the <a href="tenants.html#intake">rental search intake form</a>. I\'ll reply with next steps and a clear scope.</p>'),
]
gv_faq_html = "".join(f'<div class="faq-item"><h3>{q}</h3><div class="ans">{a}</div></div>' for q, a in GV_FAQ)
AREAS_GV = [
 ("Vancouver", "Transit-rich, walkable and diverse neighbourhoods, with a mix of older and newer rentals.", "SkyTrain: Expo, Millennium and Canada lines, plus frequent buses.", False),
 ("Burnaby + New Westminster", "Often good value, with many condo options close to SkyTrain.", "SkyTrain: Expo and Millennium lines.", False),
 ("Richmond", "Shopping and airport access, with many condo communities.", "Canada Line to downtown Vancouver and YVR.", False),
 ("North Shore", "North and West Vancouver: outdoor access, family-friendly neighbourhoods and a relaxed lifestyle.", "Lions Gate or Ironworkers Memorial bridge, or the SeaBus from Lonsdale Quay to Waterfront.", False),
 ("Tri-Cities, BC", "Coquitlam, Port Coquitlam and Port Moody: parks, trails and a mix of condos, townhomes and suites. I work in Port Moody and play soccer in Port Coquitlam, so this is the area I know especially well.", "Millennium Line (Evergreen Extension) and the weekday West Coast Express.", True),
 ("Surrey + Langley", "More space and newer rentals, with a wider range of prices — and longer commutes for some.", "Expo Line in Surrey; the Surrey–Langley SkyTrain extension is under construction.", False),
]
areas_gv_html = "".join(f'<div class="area-card{" highlight" if hl else ""}"><h3>{n}</h3><p>{d}</p><p class="transit">{t}</p></div>' for n, d, t, hl in AREAS_GV)

gv = head(GV_TITLE, GV_DESC, "guide", page_url=GV_URL)
gv += f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Relocation guide · Greater Vancouver</span>
    <h1>Relocating to Greater Vancouver? Here's how a local agent can help</h1>
    <p class="lead">Areas at a glance, commuting, renting basics in B.C., and how I help relocating tenants and buyers line up the right home before they arrive.</p>
    <div class="btn-row" style="margin-top:22px">
      <a class="btn btn-light" href="tenants.html#intake">Need a rental? Start here {I["arrow"]}</a>
      <a class="btn btn-ghost-light" href="{TEL}">{I["phone"]} Call or text {PHONE}</a>
    </div>
  </div>
</section>

<article class="guide">
<section class="section">
  <div class="container guide-intro">
    <div>
      <p class="lead" style="color:var(--ink)">I'm Devin Desaulniers, a Real Estate Associate with Axford Real Estate in Port Moody. I've lived in the Greater Vancouver area for 28 years, and for the last seven years I've been helping people relocate to and from Vancouver — as tenants who need a rental lined up before they arrive, or as buyers.</p>
      <p>If you're moving from another province (or from elsewhere in BC), the hard part is usually the same: you need honest advice about areas, a realistic commute and a place that works before your furniture shows up. This page is a plain-language overview of Greater Vancouver, plus how I can help.</p>
    </div>
    <div class="hero-card guide-photo">
      {picture("assets/img/devin-headshot",(480,800),800,1000,"Devin Desaulniers, Real Estate Associate with Axford Real Estate","headshot",eager="auto",sizes_attr="(max-width: 899px) 70vw, 280px")}
      <div class="who"><strong>Devin Desaulniers</strong><span>Real Estate Associate · Axford Real Estate</span></div>
    </div>
  </div>
</section>

<section class="section section--grey" id="areas">
  <div class="container narrow-wide">
    <h2>Greater Vancouver at a glance</h2>
    <p>Greater Vancouver is a collection of cities, each with its own feel, rents and commute. Here's a quick snapshot to start your shortlist:</p>
    <div class="area-grid">{areas_gv_html}</div>
    <h3 style="margin-top:28px">Getting around</h3>
    <p>TransLink runs SkyTrain, buses, the SeaBus and the West Coast Express commuter rail (weekday rush-hour service between Mission and Waterfront Station in downtown Vancouver). Driving times vary a lot by bridge and time of day, so tell me where you'll work or study and I'll factor the commute into every shortlist. Buying in the Tri-Cities, BC? See my <a href="buyers.html#neighbourhoods">neighbourhood guides</a>.</p>
  </div>
</section>

<section class="section" id="renting-basics">
  <div class="container narrow-wide">
    <h2>Renting in B.C.: the basics</h2>
    <p>A few rules and habits that protect you, especially when you're renting from out of province:</p>
    <ul class="list-check">
      <li><strong>Deposits are capped.</strong> A security deposit can be at most half of one month's rent, and a pet damage deposit (if applicable) at most another half month.</li>
      <li><strong>Rent increases are limited.</strong> Rent can go up only once every 12 months, by no more than the annual limit (2.3% for 2026, 2.2% for 2027), and your landlord must give three full months' written notice.</li>
      <li><strong>Do a move-in condition inspection</strong> with the landlord, document the existing condition and keep a copy of the report.</li>
      <li><strong>Get it in writing:</strong> rent, term, utilities, parking, pets, occupants and any special terms.</li>
      <li><strong>Verify before you pay.</strong> Confirm the property and the person you're dealing with before sending money, and be cautious of wire transfers, gift cards, cryptocurrency or pressure to pay before a viewing.</li>
    </ul>
    <h3 style="margin-top:24px">Have your application ready</h3>
    <p>Photo ID, proof of income (recent pay stubs, an employment or offer letter, or bank statements / a Notice of Assessment if you're self-employed), landlord and employer references, and a short renter profile. A credit report you get yourself can speed things up.</p>
    <p>The full checklist — budget, viewings, applications and move-in — is in my free <a href="tenants.html#resources">Greater Vancouver renter's guide (PDF)</a>.</p>
    <p class="form-note">General information only, not legal advice. Confirm current rules with the <a href="{RTB}" target="_blank" rel="noopener">B.C. Residential Tenancy Branch</a>.</p>
  </div>
</section>

<section class="section section--blue" id="rentals">
  <div class="container narrow-wide">
    <span class="eyebrow">Tenant-side rental help</span>
    <h2>How I help relocating tenants</h2>
    <p style="color:#dbe7f4">You don't have to wait until you land to secure a rental. My tenant-side relocation rental service is <strong style="color:#fff">$1,500 total + GST, paid by the tenant</strong> — $750 at the beginning of the engagement (non-refundable) and $750 once you successfully secure a rental. It includes:</p>
    <ul class="list-check">
      <li>A personalized consultation on your budget, commute, lifestyle and priorities, including green flags and red flags to watch for</li>
      <li>A rental search across Greater Vancouver, in the areas we agree on, with early access through Axford Real Estate's own rental opportunities</li>
      <li>Showings — I attend with you, or do live video walkthroughs with floor plans while you're still out of province</li>
      <li>Lease review &amp; negotiation before you sign</li>
    </ul>
    <p style="color:#dbe7f4">I represent your search on the tenant side — not a landlord's inventory. (Axford also has a separate property management business; this service is different.)</p>
    <p style="color:#dbe7f4">Most Greater Vancouver rentals list only a few weeks before they're available, so the active search usually starts about 4–6 weeks before move-in. Use the weeks before that to settle your budget, areas and documents.</p>
    <div class="btn-row" style="margin-top:20px">
      <a class="btn btn-light" href="tenants.html#intake">Start your rental search {I["arrow"]}</a>
      <a class="btn btn-ghost-light" href="tenants.html">See the relocation rental service</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container narrow-wide">
    <h2>How I help relocating buyers</h2>
    <p>For buyers moving to Greater Vancouver:</p>
    <ol class="mini-steps guide-steps">
      <li><div><h3>Pre-move planning</h3><p>Budget, an area shortlist, strata vs freehold trade-offs, and what good value actually looks like right now.</p></div></li>
      <li><div><h3>Remote-friendly search</h3><p>Video tours, floor plans and clear notes on condition, strata documents and comparable sales, so you're not flying blind from another province.</p></div></li>
      <li><div><h3>Offer strategy and negotiation</h3><p>Local market pace, subject clauses and timelines that fit a cross-province move.</p></div></li>
      <li><div><h3>Closing through move-in</h3><p>Coordination with your lawyer or notary, lender and movers so the handoff is calm.</p></div></li>
    </ol>
    <p style="margin-top:18px">Start with your budget using my free <a href="{CALC}" target="_blank" rel="noopener">mortgage affordability calculator</a>, then <a href="buyers.html#listings">ask me to send you listings</a>.</p>
    <p class="form-note">Office: Axford Real Estate, {BROKERAGE_ADDR}. Licensed since 2020.</p>
  </div>
</section>

<section class="section section--grey" id="faq">
  <div class="container">
    <div class="center narrow">
      <span class="eyebrow">FAQ</span>
      <h2>Relocating to Greater Vancouver: common questions</h2>
    </div>
    <div class="faq-list">{gv_faq_html}</div>
  </div>
</section>
</article>

<section class="section section--blue">
  <div class="container center narrow">
    <h2>Relocating to Greater Vancouver?</h2>
    <p style="color:#dbe7f4">I'm happy to help with a tenant-side rental search before you arrive, or as your buyer's agent.</p>
    <div class="btn-row" style="justify-content:center;margin-top:20px">
      <a class="btn btn-light" href="tenants.html#intake">Start a rental search {I["arrow"]}</a>
      <a class="btn btn-ghost-light" href="buyers.html#listings">Get listings sent to me</a>
      <a class="btn btn-ghost-light" href="{TEL}">Call or text {PHONE}</a>
      <a class="btn btn-ghost-light" href="mailto:{EMAIL}?subject=Relocating%20to%20Greater%20Vancouver">Email Devin</a>
    </div>
  </div>
</section>
"""
gv += foot()

# Old URL: tiny redirect so existing links keep working
NEW_ABS = SITE + GV_URL
redirect = f"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<title>Moved: Relocating to Greater Vancouver guide | Devin Desaulniers</title>
<meta name="robots" content="noindex, nofollow"><!-- redirect page: keep noindex so the old URL stays out of search -->
<link rel="canonical" href="{NEW_ABS}">
<meta http-equiv="refresh" content="0; url={GV_URL}">
<script>location.replace("{GV_URL}" + location.hash);</script>
</head>
<body>
<p>This guide has moved to <a href="{GV_URL}">Relocating to Greater Vancouver</a>.</p>
</body>
</html>
"""

for fn, html in [("index.html",home),("buyers.html",buyers),("tenants.html",tenants),(GV_URL,gv),("relocating-to-coquitlam.html",redirect)]:
    open(os.path.join(OUT,fn),"w").write(html)
print("built")
