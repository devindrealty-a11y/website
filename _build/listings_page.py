"""For-sale and for-rent search pages. Hidden until LISTINGS_LIVE."""
from partials import BROKERAGE, BROKERAGE_ADDR, EMAIL, LISTINGS_LIVE, PHONE, TEL, foot, head

MODES = {
    "sale": {
        "file": "listings.html",
        "nav": "listings",
        "title": "Homes for sale in Greater Vancouver and the Fraser Valley | Devin Desaulniers, Axford Real Estate",
        "desc": (
            "Search active residential listings in Greater Vancouver and the Fraser Valley "
            "with Devin Desaulniers, Real Estate Associate at Axford Real Estate."
        ),
        "h1": "Homes for sale",
        "lead": (
            "Active residential listings in Greater Vancouver and the Fraser Valley, from the REALTOR.ca DDF® feed. "
            "This search is operated by Devin Desaulniers, Real Estate Associate with {brokerage}."
        ),
        "min_label": "Min price",
        "max_label": "Max price",
        "step": "1000",
        "sort_asc": "Price: low to high",
        "sort_desc": "Price: high to low",
        "more": "Show more homes",
        "ask": "Ask Devin about this home",
        "ask_lead": "Send a note to Devin Desaulniers at {brokerage}. This message comes to Devin. It is not sent to the listing brokerage.",
        "form_key": "listingInquiry",
        "subject": "New listing inquiry",
        "form_name": "Listing inquiry",
        "placeholder": "I would like to know more about this home.",
        "consent": "about this home",
        "closed": "Sold listings are not shown.",
        "feed": "listings/data.json",
        "sample": "_fixtures/listings-sample.json",
    },
    "rent": {
        "file": "rentals.html",
        "nav": "rentals",
        "title": "Homes for rent in Greater Vancouver and the Fraser Valley | Devin Desaulniers, Axford Real Estate",
        "desc": (
            "Search active residential rentals in Greater Vancouver and the Fraser Valley "
            "with Devin Desaulniers, Real Estate Associate at Axford Real Estate."
        ),
        "h1": "Homes for rent",
        "lead": (
            "Active residential rentals in Greater Vancouver and the Fraser Valley, from the REALTOR.ca DDF® feed. "
            "Rent is shown per month. This search is operated by Devin Desaulniers, Real Estate Associate with {brokerage}."
        ),
        "min_label": "Min rent",
        "max_label": "Max rent",
        "step": "50",
        "sort_asc": "Rent: low to high",
        "sort_desc": "Rent: high to low",
        "more": "Show more rentals",
        "ask": "Ask Devin about this rental",
        "ask_lead": "Send a note to Devin Desaulniers at {brokerage}. This message comes to Devin. It is not sent to the listing brokerage.",
        "form_key": "rentalInquiry",
        "subject": "New rental inquiry",
        "form_name": "Rental inquiry",
        "placeholder": "I would like to know more about this rental.",
        "consent": "about this rental",
        "closed": "Leased, rented, and sold listings are not shown.",
        "feed": "listings/rentals.json",
        "sample": "_fixtures/rentals-sample.json",
    },
}


def render(mode="sale"):
    spec = MODES[mode]
    robots = "" if LISTINGS_LIVE else '<meta name="robots" content="noindex, nofollow">\n'
    active = spec["nav"] if LISTINGS_LIVE else ""
    html = head(spec["title"], spec["desc"], active, page_url=spec["file"], extra_head=robots)
    lead = spec["lead"].format(brokerage=BROKERAGE)
    ask_lead = spec["ask_lead"].format(brokerage=BROKERAGE)
    html += f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">{BROKERAGE}</span>
    <h1>{spec["h1"]}</h1>
    <p class="lead">{lead}</p>
    <div class="ls-axford">
      <span class="ls-axford-logo"><img src="assets/img/axford-logo.png" alt="{BROKERAGE}" width="180" height="38"></span>
      <p><strong>{BROKERAGE}</strong><br>Devin Desaulniers, Real Estate Associate<br>{BROKERAGE_ADDR}<br><a href="{TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
  </div>
</section>

<div class="ls-sample" id="ls-sample" hidden>
  <div class="container">
    <p><strong>Sample data for local preview only.</strong> These homes, prices, photos, and brokerages are fictional. They are not listings from the REALTOR.ca DDF® feed.</p>
  </div>
</div>

<div id="ls-search">
  <section class="section" style="padding-top:32px">
    <div class="container">
      <form class="ls-filters" id="ls-filters" role="search">
        <div class="field ls-grow"><label for="ls-q">City or area</label><input id="ls-q" name="q" type="search" placeholder="Coquitlam, Surrey, Langley…" autocomplete="off"></div>
        <div class="field"><label for="ls-min">{spec["min_label"]}</label><input id="ls-min" name="min" type="number" inputmode="numeric" min="0" step="{spec["step"]}" placeholder="Any"></div>
        <div class="field"><label for="ls-max">{spec["max_label"]}</label><input id="ls-max" name="max" type="number" inputmode="numeric" min="0" step="{spec["step"]}" placeholder="Any"></div>
        <div class="field"><label for="ls-beds">Bedrooms</label><select id="ls-beds" name="beds"><option value="">Any</option><option value="1">1+</option><option value="2">2+</option><option value="3">3+</option><option value="4">4+</option><option value="5">5+</option></select></div>
        <div class="field"><label for="ls-baths">Bathrooms</label><select id="ls-baths" name="baths"><option value="">Any</option><option value="1">1+</option><option value="2">2+</option><option value="3">3+</option><option value="4">4+</option></select></div>
        <div class="field"><label for="ls-type">Property type</label><select id="ls-type" name="type"><option value="">Any</option><option>Detached house</option><option>Condo / apartment</option><option>Townhouse</option><option>Half duplex / duplex</option><option>Other residential</option></select></div>
        <div class="field"><label for="ls-sort">Sort</label><select id="ls-sort" name="sort"><option value="updated">Recently updated</option><option value="price-asc">{spec["sort_asc"]}</option><option value="price-desc">{spec["sort_desc"]}</option><option value="city">City A–Z</option></select></div>
        <div class="ls-filter-actions"><button type="submit" class="btn btn-primary">Search</button><button type="button" class="btn btn-outline" id="ls-clear">Clear</button></div>
      </form>
      <p class="ls-count" id="ls-count" role="status" aria-live="polite">Loading listings…</p>
      <div class="ls-grid" id="ls-results"></div>
      <div class="ls-more-wrap"><button type="button" class="btn btn-outline" id="ls-more" hidden>{spec["more"]}</button></div>
    </div>
  </section>
