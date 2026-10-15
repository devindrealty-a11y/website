import os, json
from partials import *
from partials import _TSTAR
import blog
import listings_page
import seo_pages
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I = ICONS

# ---------------- BLOG POSTS (Markdown in _posts/, see _build/BLOG.md) ----------------
POSTS = blog.load_posts()

def sec_head(eyebrow, heading, aside="", center=False):
    """Section heading: eyebrow + H2 on the left, optional lead/links on the right (stacks on mobile)."""
    aside_html = f'<div class="sec-head-aside">{aside}</div>' if aside else ""
    return (f'<div class="sec-head{" sec-head--center" if center else ""}">'
            f'<div><span class="eyebrow">{eyebrow}</span><h2>{heading}</h2></div>{aside_html}</div>')

def page_nav(items):
    links = "".join(f'<a href="#{a}">{t}</a>' for a, t in items)
    return f'<nav class="page-nav" aria-label="On this page"><div class="container"><span class="pn-label">On this page</span>{links}</div></nav>'

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

STARS5 = '<span class="stars" aria-hidden="true">' + _TSTAR * 5 + '</span>'
TOURS_LINK = f'<a class="link-arrow" href="videos.html">See all six video tours {I["arrow"]}</a>'
HOME_SERVICES_ASIDE = """<p class="lead">Whether you're buying, curious what your home would sell for, or moving to the Lower Mainland and need a rental, I'll make the process clear and manageable.</p>"""
HOME_PROCESS_ASIDE = """<p class="lead">Buying or renting, my job is to keep you informed and represent your interests at every step.</p>"""
HOME_TOURS_ASIDE = f"<p>{YT_NOTE} Press play to watch here.</p>{TOURS_LINK}"

home = head("Devin Desaulniers | Real Estate Associate, Axford Real Estate | Tri-Cities, BC",
            "Devin Desaulniers, Real Estate Associate with Axford Real Estate, helping buyers and relocating tenants in Coquitlam, Port Coquitlam, Port Moody and Greater Vancouver.", "home",
            extra_head=VIDEO_JSONLD + "\n" + blog.rss_link(""))
