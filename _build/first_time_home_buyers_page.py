"""First-time home buyers page: GST rebate and B.C. property transfer tax.

Numbers are from CRA, Finance Canada, and gov.bc.ca, checked November 28, 2026.
Copy rules: write "Tri-Cities, BC". Do not use "best", "top", or "expert".
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from partials import EMAIL, PHONE, TEL, foot, head

PAGE = "first-time-home-buyers.html"
AS_OF = "November 28, 2026"

FAQS = [
    (
        "Is the federal GST rebate for first-time buyers law?",
        "Yes. Bill C-4, the Making Life More Affordable for Canadians Act, received Royal Assent on March 12, 2026. The Canada Revenue Agency said on March 17, 2026 that it is accepting applications. On a new home with a price of $1 million or less, an eligible buyer can get back up to 100% of the GST, to a maximum of $50,000. The rebate shrinks between $1 million and $1.5 million, and it is $0 at $1.5 million or more.",
    ),
    (
        "Does the GST rebate apply to a resale home?",
        "No. The First-Time Home Buyers' GST/HST rebate is for a newly built or substantially renovated home that will be your primary residence. A resale home is not charged GST in the usual sale, so there is no GST rebate to claim.",
    ),
    (
        "How much property transfer tax is charged on an $800,000 resale home?",
        "Using the general rates, the tax is $14,000: 1% of the first $200,000 is $2,000, and 2% of the remaining $600,000 is $12,000. A qualifying first-time buyer gets an $8,000 exemption at that price and pays $6,000. Those figures match the Province's exemption table.",
    ),
    (
        "Does a first-time buyer pay no property transfer tax on a home up to $835,000?",
        "Not always. If the fair market value is $500,000 or less, a qualifying buyer can be exempt from the full tax. From above $500,000 up to $835,000, the exemption is $8,000, which is the tax on the first $500,000. You still pay the tax on the rest. Between $835,000 and $860,000 the $8,000 shrinks, and at $860,000 there is no exemption.",
    ),
    (
        "What if the home is newly built?",
        "A separate newly built home exemption can remove the property transfer tax when the fair market value is $1,100,000 or less. It shrinks between $1,100,000 and $1,150,000, and it is gone at $1,150,000. You do not have to be a first-time buyer. At $1,100,000 the tax before the exemption is $20,000, and a full exemption brings it to $0.",
    ),
    (
        "Can I use a First Home Savings Account and the RRSP Home Buyers' Plan for the same home?",
        "Yes, if you meet the rules for each one. An FHSA lets you contribute up to $8,000 in the year you open it, with a $40,000 lifetime limit. A qualifying withdrawal is tax-free. The Home Buyers' Plan lets you withdraw up to $60,000 from your RRSPs. For a first withdrawal in 2026, 2027, or 2028, repayment starts in the fifth year after the withdrawal.",
    ),
    (
        "Is the estimator on this page my tax bill?",
        "No. It is an estimate of B.C. property transfer tax from the published rates and exemptions, using the price and the two yes-or-no answers you enter. It assumes a fully residential property of 0.5 hectares or smaller and a buyer who meets the other legal tests. Your lawyer or notary calculates the tax when the home is registered.",
    ),
]


def faq_jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in FAQS
        ],
    }
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + "\n</script>"


def faq_html():
    parts = []
    for q, a in FAQS:
        parts.append(f'<div class="faq-item"><h3>{q}</h3><div class="ans"><p>{a}</p></div></div>')
    return "".join(parts)


BODY = """
<section class="page-hero ftb-hero-photo">
  <img class="ftb-hero-bg" src="assets/img/blog/photos/vancouver-skyline-queen-elizabeth-park.jpg" alt="Downtown Vancouver and the North Shore mountains, from Queen Elizabeth Park">
  <div class="ftb-hero-shade" aria-hidden="true"></div>
  <div class="container">
    <span class="eyebrow">First home · British Columbia</span>
    <h1>The taxes on a first home in BC</h1>
    <p class="lead">Two amounts can change the cash you need up front: the federal GST on a new home, and B.C. property transfer tax. This page uses the government rules as of November 28, 2026. Devin Desaulniers is a Real Estate Associate with Axford Real Estate in the Tri-Cities, BC.</p>
    <div class="ftb-stats">
      <div class="ftb-stat"><strong>$50,000</strong><span>Maximum federal GST rebate on a new home with a price of $1&nbsp;million or less.</span></div>
      <div class="ftb-stat"><strong>$8,000</strong><span>First-time property transfer tax exemption on a resale home over $500,000 and up to $835,000.</span></div>
      <div class="ftb-stat"><strong>$0</strong><span>Property transfer tax on a qualifying newly built home of $1.1&nbsp;million or less.</span></div>
    </div>
    <p class="hero-note">This is not tax or legal advice. Confirm the numbers with your lawyer, notary, or accountant before you rely on them.</p>
    <div class="btn-row">
      <a class="btn btn-light" href="#guide">Get the free First-Time Buyer guide</a>
      <a class="btn btn-ghost-light" href="#estimator">Estimate the transfer tax</a>
    </div>
  </div>
  <p class="ftb-hero-cap">Downtown Vancouver and the North Shore mountains, from Queen Elizabeth Park. Photo: Kyle Pearce / <a href="https://commons.wikimedia.org/wiki/File:Vancouver_Skyline_and_Mountains.jpg" target="_blank" rel="noopener">Wikimedia Commons</a> (CC BY-SA 2.0).</p>
