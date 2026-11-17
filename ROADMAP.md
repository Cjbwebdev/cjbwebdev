# cjbwebdevelopment.com — ROADMAP

> **Last Audit:** 2026-08-04 | **Server:** Hetzner CX23 (65.109.130.180) | **Port:** 8058

## 📊 Current State
- **Live URL:** https://cjbwebdevelopment.com ✅ 200
- **DB:** SQLite
- **Portfolio:** All live projects showcased
- **Blog:** Empty
- **CI/CD:** No GitHub Actions workflow

## ✅ Completed

| # | Task |
|---|------|
| 1 | CSP + Tailwind local build (no CDN) |
| 2 | Blog 500 errors patched |
| 3 | Security headers (HSTS, CSP, X-Frame, etc.) |
| 4 | sitemap.xml + robots.txt |
| 5 | Portfolio case studies |

## 🔴 REMAINING

| # | Issue | Priority |
|---|-------|----------|
| 1 | SQLite → PostgreSQL migration | MEDIUM |
| 2 | Blog content (3 posts) | LOW |
| 3 | Add CI/CD workflow | LOW |

## 🔴 Audit 2026-11-01 (scheduled rotation)

### New findings
1. **"UK, UK" copy bug in meta descriptions** — duplicated location string in 4 templates:
   - `templates/pages/home.html` line 4 — "developer in the UK, UK."
   - `templates/pages/contact.html` line 4 — "Based in the UK, UK."
   - `templates/pages/portfolio.html` line 4 — "Built in the UK, UK."
   - `templates/base.html` line 16 (og:description) — "Based in the UK, UK."
   Fix: drop the trailing ", UK" in each (trivial template edit + `docker cp` + restart).
2. **Duplicate security headers (nginx + Django)** — nginx `/etc/nginx/sites-enabled/cjbwebdev` emits CSP/X-Frame-Options/X-Content-Type-Options/Referrer-Policy, and Django's middleware emits the same four. Two CSP headers with slightly different values (nginx omits the `https://` scheme on fonts.googleapis.com/cdnjs.cloudflare.com). Not currently breaking rendering, but should be consolidated to a single source.

### Verified green 2026-11-01
- Homepage/sitemap/robots all 200 (ads.txt 404 = expected, not configured). H1 present + clean hierarchy. About/services/portfolio/hire/contact/blog + 3 django-developer location pages all 200. No console errors, no failed requests.

## Audit — cjbwebdevelopment.com (17 Nov 2026)

Automated + rendered check of the live site. Every finding below was measured,
not guessed: static checks read the HTML the public receives, rendered checks
read the DOM after the app boots at 1280 and 390 pixels.

### SEO and markup findings
- [x] None found in the automated pass.

### Rendered findings (DOM after boot)
- [ ] **MED** tap targets under 40px: 12 (CJB Web Development, View All Services, View All Projects, London, Berlin, Amsterdam, Dublin, Paris)
- [ ] **MED** mobile tap targets under 40px: 12
- [ ] **MED** controls with no href: Decline, Accept All
- [ ] Page height: desktop 3965px, mobile 3965px
- [ ] Sections on the homepage: 5
  - section.relative pt-16 lg:pt-24 pb-16 lg:pb-32 overflow-hi — 664px, 317 chars, "Django Developer Contractor in the UK"
  - section.py-20 lg:py-28 bg-dark-600/50 — 903px, 610 chars, "Services"
  - section.py-20 lg:py-28 — 1243px, 547 chars, "Featured Projects"
  - section.py-16 bg-dark-600/50 — 66px, 140 chars, "(no heading)"
  - section.py-20 lg:py-28 relative overflow-hidden — 364px, 153 chars, "Have a Django Project in Mind?"
- [x] H1 renders: "Django Developer Contractor in the UK"

### Manual UX pass (critical eye)

- [ ] Hero: image present, text readable at 390 and 1280, CTA above the fold
- [ ] Every section: no dead space, no clipped card, no orphan word in a heading
- [ ] Every button/link: label says what happens, lands on the right page
- [ ] Forms: labels, validation messages, success state
- [ ] Trust: phone, insurance, real photos — no emoji, no stock-looking AI art

