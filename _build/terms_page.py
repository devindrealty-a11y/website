"""Terms of use for the weekly rent report dataset.

This is the URL in the Dataset license field. It is a custom terms page,
not a Creative Commons license. Listing records stay with the boards.
"""
from partials import (
    BROKERAGE_PHONE,
    BROKERAGE_TEL,
    EMAIL,
    ICONS,
    PHONE,
    TEL,
    foot,
    head,
)

PAGE = "terms.html"


def render():
    page = head(
        "Terms of use | Devin Desaulniers, Axford Real Estate",
        "How the weekly Greater Vancouver rent report may be used. Listing data is provided through the CREA DDF® and is owned by the respective boards.",
        "terms",
        page_url=PAGE,
    )
    page += f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Terms of use</span>
    <h1>Weekly rent report terms of use</h1>
    <p class="lead">These terms apply to the weekly rent report on this site. They are the license for that report. They are not a Creative Commons license, and they do not put the listing data in the public domain.</p>
  </div>
</section>

<section class="section">
  <div class="container narrow-wide">
    <div class="post-body">
      <p>Published October 20, 2026. This page is the terms of use for the <a href="rent-report.html">Moving to Greater Vancouver: Weekly Rent Report</a>, including the weekly figures saved with that report.</p>

      <h2>What the report is</h2>
      <p>I compile the report: median and average asking rents, listing counts, and the change from the previous week for Greater Vancouver. The figures are asking rents on active residential listings. They are not rents on signed leases, and they are not guaranteed.</p>

      <h2>Who owns the listing data</h2>
      <p>The homes behind those figures are listing data provided through the CREA Data Distribution Facility (DDF®), the REALTOR.ca feed. That listing data is owned by the respective real estate boards and their members. Devin Desaulniers and Axford Real Estate do not own the listing records, photographs, or remarks, and these terms do not grant any right in them.</p>
      <p>REALTOR® and MLS® are trademarks owned or controlled by The Canadian Real Estate Association (CREA).</p>

      <h2>What you may do</h2>
      <p>You may read the report on this website and share a link to it. You may quote a summary figure — a median, an average, or a count — with a link back to the report, for private, non-commercial commentary.</p>

      <h2>What you may not do</h2>
      <p>You may not copy the listing records, photographs, or remarks, and you may not build another database from them. Screen scraping and database scraping of this site, the report, and the homes for sale and homes for rent pages are not allowed. Commercial use of the listing content is not allowed. Those limits are the same ones that already apply to listing content on this site under the CREA DDF® rules.</p>
      <p>The summary tables are my compilation for readers of this site. Quoting a figure does not include a right to reuse the underlying board data.</p>

      <h2>Questions</h2>
      <p>Questions about these terms can come to me at my brokerage:</p>
    </div>
    <ul class="contact-list">
      <li><span class="cl-icon">{ICONS["building"]}</span><div><small>Mailing address</small><span>Devin Desaulniers<br>Axford Real Estate<br>2326 Clarke St<br>Port Moody, BC <span class="nw">V3H 1Y8</span></span></div></li>
      <li><span class="cl-icon">{ICONS["mail"]}</span><div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
      <li><span class="cl-icon">{ICONS["phone"]}</span><div><small>Brokerage office</small><a href="{BROKERAGE_TEL}">{BROKERAGE_PHONE}</a></div></li>
      <li><span class="cl-icon">{ICONS["phone"]}</span><div><small>Direct line (call or text)</small><a href="{TEL}">{PHONE}</a></div></li>
    </ul>
  </div>
</section>
"""
    page += foot()
    return page