</section>

<section class="section">
  <div class="container">
    <div class="guide-intro">
      <div>
        <span class="eyebrow">Start here</span>
        <h2>Three programs, three different tests</h2>
        <p class="lead guide-lead">A resale home and a new home are taxed differently. The GST rebate is federal and only for a new home. Property transfer tax is provincial and has two exemptions that do not work the same way.</p>
        <p>I work with buyers in Coquitlam, Port Coquitlam, Port Moody, and the rest of Greater Vancouver. The thresholds below are province-wide and federal. They are not a quote for a specific home.</p>
      </div>
      <figure class="ftb-photo">
        <img src="assets/img/guides/coquitlam-2018.jpg" width="1600" height="1067" alt="Houses and towers in Coquitlam, with the North Shore mountains behind them" decoding="async">
        <figcaption>Coquitlam, May 2018. Photo: Alex of Canada / <a href="https://commons.wikimedia.org/wiki/File:Coquitlam_from_Westwood_Plateau_March_12_2018.jpeg" target="_blank" rel="noopener">Wikimedia Commons</a> (CC BY-SA 4.0).</figcaption>
      </figure>
    </div>
    <div class="money-grid">
      <article class="money-card">
        <h3>GST on a new home</h3>
        <p class="money-fig">Up to $50,000</p>
        <p>In force. A full rebate of the GST, capped at $50,000, when the price is $1&nbsp;million or less. It shrinks after that and ends at $1.5&nbsp;million. Resale homes do not qualify.</p>
      </article>
      <article class="money-card">
        <h3>First-time transfer tax</h3>
        <p class="money-fig">$8,000 off</p>
        <p>On a resale home over $500,000 and up to $835,000, the exemption is $8,000. That is the tax on the first $500,000. You still pay tax on the rest of the price.</p>
      </article>
      <article class="money-card">
        <h3>New-home transfer tax</h3>
        <p class="money-fig">Often $0</p>
        <p>The newly built home exemption can remove the whole property transfer tax at $1.1&nbsp;million or less. You do not have to be a first-time buyer.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--paper" id="gst">
  <div class="container narrow-wide">
    <span class="eyebrow">Federal · in force</span>
    <h2>GST relief for a first home that is new</h2>
    <p>Bill C-4 received Royal Assent on March 12, 2026. The Canada Revenue Agency said on March 17, 2026 that it is accepting the First-Time Home Buyers' GST/HST rebate. This is law, not a proposal.</p>
    <p>In British Columbia a new home is charged 5% GST. B.C. does not add provincial HST on that purchase. The rebate gives back the GST (or, in HST provinces, the federal part of the HST). The CRA's published example: a new home priced at $1.25&nbsp;million is the midpoint between $1&nbsp;million and $1.5&nbsp;million, so the rebate is 50% of the $50,000 maximum, which is $25,000.</p>
    <div class="example-grid">
      <div class="example-card"><span class="ex-label">$1 million or less</span><strong>Up to 100%</strong><p>Of the GST you paid, to a maximum rebate of $50,000.</p></div>
      <div class="example-card"><span class="ex-label">$1.25 million</span><strong>$25,000</strong><p>The CRA's midpoint example. Half of the $50,000 maximum.</p></div>
      <div class="example-card"><span class="ex-label">$1.5 million or more</span><strong>$0</strong><p>No First-Time Home Buyers' GST/HST rebate.</p></div>
    </div>
    <h3>Who can claim it</h3>
    <ul class="list-check">
      <li>You are 18 or older, and a Canadian citizen or permanent resident.</li>
      <li>The home is newly built or substantially renovated, and it will be your primary residence. You are the first person to live in it after that work.</li>
      <li>You, and your spouse or common-law partner if you have one, did not live in a home that either of you owned in the year you buy it, or in the four calendar years before that.</li>
      <li>For a home bought from a builder, the purchase agreement is dated on or after March 20, 2025, and before 2031. The date you both agreed is the one that counts, not the later date when conditions are waived.</li>
      <li>If more than one person is on title, only one person claims the rebate, and that person has to be a first-time buyer under this test. A parent on title who already owns a home does not block the claim by itself.</li>
    </ul>
    <p>There is also the older GST/HST new housing rebate. It is 36% of the GST, to a maximum of $6,300, when the home is $350,000 or less. It shrinks between $350,000 and $450,000, and it is $0 at $450,000 or more. On a home of $450,000 or less, the two rebates together can return all of the GST. You do not get the $6,300 as well as a full GST refund. Most new homes in the Tri-Cities, BC are over $450,000, so the older rebate is often $0 and the new first-time rebate is the one that matters.</p>
    <p>An assignment of a contract that was signed before March 20, 2025 does not create a new agreement date for this rebate. The CRA memorandum walks through that case. If your contract date is close to the cutoff, ask your lawyer to read it before you count on the rebate.</p>
    <p class="form-note">Sources, checked November 28, 2026: <a href="https://www.canada.ca/en/department-finance/news/2026/03/legislation-to-make-life-more-affordable-receives-royal-assent.html" target="_blank" rel="noopener">Finance Canada, Royal Assent, March 12, 2026</a>; <a href="https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/gst-hst-rebates/first-time-home-buyers-gst-hst-rebate/what-rebate.html" target="_blank" rel="noopener">CRA, what the rebate is</a>; <a href="https://www.canada.ca/en/revenue-agency/services/forms-publications/publications/19-3-10/first-time-home-buyers-gst-hst-rebate.html" target="_blank" rel="noopener">GST/HST Memorandum 19-3-10 (October 2026)</a>.</p>
  </div>
