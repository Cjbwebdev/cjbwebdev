from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm

# ── Project Data ──────────────────────────────────────────────

PROJECTS = [
    {
        'name': 'holidayhub.site',
        'url': 'https://holidayhub.site',
        'tech': 'Django',
        'desc': 'Holiday price comparison — 7+ UK travel providers, CJ & Awin affiliates',
        'long_desc': 'Holiday price comparison platform aggregating deals from 7+ UK travel providers. Real-time destination search cards, Commission Junction affiliate integration (IBEROSTAR, Hotels.com, CheapTickets, EconomyBookings), and multi-network monetisation.',
        'tags': ['Django', 'Python', 'PostgreSQL', 'Web Scraping', 'Affiliate'],
        'status': 'live',
        'image': 'img/projects/holidayhub.svg',
    },
    {
        'name': 'catn.site',
        'url': 'https://catn.site',
        'tech': 'Django',
        'desc': 'Cat N vehicle marketplace — 6,650+ listings from 5 sources',
        'long_desc': 'Category N write-off vehicle aggregator pulling from eBay, Gumtree, AutoTrader, Facebook Marketplace, and Copart. 6,650+ active listings with real-time deal ticker and advanced search.',
        'tags': ['Django', 'Python', 'PostgreSQL', 'Scraping', 'Automation'],
        'status': 'live',
        'image': 'img/projects/catn.svg',
    },
    {
        'name': 'urentmy.com',
        'url': 'https://urentmy.com',
        'tech': 'Django',
        'desc': 'Peer-to-peer rental marketplace — 2M profiles, 100k+ locations',
        'long_desc': 'Peer-to-peer rental marketplace with 2M pre-loaded business profiles across 100k+ locations. Time slot bookings, events, services, adverts, and affiliate programme. Stripe payments live.',
        'tags': ['Django', 'Python', 'Stripe', 'PostgreSQL', 'Marketplace'],
        'status': 'live',
        'image': 'img/projects/urentmy.svg',
    },
    {
        'name': 'policygen.site',
        'url': 'https://policygen.site',
        'tech': 'Django',
        'desc': 'AI legal document generator — GDPR/CCPA/LGPD in 90 seconds',
        'long_desc': 'AI-powered legal document generator producing customised privacy policies, T&Cs, cookie policies, disclaimers, and refund policies. GDPR, CCPA, and LGPD compliant. From £9/mo vs £500+ lawyer fees.',
        'tags': ['Django', 'Python', 'AI', 'DeepSeek', 'Document Generation'],
        'status': 'live',
        'image': 'img/projects/policygen.svg',
    },
    {
        'name': 'rankyu.co',
        'url': 'https://rankyu.co',
        'tech': 'Django + React',
        'desc': 'AI SEO agent — GA4 + GSC unified, Slack-native, DeepSeek-powered',
        'long_desc': 'AI SEO agent connecting Google Analytics 4 and Search Console. Delivers analysis and recommendations to Slack. DeepSeek-powered engine watches traffic patterns, detects ranking drops, and suggests fixes.',
        'tags': ['Django', 'React', 'AI', 'DeepSeek', 'Slack API'],
        'status': 'live',
        'image': 'img/projects/rankyu.svg',
    },
]

FEATURED_IDS = ['holidayhub.site', 'catn.site', 'urentmy.com']


# ── Views ─────────────────────────────────────────────────────

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
                    ['support@cjbwebdevelopment.com'],
                    fail_silently=False,
                )
                messages.success(request, 'Message sent! I\'ll get back to you within 24 hours.')
            except Exception:
                messages.error(request, 'Sorry, something went wrong. Please email me directly at support@cjbwebdevelopment.com.')
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})


def services(request):
    return render(request, 'pages/services.html')


def portfolio(request):
    return render(request, 'pages/portfolio.html', {'projects': PROJECTS})
