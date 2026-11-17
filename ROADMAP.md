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

Measured against the live site at 1280 and 390 pixels. Redirects are followed and
reported as redirects, not as duplicate pages.

### SEO and markup
- [x] No issues found.

### Rendered (DOM after boot)
- [ ] **MED** 12 tap targets under 40px on mobile
- [x] H1 renders: "Django Developer Contractor in the UK"
- [x] Page height: 3965px desktop, 3965px mobile

### Manual UX pass

- [ ] Hero: photo loads, text readable at both widths, one clear CTA above the fold
- [ ] Section by section: no dead space, no clipped card, no orphan word in a heading
- [ ] Every button and link: label says what happens and lands where it says
- [ ] Forms: labels, inline validation, real success state
- [ ] No emoji, no AI art, no repeated CTA wording

### Metadata audit (17 Nov 2026)

- [x] All 13 city pages had descriptions of 213-224 characters, so Google truncated
      every one. Template now trims the market sentence: 117-122 characters.
- [x] /portfolio/ was 168 characters and ended "Built in the UK, UK." Rewritten to
      139 characters with the duplicated country removed.
- [x] Whole sitemap re-checked: no page over 165 characters.