home += f'''
<section class="hero">
  <div class="container hero-inner">
    <div class="hero-copy">
      <span class="eyebrow"><span class="nw">Coquitlam ·</span> <span class="nw">Port Coquitlam ·</span> <span class="nw">Port Moody</span></span>
      <h1>Your <span class="nw">Tri-Cities, BC</span> real estate <em>neighbour</em>.</h1>
      <p class="lead">I'm Devin Desaulniers, a Real Estate Associate with <strong>Axford Real Estate</strong>. I've lived in the Greater Vancouver area for 28 years, and I help home buyers and relocating tenants across Greater Vancouver — especially here in the Tri-Cities, BC.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="buyers.html">I'm buying {I["arrow"]}</a>
        <a class="btn btn-outline" href="tenants.html">I'm relocating &amp; renting</a>
      </div>
      <p class="hero-call">{I["phone"]}<span>Prefer to talk? Call or text <a href="{TEL}">{PHONE}</a></span></p>
    </div>
  </div>
  <figure class="hero-photo">
    {picture("assets/img/devin-headshot",(480,800),800,1000,"Devin Desaulniers, Real Estate Associate with Axford Real Estate","hero-img",eager=True,sizes_attr="(max-width: 959px) 100vw, 46vw")}
    <figcaption><strong>Devin Desaulniers</strong><span>Real Estate Associate · Axford Real Estate</span></figcaption>
  </figure>
</section>

<section class="trust" aria-label="Devin at a glance">
  <div class="container">
    <ul class="trust-list">
      <li><span class="trust-k">28 years</span><span class="trust-v">living in Greater Vancouver</span></li>
      <li><span class="trust-k">Since 2020</span><span class="trust-v">licensed in real estate</span></li>
      <li><a href="{DEVIN_GBP}" target="_blank" rel="noopener" aria-label="Devin Desaulniers: {DEVIN_GBP_RATING} stars on Google from {DEVIN_GBP_COUNT} reviews (opens Google Maps in a new tab)"><span class="trust-k">{DEVIN_GBP_RATING} {STARS5}</span><span class="trust-v">on Google · {DEVIN_GBP_COUNT} reviews</span></a></li>
      <li><a href="{AXFORD_MAPS}" target="_blank" rel="noopener" aria-label="Axford Real Estate: {AXFORD_FIVE_STAR} five-star Google reviews (opens Google Maps in a new tab)"><span class="trust-k">{AXFORD_FIVE_STAR}</span><span class="trust-v">five-star Google reviews for Axford Real Estate</span></a></li>
    </ul>
  </div>
</section>

<section class="section" id="services">
  <div class="container">
    {sec_head("Services", "How I can help", HOME_SERVICES_ASIDE)}
    <div class="paths">
      <article class="path">
        <div class="path-top"><span class="path-icon">{I["home"]}</span><span class="path-label">For buyers</span></div>
        <h3>Buying a home</h3>
        <p>Neighbourhood guidance, listing alerts tailored to you, showings, and support with offers and negotiation from search to completion.</p>
        <a class="btn btn-primary" href="buyers.html">Buyer info &amp; neighbourhoods {I["arrow"]}</a>
      </article>
      <article class="path path--dark">
        <div class="path-top"><span class="path-icon">{I["key"]}</span><span class="path-label">For relocating tenants</span></div>
        <h3>Relocation rental service</h3>
        <p>Moving to Greater Vancouver? I represent tenants through the whole search: consultation, property search, in-person or virtual showings, and lease review &amp; negotiation — <strong>$1,500 + GST, paid by the tenant in two parts</strong>.</p>
        <a class="btn btn-light" href="tenants.html">See how it works {I["arrow"]}</a>
      </article>
    </div>
    <div class="offer-links">
      <a class="offer-link" href="home-evaluation.html">
        <span class="offer-link-k">Selling, or just curious</span>
        <span class="offer-link-t">Free home evaluation</span>
        <span class="offer-link-d">Send me your address and I'll email you a market evaluation.</span>
      </a>
      <a class="offer-link" href="buyer-opinion.html">
        <span class="offer-link-k">Looking at a property</span>
        <span class="offer-link-t">Get an expert opinion</span>
        <span class="offer-link-d">Send me the address and I'll email you my take on its value.</span>
      </a>
    </div>
  </div>
</section>

<section class="section section--paper video-section" id="video">
  <div class="container video-grid">
    <div class="video-copy">
      <span class="eyebrow">Relocation video</span>
      <h2>Moving to Greater Vancouver?</h2>
      <p class="lead">I help people relocating to Greater Vancouver find a rental, with in-person or virtual showings. Watch the video, then see how my relocation rental service works.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="tenants.html">See the relocation rental service {I["arrow"]}</a>
        <a class="btn btn-outline" href="{TEL}">Call or text {PHONE}</a>
      </div>
    </div>
    <div class="video-frame">
      <video controls playsinline preload="metadata" poster="{VIDEO_POSTER}" width="1280" height="720" aria-label="Moving to Greater Vancouver: relocation video presented by Devin Desaulniers, Real Estate Associate with Axford Real Estate" title="Moving to Greater Vancouver? Relocation video by Devin Desaulniers">
        <source src="{VIDEO_MP4}" type="video/mp4">
        <p>Your browser can't play this video. <a href="{VIDEO_MP4}">Download the relocation video (MP4)</a>.</p>
      </video>
    </div>
  </div>
</section>

<section class="section" id="process">
  <div class="container">
    {sec_head("How it works", "A clear process, whether you’re buying or renting", HOME_PROCESS_ASIDE)}
    <ol class="process">
      <li><span class="process-n" aria-hidden="true">01</span><h3>Consultation</h3><p>We talk through your budget, preferred areas, timing, commute and must-haves.</p></li>
      <li><span class="process-n" aria-hidden="true">02</span><h3>Search</h3><p>Listing alerts for buyers, and a rental search across Facebook Marketplace, Craigslist and other sources for tenants. I help you screen what comes up.</p></li>
      <li><span class="process-n" aria-hidden="true">03</span><h3>Showings</h3><p>I book and attend showings with you, or walk you through on live video when you can't be there.</p></li>
      <li><span class="process-n" aria-hidden="true">04</span><h3>Offer or lease</h3><p>Buying: I review comparable sales and negotiate your offer. Renting: we review the lease together and I negotiate where appropriate.</p></li>
    </ol>
  </div>
</section>

<section class="section section--night" id="tours">
  <div class="container">
    {sec_head("Video tours", "Property tours on my YouTube channel", HOME_TOURS_ASIDE)}
    {tours_grid(YT_HOME)}
  </div>
</section>

<section class="section section--paper" id="about">
  <div class="container about-grid">
    <figure class="about-photo">
      {picture("assets/img/devin-bw",(420,720),720,951,"Devin Desaulniers","bw-photo",sizes_attr="(max-width: 959px) 80vw, 440px")}
    </figure>
    <div class="about-copy">
      <span class="eyebrow">About Devin</span>
      <h2>Local roots, <span class="nw">Tri-Cities, BC</span> focus</h2>
      <p class="about-lead">I've lived in the Greater Vancouver area for 28 years, I work in Port Moody, and I play soccer on a Port Coquitlam team — so I know the Tri-Cities, BC especially well. I love this area, and I know it as a resident, not just from a map.</p>
      <p>For the last seven years I've been helping people relocate to and from Vancouver, and I've been licensed in real estate since 2020. Today I'm a Real Estate Associate with Axford Real Estate, helping buyers and tenants across Greater Vancouver, with a particular focus on Coquitlam, Port Coquitlam and Port Moody.</p>
      <p>When I'm not working, you'll find me on the soccer pitch or a pickleball court somewhere around town.</p>
      <ul class="facts">
        <li><b>2020</b><span>Licensed in real estate</span></li>
        <li><b>28 years</b><span>Living in the Greater Vancouver area</span></li>
        <li><b>7 years</b><span>Helping people relocate to &amp; from Vancouver</span></li>
        <li><b>Port Moody</b><span>Where I work · Tri-Cities, BC focus</span></li>
        <li class="fact-wide"><b>Axford Real Estate</b><span>Brokerage · {BROKERAGE_ADDR}</span></li>
      </ul>
      {social_row()}
    </div>
  </div>
</section>

{testimonials_section(["thurza","jackie","jordan","florian"], "What clients say", lead="Buyers and sellers I've worked with, in their own words.", featured="thurza", sec_id="testimonials", bg="")}

{blog.home_strip(POSTS)}

<section class="section section--calc">
  <div class="container">{calc_cta()}</div>
</section>

<section class="section contact" id="contact">
  <div class="container contact-grid">
    <div class="contact-copy">
      <span class="eyebrow">Get in touch</span>
      <h2>Let's talk about your move</h2>
      <p class="lead">Buying, relocating, or just have a question about the Tri-Cities, BC? Reach out — I'm happy to help.</p>
      <ul class="contact-list">
        <li><span class="cl-icon">{I["phone"]}</span><div><small>Call or text</small><a href="{TEL}">{PHONE}</a></div></li>
        <li><span class="cl-icon">{I["mail"]}</span><div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
        <li><span class="cl-icon">{I["pin"]}</span><div><small>Service area</small><span>Greater Vancouver · Tri-Cities, BC</span></div></li>
        <li><span class="cl-icon">{I["building"]}</span><div><small>Brokerage</small><span>Axford Real Estate<br>{BROKERAGE_ADDR}</span></div></li>
      </ul>
    </div>
    <div class="contact-actions">
      <div class="action-card action-card--dark">
        <h3>Talk it through</h3>
        <p>A quick call or text is usually the fastest way to sort out next steps.</p>
        <div class="btn-row">
          <a class="btn btn-light" href="{TEL}">{I["phone"]} Call {PHONE}</a>
          <a class="btn btn-ghost-light" href="mailto:{EMAIL}">Email Devin</a>
        </div>
      </div>
      <div class="action-card">
        <h3>Prefer a form?</h3>
        <p>Tell me what you're looking for and I'll follow up.</p>
        <div class="btn-row">
          <a class="btn btn-outline" href="buyers.html#listings">Get listings sent to me</a>
          <a class="btn btn-outline" href="home-evaluation.html">Free home evaluation</a>
          <a class="btn btn-outline" href="buyer-opinion.html">Get an expert opinion</a>
          <a class="btn btn-outline" href="tenants.html#intake">Start a rental search</a>
        </div>
      </div>
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
  "Mundy Park, Lafarge Lake & Town Centre Park, Como Lake, and trails on Westwood Plateau and Burke Mountain.",
  "Coquitlam is the largest of the Tri-Cities, BC, and one of the three cities I focus on. Buyers here are often choosing between a hillside area like Burke Mountain or Westwood Plateau and City Centre, and the commute is usually the deciding piece. Tell me where you'll be heading each day and we'll compare them on that. For the SkyTrain neighbourhood on the Burnaby border, read my <a href=\"burquitlam-neighbourhood-guide.html\">Burquitlam neighbourhood guide</a>."),
 ("Port Coquitlam","Riverside community with a small-town feel",
  "“PoCo” sits between the Coquitlam and Pitt rivers, with a walkable downtown, family-friendly residential neighbourhoods and the Traboulay PoCo Trail looping around the city. It's also Terry Fox's hometown — and where I play soccer.",
  ["Downtown PoCo","Citadel Heights","Mary Hill","Oxford Heights","Lincoln Park","Riverwood","Birchland Manor","Glenwood"],
  "West Coast Express at Port Coquitlam station; Lougheed Highway and the Mary Hill Bypass connect to the rest of the region.",
  "Traboulay PoCo Trail, Coquitlam River and Pitt River dikes, and plenty of community sports fields.",
  'I play soccer on a Port Coquitlam team, so PoCo is part of my ordinary week, not just somewhere I come for showings. If a smaller downtown and the Traboulay PoCo Trail suit the way you live, put it on your list. The longer version is my <a href="port-coquitlam.html">Port Coquitlam guide</a>.'),
 ("Port Moody","Waterfront “City of the Arts”",
  "Set at the eastern end of Burrard Inlet, Port Moody combines a waterfront lifestyle with forested hillsides. Rocky Point Park, the Shoreline Trail and the craft breweries along Murray Street's “Brewers Row” are local favourites.",
  ["Moody Centre","Inlet Centre / Suter Brook","Newport Village","Heritage Mountain","Heritage Woods","College Park","Glenayre","Ioco"],
  "Millennium Line SkyTrain (Moody Centre, Inlet Centre) and West Coast Express at Moody Centre.",
  "Rocky Point Park, the Shoreline Trail, Old Orchard Park, and quick access to Belcarra and Buntzen Lake.",
  'Port Moody is where I work, at Axford Real Estate on Clarke Street. SkyTrain at Moody Centre and Inlet Centre, the parks along the inlet and the hillside neighbourhoods give you a few different ways to live here, so we\'ll start with how you plan to get around and what you want close by. More detail is in my <a href="port-moody.html">Port Moody guide</a>.'),
 ("Anmore & Belcarra","Quiet villages north of Port Moody",
  "Two small, semi-rural villages tucked into the forest above Port Moody. Homes here tend to sit on larger, treed lots, and residents trade some convenience for privacy and nature on their doorstep.",
  ["Village of Anmore","Village of Belcarra"],
  "Mostly car-dependent; Port Moody's SkyTrain and West Coast Express stations are the nearest rapid transit.",
  "Buntzen Lake, Belcarra Regional Park and Sasamat Lake (White Pine Beach).",
  "I don't treat Anmore and Belcarra as an extension of Port Moody: they're separate villages with their own trade-offs. Larger lots and more privacy usually come with a car for most trips, and the nearest rapid transit is in Port Moody, so it's worth mapping out your commute and errands before you get attached to a home."),
]
hood_cards = ""
for name,tag,desc,nbhd,transit,outdoors,take in hoods:
    hood_cards += f'''<article class="hood">
  <div class="hood-head"><h3>{name}</h3><p class="hood-tag">{tag}</p></div>
  <div class="hood-body">
    <p>{desc}</p>
    <h4>Neighbourhoods to know</h4>
    <ul class="tags">{"".join(f"<li>{n}</li>" for n in nbhd)}</ul>
    <h4>Getting around</h4>
    <p>{transit}</p>
    <h4>Outdoors</h4>
    <p>{outdoors}</p>
    <h4>Devin's take</h4>
    <p>{take}</p>
  </div>