</div>

<div id="ls-detail" hidden>
  <section class="section" style="padding-top:28px">
    <div class="container">
      <p class="ls-back"><a href="{spec["file"]}" id="ls-back">← Back to search</a></p>
      <div class="ls-detail-grid">
        <div>
          <div class="ls-frame" id="ls-photo"></div>
          <div class="ls-thumbs" id="ls-thumbs"></div>
          <div class="ls-photo-nav">
            <button type="button" class="btn btn-outline" id="ls-prev">Previous photo</button>
            <button type="button" class="btn btn-outline" id="ls-next">Next photo</button>
          </div>
        </div>
        <div>
          <p class="ls-price" id="ls-price"></p>
          <h2 id="ls-heading" tabindex="-1"></h2>
          <p class="ls-meta" id="ls-meta"></p>
          <p class="ls-broker" id="ls-broker"></p>
          <p class="ls-agent" id="ls-agent"></p>
          <p id="ls-realtor-link"></p>
          <div id="ls-badge"></div>
          <div class="ls-facts" id="ls-facts"></div>
        </div>
      </div>
      <div class="ls-remarks" id="ls-remarks"></div>

      <div class="ls-inquiry">
        <h2>{spec["ask"]}</h2>
        <p class="lead">{ask_lead}</p>
        <form class="form-card" data-form-key="{spec["form_key"]}" action="#" method="POST">
          <input type="hidden" name="_subject" value="{spec["subject"]}">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="form" value="{spec["form_name"]}">
          <input type="hidden" name="listing_id" id="inq-id">
          <input type="hidden" name="listing_mls" id="inq-mls">
          <input type="hidden" name="listing_address" id="inq-address">
          <input type="hidden" name="listing_url" id="inq-url">
          <div class="hp" aria-hidden="true"><label>Leave this field empty <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
          <div class="form-grid cols-2">
            <div class="field"><label for="inq-name">Full name <span class="req">*</span></label><input id="inq-name" name="name" autocomplete="name" required></div>
            <div class="field"><label for="inq-email">Email <span class="req">*</span></label><input id="inq-email" name="email" type="email" autocomplete="email" required></div>
            <div class="field"><label for="inq-phone">Phone</label><input id="inq-phone" name="phone" type="tel" autocomplete="tel"></div>
            <div class="field full"><label for="inq-notes">Message</label><textarea id="inq-notes" name="message" placeholder="{spec["placeholder"]}"></textarea></div>
            <div class="field full">
              <div class="checks"><label style="background:none;border:0;padding:0;align-items:flex-start"><input type="checkbox" name="consent" value="yes" required style="margin-top:4px"> <span>I agree to be contacted by Devin Desaulniers ({BROKERAGE}) by email or phone {spec["consent"]}. I can opt out at any time. <span class="req">*</span></span></label></div>
            </div>
            <div class="full">
              <button type="submit" class="btn btn-primary">Send inquiry</button>
              <div class="form-status" role="status" aria-live="polite"></div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </section>
</div>

<section class="section section--grey ls-legal">
  <div class="container narrow-wide">
    <h2>Listing data</h2>
    <p><strong>{BROKERAGE}</strong> operates this website. Devin Desaulniers is a Real Estate Associate with {BROKERAGE}, {BROKERAGE_ADDR}, and a member of The Canadian Real Estate Association.</p>
    <p>Trademarks are owned or controlled by The Canadian Real Estate Association (CREA) and identify real estate professionals who are members of CREA (REALTOR®) and/or the quality of services they provide (MLS®).</p>
    <p>The listing information is deemed reliable but is not guaranteed. The information contained on this site is based in whole or in part on information that is provided by members of The Canadian Real Estate Association (CREA), who are responsible for its accuracy. REALTOR.ca Canada Inc. reproduces and distributes this information as a service for its members and neither CREA nor REALTOR.ca Canada Inc. assumes responsibility for its accuracy.</p>
    <p>The listing content on this website is protected by copyright and other laws, and is intended solely for the private, non-commercial use by individuals. Any other reproduction, distribution or use of the content, in whole or in part, is specifically forbidden. The prohibited uses include commercial use, “screen scraping”, “database scraping”, and any other activity intended to collect, store, reorganize or manipulate data on the pages produced by or displayed on this website.</p>
    <p>Each listing shows the listing brokerage and a “Powered by REALTOR.ca” mark that links to that listing on REALTOR.ca. {spec["closed"]} Opening a listing sends a view event to the CREA DDF® Analytics Web Service. By using this search you accept these terms.</p>
  </div>
</section>
<script src="assets/js/listings.js" data-mode="{mode}" data-feed="{spec["feed"]}" data-sample="{spec["sample"]}"></script>
<noscript><div class="container"><p>This search needs JavaScript to filter the listing file in your browser.</p></div></noscript>
"""
    html += foot()
    return html
