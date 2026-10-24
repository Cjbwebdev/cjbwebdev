from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def robots_txt(request):
    return HttpResponse("User-agent: *\nAllow: /\nSitemap: https://cjbwebdevelopment.com/sitemap.xml\n", content_type="text/plain")

def sitemap_xml(request):
    urls = [
        "https://cjbwebdevelopment.com/",
        "https://cjbwebdevelopment.com/about/",
        "https://cjbwebdevelopment.com/hire/",
        "https://cjbwebdevelopment.com/contact/",
        "https://cjbwebdevelopment.com/services/",
        "https://cjbwebdevelopment.com/portfolio/",
        "https://cjbwebdevelopment.com/blog/",
        "https://cjbwebdevelopment.com/django-developer/london/",
        "https://cjbwebdevelopment.com/django-developer/berlin/",
        "https://cjbwebdevelopment.com/django-developer/amsterdam/",
        "https://cjbwebdevelopment.com/django-developer/dublin/",
        "https://cjbwebdevelopment.com/django-developer/paris/",
        "https://cjbwebdevelopment.com/django-developer/barcelona/",
        "https://cjbwebdevelopment.com/django-developer/munich/",
        "https://cjbwebdevelopment.com/django-developer/stockholm/",
        "https://cjbwebdevelopment.com/django-developer/copenhagen/",
        "https://cjbwebdevelopment.com/django-developer/vienna/",
        "https://cjbwebdevelopment.com/django-developer/zurich/",
        "https://cjbwebdevelopment.com/django-developer/brussels/",
        "https://cjbwebdevelopment.com/pricing/",
        "https://cjbwebdevelopment.com/privacy/",
        "https://cjbwebdevelopment.com/terms/",
    ]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f"  <url><loc>{url}</loc></url>\n"
    xml += '</urlset>'
    return HttpResponse(xml, content_type="application/xml")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('blog/', include('blog.urls')),
    path('sitemap.xml', sitemap_xml, name='sitemap'),
    path('robots.txt', robots_txt, name='robots'),
]
