import os
from partials import *
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I = ICONS

MOUNTAINS = '''<svg class="hero-mountains" viewBox="0 0 1440 220" preserveAspectRatio="none" aria-hidden="true">
<path d="M0 150 L120 90 L210 130 L330 50 L450 120 L560 70 L680 135 L800 60 L930 125 L1040 80 L1160 140 L1290 75 L1440 125 L1440 220 L0 220Z" fill="#3474b6" opacity=".10"/>
<path d="M0 175 L150 125 L260 160 L380 105 L520 165 L640 120 L770 170 L900 115 L1030 168 L1170 120 L1300 165 L1440 140 L1440 220 L0 220Z" fill="#808082" opacity=".14"/>
<path d="M0 200 C240 180 480 214 720 196 C960 178 1200 210 1440 192 L1440 220 L0 220Z" fill="#ffffff"/>
</svg>'''

# ---------------- HOME ----------------
home = head("Devin Desaulniers | Real Estate Associate, Axford Real Estate | Tri-Cities, BC",
            "Devin Desaulniers, Real Estate Associate with Axford Real Estate, helping buyers and relocating tenants in Coquitlam, Port Coquitlam, Port Moody and Greater Vancouver.", "home")
home += f'''
<section class="hero">
  <div class="container hero-inner">
    <div>
      <span class="eyebrow">Coquitlam · Port Coquitlam · Port Moody</span>
      <h1>Your Tri-Cities real estate <span class="accent">neighbour</span>.</h1>
      <p class="lead">I'm Devin Desaulniers, a Real Estate Associate with <strong>Axford Real Estate</strong>. I've lived in Coquitlam my whole life, and I help home buyers and relocating tenants across Greater Vancouver — especially here in the Tri-Cities.</p>
      <ul class="chips">
        <li>Licensed since 2020</li>
        <li>Lifelong Coquitlam resident</li>
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
      <h2>Local roots, Tri-Cities focus</h2>
      <p>I've lived in Coquitlam for all 28 years of my life, I work in Port Moody, and I play soccer on a Port Coquitlam team — so the Tri-Cities really are home. I love this area, and I know it as a resident, not just from a map.</p>
      <p>For the last seven years I've been helping people relocate to and from Vancouver, and I've been licensed in real estate since 2020. Today I'm a Real Estate Associate with Axford Real Estate, helping buyers and tenants across Greater Vancouver, with a particular focus on Coquitlam, Port Coquitlam and Port Moody.</p>
      <p>When I'm not working, you'll find me on the soccer pitch or a pickleball court somewhere around town.</p>
    </div>
    <div class="facts">
      <div class="fact"><b>2020</b><span>Licensed in real estate</span></div>
      <div class="fact"><b>28 years</b><span>Living in Coquitlam</span></div>
      <div class="fact"><b>7 years</b><span>Helping people relocate to &amp; from Vancouver</span></div>
      <div class="fact"><b>Port Moody</b><span>Where I work · Tri-Cities focus</span></div>
      <div class="fact" style="grid-column:1/-1"><b>Axford Real Estate</b><span>Brokerage · {ph("brokerage address")}</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">{calc_cta()}</div>
</section>

<section class="section section--blue" id="contact">
  <div class="container">
    <div class="narrow center">
      <span class="eyebrow">Get in touch</span>
      <h2>Let's talk about your move</h2>
      <p style="color:#dbe7f4">Buying, relocating, or just have a question about the Tri-Cities? Reach out — I'm happy to help.</p>
    </div>
    <div class="contact-grid" style="margin-top:32px">
      <div class="contact-item"><div class="icon">{I["mail"]}</div><div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
      <div class="contact-item"><div class="icon">{I["phone"]}</div><div><small>Phone</small><a href="{TEL}">{PHONE}</a></div></div>
      <div class="contact-item"><div class="icon">{I["pin"]}</div><div><small>Service area</small><span>Greater Vancouver · Tri-Cities, BC</span></div></div>
      <div class="contact-item"><div class="icon">{I["building"]}</div><div><small>Brokerage</small><span>Axford Real Estate</span><br>{ph("office address")}</div></div>
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
 ("Coquitlam","The largest of the Tri-Cities",
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

buyers = head("Buying a Home in the Tri-Cities | Devin Desaulniers, Axford Real Estate",
              "Neighbourhood guides for Coquitlam, Port Coquitlam, Port Moody and nearby areas, a free mortgage affordability calculator, and personalised listing alerts from Devin Desaulniers, Axford Real Estate.", "buyers")
buyers += f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">For buyers</span>
    <h1>Buying in the Tri-Cities &amp; Greater Vancouver</h1>
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
            <p>Call <a href="{TEL}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
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

<section class="section" id="neighbourhoods">
  <div class="container">
    <div class="center narrow">
      <span class="eyebrow">Neighbourhood guides</span>
      <h2>Get to know the Tri-Cities</h2>
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
TEN_TITLE = "Relocating to Vancouver? Rental Help for Tenants | Devin Desaulniers"
TEN_DESC = "Moving to Vancouver or the Tri-Cities? Get local rental help: consultation, property search with early access, in-person or virtual showings, and lease review & negotiation. $1,500 + GST, paid in two parts."
tenants = head(TEN_TITLE, TEN_DESC, "tenants", og_image="assets/img/og-tenants.png", page_url="tenants.html", body_class="has-sticky")
def faq(q, a):
    tag = ' <span class="ph" style="font-size:.75rem">needs Devin\'s input</span>' if "PLACEHOLDER" in a else ""
    return f'<details><summary>{q}{tag}</summary><div class="ans">{a}</div></details>'
faqs = "".join([
 faq("How much does it cost, and who pays?", "<p>The service fee is <strong>$1,500 total + GST</strong>, paid by you, the tenant, in two parts: <strong>$750</strong> at the beginning of our engagement and <strong>$750</strong> once you successfully secure a rental.</p>"),
 faq("What's included?", "<p>Four things: a personalized consultation (including green flags and red flags to watch for), a property search with early access to rental opportunities, booking and attending showings (or virtual showings when you can't make it), and lease review &amp; negotiation.</p>"),
 faq("Where do you find rentals?", "<p>I search Facebook Marketplace, Craigslist and other rental sources. Through Axford Real Estate I also have access to our own rental opportunities and firsthand relationships with the property managers in our office.</p>"),
 faq("When do I pay?", "<p>$750 (+ GST) at the beginning of the engagement, and the remaining $750 (+ GST) once you successfully secure a rental.</p>"),
 faq("What if we don't find a place that works?", f"<p>The second $750 is only due once you successfully secure a rental. {ph('whether any of the first $750 is refundable, and any time limit on the engagement')}</p>"),
 faq("Do I need to be in Vancouver to get started?", "<p>No. When you can't make it to a showing, I'll do a virtual showing — a live video walkthrough — so you can see the home and ask questions from wherever you are. If you're in town, I'll attend showings with you and, when practical, drive us between appointments.</p>"),
 faq("How far ahead of my move should I reach out?", f"<p>{ph('Devin’s recommended lead time before move-in date')}</p>"),
 faq("Which areas do you cover?", '<p>Greater Vancouver, with deep roots in the Tri-Cities — Coquitlam, Port Coquitlam and Port Moody. <a href="buyers.html#neighbourhoods">Read the neighbourhood guides</a>.</p>'),
 faq("Do you work for the landlord?", f"<p>No — this is a tenant representation service. I represent you, and you pay my fee. {ph('disclosure wording when the rental is one of Axford’s own listings / managed by Axford property managers — confirm with managing broker')}</p>"),
 faq("Can you help with pets, parking or commute needs?", "<p>Yes. In our consultation we go over your budget, preferred areas, timing, commute, lifestyle and must-haves, and I focus the search on rentals that fit.</p>"),
 faq("Do you offer property management?", "<p>No. I don’t manage rental properties — this service is for helping tenants find and lease a home.</p>"),
])
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
      <div class="trust-row">
        <span>{I["key"]} Licensed since 2020</span>
        <span>{I["pin"]} 28 years in Coquitlam</span>
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
        <li><b>$750</b><span>at the beginning of the engagement</span></li>
        <li><b>$750</b><span>once you successfully secure a rental</span></li>
      </ul>
      <a class="btn btn-light" href="#intake">Start your search {I["arrow"]}</a>
    </div>
    <p class="form-note center" style="margin-top:14px">I help tenants find and lease a home. I do not provide property management services.</p>
  </div>
</section>

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

<section class="section">
  <div class="container about-grid" style="align-items:center">
    <div>
      <span class="eyebrow">Your local on the ground</span>
      <h2>Hi, I'm Devin.</h2>
      <p>I've lived in Coquitlam for 28 years, I work in Port Moody, and I play soccer on a Port Coquitlam team and pickleball around the Tri-Cities. I love this area, and I know it as a local — so I can tell you what a neighbourhood is actually like, not just what the listing says.</p>
      <p>For the last seven years I've been helping people relocate to and from Vancouver. I've been licensed in real estate since 2020, and today I'm a Real Estate Associate with <strong>Axford Real Estate</strong>.</p>
      <p><a href="{TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="index.html#about">More about me</a></p>
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
    <div class="faq">{faqs}</div>
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

for fn, html in [("index.html",home),("buyers.html",buyers),("tenants.html",tenants)]:
    open(os.path.join(OUT,fn),"w").write(html)
print("built")
