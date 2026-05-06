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
        'desc': 'Holiday price comparison — 23+ providers, real-time deals',
        'long_desc': 'Holiday price comparison platform aggregating deals from 23+ UK travel providers. Real-time scraping, affiliate integration (Awin, CJ), and automated deal matching.',
        'tags': ['Django', 'Python', 'PostgreSQL', 'Web Scraping', 'Affiliate'],
        'status': 'live',
        'image': '',
    },
    {
        'name': 'catn.site',
        'url': 'https://catn.site',
        'tech': 'Django',
        'desc': 'Content platform with multi-source data aggregation',
        'long_desc': 'Content platform aggregating data from multiple sources including eBay, Gumtree, AutoTrader, and Facebook Marketplace. Automated scraping and processing pipelines.',
        'tags': ['Django', 'Python', 'PostgreSQL', 'Scraping', 'Automation'],
        'status': 'live',
        'image': '',
    },
    {
        'name': 'urentmy.com',
        'url': 'https://urentmy.com',
        'tech': 'Django',
        'desc': 'Rental marketplace with booking and payment',
        'long_desc': 'Property rental marketplace with booking management, payment integration, and user dashboards. Built for handling real transactions and customer interactions.',
        'tags': ['Django', 'Python', 'Stripe', 'PostgreSQL', 'E-commerce'],
        'status': 'live',
        'image': '',
    },
    {
        'name': 'policygen.site',
        'url': 'https://policygen.site',
        'tech': 'Django',
        'desc': 'Automated policy document generation system',
        'long_desc': 'Automated document generation platform creating customised policies from templates. PDF generation, user input processing, and template management system.',
        'tags': ['Django', 'Python', 'PDF Generation', 'MySQL', 'Templating'],
        'status': 'live',
        'image': '',
    },
    {
        'name': 'DisputeDefender',
        'url': 'https://disputedefender.site',
        'tech': 'Django',
        'desc': 'Automated dispute resolution tool',
        'long_desc': 'Automated dispute resolution platform helping users generate and manage formal disputes. Document generation, case tracking, and template-based workflows.',
        'tags': ['Django', 'Python', 'Automation', 'Document Generation'],
        'status': 'live',
        'image': '',
    },
    {
        'name': 'LeadSaver AI',
        'url': 'https://leadsaver-ai.com',
        'tech': 'Django',
        'desc': 'AI-powered lead capture and automation',
        'long_desc': 'AI-powered lead capture and automation platform. Intelligent form processing, automated follow-ups, and lead scoring using LLM integration.',
        'tags': ['Django', 'Python', 'LLM', 'Automation', 'AI'],
        'status': 'live',
        'image': '',
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