</section>

<section class="section" id="ptt">
  <div class="container">
    <span class="eyebrow">British Columbia</span>
    <h2>Property transfer tax, in cards</h2>
    <p class="lead">This is a one-time tax when the home is registered. It is not the yearly property tax bill from the city. The general rates, from the Province, are:</p>
    <div class="rate-grid">
      <div class="rate-card"><strong>1%</strong><span>On the first $200,000 of fair market value.</span></div>
      <div class="rate-card"><strong>2%</strong><span>On the portion above $200,000, up to $2&nbsp;million.</span></div>
      <div class="rate-card"><strong>3%</strong><span>On the portion above $2&nbsp;million.</span></div>
      <div class="rate-card"><strong>+2%</strong><span>A further 2% on the residential value above $3&nbsp;million.</span></div>
    </div>
    <h3 class="sub-h">A resale home at $800,000</h3>
    <p>This price is in the Province's own exemption table. The home is under $2&nbsp;million, so only the 1% and 2% bands apply.</p>
    <div class="example-grid">
      <div class="example-card"><span class="ex-label">1% of the first $200,000</span><strong>$2,000</strong><p>$200,000 × 1%.</p></div>
      <div class="example-card"><span class="ex-label">2% of the next $600,000</span><strong>$12,000</strong><p>$600,000 × 2%.</p></div>
      <div class="example-card example-total"><span class="ex-label">Tax before any exemption</span><strong>$14,000</strong><p>$2,000 + $12,000. The Province's table shows the same $14,000.</p></div>
    </div>
    <p>If you qualify for the First Time Home Buyers' Program, the exemption at $800,000 is $8,000. You pay <strong>$6,000</strong>. The same table lists that $6,000 as the tax payable.</p>
    <p>If that $800,000 home is newly built and you qualify for the newly built home exemption instead, the tax payable is <strong>$0</strong>. The new-home exemption removes the whole tax at this price. The first-time program would have left $6,000.</p>
    <p class="form-note">Fair market value is the price a willing buyer would pay a willing seller on the registration date. The general rates and the further 2% are on the <a href="https://www2.gov.bc.ca/gov/content/taxes/property-taxes/property-transfer-tax" target="_blank" rel="noopener">property transfer tax page</a> (updated December 3, 2025). The $4.5&nbsp;million worked example on the Province's calculation page, updated November 26, 2024, is how the further 2% is applied. Checked November 28, 2026.</p>
  </div>
