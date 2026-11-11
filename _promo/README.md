# Promotion kit

Unpublished working notes for Devin Desaulniers, REALTOR®, Real Estate Associate with Axford Real Estate in Port Moody. Nothing in this folder is a page on https://devindesaulniers.ca/.

| File | What it is |
| --- | --- |
| [meta-ads.md](meta-ads.md) | Facebook and Instagram plan at $5–$10 a day |
| [google-business-posts.md](google-business-posts.md) | Eight weekly Google Business Profile posts |
| [youtube.md](youtube.md) | Description footer, six tailored descriptions, pinned comment |
| [communities.md](communities.md) | Reddit and Facebook groups, with rules and five post drafts |
| [rollout.md](rollout.md) | Four-week checklist |

## Why this folder is not on the public site

This repository is published with GitHub Pages from the `main` branch. There is no `.nojekyll` file, so Pages builds the site with Jekyll.

Jekyll skips any file or folder whose name starts with `_`, `.`, `#`, or `~`, except its own special folders (`_posts`, `_layouts`, `_includes`, `_sass`, `_data`, `_drafts`, `_plugins`). `_promo` is not one of those, so Jekyll leaves it out of the published site. `_posts` and `_build` stay as they are: `_posts` is a Jekyll special folder, and `_build` is already skipped by the same underscore rule.

`_config.yml` in the repo root states the exclude again. In Jekyll, a custom `exclude` list replaces the built-in one, so that file repeats Jekyll's usual excludes and adds `_promo`.

Do not add a `.nojekyll` file to turn Jekyll off. With Jekyll off, GitHub Pages copies the repository as-is and `_promo` would become public. If a later change adds `.nojekyll`, move this folder out of the Pages publishing source first.

Checked against the repo on October 11, 2026: no `.nojekyll`, no previous `_config.yml`, Pages source is the repository root.

## Before anything goes live

Have Axford Real Estate's managing broker read the ad text, the YouTube footer, and any community post that names the service. The site still has a placeholder for the standard non-solicitation disclaimer. These drafts follow the public rules below. They are not a broker approval.

- Every advertisement names the brokerage **Axford Real Estate**, in full, where a reader can see it. A short form is not enough. On Meta, put it inside the first 125 characters of the primary text, because that is what shows before "See more."
- No "best," "top," "#1," or any other ranking of Devin or the brokerage.
- No promise of a rental, a price, or a sale result. The fee language matches the site: $1,500 + GST, paid by the tenant, $750 non-refundable at the start and $750 once a rental is secured. The second $750 is not owed if no rental is secured.
- The six YouTube tours are video tours. They are not listings he is offering for sale or for rent.
- Facts in the Google posts and community drafts come from the five posts already in `/blog`. Dates and figures are from those posts, not new research.
