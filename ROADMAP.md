# cjbwebdevelopment.com — Roadmap

> **Last Audit:** 2026-05-26 | **Last Update:** 2026-05-26 | **Server:** Hetzner CX23 (65.109.130.180) | **Port:** 8058

## 📊 Current State
- **Live URL:** https://cjbwebdevelopment.com
- **DB:** SQLite — only site not on PostgreSQL
- **Portfolio:** All 5 live projects showcased with case studies

## ✅ COMPLETED

### 2026-05-26
| # | Task | Result |
|---|---|---|
| 8 | CSP broke Tailwind CDN | Built Tailwind CSS locally (36KB, v4), removed CDN dependency, site fully styled |
| 9 | Blog 500 errors | patched blog_post view to return 404 for missing templates |
| 10 | Security middleware | Added SecurityHeadersMiddleware with proper CSP headers |

### 2026-05-25
| # | Task | Result |
|---|---|---|
| 1 | Migrations applied | All Django migrations running |
| 2 | sitemap.xml | Custom XML sitemap returning 200 |
| 3 | robots.txt | With sitemap URL reference |
| 4 | HSTS header | max-age=31536000 via nginx |
| 5 | CSP header | Added via nginx |
| 6 | Permissions-Policy header | Added via nginx |
| 7 | Portfolio case studies | All 5 projects already listed |

## 🟡 REMAINING
| # | Issue | Priority |
|---|---|---|
| 1 | **SQLite → PostgreSQL** — Only site not on PostgreSQL | MEDIUM |
| 2 | **No blog content** — Blog section exists but empty | LOW |

### 🎯 NEXT ACTIONS
1. Migrate to PostgreSQL (same Hetzner host, new DB)
2. Write 3 blog posts about Django development

