from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm

def home(request):
    projects = [
        {'name': 'catn.site', 'url': 'https://catn.site', 'desc': 'Cat-themed website'},
        {'name': 'urentmy.com', 'url': 'https://urentmy.com', 'desc': 'Rental platform'},
        {'name': 'policygen.site', 'url': 'https://policygen.site', 'desc': 'Policy generator'},
    ]
    return render(request, 'pages/home.html', {'projects': projects})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            full_message = f"From: {name} <{email}>\n\nSubject: {subject}\n\nMessage:\n{message}"
            send_mail(
                f'Contact: {subject}',
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                ['support@cjbwebdevelopment.com'],
                fail_silently=False,
            )
            messages.success(request, 'Thank you for your message. We will get back to you soon.')
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})

def services(request):
    return render(request, 'pages/services.html')

def portfolio(request):
    projects = [
        {'name': 'catn.site', 'url': 'https://catn.site', 'desc': 'Cat-themed website'},
        {'name': 'urentmy.com', 'url': 'https://urentmy.com', 'desc': 'Rental platform'},
        {'name': 'policygen.site', 'url': 'https://policygen.site', 'desc': 'Policy generator'},
    ]
    return render(request, 'pages/portfolio.html', {'projects': projects})
