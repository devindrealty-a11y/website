# Creative briefs

Parent: [README](README.md). Which file runs on which ad: [meta-ads.md](meta-ads.md).

Launch does not depend on a new shoot. The homepage already has a 32-second relocation video. Two static cards, exported from the brand colours below, cover the rest. A 9:16 cut is a week-two improvement, not a launch blocker.

## Brand

Sampled from the live site stylesheet.

| Role | Value |
| --- | --- |
| Ink (headlines) | `#132639` |
| Night (hero bands) | `#0d1b2a` |
| Blue accent | `#3474b6` (large areas and icons, not small text on white) |
| Blue for small text | `#24578c` |
| Paper background | `#f4f6f8` |
| Body text | `#27333f` |
| Display face | Newsreader, or a similar old-style serif if the export tool lacks it |
| Name and buttons | Montserrat |
| Body | Inter |

Logo files already in the repo: `assets/img/devin-mark.png`, `assets/img/devin-logo.png`, `assets/img/axford-logo.png`. Headshot: `assets/img/devin-headshot-800.jpg`. Black-and-white alternate: `assets/img/devin-bw-720.jpg`.

Every static includes, in readable type:

- Devin Desaulniers
- Real Estate Associate
- Axford Real Estate

The Axford mark stays intact. Do not recolour it or place it on a busy photo where the wordmark disappears.

## Assets already cleared to use

| Asset | Path | Use |
| --- | --- | --- |
| Relocation video, 1280×720, H.264, about 32 seconds, with a poster frame | `assets/video/greater-vancouver-relocation-ad.mp4` and `greater-vancouver-relocation-ad-poster.jpg` | Primary video for T1–T3. It is the same file as the homepage "Moving to Greater Vancouver?" section. |
| Colour headshot | `assets/img/devin-headshot-800.jpg` | Static cards. |
| Axford logo | `assets/img/axford-logo.png` | End card and the lower corner of statics. |

## Assets that stay out of the ads

- Photos, addresses, and prices from `listings/data.json`, `listings/rentals.json`, or any REALTOR.ca page. Those are other brokerages' listings. The DDF feed on `rentals.html` and `listings.html` is for the website search, not for ad creative.
- The six YouTube property tours. The site is explicit that they are video tours, not Devin's listings, and they are never labelled for sale or sold. Running one as an ad would read as "this home is available through me."
- Named Google reviews (Susan M., Hugo K., Thurza A., and the others). They are published on the site as reviews. They are not cleared here as paid-ad endorsements. Leave names and quotations out of the images and the primary text.
- Star counts, until they are re-counted the week of launch. The site shows Devin at 5.0 from 15 Google reviews as of October 3, 2026, and Axford at 148 five-star reviews as of October 2, 2026. Both will have moved by November 1. If a fresh count is done, a line such as "5.0 on Google" can be added to a card. If it is not done, the cards below ship without a number.
- Stock photos of "happy families", keys in a hand, or the Vancouver skyline from a library that the license does not cover for ads. The headshot and the existing video are enough.
- Any line about family status, age, or who a neighbourhood is for ("perfect for young professionals", "ideal for families").

## Video — tenant, from the file you already have

**Source.** `assets/video/greater-vancouver-relocation-ad.mp4` (16:9, ~32s). Upload this as-is for in-feed on November 1.

**End card, if you re-export.** Last 3 seconds, night background `#0d1b2a`, white type:

- Line up your rental first
- Devin Desaulniers · Axford Real Estate
- $1,500 + GST · paid in two parts
- devindesaulniers.ca

**Captions.** Burned in, not only the platform's auto captions. Large enough for a phone with the sound off. The first caption restates the spoken hook. If the current file has no captions, launch it anyway and add a captioned export in the first week. Silence-off viewing is most of Stories and Reels.

**9:16 cut (week of November 9, not launch day).** Centre-crop or pad the same master to 1080×1920. Keep the face and the end card inside the middle 4:5, clear of the top 14% and bottom 20% where the interface covers Stories. 15 to 30 seconds. No new claims.

**4:5 feed cut (same week, if time).** 1080×1350, same rules.

Do not add music that the platform's music library then regional-blocks. The existing audio is the safe track.

## Static A — tenant fee card (4:5 and 1:1)

For T1–T3, alongside the video.

- Size: 1080×1350 and a 1080×1080 export.
- Background: `#0d1b2a`. Type: white. Accent rule: `#3474b6`.
- Left or lower third: headshot, cropped as a clean circle or a straight rectangle with no drop shadow heavier than the site's.
- Text, in this order, and no other claims:

```
Moving to Greater Vancouver?

Line up the rental before you arrive.

$1,500 + GST
$750 to start · $750 when you secure it

Devin Desaulniers
Real Estate Associate, Axford Real Estate
```

- The dollar figures must match the site. If the fee changes, the card changes the same day and the running ads are paused until it does.
- Logo: Axford mark on the paper-coloured footer strip `#f4f6f8`, full colour.

## Static B — rentals search card (4:5)

For T4 only, because that ad opens `rentals.html`.

```
Homes for rent
Greater Vancouver and the Fraser Valley

Search active listings.
Rent is shown per month.

Moving from away?
Tenant representation is $1,500 + GST.

Devin Desaulniers · Axford Real Estate
```

No photo of a specific home. A simple line drawing of a house, or the headshot, is the image. A screenshot of the live search page is acceptable if the addresses and photos are blurred or cropped out of frame. A screenshot that shows another brokerage's photo is not.

## Static C — buyer card (4:5 and 1:1)

For B1–B4. Make four exports that share the layout and swap only the first line, so each ad has its own file:

| File | First line |
| --- | --- |
| `buyer-b1.png` | Buying in the Tri-Cities, BC |
| `buyer-b2.png` | A clear plan for a first home |
| `buyer-b3.png` | Buying after a move |
| `buyer-b4.png` | Send me the listings you want |

Shared lines under that:

```
Coquitlam · Port Coquitlam · Port Moody
and Greater Vancouver

Devin Desaulniers
Real Estate Associate, Axford Real Estate
```

Background `#f4f6f8`, headlines `#132639`, a `#3474b6` rule, headshot, Axford mark. No sold price, no "I saved my client $X", no mortgage rate.

## Stories and Reels safe area

- 1080×1920.
- Keep type and the logo inside the central safe zone: about 250 px from the top and 320 px from the bottom.
- The fee, if shown, is in that safe zone, not in the corner the call-to-action button covers.

## File names to export

```
ads-creative/tenant-fee-4x5.png
ads-creative/tenant-fee-1x1.png
ads-creative/rentals-search-4x5.png
ads-creative/buyer-b1-4x5.png
ads-creative/buyer-b2-4x5.png
ads-creative/buyer-b3-4x5.png
ads-creative/buyer-b4-4x5.png
ads-creative/relocation-16x9.mp4          (copy of the existing master)
ads-creative/relocation-9x16-captioned.mp4 (week two)
```

Keep the exports outside the website repo, or in a folder you do not publish. They are ads, not new pages. This plan does not add image files to the site.

## Quality check before upload

- Name, designation, and Axford Real Estate are readable at phone width.
- Fee matches `tenants.html` that day.
- No other brokerage's photo, address, or price.
- No client name and no review quote.
- Captions exist on any video that will run in Stories or Reels after week one.
- The 16:9 master plays with sound and matches the homepage video, so the ad and the page do not tell two different stories.
