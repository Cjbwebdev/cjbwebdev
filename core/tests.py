"""
Comprehensive test suite for cjbwebdev-site.
Covers all views, URLs, forms, auth, CSRF, security, and project data.
"""
from django.test import TestCase, Client, override_settings
from django.urls import reverse, resolve
from django.core import mail
from django.conf import settings
from .forms import ContactForm
from .views import PROJECTS, FEATURED_IDS


# ═══════════════════════════════════════════════════════════════
# ContactForm Tests
# ═══════════════════════════════════════════════════════════════

class TestContactForm(TestCase):
    """Test the ContactForm validation and widget attributes."""

    def test_01_valid_form_data(self):
        """Form accepts valid submission data."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Project Inquiry',
            'message': 'I would like to discuss a project.',
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    def test_02_missing_required_fields(self):
        """Form rejects submissions with missing required fields."""
        # Empty form
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('subject', form.errors)
        self.assertIn('message', form.errors)

    def test_03_invalid_email(self):
        """Form rejects invalid email addresses."""
        data = {
            'name': 'John',
            'email': 'not-an-email',
            'subject': 'Test',
            'message': 'Hello',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_04_widget_css_classes(self):
        """Form fields have the expected CSS classes on widgets."""
        form = ContactForm()
        self.assertIn('class="form-control"', str(form['name']))
        self.assertIn('class="form-control"', str(form['email']))
        self.assertIn('class="form-control"', str(form['subject']))
        self.assertIn('class="form-control"', str(form['message']))

    def test_05_field_max_lengths(self):
        """Form enforces max_length constraints."""
        data = {
            'name': 'A' * 101,  # exceeds max_length=100
            'email': 'test@example.com',
            'subject': 'Test',
            'message': 'Hi',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_06_subject_max_length(self):
        """Subject field enforces max_length=200."""
        data = {
            'name': 'John',
            'email': 'test@example.com',
            'subject': 'X' * 201,
            'message': 'Hi',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)


# ═══════════════════════════════════════════════════════════════
# Home Page Tests
# ═══════════════════════════════════════════════════════════════

class TestHomeView(TestCase):
    """Test the home page view."""

    def test_07_home_status_200(self):
        """Home page returns HTTP 200."""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_08_home_template(self):
        """Home page uses the correct template."""
        response = self.client.get(reverse('core:home'))
        self.assertTemplateUsed(response, 'pages/home.html')

    def test_09_home_project_count(self):
        """Home context includes project_count matching PROJECTS length."""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.context['project_count'], len(PROJECTS))

    def test_10_home_featured_projects(self):
        """Home context includes only featured projects."""
        response = self.client.get(reverse('core:home'))
        featured = response.context['featured_projects']
        self.assertEqual(len(featured), len(FEATURED_IDS))
        featured_names = [p['name'] for p in featured]
        self.assertEqual(set(featured_names), set(FEATURED_IDS))

    def test_11_home_content_type(self):
        """Home page returns HTML content type."""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')


# ═══════════════════════════════════════════════════════════════
# Contact Page Tests
# ═══════════════════════════════════════════════════════════════

class TestContactView(TestCase):
    """Test the contact page GET and POST."""

    def test_12_contact_get_200(self):
        """Contact GET returns 200 with form in context."""
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_13_contact_get_template(self):
        """Contact page uses correct template."""
        response = self.client.get(reverse('core:contact'))
        self.assertTemplateUsed(response, 'pages/contact.html')

    def test_14_contact_get_csrf_token(self):
        """Contact GET response includes CSRF token."""
        response = self.client.get(reverse('core:contact'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_15_contact_post_valid_sends_email(self):
        """Valid contact POST sends email and shows success message."""
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'subject': 'Website Inquiry',
            'message': 'Can you build me a site?',
        }
        response = self.client.post(reverse('core:contact'), data, follow=True)
        # Should redirect back to contact after successful post
        self.assertRedirects(response, reverse('core:contact'))
        # One email should have been sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn('Website Inquiry', email.subject)
        self.assertIn('Jane Doe', email.body)
        self.assertIn('jane@example.com', email.body)
        self.assertIn('Can you build me a site?', email.body)
        self.assertEqual(email.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(email.to, ['support@cjbwebdevelopment.com'])

    def test_16_contact_post_success_message(self):
        """Successful contact submission adds a success message."""
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'subject': 'Test',
            'message': 'Testing messages framework.',
        }
        response = self.client.post(reverse('core:contact'), data, follow=True)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertIn('Message sent', str(messages_list[0]))

    def test_17_contact_post_invalid_shows_errors(self):
        """Invalid contact POST re-renders form with errors."""
        data = {
            'name': '',
            'email': 'bad-email',
            'subject': '',
            'message': '',
        }
        response = self.client.post(reverse('core:contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        # No email should be sent
        self.assertEqual(len(mail.outbox), 0)

    def test_18_contact_post_no_csrf_403(self):
        """POST without CSRF token is rejected with 403 (CSRF middleware active)."""
        # Create a client that doesn't enforce CSRF in tests — actually
        # Django's test client does enforce CSRF by default.
        # We test that a POST without proper token fails.
        client = Client(enforce_csrf_checks=True)
        data = {
            'name': 'Attacker',
            'email': 'bad@evil.com',
            'subject': 'Spam',
            'message': 'Buy now!!!',
        }
        response = client.post(reverse('core:contact'), data)
        self.assertEqual(response.status_code, 403)

    def test_19_contact_get_no_messages(self):
        """Fresh GET to contact has no messages."""
        response = self.client.get(reverse('core:contact'))
        messages_list = list(response.context.get('messages', []))
        self.assertEqual(len(messages_list), 0)


# ═══════════════════════════════════════════════════════════════
# Services Page Tests
# ═══════════════════════════════════════════════════════════════

class TestServicesView(TestCase):
    """Test the services page."""

    def test_20_services_status_200(self):
        """Services page returns HTTP 200."""
        response = self.client.get(reverse('core:services'))
        self.assertEqual(response.status_code, 200)

    def test_21_services_template(self):
        """Services page uses correct template."""
        response = self.client.get(reverse('core:services'))
        self.assertTemplateUsed(response, 'pages/services.html')

    def test_22_services_html_content(self):
        """Services page contains expected content."""
        response = self.client.get(reverse('core:services'))
        self.assertContains(response, '<html', html=False)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')


# ═══════════════════════════════════════════════════════════════
# Portfolio Page Tests
# ═══════════════════════════════════════════════════════════════

class TestPortfolioView(TestCase):
    """Test the portfolio page."""

    def test_23_portfolio_status_200(self):
        """Portfolio page returns HTTP 200."""
        response = self.client.get(reverse('core:portfolio'))
        self.assertEqual(response.status_code, 200)

    def test_24_portfolio_template(self):
        """Portfolio page uses correct template."""
        response = self.client.get(reverse('core:portfolio'))
        self.assertTemplateUsed(response, 'pages/portfolio.html')

    def test_25_portfolio_all_projects(self):
        """Portfolio context includes ALL projects."""
        response = self.client.get(reverse('core:portfolio'))
        self.assertEqual(len(response.context['projects']), len(PROJECTS))
        # Verify each project has required keys
        for project in response.context['projects']:
            self.assertIn('name', project)
            self.assertIn('url', project)
            self.assertIn('tech', project)
            self.assertIn('desc', project)
            self.assertIn('tags', project)
            self.assertIn('status', project)

    def test_26_portfolio_project_statuses(self):
        """All portfolio projects have 'live' status."""
        response = self.client.get(reverse('core:portfolio'))
        for project in response.context['projects']:
            self.assertEqual(project['status'], 'live')


# ═══════════════════════════════════════════════════════════════
# Blog Views Tests
# ═══════════════════════════════════════════════════════════════

class TestBlogViews(TestCase):
    """Test the blog index and post views."""

    def test_27_blog_index_status_200(self):
        """Blog index returns HTTP 200."""
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)

    def test_28_blog_index_template(self):
        """Blog index uses correct template."""
        response = self.client.get(reverse('blog:index'))
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_29_blog_index_has_posts(self):
        """Blog index context includes posts list."""
        response = self.client.get(reverse('blog:index'))
        self.assertIn('posts', response.context)
        posts = response.context['posts']
        # There should be at least 1 real blog post (excluding index.html and post_template.html)
        self.assertGreater(len(posts), 0)

    def test_30_blog_index_post_structure(self):
        """Each post in the index has slug, title, date, snippet keys."""
        response = self.client.get(reverse('blog:index'))
        for post in response.context['posts']:
            self.assertIn('slug', post)
            self.assertIn('title', post)
            self.assertIn('date', post)
            self.assertIn('snippet', post)

    def test_31_blog_index_excludes_templates(self):
        """Blog index excludes index.html and post_template.html from posts."""
        response = self.client.get(reverse('blog:index'))
        slugs = [p['slug'] for p in response.context['posts']]
        self.assertNotIn('index', slugs)
        self.assertNotIn('post_template', slugs)

    def test_32_blog_post_valid_slug(self):
        """A valid blog post slug returns 200."""
        # Get the first post slug from the index
        index_response = self.client.get(reverse('blog:index'))
        if index_response.context['posts']:
            first_slug = index_response.context['posts'][0]['slug']
            response = self.client.get(
                reverse('blog:post', kwargs={'slug': first_slug})
            )
            self.assertEqual(response.status_code, 200)

    def test_33_blog_post_invalid_slug_raises_template_does_not_exist(self):
        """An invalid blog post slug raises TemplateDoesNotExist (blog view does not catch it).
        
        In production with DEBUG=False this would become a 500; we verify the
        exception type to ensure it's a missing-template issue, not a crash.
        """
        from django.template import TemplateDoesNotExist
        with self.assertRaises(TemplateDoesNotExist):
            self.client.get(
                reverse('blog:post', kwargs={'slug': 'nonexistent-post-xyz-123'})
            )

    def test_34_blog_index_html_content(self):
        """Blog index has proper HTML structure."""
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')


# ═══════════════════════════════════════════════════════════════
# Admin View Tests
# ═══════════════════════════════════════════════════════════════

class TestAdminView(TestCase):
    """Test admin site accessibility and redirects."""

    def test_35_admin_login_redirect(self):
        """Unauthenticated access to /admin/ redirects to login."""
        response = self.client.get('/admin/')
        # Should redirect to admin login page (302)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_36_admin_login_page_accessible(self):
        """Admin login page is accessible."""
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log in')

    def test_37_admin_csrf_on_login(self):
        """Admin login page includes CSRF token."""
        response = self.client.get('/admin/login/')
        self.assertContains(response, 'csrfmiddlewaretoken')


# ═══════════════════════════════════════════════════════════════
# Security & Middleware Tests
# ═══════════════════════════════════════════════════════════════

class TestSecurity(TestCase):
    """Test security headers and middleware behavior."""

    def test_38_xframe_options_header(self):
        """All pages include X-Frame-Options header (clickjacking protection)."""
        urls = [
            reverse('core:home'),
            reverse('core:contact'),
            reverse('core:services'),
            reverse('core:portfolio'),
            reverse('blog:index'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertIn('X-Frame-Options', response,
                          f"X-Frame-Options missing from {url}")
            self.assertEqual(response['X-Frame-Options'], 'DENY')

    def test_39_csrf_cookie_set(self):
        """CSRF cookie is set on a page that renders a csrf_token (contact form)."""
        # The CSRF cookie is only set when {% csrf_token %} is rendered in a template.
        # The contact page has a form, so it should set the cookie.
        response = self.client.get(reverse('core:contact'))
        self.assertIn('csrftoken', response.cookies,
                      "CSRF cookie not set — ensure csrf_token is used in contact form")

    def test_40_content_type_html(self):
        """All pages return correct Content-Type."""
        urls = [
            reverse('core:home'),
            reverse('core:contact'),
            reverse('core:services'),
            reverse('core:portfolio'),
            reverse('blog:index'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(
                response['Content-Type'],
                'text/html; charset=utf-8',
                f"Wrong Content-Type for {url}"
            )

    def test_41_content_security_headers(self):
        """SecurityMiddleware adds appropriate headers."""
        response = self.client.get(reverse('core:home'))
        # X-Content-Type-Options should be present
        self.assertIn('X-Content-Type-Options', response)
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')


# ═══════════════════════════════════════════════════════════════
# URL Resolution Tests
# ═══════════════════════════════════════════════════════════════

class TestURLResolution(TestCase):
    """Test that URL names resolve to the correct view functions."""

    def test_42_url_name_home(self):
        """URL name 'core:home' resolves to home view."""
        from core.views import home
        resolver = resolve('/')
        self.assertEqual(resolver.func, home)
        self.assertEqual(resolver.url_name, 'home')

    def test_43_url_name_contact(self):
        """URL name 'core:contact' resolves to contact view."""
        from core.views import contact
        resolver = resolve('/contact/')
        self.assertEqual(resolver.func, contact)

    def test_44_url_name_services(self):
        """URL name 'core:services' resolves to services view."""
        from core.views import services
        resolver = resolve('/services/')
        self.assertEqual(resolver.func, services)

    def test_45_url_name_portfolio(self):
        """URL name 'core:portfolio' resolves to portfolio view."""
        from core.views import portfolio
        resolver = resolve('/portfolio/')
        self.assertEqual(resolver.func, portfolio)

    def test_46_url_name_blog_index(self):
        """URL name 'blog:index' resolves to blog_index view."""
        from blog.views import blog_index
        resolver = resolve('/blog/')
        self.assertEqual(resolver.func, blog_index)

    def test_47_reverse_lookup_home(self):
        """reverse('core:home') returns '/'."""
        self.assertEqual(reverse('core:home'), '/')

    def test_48_reverse_lookup_contact(self):
        """reverse('core:contact') returns '/contact/'."""
        self.assertEqual(reverse('core:contact'), '/contact/')

    def test_49_reverse_lookup_blog(self):
        """reverse('blog:index') returns '/blog/'."""
        self.assertEqual(reverse('blog:index'), '/blog/')


# ═══════════════════════════════════════════════════════════════
# Project Data Integrity Tests
# ═══════════════════════════════════════════════════════════════

class TestProjectData(TestCase):
    """Test the PROJECTS data structure integrity."""

    def test_50_projects_not_empty(self):
        """PROJECTS list is not empty."""
        self.assertGreater(len(PROJECTS), 0)

    def test_51_project_required_keys(self):
        """Every project has all required keys."""
        required_keys = {'name', 'url', 'tech', 'desc', 'long_desc', 'tags', 'status', 'image'}
        for project in PROJECTS:
            self.assertTrue(
                required_keys.issubset(project.keys()),
                f"Project {project.get('name', '?')} missing keys: "
                f"{required_keys - set(project.keys())}"
            )

    def test_52_featured_ids_match_projects(self):
        """All FEATURED_IDS correspond to actual project names."""
        project_names = {p['name'] for p in PROJECTS}
        for fid in FEATURED_IDS:
            self.assertIn(fid, project_names,
                          f"Featured ID '{fid}' not found in PROJECTS")

    def test_53_project_urls_valid(self):
        """All project URLs start with https://."""
        for project in PROJECTS:
            self.assertTrue(
                project['url'].startswith('https://'),
                f"Project {project['name']} URL is not HTTPS: {project['url']}"
            )

    def test_54_project_tags_are_lists(self):
        """All project tags are non-empty lists."""
        for project in PROJECTS:
            self.assertIsInstance(project['tags'], list)
            self.assertGreater(len(project['tags']), 0)

    def test_55_featured_projects_are_three(self):
        """Featured projects are exactly 3."""
        self.assertEqual(len(FEATURED_IDS), 3)


