from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path("about/", views.about, name="about"),
    path("hire/", views.hire, name="hire"),
    path("pricing/", views.pricing, name="pricing"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    # Legacy booking URL redirects to the hire page (booking happens there).
    path("book/", RedirectView.as_view(url="/hire/", permanent=True), name="book"),
    path("django-developer/<slug:city_slug>/", views.city_page, name="city"),
]
