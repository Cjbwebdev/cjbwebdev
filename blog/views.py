from django.shortcuts import render
from pathlib import Path
import os, re

BLOG_DIR = Path(__file__).resolve().parent.parent / 'templates' / 'blog'

def blog_index(request):
    posts = []
    if BLOG_DIR.exists():
        for f in sorted(BLOG_DIR.glob('*.html'), reverse=True):
            if f.name in ('index.html', 'post_template.html'):
                continue
            content = f.read_text()
            title = re.search(r'<title>(.*?)</title>', content, re.I)
            title = title.group(1).split('|')[0].strip().replace('&#x27;', "'") if title else f.stem.replace('-', ' ').title()
            date_m = re.search(r'<meta name="date" content="(.*?)"', content)
            snippet = re.search(r'<meta name="description" content="(.*?)"', content)
            posts.append({
                'slug': f.stem,
                'title': title,
                'date': date_m.group(1) if date_m else '',
                'snippet': snippet.group(1)[:200] if snippet else '',
            })
    return render(request, 'blog/index.html', {'posts': posts})

def blog_post(request, slug):
    return render(request, f'blog/{slug}.html')
