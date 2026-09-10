# Alpha Fitness — Technical SEO Audit Remediation Guide
### Senior-reviewed fix playbook for junior developers

| | |
|---|---|
| **Site** | [myalphafitness.ca](https://myalphafitness.ca) |
| **Original audit crawl** | September 4, 2026 (Screaming Frog) |
| **Senior recheck** | September 10, 2026 (live site + curl verification) |
| **Reviewed by** | Senior Developer / Tech Lead |
| **Assigned to** | Junior Developer (+ SEO/Content for copy tasks) |
| **Stack (confirmed)** | PHP on LiteSpeed, shared `<head>` SEO block, JSON-LD in templates |

---

## Senior review — executive summary

This audit is **mostly accurate**, but the live site has improved since the crawl. Treat the original “0 structured data” finding as **outdated** — schema exists on several templates already. Focus effort on what is **still broken or inconsistent**.

### What the junior dev must fix first (this week)

| Order | ID | Issue | Why senior prioritizes it |
|---|---|---|---|
| 1 | SEO-004 | `fr/gear.php` → 404 | Live bug. FR nav links to `gear.php` which resolves to `/fr/gear.php`. French `/fr/equipement.php` already exists (200 OK). |
| 2 | SEO-002 | Meta keywords on 130 pages | One template delete = 107 pages fixed. Zero SEO value, signals neglect. |
| 3 | SEO-008 | News tag canonicals wrong | Tag pages currently canonicalise to **themselves** (`news.php?tag=…`), not `/news.php`. Actively creates duplicates. |
| 4 | SEO-007 | Duplicate titles/metas | Quick copy fixes on 2 residential pages + 7 facility pages. |
| 5 | SEO-001 | Finish schema rollout | Partially done — extend pattern already in codebase, don’t rebuild from scratch. |

### Senior recheck — corrected status

| Audit finding | Sep 4 report | Sep 10 live recheck | Still action needed? |
|---|---|---|---|
| Structured data | 0 pages | **Partially fixed** — LocalBusiness/WebSite/Service on homepage; BlogPosting+FAQPage+BreadcrumbList on blog; Article on service pages | **Yes** — extend to all templates + validate |
| Meta keywords | 130 pages | **Still open** | **Yes** |
| Duplicate H1 | 86 pages | **Still open** — mostly template/category pages sharing generic H1s | **Yes** |
| Broken `fr/gear.php` | 404 | **Still 404** — root cause: FR nav uses `href="gear.php"` | **Yes — urgent** |
| Titles >60 chars | 70 pages | **Still open** | **Yes** (content) |
| Meta desc >155 chars | 61 pages | **Still open** | **Yes** (content) |
| Duplicate titles | 4 groups | **Still open** | **Yes** |
| Unsafe cross-origin links | 57 | **Partially fixed** — LinkedIn links on `about.php` still missing `noopener` | **Yes** |
| Hreflang gaps | 3 pages | Not re-crawled | **Yes** (low priority) |
| Images >100KB | 70 | Not re-measured | **Yes** (maintenance) |

### New findings from senior recheck (not in original audit)

| Issue | URL | Action |
|---|---|---|
| FR nav broken gear link | `/fr/` pages link to `gear.php` → `/fr/gear.php` (404) | Redirect **or** fix nav to `equipement.php` |
| News tag self-canonical | `news.php?tag=gym-design` canonical = itself | Change canonical to `/news.php` |
| Duplicate FAQ in schema | Blog sample has same question twice in FAQPage JSON-LD | Deduplicate when generating FAQ schema |
| Underscore URLs return 404 | `commercial_boutiques.php`, `corporate_wellness.php`, `hospitality_wellness.php` | Audit internal links; add 301 to correct pages if linked |

---

## How to use this document

1. Open **`alpha-fitness-seo-audit-tracker.csv`** in Google Sheets for day-to-day tracking.
2. Fix tasks **in priority order** (Critical → High → Medium → Low).
3. Mark **Done** only when **Verification** steps pass.
4. Content changes (titles, H1s, descriptions) need SEO approval before deploy.
5. **Never change live URL slugs** without a 301 redirect plan.

### Definition of done (senior standard)

A task is complete only when **all** of the following are true:

- [ ] Code/content change is deployed to production
- [ ] Verification command or tool passes (listed per task)
- [ ] No regression on EN **and** FR version of the page
- [ ] PR/commit link recorded in tracker
- [ ] Senior or SEO has spot-checked at least 1 sample URL

---

## Codebase map (where to look)

The site is PHP. Based on live HTML, SEO is managed in a shared head block:

```html
<!-- SEO: Canonical, hreflang, OG, Twitter -->
```

**Search these first in the repo:**

```bash
grep -r 'meta name="keywords"' --include="*.php" .
grep -r 'application/ld+json' --include="*.php" .
grep -r 'hreflang' --include="*.php" .
grep -r 'pageTitle\|page_title\|\$title' --include="*.php" .
grep -r 'gear.php' --include="*.php" .
```

**Expected file locations (names may vary):**

| Purpose | Likely files |
|---|---|
| Shared `<head>` / SEO | `includes/head.php`, `includes/seo.php`, `header.php`, `partials/meta.php` |
| JSON-LD schema | Same as above, or `includes/schema.php` |
| FR navigation | `fr/includes/header.php`, shared nav partial |
| News / blog | `news.php`, `blog-article.php`, `fr/nouvelles.php` |
| Redirects | `.htaccess` (LiteSpeed/Apache) |

---

## Master tracker

| ID | Priority | Issue | Owner | Effort | Phase |
|---|---|---|---|---|---|
| SEO-001 | Critical | Complete structured data rollout | Developer | 6–8 hrs | Week 2 |
| SEO-002 | High | Remove meta keywords (130 pages) | Developer | 1 hr | Week 1 |
| SEO-003 | High | Fix duplicate H1 tags (86 pages) | Dev + SEO | 1 day | Week 2–3 |
| SEO-004 | High | Fix broken `fr/gear.php` | Developer | 30 min | Week 1 |
| SEO-005 | Medium | Shorten page titles (50–60 chars) | SEO/Content | 4–6 hrs | Week 2 |
| SEO-006 | Medium | Shorten meta descriptions (120–155 chars) | SEO/Content | 3–4 hrs | Week 2 |
| SEO-007 | Medium | Resolve duplicate titles & metas | Dev + SEO | 3 hrs | Week 1–2 |
| SEO-008 | Medium | Fix news tag canonicals | Developer | 30 min | Week 1 |
| SEO-009 | Low | Add `rel="noopener noreferrer"` | Developer | 1 hr | Week 3 |
| SEO-010 | Low | Fix hreflang return links (3 pages) | Developer | 30 min | Week 3 |
| SEO-011 | Low | Compress images; add dimensions | Developer | 4–6 hrs | Quarter |
| SEO-012 | Low | Hyphens on new URLs only | Developer | Ongoing | Ongoing |

---

# Detailed fixes (senior-reviewed)

---

## SEO-004 — Broken French gear page (FIX FIRST)

| | |
|---|---|
| **Priority** | High — live user-facing bug |
| **Senior review** | This is not a content issue. `/fr/equipement.php` works (200). `/fr/gear.php` does not. FR header/nav still links to `gear.php`, which resolves relative to `/fr/gear.php`. Fix navigation **and** add redirect as safety net. |
| **Risk if ignored** | French users hit 404 from main nav; wasted crawl budget; broken hreflang equity |

### Root cause
FR templates use `href="gear.php"` instead of `href="equipement.php"`.

### How to fix

**Step 1 — Confirm live state**
```bash
curl -I https://myalphafitness.ca/fr/gear.php        # expect 404 today
curl -I https://myalphafitness.ca/fr/equipement.php  # expect 200
curl -s https://myalphafitness.ca/fr/ | grep gear    # find bad links
```

**Step 2 — Fix navigation (primary fix)**

In the FR header/nav partial, replace every gear link:
```html
<!-- BEFORE -->
<a href="gear.php">...</a>

<!-- AFTER -->
<a href="equipement.php">...</a>
```

Search entire repo:
```bash
grep -rn 'href="gear.php"' fr/
grep -rn "href='gear.php'" fr/
```

**Step 3 — Add 301 redirect (safety net)**

In `.htaccess`:
```apache
# Redirect legacy FR gear URL to correct French page
Redirect 301 /fr/gear.php https://myalphafitness.ca/fr/equipement.php
```

**Step 4 — Update hreflang** (if `fr/gear.php` was listed anywhere)

Ensure gear/equipement EN/FR pair is:
```html
<link rel="alternate" hreflang="en-CA" href="https://myalphafitness.ca/gear.php">
<link rel="alternate" hreflang="fr-CA" href="https://myalphafitness.ca/fr/equipement.php">
```

### Do NOT
- Leave a 404 in place
- Redirect to English `/gear.php` (bad UX for French users)
- Create duplicate gear pages in both FR URLs

### Verification
```bash
curl -I https://myalphafitness.ca/fr/gear.php   # must be 301 → equipement.php
curl -s https://myalphafitness.ca/fr/ | grep 'gear.php'  # must return nothing
```
- [ ] FR nav “Gear/Équipement” opens `/fr/equipement.php`
- [ ] Screaming Frog: 0 client errors for gear URLs

---

## SEO-002 — Remove meta keywords (130 pages)

| | |
|---|---|
| **Priority** | High — one template fix clears ~107 pages |
| **Senior review** | Easiest high-impact win. Google ignores this tag since 2009. Delete it everywhere; do not replace with anything. |
| **Risk if ignored** | Page bloat, looks outdated to partners/competitors reviewing source |

### How to fix

**Step 1 — Find all occurrences**
```bash
grep -rn 'meta name="keywords"' --include="*.php" .
```

**Step 2 — Remove from shared template**

Delete this entire line from the shared head/SEO partial:
```html
<meta name="keywords" content="..." />
```

**Step 3 — Remove page-level overrides**

Some facility pages have custom keyword blocks (Treana, Liveo Mascouche, service pages). Remove each one individually.

**Step 4 — Deploy and verify**
```bash
curl -s https://myalphafitness.ca/about.php | grep 'meta name="keywords"'
curl -s https://myalphafitness.ca/fr/a-propos.php | grep 'meta name="keywords"'
# Both must return empty
```

### Do NOT
- Replace meta keywords with another hidden keyword block
- Only remove from English — FR pages must be cleaned too

### Verification
- [ ] `grep -r 'meta name="keywords"'` returns 0 results in codebase
- [ ] Screaming Frog: Meta Keywords = 0 pages

---

## SEO-008 — News tag pages: wrong canonical

| | |
|---|---|
| **Priority** | Medium — actively causing duplicate titles |
| **Senior review** | Live check shows `news.php?tag=gym-design` has `canonical` pointing to **itself**, not `/news.php`. This is worse than having no canonical. Must fix in PHP logic. |
| **Risk if ignored** | Google indexes multiple news URLs with identical titles |

### How to fix

**Step 1 — Confirm bug**
```bash
curl -s "https://myalphafitness.ca/news.php?tag=gym-design" | grep canonical
# Currently wrong: href="...news.php?tag=gym-design"
```

**Step 2 — Fix canonical logic in `news.php`**

When a `tag` query parameter is present, force canonical to main news page:
```php
<?php
$canonicalUrl = 'https://myalphafitness.ca/news.php';

if (!empty($_GET['tag'])) {
    // Filter/tag view — canonical to main news index
    $canonicalUrl = 'https://myalphafitness.ca/news.php';
    // Optional: prevent indexing of filter views
    $robotsMeta = 'noindex, follow';
} else {
    $robotsMeta = 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1';
}
?>

<link rel="canonical" href="<?= htmlspecialchars($canonicalUrl) ?>">
<meta name="robots" content="<?= htmlspecialchars($robotsMeta) ?>">
```

Mirror the same logic in `fr/nouvelles.php`.

**Step 3 — Keep tag links in UI** — users can still filter; SEO duplication is handled by canonical.

### Do NOT
- Canonicalise tag pages to themselves
- Remove tag functionality from the UI

### Verification
```bash
curl -s "https://myalphafitness.ca/news.php?tag=gym-design" | grep canonical
# Must show: href="https://myalphafitness.ca/news.php"
```
- [ ] All 3 tag URLs canonical → `/news.php`
- [ ] Screaming Frog duplicate titles for news tags = 0

---

## SEO-001 — Structured data (complete rollout)

| | |
|---|---|
| **Priority** | Critical — but partially done; extend existing pattern |
| **Senior review** | Do not rebuild schema from zero. Copy the working `@graph` JSON-LD pattern from homepage/blog. Gaps: facility pages, FR mirrors, consistent FAQ on all blog posts. Also fix duplicate FAQ questions in JSON-LD. |
| **Risk if ignored** | Missed rich results (FAQ snippets, breadcrumbs, local panel) |

### Current live coverage (Sep 10)

| Page type | Schema present | Gap |
|---|---|---|
| Homepage | LocalBusiness, Organization, WebSite, Service | Verify only |
| Blog posts | BlogPosting, FAQPage, BreadcrumbList | Confirm all 23 posts; dedupe FAQ |
| Service pages | Article, BreadcrumbList | Add `Service` type |
| Facility pages | Organization graph only | Add BreadcrumbList + WebPage |
| News index | Organization graph only | Optional CollectionPage (already on facilities.php) |

### How to fix

**Step 1 — Audit templates**
```bash
curl -s "https://myalphafitness.ca/facilities-espacew.php" | grep '@type'
curl -s "https://myalphafitness.ca/blog-article.php?slug=..." | grep '@type'
```

**Step 2 — Centralize in `includes/schema.php`**

Create helper functions:
```php
function schemaOrganizationGraph(): array { /* existing homepage graph */ }

function schemaBreadcrumbs(array $items): array {
    return [
        '@type' => 'BreadcrumbList',
        'itemListElement' => array_map(fn($i, $item) => [
            '@type' => 'ListItem',
            'position' => $i + 1,
            'name' => $item['name'],
            'item' => $item['url'],
        ], array_keys($items), $items),
    ];
}

function schemaFAQFromDom(string $html): ?array {
    // Parse visible FAQ Q&A from page — only output if section exists
    // IMPORTANT: deduplicate questions (trim whitespace, compare case-insensitive)
}
```

**Step 3 — Output one JSON-LD block per page**
```php
<script type="application/ld+json">
<?= json_encode([
    '@context' => 'https://schema.org',
    '@graph' => array_filter([
        ...schemaOrganizationGraph(),
        $pageSchema,        // BlogPosting | Service | WebPage
        $breadcrumbSchema,  // when not homepage
        $faqSchema,         // only when FAQ section exists on page
    ]),
], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT) ?>
</script>
```

**Step 4 — Service pages — add Service schema**

On each of the 6 service pages (EN + FR):
```json
{
  "@type": "Service",
  "name": "Commercial Gym Design",
  "serviceType": "Commercial Gym Design and Equipment",
  "provider": {"@id": "https://myalphafitness.ca/#organization"},
  "areaServed": {"@type": "Country", "name": "Canada"},
  "description": "..."
}
```

**Step 5 — Facility pages — minimum BreadcrumbList**

Example for `facilities-espacew.php`:
```
Home → Facilities → Espace W
```

**Step 6 — Fix FAQ duplicate bug**

Live blog post repeats *“How do I know when commercial gym equipment needs replacing?”* twice. When building FAQ schema:
```php
$seen = [];
foreach ($questions as $q) {
    $key = strtolower(trim($q['name']));
    if (isset($seen[$key])) continue;
    $seen[$key] = true;
    $mainEntity[] = $q;
}
```

**Step 7 — Validate**
- [Google Rich Results Test](https://search.google.com/test/rich-results) on 5 URLs (EN + FR)
- Fix all errors before closing task

### Do NOT
- Add FAQ schema on pages without visible FAQ content (Google manual action risk)
- Output invalid JSON (unescaped quotes in answers)
- Duplicate the entire Organization block differently on every page — use `@id` references

### Verification
- [ ] Rich Results Test passes: homepage, 1 service, 1 facility, 1 blog (EN + FR)
- [ ] FAQ schema question count matches visible FAQ count on page
- [ ] No duplicate questions in JSON-LD

---

## SEO-003 — Duplicate H1 tags (86 pages)

| | |
|---|---|
| **Priority** | High |
| **Senior review** | Pages have *an* H1, but many category/listing templates reuse the same H1 (e.g. shared section labels). Service landing pages already have good unique H1s. Focus on category templates, FR mirrors, and news tag views. |
| **Risk if ignored** | Google cannot distinguish page topics; weaker rankings |

### Rules
- Exactly **one** `<h1>` per page
- H1 must be **unique sitewide** (EN and FR are separate pages — both need unique text)
- H1 should contain the **primary keyword** but does not need to match `<title>` exactly
- Section labels like “OUR SERVICES” must be `<h2>`, not `<h1>`

### How to fix

**Step 1 — Export duplicates from Screaming Frog**

Filter: HTML → H1 → sort by H1 text → export URLs where count > 1.

**Step 2 — Fix template architecture**

Each page file (or CMS record) must set its own H1:
```php
// At top of facilities-espacew.php
$pageH1 = 'Espace W Condo Gym Design — Mascouche';

// In template — ONLY one h1 tag
<h1><?= htmlspecialchars($pageH1, ENT_QUOTES, 'UTF-8') ?></h1>
```

**Step 3 — Demote shared headings**

If a section heading is reused across pages, change it:
```html
<!-- BEFORE (wrong — duplicated as H1 on many pages) -->
<h1>OUR SERVICES</h1>

<!-- AFTER -->
<h2>Our Services</h2>
```

**Step 4 — SEO writes copy for each URL**

| Page type | Good H1 example |
|---|---|
| Commercial gym design | Commercial Gym Design in Quebec and Canada |
| Facility case study | Carabins UdeM High-Performance Athletic Centre |
| Blog post | Commercial Gym Equipment Cost in Canada: 2026 Budget Guide |
| Category listing | Education & Sports Institution Gym Projects |

**Step 5 — Fix news tag pages**

Tag views should not reuse the main news H1. Either:
- Use canonical + noindex (SEO-008), **or**
- Set H1 to `News: Gym Design` (unique per tag)

### Do NOT
- Hide duplicate H1s with CSS
- Use multiple H1 tags for styling
- Copy the same H1 across EN/FR without translating

### Verification
- [ ] Screaming Frog: each H1 text appears on only 1 URL per language
- [ ] View source: exactly one `<h1>` per page

---

## SEO-007 — Duplicate titles & meta descriptions

| | |
|---|---|
| **Priority** | Medium |
| **Senior review** | Confirmed live: `residential-gym-ac.php` and `residential-gym-sf.php` share the same title. Seven facility pages share a generic meta description; `facilities-espacew.php` even references the wrong facility (“Vita Sport”). |

### Duplicate titles to fix

| Current duplicate title | URLs | New title (suggested) |
|---|---|---|
| Residential Gym - A Complete Training Environment | `residential-gym-ac.php` | AC Residential Gym Design \| Alpha Fitness |
| Same | `residential-gym-sf.php` | SF Garage Gym Design \| Alpha Fitness |
| Stay Updated on the Latest… | `news.php`, `news.php?tag=*` | Fix via SEO-008 canonical |
| Alpha Fitness - Creating Custom Gyms… | `about.php`, 2 FR facility pages | Unique FR facility titles per project |

### Duplicate meta descriptions — 7 facility pages

Affected: `facilities-espacew`, `facilities-vita-sport`, `facilities-apte`, `facilities-erco`, `facilities-vi-mascouche`, `facilities-progym`, `facilities-privilege-gym`

**How to fix in code:**

Each facility PHP file (or CMS entry) should set its own meta:
```php
$pageTitle = 'Espace W Gym Design and Layout';
$metaDescription = 'See how Alpha Fitness designed a compact condo gym for Espace W — layout, equipment selection, and premium finishes.';
```

**Template pattern:**
```php
<meta name="description" content="<?= htmlspecialchars($metaDescription, ENT_QUOTES, 'UTF-8') ?>">
```

### Verification
- [ ] Screaming Frog: Duplicate Titles = 0
- [ ] Screaming Frog: Duplicate Meta Descriptions = 0
- [ ] `facilities-espacew.php` description mentions “Espace W”, not “Vita Sport”

---

## SEO-005 — Page titles over 60 characters

| | |
|---|---|
| **Priority** | Medium (content task) |
| **Senior review** | 44% of titles too long. Developer implements; SEO/content writes copy. Use a character counter before deploy. |

### Rules
- Target: **50–60 characters**
- Primary keyword near the start
- `| Alpha Fitness` suffix only if it fits
- Must be unique per URL

### Priority EN rewrites (from audit)

| URL | Chars | Suggested title (≤60) |
|---|---|---|
| `/facilities-mille-voix.php` | 83 | Mille-Voix High School Gym Design \| Alpha Fitness |
| `/boutique-gym-design.php` | 79 | Boutique Gym Design Guide \| Alpha Fitness |
| `/facilities-infinite-gym.php` | 78 | Infinite Gym Church Conversion \| Alpha Fitness |
| `/athletic-facility-design.php` | 76 | Athletic Training Facility Design \| Alpha Fitness |
| `/about.php` | 65 | About Alpha Fitness \| Custom Gym Design Canada |
| `/privacy.php` | 13 | Privacy Policy \| Alpha Fitness Canada |
| `/facilities.php` | 71 | Commercial Gym Design & Equipment \| Alpha Fitness |

### How to implement
```php
$pageTitle = 'Boutique Gym Design Guide | Alpha Fitness';
```
```html
<title><?= htmlspecialchars($pageTitle, ENT_QUOTES, 'UTF-8') ?></title>
```

Also fix **55 French titles** over 60 chars — same rules, native French copy.

### Verification
- [ ] Screaming Frog: Page Titles > 60 chars ≈ 0
- [ ] Spot-check with [Moz Title Tag Preview Tool](https://moz.com/learn/seo/title-tag)

---

## SEO-006 — Meta descriptions over 155 characters

| | |
|---|---|
| **Priority** | Medium (content task) |
| **Senior review** | Descriptions read like on-page copy, not SERP snippets. Rewrite for click-through, not keyword stuffing. |

### Rules
- Target: **120–155 characters**
- Unique per page
- Answer: “What does the visitor get from this page?”
- Soft CTA where natural

### Examples

**`/commercial-gym-design.php` (was 220 chars):**
> Plan a commercial gym layout members actually use. Zoning, sizing, and equipment tips for Canadian gym owners.

**`/residential-gym-ac.php` (was 53 chars — too short):**
> Explore this space-efficient home gym build — strength and cardio zones designed for daily endurance training.

### How to implement
```php
$metaDescription = 'Plan a commercial gym layout members actually use. Zoning, sizing, and equipment tips for Canadian gym owners.';
```

### Verification
- [ ] Screaming Frog: Meta Description > 155 chars = 0
- [ ] All descriptions ≥ 120 chars (except pages intentionally minimal like privacy)

---

## SEO-009 — External links missing `rel="noopener"`

| | |
|---|---|
| **Priority** | Low |
| **Senior review** | Form links already fixed. Team LinkedIn links on `about.php` still use `target="_blank"` without `rel="noopener noreferrer"`. Fix once in template. |

### How to fix

**Find offenders:**
```bash
grep -rn 'target="_blank"' --include="*.php" . | grep -v noopener
```

**Fix pattern:**
```html
<a href="https://www.linkedin.com/in/..." target="_blank" rel="noopener noreferrer" class="team-linkedin">
```

**Better — helper function:**
```php
function externalLink($url, $label, $class = '') {
    return sprintf(
        '<a href="%s" target="_blank" rel="noopener noreferrer" class="%s">%s</a>',
        htmlspecialchars($url),
        htmlspecialchars($class),
        $label
    );
}
```

### Verification
- [ ] Screaming Frog: Unsafe Cross-Origin Links = 0

---

## SEO-010 — Hreflang missing return links (3 pages)

| | |
|---|---|
| **Priority** | Low |
| **Senior review** | Site-wide hreflang is strong (159/159 in audit). Three pages have incomplete sets. Fix in the shared SEO partial if possible. |

### How to fix

Every indexable page needs **all three** tags (including self-reference):
```html
<link rel="alternate" hreflang="en-CA" href="https://myalphafitness.ca/PAGE.php">
<link rel="alternate" hreflang="fr-CA" href="https://myalphafitness.ca/fr/PAGE-FR.php">
<link rel="alternate" hreflang="x-default" href="https://myalphafitness.ca/PAGE.php">
```

Both EN and FR pages must reference each other.

**Step 1:** Run Screaming Frog → Hreflang report → export 3 broken URLs.

**Step 2:** Add missing return links in SEO partial or page config array:
```php
$hreflang = [
    'en-CA' => 'https://myalphafitness.ca/facilities-espacew.php',
    'fr-CA' => 'https://myalphafitness.ca/fr/facilities-espacew.php',
    'x-default' => 'https://myalphafitness.ca/facilities-espacew.php',
];
```

### Verification
- [ ] Screaming Frog hreflang errors = 0
- [ ] [Hreflang checker](https://technicalseo.com/tools/hreflang/) passes for sample URLs

---

## SEO-011 — Image optimization

| Issue | Count | Fix |
|---|---|---|
| Images >100KB | 70 | Compress to WebP, target <80KB for heroes |
| Missing width/height | 7 | Add dimensions to prevent CLS |
| Alt text >100 chars | 1 | Shorten |

### How to fix

**Priority order:** Homepage → top facility pages → service heroes → rest.

**Compress:**
```bash
# Example using cwebp (install if needed)
cwebp -q 80 input.jpg -o output.webp
```

**Add dimensions:**
```html
<img src="images/project.webp" alt="Espace W condo gym" width="1200" height="800" loading="lazy">
```

### Do NOT
- Upscale small images
- Strip alt text to save space
- Lazy-load above-the-fold hero without testing LCP

### Verification
- [ ] Screaming Frog: images over 100KB reduced (target ≤10% of total)
- [ ] Lighthouse CLS stable on homepage + 2 facility pages

---

## SEO-012 — URL structure (informational)

| Issue | Senior decision |
|---|---|
| 7 URLs with underscores | **Do not rename live URLs** — needs 301 migration. Use hyphens on new pages only. |
| Parameter URLs (`news.php?tag=`) | Fix with canonical (SEO-008) |
| Underscore URLs returning 404 | Audit if internally linked; add 301 to correct destination |

---

# Week-by-week plan

### Week 1 — Developer quick wins (~4 hours)

| Task | ID | Owner |
|---|---|---|
| Fix FR gear nav + 301 redirect | SEO-004 | Developer |
| Remove meta keywords from template | SEO-002 | Developer |
| Fix news tag canonical logic | SEO-008 | Developer |
| Fix duplicate residential gym titles | SEO-007 | Developer + SEO |
| Fix `privacy.php` title | SEO-005 | SEO |

### Week 2–3 — High impact

| Task | ID | Owner |
|---|---|---|
| Complete schema rollout + FAQ dedupe | SEO-001 | Developer |
| Rewrite top 15 EN titles | SEO-005 | SEO |
| Rewrite top 10 EN meta descriptions | SEO-006 | SEO |
| Unique facility meta descriptions (7 pages) | SEO-007 | SEO |
| Fix duplicate H1s | SEO-003 | Dev + SEO |

### Week 4+ — Maintenance

| Task | ID | Owner |
|---|---|---|
| noopener on external links | SEO-009 | Developer |
| hreflang cleanup | SEO-010 | Developer |
| Image compression | SEO-011 | Developer |
| French title/description pass | SEO-005/006 | French SEO |

---

# Sign-off template

| Field | Value |
|---|---|
| Task ID | SEO-___ |
| Developer | |
| SEO reviewer | |
| Date completed | |
| Commit / PR | |
| Verification tool | |
| Pass / Fail | |
| Senior approval | |

---

# References

- Original audit: September 4, 2026 (Screaming Frog, 449 URLs crawled)
- [Google Structured Data Guidelines](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Hreflang documentation](https://developers.google.com/search/docs/specialty/international/localized-versions)

---

*Senior-reviewed remediation guide — Alpha Fitness / myalphafitness.ca — Internal use only*
