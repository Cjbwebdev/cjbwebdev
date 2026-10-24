from datetime import datetime, timedelta, time
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from .forms import ContactForm
from .models import Booking

# ── Scheduling constants ──────────────────────────────────────
SLOT_DURATION = 30  # minutes
SLOT_START_HOUR = 14  # 2:30pm
SLOT_START_MINUTE = 30
SLOT_END_HOUR = 19  # 7pm
WORKDAYS = [0, 1, 2, 3, 4]  # Mon-Fri

# ── Project Data ──────────────────────────────────────────────

PROJECTS = [
    {
        'name': 'holidayhub.site',
        'url': 'https://holidayhub.site',
        'tech': 'Django',
        'desc': 'Holiday price comparison, 7+ UK travel providers, CJ & Awin affiliates',
        'long_desc': 'Holiday price comparison platform aggregating deals from 7+ UK travel providers. Real-time destination search cards, Commission Junction affiliate integration (IBEROSTAR, Hotels.com, CheapTickets, EconomyBookings), and multi-network monetisation.',
        'tags': ['Django', 'Python', 'PostgreSQL', 'Web Scraping', 'Affiliate'],
        'status': 'live',
        'image': 'img/projects/holidayhub.svg',
    },
    {
        'name': 'catn.site',
        'url': 'https://catn.site',
        'tech': 'Django',
        'desc': 'Cat N vehicle marketplace, 6,650+ listings from 5 sources',
        'long_desc': 'Category N write-off vehicle aggregator pulling from eBay, Gumtree, AutoTrader, Facebook Marketplace, and Copart. 6,650+ active listings with real-time deal ticker and advanced search.',
        'tags': ['Django', 'Python', 'PostgreSQL', 'Scraping', 'Automation'],
        'status': 'live',
        'image': 'img/projects/catn.svg',
    },
    {
        'name': 'urentmy.com',
        'url': 'https://urentmy.com',
        'tech': 'Django',
        'desc': 'Peer-to-peer rental marketplace, 2M profiles, 100k+ locations',
        'long_desc': 'Peer-to-peer rental marketplace with 2M pre-loaded business profiles across 100k+ locations. Time slot bookings, events, services, adverts, and affiliate programme. Stripe payments live.',
        'tags': ['Django', 'Python', 'Stripe', 'PostgreSQL', 'Marketplace'],
        'status': 'live',
        'image': 'img/projects/urentmy.svg',
    },
    {
        'name': 'policygen.site',
        'url': 'https://policygen.site',
        'tech': 'Django',
        'desc': 'AI legal document generator, GDPR/CCPA/LGPD in 90 seconds',
        'long_desc': 'AI-powered legal document generator producing customised privacy policies, T&Cs, cookie policies, disclaimers, and refund policies. GDPR, CCPA, and LGPD compliant. From £9/mo vs £500+ lawyer fees.',
        'tags': ['Django', 'Python', 'AI', 'DeepSeek', 'Document Generation'],
        'status': 'live',
        'image': 'img/projects/policygen.svg',
    },
    {
        'name': 'rankyu.co',
        'url': 'https://rankyu.co',
        'tech': 'Django + React',
        'desc': 'AI SEO agent, GA4 + GSC unified, Slack-native, DeepSeek-powered',
        'long_desc': 'AI SEO agent connecting Google Analytics 4 and Search Console. Delivers analysis and recommendations to Slack. DeepSeek-powered engine watches traffic patterns, detects ranking drops, and suggests fixes.',
        'tags': ['Django', 'React', 'AI', 'DeepSeek', 'Slack API'],
        'status': 'live',
        'image': 'img/projects/rankyu.svg',
    },
    {
        'name': 'jobrdy.online',
        'url': 'https://jobrdy.online',
        'tech': 'Django',
        'desc': 'AI-powered job board aggregator, scrapes 50+ sources, real-time alerts',
        'long_desc': 'AI job board aggregator pulling listings from 50+ sources. Real-time alerts, smart filtering, automated application tracking.',
        'tags': ['Django', 'Python', 'PostgreSQL', 'Scraping', 'AI'],
        'status': 'live',
        'image': 'img/projects/jobrdy.svg',
    },
    {
        'name': 'shieldguard.site',
        'url': 'https://shieldguard.site',
        'tech': 'Django',
        'desc': 'GDPR cookie consent & privacy compliance platform, one-line install',
        'long_desc': 'GDPR/CCPA cookie consent management. One-line JavaScript install, automatic cookie scanning, customizable consent banners, compliance reporting.',
        'tags': ['Django', 'JavaScript', 'PostgreSQL', 'GDPR', 'SaaS'],
        'status': 'live',
        'image': 'img/projects/shieldguard.svg',
    },
    {
        'name': 'rankinganswer.com',
        'url': 'https://rankinganswer.com',
        'tech': 'Django + React',
        'desc': 'AI SEO content generator, finds ranking gaps, auto-publishes articles',
        'long_desc': 'AI-powered SEO content platform. Finds ranking opportunities, generates optimised articles, auto-publishes. Built for agencies scaling content.',
        'tags': ['Django', 'React', 'AI', 'SEO', 'Content'],
        'status': 'live',
        'image': 'img/projects/rankinganswer.svg',
    },
    {
        'name': 'bubblewatch',
        'url': 'https://cjbwebdevelopment.com',
        'tech': 'Django',
        'desc': 'AI bubble watchdog, tracks funding, hype cycles, investigative reports',
        'long_desc': 'Investigative journalism platform tracking AI industry bubbles, venture funding patterns, and hype cycles. Automated data collection and editorial CMS.',
        'tags': ['Django', 'Python', 'Journalism', 'Data', 'AI'],
        'status': 'live',
        'image': 'img/projects/bubblewatch.svg',
    },

]

