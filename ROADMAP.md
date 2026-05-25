# cjbwebdevelopment.com — Roadmap

> **Last Audit:** 2026-05-25 | **Server:** Hetzner CX23 (65.109.130.180) | **Port:** 8058

## 📊 Current State
- **Live URL:** https://cjbwebdevelopment.com
- **Container:** cjbwebdev, network=host
- **DB:** SQLite (NOT PostgreSQL — only site using SQLite)
- **Stack:** Django, portfolio/freelancer site
- **Revenue:** £0 — portfolio site, not monetized directly

## 🔄 Audit Re-Check — 2026-05-25

### ✅ RESOLVED
| # | Issue | How Verified |
|---|---|---|
| 1 | Migrations not applied (all `[ ]`) | Ran `python manage.py migrate` — all applied OK |

### 🔴 REMAINING
| # | Issue | Priority |
|---|---|---|
| 1 | **No sitemap.xml** — returns 404 | HIGH |
| 2 | **No robots.txt** — returns 404 | HIGH |
| 3 | **Missing HSTS header** — no Strict-Transport-Security | HIGH |
| 4 | **Missing CSP header** — no Content-Security-Policy | MEDIUM |
| 5 | **SQLite in production** — all other sites use PostgreSQL. SQLite has concurrency limits. | MEDIUM |
| 6 | **Missing Permissions-Policy header** | LOW |

### 🎯 TOP 5 PRIORITY ACTIONS
1. **Add sitemap.xml** — Django sitemap framework for SEO
2. **Add robots.txt** — With proper sitemap URL
3. **Add HSTS + CSP headers** — via nginx (same pattern as catn fix)
4. **Migrate to PostgreSQL** — Match all other projects' infrastructure
5. **Add portfolio case studies** — Showcase the 5 other live projects
