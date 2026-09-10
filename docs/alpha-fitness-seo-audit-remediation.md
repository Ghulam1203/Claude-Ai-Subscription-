# Alpha Fitness — Technical SEO Audit Remediation Guide

**Site:** [myalphafitness.ca](https://myalphafitness.ca)  
**Original crawl:** September 4, 2026  
**Rechecked:** September 10, 2026  
**Audience:** Junior developer + content/SEO support  
**Purpose:** Fix every issue from the audit with clear steps, verification, and ownership

---

## How to use this document

1. Work **top to bottom by priority** (Critical → High → Medium → Low).
2. Mark each task **Done** only after completing the **Verification** step.
3. Content tasks (titles, descriptions, H1 copy) need SEO/content approval before deploy.
4. Do **not** change existing URL slugs unless explicitly noted — use redirects if a URL must change.

---

## Recheck summary (September 10, 2026)

| Finding (original audit) | Original status | Recheck status | Action still needed? |
|---|---|---|---|
| Zero structured data sitewide | Critical | **Partially fixed** — LocalBusiness, WebSite, Service on homepage; BlogPosting + FAQPage + BreadcrumbList on blog posts; Article + BreadcrumbList on service pages | **Yes** — roll out to all page types; validate in Rich Results Test |
| 130 pages with meta keywords | High | **Still open** — meta keywords present on homepage, about, blog, etc. | **Yes** — remove from template |
| 86 duplicate H1 tags | High | **Still open** — generic/section H1s still used on multiple templates | **Yes** |
| `fr/gear.php` 404 error | High | **Still open** — returns HTTP 404 | **Yes** — fix or 301 redirect |
| 70 titles over 60 characters | Medium | **Still open** | **Yes** — content rewrite |
| 61 meta descriptions over 155 chars | Medium | **Still open** | **Yes** — content rewrite |
| 4 duplicate page titles | Medium | **Still open** — e.g. both residential gym pages share title | **Yes** |
| 57 unsafe cross-origin links | Low | **Partially fixed** — some links have `noopener`; LinkedIn team links still missing it | **Yes** — template fix |
| 3 hreflang missing return links | Low | Not re-verified page-by-page | **Yes** — low priority cleanup |
| 70 images over 100KB | Low | Not re-measured | **Yes** — scheduled maintenance |
| 7 URLs with underscores | Low | Informational only | **No change to existing URLs** |

---

## Master issue tracker

| ID | Priority | Issue | Owner | Effort | Phase |
|---|---|---|---|---|---|
| SEO-001 | Critical | Complete structured data rollout (FAQ, Service, BreadcrumbList on all relevant pages) | Developer | 6–8 hrs | Week 2 |
| SEO-002 | High | Remove meta keywords from all pages | Developer | 1 hr | Week 1 |
| SEO-003 | High | Fix duplicate H1 tags (86 pages) | Dev + SEO | 1 day | Week 2–3 |
| SEO-004 | High | Fix or redirect broken `fr/gear.php` | Developer | 30 min | Week 1 |
| SEO-005 | Medium | Shorten page titles to 50–60 characters | SEO/Content | 4–6 hrs | Week 2 |
| SEO-006 | Medium | Shorten meta descriptions to 120–155 characters | SEO/Content | 3–4 hrs | Week 2 |
| SEO-007 | Medium | Resolve duplicate titles & meta descriptions | SEO/Content + Dev | 3 hrs | Week 1–2 |
| SEO-008 | Medium | Canonicalise news tag/filter URLs | Developer | 30 min | Week 1 |
| SEO-009 | Low | Add `rel="noopener noreferrer"` to external `target="_blank"` links | Developer | 1 hr | Week 3 |
| SEO-010 | Low | Fix 3 hreflang missing return/self links | Developer | 30 min | Week 3 |
| SEO-011 | Low | Compress images >100KB; add width/height where missing | Developer | 4–6 hrs | Quarter |
| SEO-012 | Low | Use hyphens in **new** URLs only | Developer | Ongoing | Ongoing |

---

## Detailed fix instructions

---

### SEO-001 — Structured data (schema markup)

**Original audit:** 0 pages with schema  
**Recheck:** Homepage and several templates already output JSON-LD. Blog posts include `BlogPosting`, `FAQPage`, and `BreadcrumbList`. Service pages include `Article` and `BreadcrumbList`. **Gap:** not consistent on every page type (facilities, gear, news listing, French equivalents).

#### Why it matters
Schema helps Google show rich results (FAQ accordions, breadcrumbs, local business panel).

#### Solution steps

**Step 1 — Audit current schema output**
```bash
# Run on any page URL
curl -s "https://myalphafitness.ca/PAGE.php" | grep -A2 'application/ld+json'
```
List which `@type` values appear per template (homepage, service, facility, blog, news index, gear, French mirror).

**Step 2 — Centralize JSON-LD in one include file**
- Create or extend something like `includes/schema.php` (or the existing SEO partial referenced in HTML comments: `<!-- SEO: Canonical, hreflang, OG, Twitter -->`).
- Output one `<script type="application/ld+json">` block per page using `@graph` (same pattern already used on homepage).

**Step 3 — Homepage (verify/enhance LocalBusiness)**
Ensure homepage JSON-LD includes:
- `@type`: `["Organization", "LocalBusiness"]`
- `name`, `url`, `logo`, `image`, `telephone`, `email`
- Full `PostalAddress` (Mascouche, QC)
- `geo`, `sameAs` (social profiles), `areaServed`, `priceRange`

**Step 4 — Service pages (6 pages)**
Add `Service` schema on:
- `commercial-gym-design.php`
- `corporate-gym-design.php`
- `boutique-gym-design.php`
- `hotel-condo-gym-design.php`
- `athletic-facility-design.php`
- French equivalents under `/fr/`

Example fields: `serviceType`, `provider` (link to `#organization`), `areaServed`, `description`.

**Step 5 — Blog posts (23 articles)**
For each article template (`blog-article.php` / French equivalent):
- Keep `BlogPosting` (or `Article`) with `headline`, `datePublished`, `dateModified`, `author`, `publisher`, `image`, `description`.
- Add `FAQPage` **only when the page has a visible FAQ section** — map each question/answer from the HTML into `mainEntity`.
- Add `BreadcrumbList`: Home → News → Article title.

**Step 6 — Facility pages**
Add `BreadcrumbList` on all facility case-study pages. Optionally use `@type: WebPage` with `about` describing the installation.

**Step 7 — Validate**
1. [Google Rich Results Test](https://search.google.com/test/rich-results) — test homepage, 1 service page, 1 facility page, 1 blog post (EN + FR).
2. Fix any errors (duplicate questions in FAQ, missing required fields, invalid dates).

#### Verification checklist
- [ ] Rich Results Test passes on 5 sample URLs (EN + FR)
- [ ] FAQ schema only on pages with visible FAQ content
- [ ] No duplicate/conflicting JSON-LD blocks with invalid JSON

---

### SEO-002 — Remove meta keywords (130 pages)

**Recheck:** Confirmed still present — 441-character boilerplate block on most pages.

#### Why it matters
Google ignores meta keywords since 2009. They add dead weight and look outdated.

#### Solution steps

**Step 1 — Find the template source**
Search the codebase:
```bash
grep -r 'meta name="keywords"' --include="*.php" .
```
Expected location: shared `<head>` partial (header include used by all PHP pages).

**Step 2 — Remove the tag from the template**
Delete the entire line:
```html
<meta name="keywords" content="..." />
```

**Step 3 — Remove page-level overrides**
Facility pages with custom keyword blocks (e.g. Treana, Liveo Mascouche) — remove those individual tags too.

**Step 4 — Deploy and spot-check**
```bash
curl -s "https://myalphafitness.ca/about.php" | grep 'meta name="keywords"'
# Should return nothing
```

#### Verification checklist
- [ ] Screaming Frog re-crawl shows **0** pages with meta keywords
- [ ] Spot-check 5 EN + 5 FR pages

---

### SEO-003 — Duplicate H1 tags (86 pages)

**Recheck:** Pages have an H1, but many share generic text (e.g. section labels like "OUR SERVICES" reused across templates).

#### Why it matters
H1 is the primary on-page topic signal. Duplicate H1s make pages look like duplicates to Google.

#### Solution steps

**Step 1 — Export duplicate H1 report from Screaming Frog**
Filter: HTML → H1 → sort by H1 text → find values used on more than one URL.

**Step 2 — Fix template-level duplicates (developer)**
- Ensure each page template pulls H1 from a **page-specific variable**, not a shared section heading.
- Example pattern in PHP:
```php
<h1><?= htmlspecialchars($pageH1) ?></h1>
```
- Set `$pageH1` per page file or from CMS/database.

**Step 3 — Write unique H1 copy (SEO/content)**
Rules:
- Exactly **one** H1 per page
- Unique across the site
- Contains primary keyword naturally
- Does not need to match `<title>` exactly

| Page type | Good H1 example |
|---|---|
| Commercial gym design | Commercial Gym Design in Quebec and Canada |
| Facility (Carabins) | Carabins UdeM High-Performance Athletic Centre |
| Blog post | Commercial Gym Equipment Cost in Canada: 2026 Budget Guide |
| Corporate gym | Corporate Gym Design for Canadian Workplaces |

**Step 4 — Fix common offenders first**
- Service landing pages using shared section H1
- Facility pages using brand-only H1
- News tag pages using same H1 as main news page

#### Verification checklist
- [ ] Screaming Frog: no H1 text appears on more than 1 URL (except intentional EN/FR pairs — those should still differ by language)
- [ ] Manual view-source: exactly one `<h1>` per page

---

### SEO-004 — Broken French page: `fr/gear.php`

**Recheck:** Confirmed **HTTP 404** (September 10, 2026).

#### Solution steps (choose one)

**Option A — Restore the page (preferred if FR gear content should exist)**
1. Copy structure from `gear.php` (English).
2. Create `fr/gear.php` with translated content, title, meta description, H1, and hreflang tags.
3. Ensure internal FR navigation links to the live page.

**Option B — 301 redirect to English gear page**
In `.htaccess` (LiteSpeed/Apache):
```apache
Redirect 301 /fr/gear.php https://myalphafitness.ca/fr/equipement.php
```
Use the correct French gear URL if one exists — verify before redirecting.

Or in PHP at top of a stub file:
```php
header('Location: https://myalphafitness.ca/gear.php', true, 301);
exit;
```

**Option C — Redirect to French homepage section**
Only if no FR gear page is planned — still use **301**, never leave 404.

#### Verification checklist
- [ ] `curl -I https://myalphafitness.ca/fr/gear.php` returns **200** or **301** (not 404)
- [ ] No internal links point to a 404
- [ ] hreflang pair updated if URL changed

---

### SEO-005 — Page titles over 60 characters (70 pages)

#### Rules
- Target length: **50–60 characters** (Google truncates longer titles)
- Include primary keyword near the start
- Append `| Alpha Fitness` only if it fits
- Every page needs a **unique** title

#### Solution steps

**Step 1 — Export the title report** (Section 4 of original audit lists worst EN offenders).

**Step 2 — Rewrite titles** (SEO/content)

| URL | Current length | Suggested rewrite (≤60 chars) |
|---|---|---|
| `/facilities-mille-voix.php` | 83 | Mille-Voix High School Gym Design \| Alpha Fitness |
| `/boutique-gym-design.php` | 79 | Boutique Gym Design Guide \| Alpha Fitness |
| `/facilities-infinite-gym.php` | 78 | Infinite Gym Church Conversion \| Alpha Fitness |
| `/athletic-facility-design.php` | 76 | Athletic Training Facility Design \| Alpha Fitness |
| `/about.php` | 65 | About Alpha Fitness \| Custom Gym Design Canada |
| `/privacy.php` | 13 | Privacy Policy \| Alpha Fitness Canada |

**Step 3 — Implement in code**
Update per-page `$pageTitle` or CMS field — do not hardcode in template only.

**Step 4 — French pages**
55 French titles also exceed 60 characters — mirror the same process for `/fr/` URLs.

#### Verification checklist
- [ ] Screaming Frog: ≤5% of titles over 60 characters (ideally 0%)
- [ ] No duplicate titles remain

---

### SEO-006 — Meta descriptions over 155 characters (61 pages)

#### Rules
- Target: **120–155 characters**
- One unique description per page
- Focus on **buyer benefit**, not boilerplate about Alpha Fitness
- Include a soft CTA where natural ("Get a quote", "See the project")

#### Solution steps

**Step 1 — Rewrite worst offenders first** (see Section 5 of original audit).

Example rewrite for `/commercial-gym-design.php`:
> Plan a commercial gym layout that members actually use. Equipment zoning, sizing, and design tips for Canadian gym owners.

**Step 2 — Fix too-short description**
`/residential-gym-ac.php` (53 chars) — expand to 120–155 chars with project-specific detail.

**Step 3 — Update in PHP/CMS** the same way as titles.

#### Verification checklist
- [ ] All descriptions between 120–155 characters
- [ ] No duplicate meta descriptions

---

### SEO-007 — Duplicate titles & meta descriptions

#### Duplicate titles to fix

| Duplicate title | URLs | Fix |
|---|---|---|
| Residential Gym - A Complete Training Environment | `residential-gym-ac.php`, `residential-gym-sf.php` | Use distinct titles: include project name/location (AC vs SF) |
| Stay Updated on the Latest… | `news.php`, `news.php?tag=*` | Canonicalise tag URLs (SEO-008) + unique titles for tags if kept indexable |
| Alpha Fitness - Creating Custom Gyms… | `about.php`, `fr/facilities-lionel-groulx.php`, `fr/facilities-extreme-evolution.php` | Write unique FR facility titles |

#### Duplicate meta descriptions (7 facility pages)
Pages sharing generic "Explore our professional gym solutions…" text:
- `facilities-espacew.php`
- `facilities-vita-sport.php`
- `facilities-apte.php`
- `facilities-erco.php`
- `facilities-vi-mascouche.php`
- `facilities-progym.php`
- `facilities-privilege-gym.php`

**Fix:** Write one unique description per facility referencing the actual client, space type, and outcome.

**Note:** `facilities-espacew.php` currently has wrong facility name in description ("Vita Sport") — fix as part of this task.

#### Verification checklist
- [ ] Screaming Frog duplicate title report = 0
- [ ] Screaming Frog duplicate meta description report = 0

---

### SEO-008 — Canonicalise news tag URLs

**Problem:** `news.php?tag=corporate-wellness`, `?tag=gym-equipment`, `?tag=gym-design` share the same title as `news.php`.

#### Solution steps

**Step 1 — Add canonical tag on tag views**
In the news tag template, output:
```html
<link rel="canonical" href="https://myalphafitness.ca/news.php">
```

**Step 2 — Optional: add `noindex` on filtered views**
If tag pages are not meant to rank:
```html
<meta name="robots" content="noindex, follow">
```

**Step 3 — Keep internal links** to tags for UX — canonical handles SEO duplication.

#### Verification checklist
- [ ] Tag URLs canonical point to `/news.php`
- [ ] Duplicate title issue cleared in crawl

---

### SEO-009 — External links missing `rel="noopener"`

**Recheck:** Form links have `noopener noreferrer`; LinkedIn links in team section do not.

#### Solution steps

**Step 1 — Find all `target="_blank"` without noopener**
```bash
grep -r 'target="_blank"' --include="*.php" . | grep -v noopener
```

**Step 2 — Update template/helper for external links**
```html
<a href="..." target="_blank" rel="noopener noreferrer">
```

Or fix the shared link renderer once.

**Step 3 — Pay special attention to**
- Team LinkedIn links on `about.php`
- Footer social icons
- Partner/external references

#### Verification checklist
- [ ] Screaming Frog "unsafe cross-origin links" = 0

---

### SEO-010 — Hreflang missing return links (3 pages)

#### Solution steps

**Step 1 — Identify the 3 URLs** from Screaming Frog hreflang report (missing return link / missing self-reference).

**Step 2 — On each EN page, include full set:**
```html
<link rel="alternate" hreflang="en-CA" href="https://myalphafitness.ca/page.php">
<link rel="alternate" hreflang="fr-CA" href="https://myalphafitness.ca/fr/page.php">
<link rel="alternate" hreflang="x-default" href="https://myalphafitness.ca/page.php">
```

**Step 3 — Mirror the same on the FR page** pointing back to EN.

**Step 4 — Self-reference is required** — each page must include its own language in the hreflang set.

#### Verification checklist
- [ ] Screaming Frog hreflang errors = 0
- [ ] [hreflang checker tool](https://technicalseo.com/tools/hreflang/) passes

---

### SEO-011 — Image optimization

| Issue | Count | Fix |
|---|---|---|
| Images >100KB | 70 | Compress to WebP, target <80KB for hero images |
| Missing width/height | 7 | Add `width` and `height` on `<img>` to prevent CLS |
| Alt text >100 chars | 1 | Shorten alt text |

#### Solution steps

**Step 1 — Priority order**
1. Homepage hero/images
2. Top traffic facility pages
3. Service page heroes
4. Remaining images

**Step 2 — Compress**
- Export WebP at 70–80% quality (Squoosh, ImageOptim, or `cwebp`)
- Replace source files; keep filenames or update references

**Step 3 — Dimensions**
```html
<img src="..." alt="..." width="800" height="600" loading="lazy">
```

**Step 4 — Re-test**
- Lighthouse / PageSpeed Insights on homepage + 2 facility pages
- Screaming Frog image report

#### Verification checklist
- [ ] ≤10% of images over 100KB (stretch goal)
- [ ] 0 images missing dimensions
- [ ] CLS score stable in Search Console

---

### SEO-012 — URL structure (informational)

| Issue | Action |
|---|---|
| 7 URLs with underscores | **Do not change existing URLs** — requires 301 migration. Use hyphens on **new** pages only. |
| 29 URLs with parameters | Canonicalise (see SEO-008) |
| 4 URLs over 115 chars | Shorten only on new pages |

---

## Week-by-week execution plan

### Week 1 — Quick wins (Developer-heavy)

| Task | ID | Time |
|---|---|---|
| Remove meta keywords from template | SEO-002 | 1 hr |
| Fix or redirect `fr/gear.php` | SEO-004 | 30 min |
| Canonicalise news tag pages | SEO-008 | 30 min |
| Fix duplicate residential gym titles | SEO-007 | 15 min |
| Fix `privacy.php` title | SEO-005 | 5 min |

### Week 2–3 — High impact

| Task | ID | Time |
|---|---|---|
| Complete schema rollout + validation | SEO-001 | 6–8 hrs |
| Rewrite top 15 EN titles | SEO-005 | 3–4 hrs |
| Rewrite top 10 EN meta descriptions | SEO-006 | 2–3 hrs |
| Unique descriptions for 7 facility pages | SEO-007 | 2 hrs |
| Fix duplicate H1s across templates | SEO-003 | 1 day |

### Week 4+ — Maintenance

| Task | ID | Time |
|---|---|---|
| noopener on external links | SEO-009 | 1 hr |
| hreflang cleanup | SEO-010 | 30 min |
| Image compression pass | SEO-011 | 4–6 hrs |
| French title/description pass | SEO-005/006 | 1 day |

---

## Sign-off template (per task)

| Field | Value |
|---|---|
| Task ID | SEO-___ |
| Completed by | |
| Date | |
| PR / commit | |
| Verified by | |
| Screaming Frog re-crawl date | |

---

## References

- Original audit: September 4, 2026 (Screaming Frog full crawl, 449 URLs)
- [Google Search Central — Structured data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Hreflang documentation](https://developers.google.com/search/docs/specialty/international/localized-versions)

---

*Document prepared for internal use — Alpha Fitness / myalphafitness.ca*