</section>

<section class="section section--paper" id="exemptions">
  <div class="container narrow-wide">
    <span class="eyebrow">Two exemptions</span>
    <h2>First-time buyers, and newly built homes</h2>
    <div class="ftb-two">
      <div>
        <h3>First Time Home Buyers' Program</h3>
        <p>This can apply to a resale home or a new home. To qualify when the home is registered you generally must:</p>
        <ul class="list-check">
          <li>Be a Canadian citizen or permanent resident.</li>
          <li>Have lived in B.C. for at least a year immediately before registration, or have filed at least 2 income tax returns as a B.C. resident in the last 6 tax years.</li>
          <li>Never have owned a principal residence anywhere in the world, and never have received this exemption or a refund of it before.</li>
          <li>Use the property only as your principal residence. It must be 0.5 hectares (1.24 acres) or smaller and contain only a home.</li>
        </ul>
        <p>You move in within 92 days and keep it as your principal residence through the first year, or you can lose part of the exemption.</p>
        <p>Amounts for a registration on or after April 1, 2024, when you own 100% and the lot is under 0.5 hectares:</p>
        <ul>
          <li>$500,000 or less: the full tax is exempt.</li>
          <li>Over $500,000 up to $835,000: the exemption is $8,000.</li>
          <li>Over $835,000 and under $860,000: the $8,000 shrinks in proportion to how close the price is to $860,000.</li>
          <li>$860,000: no exemption.</li>
        </ul>
      </div>
      <div>
        <h3>Newly built home exemption</h3>
        <p>This is separate. You do not have to be buying for the first time. The home must be newly built and not yet lived in, registered after February 16, 2016, and this must be the first registration after the home was completed. You must be a Canadian citizen or permanent resident, and the home must be your principal residence, in B.C., on 0.5 hectares or less.</p>
        <p>For a registration on or after April 1, 2024:</p>
        <ul>
          <li>$1,100,000 or less: the full property transfer tax is exempt. At $1,100,000 that tax is $20,000, so the exemption is $20,000 and the tax payable is $0.</li>
          <li>Over $1,100,000 and under $1,150,000: the exemption shrinks. The Province's formula is the tax, multiplied by ($1,150,000 minus the price) divided by $50,000.</li>
          <li>$1,150,000: no exemption. The tax at that price is $21,000.</li>
        </ul>
        <p>You move in within 92 days and occupy the home for the rest of the first year.</p>
        <p>On a new home under $1.1&nbsp;million, this exemption removes more tax than the first-time program. The estimate on this page uses it when you say the home is a new build and the price still qualifies.</p>
      </div>
    </div>
    <p class="form-note">If only some of the buyers qualify, or the lot is larger than 0.5 hectares, the exemption is smaller. Foreign buyers can also owe an additional property transfer tax in specified areas of B.C. The rate and the map are on the Province's additional-tax page. This page does not add that tax. Sources: <a href="https://www2.gov.bc.ca/gov/content/taxes/property-taxes/property-transfer-tax/exemptions/first-time-home-buyers" target="_blank" rel="noopener">First Time Home Buyers' Program</a> (updated June 20, 2025), <a href="https://www2.gov.bc.ca/gov/content/taxes/property-taxes/property-transfer-tax/exemptions/first-time-home-buyers/current-amount" target="_blank" rel="noopener">exemption amounts</a> (updated December 3, 2025), <a href="https://www2.gov.bc.ca/gov/content/taxes/property-taxes/property-transfer-tax/exemptions/newly-built-home-exemption" target="_blank" rel="noopener">newly built home exemption</a> (updated January 6, 2026), and <a href="https://www2.gov.bc.ca/gov/content/taxes/property-taxes/property-transfer-tax/exemptions/newly-built-home-exemption/exemption-amounts" target="_blank" rel="noopener">newly built amounts</a> (updated December 3, 2025).</p>
  </div>