FEATURED_IDS = ['holidayhub.site', 'catn.site', 'urentmy.com']


# ── Page Views ─────────────────────────────────────────────────

def home(request):
    featured = [p for p in PROJECTS if p['name'] in FEATURED_IDS]
    ctx = {
        'project_count': len(PROJECTS),
        'featured_projects': featured,
    }
    return render(request, 'pages/home.html', ctx)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            full_message = (
                f"From: {name} <{email}>\n\n"
                f"Subject: {subject}\n\n"
                f"Message:\n{message}"
            )
            try:
                send_mail(
                    f'Contact: {subject}',
                    full_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['curtisbooth87@yahoo.com'],
                    fail_silently=False,
                )
                messages.success(request, "Message sent! I'll get back to you within 24 hours.")
            except Exception:
                messages.error(request, "Sorry, something went wrong. Please try again or reach out via the contact form.")
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})


def services(request):
    return render(request, 'pages/services.html')


def portfolio(request):
    return render(request, 'pages/portfolio.html', {'projects': PROJECTS})


def about(request):
    """About page — professional narrative and credentials."""
    return render(request, "pages/about.html")


def pricing(request):
    """Pricing page — service tiers and engagement options."""
    return render(request, "pages/pricing.html")


def privacy(request):
    """Privacy policy page."""
    return render(request, "pages/privacy.html")


def terms(request):
    """Terms of service page."""
    return render(request, "pages/terms.html")


# ── City Landing Pages ────────────────────────────────────────

CITY_PAGES = CITY_PAGES = [
    {
        'slug': 'london',
        'name': 'London',
        'country': 'UK',
        'market': "London is the UK's largest tech hub with over 3,000 active Django contracts at any time. Fintech, healthtech, and SaaS companies compete for senior Django talent, rates reflect the demand.",
        'rate': '£500–700/day',
        'demand': 'Very high',
        'flag': '',
    },
    {
        'slug': 'berlin',
        'name': 'Berlin',
        'country': 'Germany',
        'market': "Berlin's startup ecosystem is the largest in Europe. Django powers backend systems at Delivery Hero, Zalando, and hundreds of early-stage ventures. Remote-friendly culture.",
        'rate': '€450–650/day',
        'demand': 'High',
        'flag': '',
    },
    {
        'slug': 'amsterdam',
        'name': 'Amsterdam',
        'country': 'Netherlands',
        'market': "Amsterdam hosts European HQs for Uber, Netflix, and Booking.com alongside a dense fintech scene. Django contractors are sought for API-heavy, data-driven platforms.",
        'rate': '€500–700/day',
        'demand': 'High',
        'flag': '',
    },
    {
        'slug': 'dublin',
        'name': 'Dublin',
        'country': 'Ireland',
        'market': "Dublin is the European home of Google, Meta, Stripe, and hundreds of SaaS companies. Django contractors fill gaps in backend teams that can't hire permanent staff fast enough.",
        'rate': '€450–650/day',
        'demand': 'High',
        'flag': '',
    },
    {
        'slug': 'paris',
        'name': 'Paris',
        'country': 'France',
        'market': "Paris has emerged as a serious tech contender with Station F, Doctolib, and a government-backed startup visa. Django developers are in demand across e-commerce and govtech.",
        'rate': '€400–600/day',
        'demand': 'Moderate-high',
        'flag': '',
    },
    {
        'slug': 'barcelona',
        'name': 'Barcelona',
        'country': 'Spain',
        'market': "Barcelona attracts international tech companies for its lower costs and strong talent pool. Django is widely used in travel tech, e-commerce, and mobile backend development.",
        'rate': '€350–500/day',
        'demand': 'Moderate',
        'flag': '',
    },
    {
        'slug': 'munich',
        'name': 'Munich',
        'country': 'Germany',
        'market': "Munich's enterprise-heavy economy, BMW, Siemens, Allianz, increasingly runs on Python/Django. Contractors bridge the gap between legacy systems and modern web apps.",
        'rate': '€500–700/day',
        'demand': 'High',
        'flag': '',
    },
    {
        'slug': 'stockholm',
        'name': 'Stockholm',
        'country': 'Sweden',
        'market': "Stockholm produces more unicorns per capita than anywhere outside Silicon Valley. Django contractors support scale-ups moving from MVP to production infrastructure.",
        'rate': '€450–650/day',
        'demand': 'Moderate-high',
        'flag': '',
    },
    {
        'slug': 'copenhagen',
        'name': 'Copenhagen',
        'country': 'Denmark',
        'market': "Copenhagen's tech scene is compact but highly concentrated, fintech, logistics, and green tech dominate. Django expertise is particularly valued for API design and data platforms.",
        'rate': '€450–600/day',
        'demand': 'Moderate',
        'flag': '',
    },
    {
        'slug': 'vienna',
        'name': 'Vienna',
        'country': 'Austria',
        'market': "Vienna sits at the crossroads of Western and Eastern European tech markets. Django is widely used in government digitalisation projects and B2B SaaS platforms.",
        'rate': '€400–550/day',
        'demand': 'Moderate',
        'flag': '',
    },
    {
        'slug': 'zurich',
        'name': 'Zurich',
        'country': 'Switzerland',
        'market': "Zurich's banking and insurance sectors are rapidly digitising. Django contractors command premium rates for secure, compliant web applications in the financial services space.",
        'rate': '€600–900/day',
        'demand': 'Moderate',
        'flag': '',
    },
    {
        'slug': 'brussels',
        'name': 'Brussels',
        'country': 'Belgium',
        'market': "Brussels hosts the EU institutions and a growing network of policy-tech and reg-tech startups. Django developers are needed for data platforms, compliance tools, and APIs.",
        'rate': '€400–550/day',
        'demand': 'Moderate',
        'flag': '',
    },
]