</article>'''

YT_BUYERS = ["TptjgpShZYM", "mR_HYgiJClc", "INd7HTnfDLs"]
BUYERS_HOODS_ASIDE = """<p class="lead">A quick introduction to the communities I focus on. Every street is different — reach out and I'll help you compare areas based on your commute, lifestyle and budget.</p>"""
BUYERS_TOURS_ASIDE = f"<p>{YT_NOTE} They're a handy way to compare layouts and finishes before you book showings.</p>{TOURS_LINK}"
BUYERS_LISTINGS_ASIDE = """<p class="lead">Tell me what you're looking for and I'll send you homes that match — including new listings as they hit the market.</p><p>Already looking at a specific property? <a href="buyer-opinion.html">Get an expert opinion</a> on its value.</p>"""

buyers = head("Buying a Home in the Tri-Cities, BC | Devin Desaulniers, Axford Real Estate",
              "Neighbourhood guides for Coquitlam, Port Coquitlam, Port Moody and nearby areas, a free mortgage affordability calculator, and personalised listing alerts from Devin Desaulniers, Axford Real Estate.", "buyers", page_url="buyers.html")
buyers += f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">For buyers</span>
    <h1>Buying in the <span class="nw">Tri-Cities, BC</span> &amp; Greater Vancouver</h1>
    <p class="lead">Local neighbourhood knowledge, listings matched to what you actually want, and a clear plan from your first showing to getting the keys.</p>
    <div class="btn-row">
      <a class="btn btn-light" href="#listings">Send me listings {I["arrow"]}</a>
      <a class="btn btn-ghost-light" href="{CALC}" target="_blank" rel="noopener">Mortgage calculator {I["ext"]}</a>
    </div>
  </div>
</section>
{page_nav([("help","How I help"),("testimonials","Reviews"),("neighbourhoods","Neighbourhoods"),("tours","Video tours"),("listings","Send me listings")])}

<section class="section section--calc">
  <div class="container">{calc_cta("Start with your budget","Before you fall in love with a listing, get a feel for your price range with my free mortgage affordability calculator. Then talk to a lender about pre-approval.")}</div>
</section>

<section class="section section--paper" id="help">
  <div class="container help-grid">
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
    </div>
    <ul class="list-check check-card">
      <li>Understand your goals, budget and must-haves</li>
      <li>Set up listing alerts for the areas and homes you're interested in</li>
      <li>Book and attend showings, and point out what to look for</li>
      <li>Review comparable sales so you can make an informed offer</li>
      <li>Prepare and negotiate your offer, including subjects like financing and inspection</li>
      <li>Guide you through subject removal, deposits and completion</li>
    </ul>
  </div>
</section>

{testimonials_section(["thurza","florian","tyson","kyron"], "What buyers say", lead="Buyers I've helped, in their own words.", featured="thurza", sec_id="testimonials", bg="")}

<section class="section section--paper" id="neighbourhoods">
  <div class="container">
    {sec_head("Neighbourhood guides", 'Get to know the <span class="nw">Tri-Cities, BC</span>', BUYERS_HOODS_ASIDE)}
    <div class="hood-grid">{hood_cards}</div>

    <div class="other-areas">
      <h3>Other nearby areas</h3>
      <p>I also help buyers in neighbouring Greater Vancouver communities, including <strong>Burnaby</strong>, <strong>New Westminster</strong>, and <strong>Pitt Meadows &amp; Maple Ridge</strong>. School District 43 serves Coquitlam, Port Coquitlam, Port Moody, Anmore and Belcarra — always confirm school catchments with the district for a specific address.</p>
      <p>Longer guides: <a href="burquitlam-neighbourhood-guide.html">Burquitlam</a>, <a href="port-moody.html">Port Moody</a> and <a href="port-coquitlam.html">Port Coquitlam</a>. Buying a first home in the Tri-Cities, BC? Read <a href="first-time-buyers-tri-cities-bc.html">first-time buyer questions</a>.</p>
      <p>If you're looking somewhere else in Greater Vancouver, tell me on the <a href="#listings">listings form</a> below: choose “Other (add in notes)” and add the area in your notes.</p>
    </div>
  </div>
</section>

<section class="section section--night" id="tours">
  <div class="container">
    {sec_head("Video tours", "Walk through a few homes first", BUYERS_TOURS_ASIDE)}
    {tours_grid(YT_BUYERS)}
  </div>
</section>

<section class="section section--paper" id="listings">
  <div class="container">
    {sec_head("Personalised listing alerts", "Send me listings", BUYERS_LISTINGS_ASIDE)}
    <form class="form-card" data-form-key="buyerListings" data-goat-event="form-listings-signup" action="#" method="POST">
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
TEN_TITLE = "Relocation Rental Agent for Greater Vancouver | Devin Desaulniers, Axford Real Estate"
TEN_DESC = "Moving to Vancouver or the Tri-Cities, BC? Get local rental help: consultation, property search with early access, in-person or virtual showings, and lease review & negotiation. $1,500 + GST, paid in two parts."

FAQ_ITEMS = seo_pages.TENANT_FAQ_PREPEND + [
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
  "<p>No — this is a tenant representation service. I represent you, and you pay my fee. If a rental is listed or managed by Axford Real Estate, my brokerage, I'll disclose that to you in writing before you commit, and you can decline it.</p>"),
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
SERVICE_JSONLD = '<script type="application/ld+json">\n' + _json.dumps({
    "@context": "https://schema.org",
    "@type": "Service",
    "serviceType": "Relocation rental search (tenant representation)",
    "provider": {"@id": SITE + "#devin-desaulniers"},
    "areaServed": {"@type": "Place", "name": "Greater Vancouver"},
    "offers": {
        "@type": "Offer",
        "price": "1500",
        "priceCurrency": "CAD",
        "description": "$1,500 + GST, paid by the tenant",
    },
}, indent=2, ensure_ascii=False) + '\n</script>'
tenants = head(TEN_TITLE, TEN_DESC, "tenants", og_image="assets/img/og-tenants.png", page_url="tenants.html", body_class="has-sticky", extra_head=FAQ_JSONLD + "\n" + SERVICE_JSONLD)
STEP1 = f"""<div class="form-grid">
  <div class="field"><label for="t-name">Full name <span class="req">*</span></label><input id="t-name" name="name" autocomplete="name" required></div>
  <div class="field"><label for="t-email">Email <span class="req">*</span></label><input id="t-email" name="email" type="email" autocomplete="email" required></div>
  <div class="field"><label for="t-phone">Phone <span class="hint">(incl. country code if outside Canada)</span></label><input id="t-phone" name="phone" type="tel" autocomplete="tel"></div>
  <div class="field"><label for="t-date">Target move-in date <span class="req">*</span></label><input id="t-date" name="move_date" type="date" required></div>
  <button type="button" class="btn btn-primary btn-block js-only" data-next-step>Next: your rental needs {I["arrow"]}</button>
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

TEN_INCLUDED_ASIDE = '<p class="lead">Searching for a rental from out of town is stressful. I represent you, the tenant, so you can make an informed decision without flying in for every viewing.</p>'
TEN_HOW_ASIDE = '<p class="lead">Five simple steps, built around your move date.</p>'
TEN_RES_ASIDE = '<p class="lead">Two free PDFs: a practical guide to renting in Greater Vancouver, and a two-page overview of how my tenant representation service works.</p>'

tenants += f"""
<section class="lp-hero" data-sticky-hide>
  <div class="container lp-hero-inner">
    <div class="lp-copy">
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
    <form class="lp-quick" id="intake" data-form-key="tenantIntake" data-goat-event="form-tenant" action="#" method="POST">
      <input type="hidden" name="_subject" value="New relocation rental intake">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="form" value="Tenant: Relocation rental intake">
      <div class="hp" aria-hidden="true"><label>Leave this field empty <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
      <h2>Start your rental search</h2>
      <p>Takes about 2 minutes. No obligation — I'll get back to you to talk next steps. Prefer to talk? <a href="{TEL}">{PHONE}</a></p>
      {STEP1}
      <div class="step2-wrap" data-step2-wrap>
        <h3 class="step2-title">Your rental needs</h3>
        {STEP2}
      </div>
    </form>
  </div>
</section>

<section class="section" id="included">
  <div class="container">
    {sec_head("My services", "Someone on your side, from first search to move-in", TEN_INCLUDED_ASIDE)}
    <div class="service-grid">
      <div class="card"><div class="icon">{I["handshake"]}</div><h3>Personalized consultation</h3><p>I'll help you identify rentals that fit your budget, commute, lifestyle and priorities. I also point out potential green flags and red flags, so you can make a more informed decision and avoid unnecessary uncertainty.</p></div>
      <div class="card"><div class="icon">{I["home"]}</div><h3>Property search &amp; early access</h3><p>I search Facebook Marketplace, Craigslist and other rental sources. Through Axford Real Estate, I also have access to our own rental opportunities and firsthand relationships with the property managers in our office.</p></div>
      <div class="card"><div class="icon">{I["video"]}</div><h3>Showings — in person or virtual</h3><p>I book and coordinate showings and attend with you. When you can't make it, I do virtual showings with a live video walkthrough, plus floor plans for the homes you're seriously considering. When practical, I can also drive us between scheduled appointments.</p></div>
      <div class="card"><div class="icon">{I["doc"]}</div><h3>Lease review &amp; negotiation</h3><p>We review the lease agreement together. I explain the important terms, talk through move-in and move-out expectations, and negotiate rent or other lease terms where appropriate.</p></div>
    </div>
    <div class="fee-block">
      <div class="fee-main">
        <span class="eyebrow">Service fee</span>
        <div class="fee-total">$1,500 <small>total + GST</small></div>
        <p>Paid by the tenant, in two parts.</p>
      </div>
      <ul class="fee-parts">
        <li><b>$750</b><span>at the beginning of the engagement (non-refundable)</span></li>
        <li><b>$750</b><span>once you successfully secure a rental</span></li>
      </ul>
      <a class="btn btn-light" href="#intake">Start your search {I["arrow"]}</a>
    </div>
    <p class="form-note center fee-note">I help tenants find and lease a home. I do not provide property management services.</p>
  </div>
</section>

{testimonials_section(["susan","hugo","aline"], "What renters say", lead="Tenants I've helped find a home, in their own words.", featured="susan", sec_id="testimonials", bg="section--paper")}

<section class="section" id="how">
  <div class="container">
    {sec_head("How I can help", "How it works", TEN_HOW_ASIDE)}
    <ol class="mini-steps five">
      <li><div><h3>Initial consultation</h3><p>We discuss your budget, preferred areas, timing and must-haves.</p></div></li>
      <li><div><h3>Property search</h3><p>I identify suitable rentals and help you screen opportunities.</p></div></li>
      <li><div><h3>Showings</h3><p>I coordinate and attend showings with you, or provide virtual showings.</p></div></li>
      <li><div><h3>Lease review &amp; negotiation</h3><p>I explain the key terms and negotiate where possible.</p></div></li>
      <li><div><h3>Move in</h3><p>I help you understand the next steps and what to expect at move-in.</p></div></li>
    </ol>
    <div class="section-cta"><a class="btn btn-primary" href="#intake">Start your rental search {I["arrow"]}</a></div>
  </div>
</section>

<section class="section section--paper" id="resources">
  <div class="container">
    {sec_head("Free renter resources", "Download my renter brochures", TEN_RES_ASIDE)}
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
          <a class="btn btn-primary btn-sm" href="assets/docs/devin-desaulniers-renter-resources.pdf" target="_blank" rel="noopener">View / download PDF {I["arrow"]}</a>
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
          <a class="btn btn-primary btn-sm" href="assets/docs/devin-desaulniers-tenant-representation.pdf" target="_blank" rel="noopener">View / download PDF {I["arrow"]}</a>
        </div>
      </article>
    </div>
    <a class="guide-callout" href="relocating-to-greater-vancouver.html">
      <span class="gc-icon">{I["pin"]}</span>
      <span><b>Moving to Greater Vancouver?</b> Read my Relocating to Greater Vancouver guide — areas at a glance, commuting, renting basics in B.C., and whether to rent or buy first.</span>
      <span class="gc-arrow">{I["arrow"]}</span>
    </a>
    <a class="guide-callout" href="newcomer-rental-faqs.html">
      <span class="gc-icon">{I["doc"]}</span>
      <span><b>New to Canada?</b> Rental questions for newcomers: deposits, credit history, scams, and lining up a home before you land.</span>
      <span class="gc-arrow">{I["arrow"]}</span>
    </a>
  </div>
</section>

<section class="section" id="about">
  <div class="container about-grid about-grid--tenants">
    <div class="about-copy">
      <span class="eyebrow">Your local on the ground</span>
      <h2>Hi, I'm Devin.</h2>
      <p>I've lived in the Greater Vancouver area for 28 years. I work in Port Moody, and I play soccer on a Port Coquitlam team and pickleball around the Tri-Cities, BC. I know this region as a local — so I can tell you what a neighbourhood is actually like, not just what the listing says.</p>
      <p>For the last seven years I've been helping people relocate to and from Vancouver. I've been licensed in real estate since 2020, and today I'm a Real Estate Associate with <strong>Axford Real Estate</strong>.</p>
      <p class="inline-links"><a href="{TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="index.html#about">More about me</a> · <a href="relocating-to-greater-vancouver.html">Moving to Greater Vancouver?</a> · <a href="newcomer-rental-faqs.html">New to Canada?</a></p>
      {social_row("Look me up")}
    </div>
    <figure class="portrait">
      {picture("assets/img/devin-headshot",(480,800),800,1000,"Devin Desaulniers, Real Estate Associate with Axford Real Estate","headshot",eager="auto",sizes_attr="(max-width: 899px) 80vw, 360px")}
      <figcaption><strong>Devin Desaulniers</strong><span>Real Estate Associate · Axford Real Estate</span></figcaption>
    </figure>
  </div>
</section>

<section class="section section--paper" id="faq">
  <div class="container">
    {sec_head("Questions", "Frequently asked questions", center=True)}
    <div class="faq-list">{faq_html}</div>
  </div>
</section>

<section class="section trust-badge-section" id="reviews">
  <div class="container center">
    <span class="eyebrow">My brokerage</span>
    <p class="tb-intro">I work with Axford Real Estate, a brokerage based in Port Moody.</p>
    {google_badge()}
  </div>
</section>

<section class="section section--night cta-band">
  <div class="container center narrow">
    <h2>Ready to find your next home?</h2>
    <p>Please feel free to reach out at any time.</p>
    <div class="btn-row">
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
    <div class="btn-row">
      <a class="btn btn-light" href="tenants.html#intake">Need a rental? Start here {I["arrow"]}</a>
      <a class="btn btn-ghost-light" href="{TEL}">{I["phone"]} Call or text {PHONE}</a>
    </div>
  </div>
</section>
{page_nav([("areas","Areas at a glance"),("renting-basics","Renting in B.C."),("rentals","Rental help"),("buying","Buying"),("faq","FAQ")])}

<article class="guide">
<section class="section">
  <div class="container guide-intro">
    <div>
      <p class="lead guide-lead">I'm Devin Desaulniers, a Real Estate Associate with Axford Real Estate in Port Moody. I've lived in the Greater Vancouver area for 28 years, and for the last seven years I've been helping people relocate to and from Vancouver — as tenants who need a rental lined up before they arrive, or as buyers.</p>
      <p>If you're moving from another province (or from elsewhere in BC), the hard part is usually the same: you need honest advice about areas, a realistic commute and a place that works before your furniture shows up. This page is a plain-language overview of Greater Vancouver, plus how I can help.</p>
    </div>
    <figure class="portrait guide-photo">
      {picture("assets/img/devin-headshot",(480,800),800,1000,"Devin Desaulniers, Real Estate Associate with Axford Real Estate","headshot",eager="auto",sizes_attr="(max-width: 899px) 70vw, 280px")}
      <figcaption><strong>Devin Desaulniers</strong><span>Real Estate Associate · Axford Real Estate</span></figcaption>
    </figure>
  </div>
</section>

<section class="section section--paper" id="areas">
  <div class="container narrow-wide">
    <span class="eyebrow">Where to live</span>
    <h2>Greater Vancouver at a glance</h2>
    <p>Greater Vancouver is a collection of cities, each with its own feel, rents and commute. Here's a quick snapshot to start your shortlist:</p>
    <div class="area-grid">{areas_gv_html}</div>
    <h3 class="sub-h">Getting around</h3>
    <p>TransLink runs SkyTrain, buses, the SeaBus and the West Coast Express commuter rail (weekday rush-hour service between Mission and Waterfront Station in downtown Vancouver). Driving times vary a lot by bridge and time of day, so tell me where you'll work or study and I'll factor the commute into every shortlist. Buying in the Tri-Cities, BC? See my <a href="buyers.html#neighbourhoods">neighbourhood guides</a>, the <a href="burquitlam-neighbourhood-guide.html">Burquitlam neighbourhood guide</a>, the <a href="port-moody.html">Port Moody guide</a> and the <a href="port-coquitlam.html">Port Coquitlam guide</a>. Buying a first home? Read <a href="first-time-buyers-tri-cities-bc.html">first-time buyer questions for the Tri-Cities, BC</a>. New to Canada and renting first? See the <a href="newcomer-rental-faqs.html">newcomer rental FAQs</a>.</p>
  </div>
</section>

<section class="section" id="renting-basics">
  <div class="container narrow-wide">
    <span class="eyebrow">Know your rights</span>
    <h2>Renting in B.C.: the basics</h2>
    <p>A few rules and habits that protect you, especially when you're renting from out of province:</p>
    <ul class="list-check">
      <li><strong>Deposits are capped.</strong> A security deposit can be at most half of one month's rent, and a pet damage deposit (if applicable) at most another half month.</li>
      <li><strong>Rent increases are limited.</strong> Rent can go up only once every 12 months, by no more than the annual limit (2.3% for 2026, 2.2% for 2027), and your landlord must give three full months' written notice.</li>
      <li><strong>Do a move-in condition inspection</strong> with the landlord, document the existing condition and keep a copy of the report.</li>
      <li><strong>Get it in writing:</strong> rent, term, utilities, parking, pets, occupants and any special terms.</li>
      <li><strong>Verify before you pay.</strong> Confirm the property and the person you're dealing with before sending money, and be cautious of wire transfers, gift cards, cryptocurrency or pressure to pay before a viewing.</li>
    </ul>
    <h3 class="sub-h">Have your application ready</h3>
    <p>Photo ID, proof of income (recent pay stubs, an employment or offer letter, or bank statements / a Notice of Assessment if you're self-employed), landlord and employer references, and a short renter profile. A credit report you get yourself can speed things up.</p>
    <p>The full checklist — budget, viewings, applications and move-in — is in my free <a href="tenants.html#resources">Greater Vancouver renter's guide (PDF)</a>.</p>
    <p class="form-note">General information only, not legal advice. Confirm current rules with the <a href="{RTB}" target="_blank" rel="noopener">B.C. Residential Tenancy Branch</a>.</p>
  </div>
</section>

<section class="section section--night" id="rentals">
  <div class="container narrow-wide">
    <span class="eyebrow">Tenant-side rental help</span>
    <h2>How I help relocating tenants</h2>
    <p>You don't have to wait until you land to secure a rental. My tenant-side relocation rental service is <strong>$1,500 total + GST, paid by the tenant</strong> — $750 at the beginning of the engagement (non-refundable) and $750 once you successfully secure a rental. It includes:</p>
    <ul class="list-check">
      <li>A personalized consultation on your budget, commute, lifestyle and priorities, including green flags and red flags to watch for</li>
      <li>A rental search across Greater Vancouver, in the areas we agree on, with early access through Axford Real Estate's own rental opportunities</li>
      <li>Showings — I attend with you, or do live video walkthroughs with floor plans while you're still out of province</li>
      <li>Lease review &amp; negotiation before you sign</li>
    </ul>
    <p>I represent your search on the tenant side — not a landlord's inventory. (Axford also has a separate property management business; this service is different.)</p>
    <p>Most Greater Vancouver rentals list only a few weeks before they're available, so the active search usually starts about 4–6 weeks before move-in. Use the weeks before that to settle your budget, areas and documents.</p>
    <div class="btn-row">
      <a class="btn btn-light" href="tenants.html#intake">Start your rental search {I["arrow"]}</a>
      <a class="btn btn-ghost-light" href="tenants.html">See the relocation rental service</a>
    </div>
  </div>
</section>

<section class="section" id="buying">
  <div class="container narrow-wide">
    <span class="eyebrow">Buying</span>
    <h2>How I help relocating buyers</h2>
    <p>For buyers moving to Greater Vancouver:</p>
    <ol class="mini-steps guide-steps">
      <li><div><h3>Pre-move planning</h3><p>Budget, an area shortlist, strata vs freehold trade-offs, and what good value actually looks like right now.</p></div></li>
      <li><div><h3>Remote-friendly search</h3><p>Video tours, floor plans and clear notes on condition, strata documents and comparable sales, so you're not flying blind from another province.</p></div></li>
      <li><div><h3>Offer strategy and negotiation</h3><p>Local market pace, subject clauses and timelines that fit a cross-province move.</p></div></li>
      <li><div><h3>Closing through move-in</h3><p>Coordination with your lawyer or notary, lender and movers so the handoff is calm.</p></div></li>
    </ol>
    <p class="after-steps">Start with your budget using my free <a href="{CALC}" target="_blank" rel="noopener">mortgage affordability calculator</a>, then <a href="buyers.html#listings">ask me to send you listings</a>.</p>
    <p class="form-note">Office: Axford Real Estate, {BROKERAGE_ADDR}. Licensed since 2020.</p>
  </div>
</section>

<section class="section section--paper" id="faq">
  <div class="container">
    {sec_head("FAQ", "Relocating to Greater Vancouver: common questions", center=True)}
    <div class="faq-list">{gv_faq_html}</div>
  </div>
</section>
</article>

<section class="section section--night cta-band">
  <div class="container center narrow">
    <h2>Relocating to Greater Vancouver?</h2>
    <p>I'm happy to help with a tenant-side rental search before you arrive, or as your buyer's agent.</p>
    <div class="btn-row">
      <a class="btn btn-light" href="tenants.html#intake">Start a rental search {I["arrow"]}</a>
      <a class="btn btn-ghost-light" href="buyers.html#listings">Get listings sent to me</a>
      <a class="btn btn-ghost-light" href="{TEL}">Call or text {PHONE}</a>
      <a class="btn btn-ghost-light" href="mailto:{EMAIL}?subject=Relocating%20to%20Greater%20Vancouver">Email Devin</a>
    </div>
  </div>
</section>
"""
gv += foot()

# ---------------- VIDEOS (YouTube property tours) ----------------
VIDEOS_URL = "videos.html"
videos = head("Property Video Tours | Devin Desaulniers, Real Estate Associate, Axford Real Estate",
              "Property video tours with Devin Desaulniers, Real Estate Associate with Axford Real Estate: walkthroughs of homes and condos in Vancouver and Greater Vancouver from his YouTube channel.",
              "videos", page_url=VIDEOS_URL)
videos += f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Video tours · YouTube</span>
    <h1>Property video tours</h1>
    <p class="lead">Video tours with Devin Desaulniers, Real Estate Associate with Axford Real Estate. Press play on any tour to watch it right here.</p>
    <p class="hero-note">{YT_NOTE}</p>
    <div class="btn-row">
      <a class="btn btn-light" href="{YOUTUBE_CHANNEL}" target="_blank" rel="noopener">Visit my YouTube channel {I["ext"]}</a>
      <a class="btn btn-ghost-light" href="{TEL}">{I["phone"]} Call or text {PHONE}</a>
    </div>
  </div>
</section>

<section class="section" id="tours">
  <div class="container">
    {tours_grid([v for v, _ in YT_TOURS], heading="h2")}
  </div>
</section>

<section class="section section--paper">
  <div class="container">
    <div class="split-cta">
      <div>
        <span class="eyebrow">Buying in Greater Vancouver</span>
        <h2>Looking for a home of your own?</h2>
        <p class="lead">Tell me what you're looking for and I'll send you homes that match — including new listings as they hit the market.</p>
      </div>
      <div class="btn-row">
        <a class="btn btn-primary" href="buyers.html#listings">Get listings sent to me {I["arrow"]}</a>
        <a class="btn btn-outline" href="buyers.html">Buyer info &amp; neighbourhoods</a>
      </div>
    </div>
  </div>
</section>
"""
videos += foot()

# ---------------- PRIVACY ----------------
# Keep in step with the real forms (buyers, tenants, home evaluation, expert opinion, listing and rental inquiries), assets/js/config.js, the GoatCounter tag in head(), and the Elfsight snippet in foot().
PRIVACY_URL = "privacy.html"
privacy = head("Privacy | Devin Desaulniers, Real Estate Associate, Axford Real Estate",
               "How the contact forms, listing inquiries, chat widget, and page-visit counter on Devin Desaulniers' website handle what you send, where it may be processed, and how to make a privacy request.",
               "privacy", page_url=PRIVACY_URL)
privacy += f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Privacy</span>
    <h1>How this site handles your information</h1>
    <p class="lead">What happens to the information you send through the contact forms, a listing inquiry, and the chat widget, how page visits are counted, and who to contact with a privacy question or request.</p>
  </div>
</section>

<section class="section">
  <div class="container narrow-wide">
    <div class="post-body">
      <p>This site is operated by Devin Desaulniers, Real Estate Associate with Axford Real Estate, {BROKERAGE_ADDR}. The sections below explain, in plain language, where the information you send me goes.</p>
      <p>This site uses GoatCounter for visit counts, with no cookies and no personal tracking. The button labelled “Want me to find yours? Tenant Relocation Service $1,500 + GST” also sends an event named <span class="nw">cta-tenant-relocation</span> when you click it. That event is the button name and the page you were on. It does not include what you type into a form.</p>

      <h2 id="forms">Contact forms</h2>
      <p>There are six forms on this site: the “Send me listings” form on the <a href="buyers.html#listings">buyers page</a>, the relocation rental intake on the <a href="tenants.html#intake">tenants page</a>, the <a href="home-evaluation.html">free home evaluation</a>, the <a href="buyer-opinion.html">expert opinion</a> on a property you're considering, and the inquiry on a home at <a href="listings.html">homes for sale</a> or <a href="rentals.html">homes for rent</a>. When you press Send, the form is sent through FormSubmit (formsubmit.co), which emails your submission to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      <p>The forms ask for:</p>
      <ul>
        <li>your name and email, and your phone number if you add it;</li>
        <li>on the home evaluation and the expert opinion forms: your email, the property address, and your name if you add it;</li>
        <li>on the listings form: the areas you're interested in, property type, price range, bedrooms and bathrooms, your timeline, whether you're pre-approved for a mortgage, and any notes;</li>
        <li>on the rental intake: your target move-in date, how you'd like to be contacted, where you're moving from, your monthly rent budget, bedrooms, preferred areas, pets, your work or school location, and any notes;</li>
        <li>on a listing or rental inquiry: the listing id, MLS® number, address and REALTOR.ca link for the home you opened, and your message.</li>
      </ul>
      <p>Each form asks you to agree that I can contact you by email or phone about your request. You can opt out at any time.</p>

      <h2 id="listing-search">Homes for sale and homes for rent</h2>
      <p>The homes on <a href="listings.html">homes for sale</a> and <a href="rentals.html">homes for rent</a> come from the REALTOR.ca DDF® feed. Opening a listing sends a view to the CREA DDF® Analytics Web Service at analytics.crea.ca. That view includes the listing id, this site's DDF destination id, and the page address. The DDF rules require it. Listing photos load from the photo addresses in the feed.</p>

      <h2 id="chat">Chat widget</h2>
      <p>Pages on this site include a chat widget, “Devin's AI Assistant”, provided by Elfsight. What you type into that chat is handled by Elfsight.</p>

      <h2 id="outside-canada">Processing outside Canada</h2>
      <p>Information you send through FormSubmit or the Elfsight chat widget may be processed outside Canada. A GoatCounter page visit may also be processed outside Canada. If you'd rather not use the forms or the chat, you can call or text me at <a href="{TEL}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>

      <h2 id="video-tours">Video tours</h2>
      <p>The YouTube video tours on this site show a preview image from YouTube, and the YouTube player itself loads only after you press play.</p>

      <h2 id="requests">Privacy questions and requests</h2>
      <p>For a privacy question or request, contact me at my brokerage:</p>
    </div>
    <ul class="contact-list">
      <li><span class="cl-icon">{I["building"]}</span><div><small>Mailing address</small><span>Devin Desaulniers<br>Axford Real Estate<br>2326 Clarke St<br>Port Moody, BC <span class="nw">V3H 1Y8</span></span></div></li>
      <li><span class="cl-icon">{I["mail"]}</span><div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
      <li><span class="cl-icon">{I["phone"]}</span><div><small>Brokerage office</small><a href="{BROKERAGE_TEL}">{BROKERAGE_PHONE}</a></div></li>
      <li><span class="cl-icon">{I["phone"]}</span><div><small>Direct line (call or text)</small><a href="{TEL}">{PHONE}</a></div></li>
    </ul>
  </div>
</section>
"""
privacy += foot()

# ---------------- OFFER PAGES (home evaluation + buyer opinion) ----------------
# Compact landing pages. Same FormSubmit AJAX path as the other forms (config.js). Not test-submitted.
_CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M20 6L9 17l-5-5"/></svg>'

def offer_page(filename, title, desc, eyebrow, h1, lead, points, form_key, goat_event, subject, form_name, form_h, button, thanks_h, thanks_p, note, id_prefix):
    photo = picture("assets/img/devin-headshot", (480, 800), 800, 1000,
                    "Devin Desaulniers, Real Estate Associate with Axford Real Estate",
                    "", eager=True, sizes_attr="(max-width: 719px) 64px, 180px")
    points_html = "".join(f"<li>{icon}<span>{text}</span></li>" for icon, text in points)
    page = head(title, desc, "offer", og_image="assets/img/devin-headshot-800.jpg", page_url=filename)
    page += f"""
<section class="offer">
  <div class="container offer-grid">
    <div class="offer-intro">
      <figure class="offer-photo">{photo}</figure>
      <span class="eyebrow">{eyebrow}</span>
      <div class="offer-copy">
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
      </div>
      <ul class="offer-points">{points_html}</ul>
    </div>
    <form class="offer-form" id="request" data-form-key="{form_key}" data-goat-event="{goat_event}" action="#" method="POST">
      <input type="hidden" name="_subject" value="{subject}">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="form" value="{form_name}">
      <div class="hp" aria-hidden="true"><label>Leave this field empty <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
      <div data-offer-fields>
        <h2>{form_h}</h2>
        <div class="form-grid">
          <div class="field"><label for="{id_prefix}-email">Your email <span class="req">*</span></label><input id="{id_prefix}-email" name="email" type="email" inputmode="email" autocomplete="email" required></div>
          <div class="field"><label for="{id_prefix}-address">Property address <span class="req">*</span></label><input id="{id_prefix}-address" name="Property address" autocomplete="street-address" required></div>
          <div class="field"><label for="{id_prefix}-name">Your name <span class="hint">(optional)</span></label><input id="{id_prefix}-name" name="name" autocomplete="name"></div>
          {consent(id_prefix)}
          <div class="full">
            <button type="submit" class="btn btn-primary btn-block">{button}</button>
            <div class="form-status" role="status" aria-live="polite"></div>
          </div>
        </div>
      </div>
      <div class="offer-thanks" data-offer-thanks hidden role="status" tabindex="-1">
        <span class="offer-thanks-mark">{_CHECK}</span>
        <h2>{thanks_h}</h2>
        <p>{thanks_p}</p>
        <a class="btn btn-outline" href="{TEL}">{I["phone"]} Call or text {PHONE}</a>
      </div>
      <p class="offer-note">{note}</p>
    </form>
  </div>
</section>
"""
    page += foot()
    return page

home_evaluation = offer_page(
    "home-evaluation.html",
    "Free Home Evaluation | Devin Desaulniers, Axford Real Estate",
    "Send Devin Desaulniers an address and he'll email you a free market evaluation of your home. Real Estate Associate with Axford Real Estate in Greater Vancouver.",
    "Free home evaluation",
    "Curious what your home would sell for?",
    "Send me the address and I'll email you a free market evaluation — recent sales nearby, and what I'd expect your home to bring. There's no cost, and asking doesn't mean you have to list.",
    [
        (I["home"], "Free, and no commitment to list"),
        (I["doc"], "Recent sales nearby, in plain language"),
        (I["mail"], "I write it and email it to you"),
    ],
    "homeEvaluation",
    "form-home-evaluation",
    "New free home evaluation",
    "Free home evaluation",
    "Request your evaluation",
    "Request my evaluation",
    "Thanks — I'll take a look.",
    "Your request is in. I'll email a market evaluation of that address to you. If you'd rather talk it through, call or text me.",
    "This is my opinion of market value from recent sales. It isn't an appraisal, and it isn't a promise of a sale price.",
    "he",
)
buyer_opinion = offer_page(
    "buyer-opinion.html",
    "Get an Expert Opinion | Devin Desaulniers, Axford Real Estate",
    "Looking at a property? Send Devin Desaulniers the address and he'll email you his take on its value. Real Estate Associate with Axford Real Estate.",
    "Get an expert opinion",
    "Looking at a property?",
    "Send me the address and I'll email you my take on its value: what similar homes have sold for, and whether the asking price lines up. Useful before you book another showing or write an offer.",
    [
        (I["pin"], "For a home you're considering"),
        (I["doc"], "Set beside recent sales"),
        (I["mail"], "I email you my take"),
    ],
    "buyerOpinion",
    "form-buyer-opinion",
    "New expert opinion request",
    "Expert opinion",
    "Ask for my take",
    "Get my take",
    "Thanks — I'll look at this one.",
    "Your request is in. I'll email you my take on the value. If you're on a deadline, call or text me.",
    "This is my opinion of value from recent sales. It isn't an appraisal, and it isn't a promise of what the property will sell for.",
    "bo",
)

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
{GOATCOUNTER}
<script>location.replace("{GV_URL}" + location.hash);</script>
</head>
<body>
<p>This guide has moved to <a href="{GV_URL}">Relocating to Greater Vancouver</a>.</p>
</body>
</html>
"""

for fn, html in [("index.html",home),("buyers.html",buyers),("tenants.html",tenants),(GV_URL,gv),("relocating-to-coquitlam.html",redirect),("home-evaluation.html",home_evaluation),("buyer-opinion.html",buyer_opinion)]:
    open(os.path.join(OUT,fn),"w").write(html)
open(os.path.join(OUT, VIDEOS_URL), "w").write(videos)
open(os.path.join(OUT, PRIVACY_URL), "w").write(privacy)
open(os.path.join(OUT, "listings.html"), "w").write(listings_page.render("sale"))
open(os.path.join(OUT, "rentals.html"), "w").write(listings_page.render("rent"))

# Blog pages, RSS feed and sitemap (sitemap lists the static pages + blog index + every post)
blog.write_blog(POSTS)
SEO_PAGES = seo_pages.write_pages()
for fn, html in SEO_PAGES:
    open(os.path.join(OUT, fn), "w").write(html)
STATIC_PAGES = ["", "tenants.html", "buyers.html", "home-evaluation.html", "buyer-opinion.html", GV_URL, "videos.html", PRIVACY_URL]
if LISTINGS_LIVE:
    STATIC_PAGES[1:1] = ["listings.html", "rentals.html", "rent-report.html"]
guide_at = STATIC_PAGES.index(GV_URL) + 1
STATIC_PAGES[guide_at:guide_at] = [fn for fn, _ in SEO_PAGES]
import rent_report
_report_lastmod = rent_report.published_lastmod(OUT)
_sitemap_lastmod = {"rent-report.html": _report_lastmod} if _report_lastmod else {}
open(os.path.join(OUT,"sitemap.xml"),"w").write(blog.sitemap_xml(STATIC_PAGES, POSTS, _sitemap_lastmod))
print("built")