</section>

<section class="section" id="estimator">
  <div class="container narrow">
    <span class="eyebrow">Estimate</span>
    <h2>A simple property transfer tax estimate</h2>
    <p>Type a price and answer two questions. The result uses the rates and exemptions above. It is an estimate, not a tax assessment.</p>
    <form id="ptt-estimator" class="form-card ptt-form">
      <div class="field">
        <label for="ptt-price">Price (fair market value)</label>
        <input id="ptt-price" name="price" inputmode="decimal" autocomplete="off" placeholder="800000">
      </div>
      <fieldset>
        <legend>Are you a first-time buyer under the B.C. program?</legend>
        <div class="choice-row">
          <label><input type="radio" name="first" value="yes"> Yes</label>
          <label><input type="radio" name="first" value="no" checked> No</label>
        </div>
      </fieldset>
      <fieldset>
        <legend>Is it a newly built home?</legend>
        <div class="choice-row">
          <label><input type="radio" name="newbuild" value="yes"> Yes</label>
          <label><input type="radio" name="newbuild" value="no" checked> No</label>
        </div>
      </fieldset>
      <div id="ptt-result" class="ptt-result" aria-live="polite"></div>
    </form>
    <p class="ftb-disclaimer">Not tax or legal advice. Confirm the tax, and whether you qualify, with your lawyer, notary, or accountant. Rules and thresholds were checked on November 28, 2026 and can change.</p>
  </div>
</section>

<section class="section section--paper" id="savings">
  <div class="container narrow-wide">
    <span class="eyebrow">Saving the down payment</span>
    <h2>FHSA and the RRSP Home Buyers' Plan</h2>
    <div class="ftb-two">
      <div>
        <h3>First Home Savings Account</h3>
        <p>In the year you open your first FHSA, your participation room is $8,000. That room covers contributions and transfers from an RRSP, combined. Over your lifetime, contributions are capped at $40,000. Money you put in can be deducted on your tax return. A qualifying withdrawal to buy your first home is tax-free. Unused room can carry forward. The exact room for a later year is in your CRA account, because the formula also looks at excess amounts.</p>
      </div>
      <div>
        <h3>Home Buyers' Plan</h3>
        <p>You can withdraw up to $60,000 from your RRSPs. You pay it back over 15 years. For a first withdrawal between January 1, 2026 and December 31, 2028, the CRA says repayment starts in the fifth year after the year of the withdrawal. A 2026 withdrawal starts repayment in 2031. You can use an FHSA withdrawal and a Home Buyers' Plan withdrawal for the same home if you qualify for both.</p>
      </div>
    </div>
    <h3>The mortgage stress test, in short</h3>
    <p>For an uninsured mortgage from a federally regulated lender, OSFI's minimum qualifying rate is the greater of your contract rate plus 2 percentage points, or 5.25%. OSFI reviews that floor and that buffer at least once a year. The page stating the current rate does not set a different number. OSFI does not require that set rate when you switch an uninsured mortgage to another federally regulated lender at renewal, if the loan amount and the amortization do not go up. Insured mortgages follow the federal mortgage-insurance rules. Your lender applies the test that fits your loan. I am not a mortgage broker, and this is not an approval.</p>
    <p class="form-note"><a href="https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/first-home-savings-account/contributing-your-fhsa.html" target="_blank" rel="noopener">CRA, FHSA contributions</a>. <a href="https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/rrsps-related-plans/what-home-buyers-plan.html" target="_blank" rel="noopener">CRA, Home Buyers' Plan</a>. <a href="https://www.osfi-bsif.gc.ca/en/supervision/financial-institutions/banks/minimum-qualifying-rate-uninsured-mortgages" target="_blank" rel="noopener">OSFI, minimum qualifying rate for uninsured mortgages</a>. Checked November 28, 2026.</p>
  </div>