# ═══════════════════════════════════════════════════════════════
# Integration / Smoke Tests
# ═══════════════════════════════════════════════════════════════

class TestIntegration(TestCase):
    """Integration-level smoke tests across the site."""

    def test_56_all_pages_accessible(self):
        """Every public page returns 200."""
        pages = [
            reverse('core:home'),
            reverse('core:contact'),
            reverse('core:services'),
            reverse('core:portfolio'),
            reverse('blog:index'),
        ]
        for url in pages:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200,
                             f"Page {url} returned {response.status_code}")

    def test_57_contact_submit_then_revisit(self):
        """After submitting contact form, revisit shows fresh form."""
        data = {
            'name': 'Test User',
            'email': 'test@test.com',
            'subject': 'Follow-up',
            'message': 'Checking form reset.',
        }
        # Submit
        self.client.post(reverse('core:contact'), data, follow=True)
        # Revisit
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        # Form should be fresh (unbound)
        form = response.context['form']
        self.assertFalse(form.is_bound)

    def test_58_blog_navigation_flow(self):
        """User can visit blog index, then a post, then go back."""
        # Blog index
        idx = self.client.get(reverse('blog:index'))
        self.assertEqual(idx.status_code, 200)
        posts = idx.context['posts']
        if posts:
            # Visit first post
            post_url = reverse('blog:post', kwargs={'slug': posts[0]['slug']})
            post_resp = self.client.get(post_url)
            self.assertEqual(post_resp.status_code, 200)
            # Go back to blog index
            idx2 = self.client.get(reverse('blog:index'))
            self.assertEqual(idx2.status_code, 200)
