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

### Site audit (17 Nov 2026)

- [x] **The contact form had never delivered an email.** `EMAIL_HOST` was empty, so
      Django's SMTP backend could not connect and every submission fell into the
      "something went wrong" branch — enquiries from the one page that exists to win
      work were lost. The container's storage had a dead Resend key (401). Fixed by
      verifying `cjbwebdevelopment.com` in Resend (DKIM, SPF MX, SPF TXT and the
      `rsend` CNAME published in Cloudflare), then recreating the container with
      Resend SMTP credentials and `DEFAULT_FROM_EMAIL` on the real domain.
      Verified end to end: a form submission produced a message the Resend API
      reports as **delivered** to curtisbooth87@yahoo.com.
- [x] **Dead links replaced.** The contact page's LinkedIn and GitHub icons both
      pointed at `#`; the GitHub icon now opens github.com/Cjbwebdev and the second
      slot is a mailto. The cookie banner's "Privacy Policy" link was also `#` — it
      goes to /privacy/. Contact page now has zero `href="#"`.
- [x] Homepage: one H1, 3,965px, nine sections, no overflow, all 13 internal links
      200. Portfolio links (holidayhub.site, catn.site, urentmy.com) all live;
      HolidayHub is a real 1,223-word page, not a stub.
- [x] Contact form: server-side POST with CSRF, four required fields, every field
      labelled. 25? tests: see test run.