</section>

<section class="section section--paper" id="faq">
  <div class="container narrow-wide">
    <span class="eyebrow">FAQ</span>
    <h2>Questions first-time buyers ask</h2>
    <div class="faq-list">__FAQ__</div>
  </div>
</section>

<section class="section" id="more">
  <div class="container narrow-wide">
    <span class="eyebrow">Keep going</span>
    <h2>The rest of the buying path</h2>
    <p>Neighbourhood notes, illustrative bank rates, and homes for sale are on the <a href="buyers.html">buyers page</a>, the <a href="mortgage-rates.html">mortgage rates</a> page, and <a href="listings.html">homes for sale</a>. A shorter question list is on <a href="first-time-buyers-tri-cities-bc.html">first-time buyer questions for the Tri-Cities, BC</a>. Monthly costs after you own are on <a href="true-cost-of-owning-a-home-bc.html">the true cost of owning a home in BC</a>.</p>
  </div>
</section>

<section class="section section--tint" id="guide">
  <div class="container narrow">
    <span class="eyebrow">Free PDF</span>
    <h2>Get the free First-Time Buyer guide by email</h2>
    <p>The guide is 9 pages: the GST rebates, both property transfer tax exemptions with a new-home example and a resale example, the FHSA, the RRSP Home Buyers' Plan, the stress test, a closing-cost checklist, the steps to buy in B.C., and the sources. Devin Desaulniers, Real Estate Associate, Axford Real Estate, will email you. Your address is not sold.</p>
    <form id="ftb-guide" class="form-card" action="#" method="post" data-pdf="assets/guides/first-time-home-buyer-guide-bc.pdf">
      <div class="hp" aria-hidden="true"><label>Leave this field empty <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
      <div class="form-grid cols-2">
        <div class="field">
          <label for="ftb-name">Your name <span class="req">*</span></label>
          <input id="ftb-name" name="name" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="ftb-email">Your email <span class="req">*</span></label>
          <input id="ftb-email" name="email" type="email" autocomplete="email" required>
        </div>
        <div class="field full">
          <label class="consent"><input type="checkbox" name="consent" value="yes" required> <span>I agree to be contacted by Devin Desaulniers (Axford Real Estate) by email about this guide. I can opt out at any time. <span class="req">*</span></span></label>
        </div>
        <div class="full">
          <button type="submit" class="btn btn-primary">Email me the guide</button>
          <div class="form-status" role="status" aria-live="polite"></div>
        </div>
      </div>
      <p class="form-note">This form is emailed to devin@axfordrealestate.ca. It is not sent to a mailing list. The PDF link appears here after the form is sent.</p>
    </form>
    <p class="ftb-disclaimer">Not tax or legal advice. Confirm the rules with your lawyer, notary, or accountant. Axford Real Estate, 2326 Clarke St, Port Moody, BC. Call or text <a href="__TEL__">__PHONE__</a>.</p>
  </div>
</section>
"""


def render():
    extra = faq_jsonld() + '\n<script src="assets/js/first-time-buyers.js" defer></script>'
    html = head(
        "First-time home buyers in BC: GST and property transfer tax | Devin Desaulniers, Axford Real Estate",
        "GST rebate and B.C. property transfer tax for first-time buyers, with the thresholds in force on November 28, 2026. Devin Desaulniers, Real Estate Associate, Axford Real Estate, Tri-Cities, BC.",
        "ftb",
        og_image="assets/img/blog/photos/vancouver-skyline-queen-elizabeth-park.jpg",
        page_url=PAGE,
        extra_head=extra,
    )
    body = BODY.replace("__FAQ__", faq_html()).replace("__TEL__", TEL).replace("__PHONE__", PHONE)
    html += body
    html += foot()
    return str(html)


if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dest = os.path.join(root, PAGE)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(render())
    print(dest)
