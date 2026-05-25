from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def robots_txt(request):
    return HttpResponse("User-agent: *\nAllow: /\nSitemap: https://cjbwebdevelopment.com/sitemap.xml\n", content_type="text/plain")

def sitemap_xml(request):
    urls = [
        "https://cjbwebdevelopment.com/",
        "https://cjbwebdevelopment.com/contact/",
        "https://cjbwebdevelopment.com/services/",
        "https://cjbwebdevelopment.com/portfolio/",
        "https://cjbwebdevelopment.com/blog/",
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