def city_page(request, city_slug):
    city = next((c for c in CITY_PAGES if c["slug"] == city_slug), None)
    if not city:
        from django.http import Http404
        raise Http404("City not found")
    return render(request, "pages/city.html", {
        "city": city,
        "all_cities": CITY_PAGES,
    })

# ── Booking System ────────────────────────────────────────────

def _get_week_slots():
    """Generate all available 30-min slots for the current week (Mon-Fri 2:30-7pm UK)."""
    now = timezone.localtime()
    monday = now.date() - timedelta(days=now.weekday())
    slots = []
    for day_offset in WORKDAYS:
        day = monday + timedelta(days=day_offset)
        slot_time = timezone.make_aware(
            datetime.combine(day, time(SLOT_START_HOUR, SLOT_START_MINUTE))
        )
        end_time = timezone.make_aware(
            datetime.combine(day, time(SLOT_END_HOUR, 0))
        )
        while slot_time + timedelta(minutes=SLOT_DURATION) <= end_time:
            if slot_time > now:
                slots.append(slot_time)
            slot_time += timedelta(minutes=SLOT_DURATION)
    return slots


def hire(request):
    """Booking page with calendar, scarcity counter, and Teams confirmation."""
    slots = _get_week_slots()
    booked_slots = set(
        Booking.objects.filter(
            slot_datetime__gte=timezone.localtime() - timedelta(hours=1)
        ).values_list("slot_datetime", flat=True)
    )
    available = [s for s in slots if s not in booked_slots]
    remaining = len(available)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        project = request.POST.get("project", "").strip()
        slot_str = request.POST.get("slot", "")

        if not all([name, email, slot_str]):
            return render(request, "pages/hire.html", {
                "error": "Please fill in all required fields.",
                "slots": available,
                "remaining": remaining,
            })

        try:
            slot_dt = timezone.make_aware(
                datetime.strptime(slot_str, "%Y-%m-%dT%H:%M")
            )
        except ValueError:
            return render(request, "pages/hire.html", {
                "error": "Invalid time slot.",
                "slots": available,
                "remaining": remaining,
            })

        if slot_dt not in available:
            return render(request, "pages/hire.html", {
                "error": "That slot is no longer available. Please choose another.",
                "slots": available,
                "remaining": remaining,
            })

        booking = Booking.objects.create(
            name=name,
            email=email,
            project_description=project,
            slot_datetime=slot_dt,
        )

        meeting_date = slot_dt.strftime("%A %d %B %Y")
        meeting_time = slot_dt.strftime("%H:%M")
        email_body = (
            f"Hi {name},\n\n"
            f"Your consultation is confirmed for:\n\n"
            f"  {meeting_date} at {meeting_time} UK time\n\n"
            f"You will receive a Microsoft Teams meeting invitation within "
            f"1 hour of this booking. If you do not see it, check your spam "
            f"folder or reply to this email.\n\n"
            f"Project details: {project or 'Not provided'}\n\n"
            f"Talk soon,\nCurtis Booth\nCJB Web Development\n"
            f"https://cjbwebdevelopment.com"
        )
        try:
            send_mail(
                f"Booking confirmed: {meeting_date} at {meeting_time}",
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [email, "curtisbooth87@yahoo.com"],
                fail_silently=False,
            )
        except Exception:
            pass  # Don't fail the booking if email fails

        return render(request, "pages/hire.html", {
            "confirmed": True,
            "name": name,
            "meeting_date": meeting_date,
            "meeting_time": meeting_time,
        })

    return render(request, "pages/hire.html", {
        "slots": available,
        "remaining": remaining,
    })
