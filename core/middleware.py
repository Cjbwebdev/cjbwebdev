"""
Security middleware for CJB Web Development — adds Content-Security-Policy
and other security headers with proper CDN allowlisting so Tailwind and
Font Awesome load correctly through Cloudflare.
"""

CSP_POLICY = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com "
    "https://cdnjs.cloudflare.com; "
    "img-src 'self' data: https:; "
    "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
    "connect-src 'self'; "
    "base-uri 'self'; "
    "object-src 'none'; "
    "frame-ancestors 'none'"
)


class SecurityHeadersMiddleware:
    """
    Adds strict security headers to every response.
    Runs early in the middleware stack so Cloudflare sees these headers
    from the origin and doesn't need to inject its own (broken) CSP.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Content Security Policy — must allow CDNs for Tailwind + Font Awesome
        response["Content-Security-Policy"] = CSP_POLICY

        # Prevent MIME type sniffing
        response["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking
        response["X-Frame-Options"] = "DENY"

        # Restrict referrer info
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Cross-origin isolation
        response["Cross-Origin-Opener-Policy"] = "same-origin"

        return response
