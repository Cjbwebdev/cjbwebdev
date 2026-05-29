"""
Resend email backend for Django.
Uses Resend's HTTP API (not SMTP) — simpler, faster, no port-blocking issues.

Setup:
1. Create account at https://resend.com
2. Get API key from https://resend.com/api-keys
3. Set RESEND_API_KEY env var
4. Set DEFAULT_FROM_EMAIL to your verified sending domain

Free tier: 100 emails/day, no credit card required.
"""
import logging
import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address

logger = logging.getLogger("resend")


class ResendBackend(BaseEmailBackend):
    """Django email backend that sends via Resend HTTP API."""

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.api_key = getattr(settings, "RESEND_API_KEY", None) or ""
        self.api_url = "https://api.resend.com/emails"

    def open(self):
        if not self.api_key:
            if not self.fail_silently:
                raise ValueError("RESEND_API_KEY is not set.")
            return False
        return True

    def close(self):
        pass

    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        sent = 0
        for message in email_messages:
            try:
                payload = {
                    "from": sanitize_address(message.from_email, message.encoding),
                    "to": [sanitize_address(addr, message.encoding) for addr in message.to],
                    "subject": message.subject,
                }
                if message.alternatives:
                    for alt_content, alt_mimetype in message.alternatives:
                        if alt_mimetype == "text/html":
                            payload["html"] = alt_content
                            break
                if "html" not in payload and message.body:
                    payload["text"] = message.body
                elif "html" not in payload:
                    payload["text"] = message.subject
                if message.cc:
                    payload["cc"] = [sanitize_address(addr, message.encoding) for addr in message.cc]
                if message.bcc:
                    payload["bcc"] = [sanitize_address(addr, message.encoding) for addr in message.bcc]
                if message.reply_to:
                    payload["reply_to"] = [sanitize_address(addr, message.encoding) for addr in message.reply_to]
                resp = requests.post(
                    self.api_url,
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    timeout=15,
                )
                if resp.status_code == 200:
                    logger.info(f"Resend sent: {message.subject} -> {message.to}")
                    sent += 1
                else:
                    error = resp.json().get("message", resp.text)
                    logger.error(f"Resend error {resp.status_code}: {error}")
                    if not self.fail_silently:
                        raise Exception(f"Resend API error: {error}")
            except Exception as e:
                logger.error(f"Resend send failed: {e}")
                if not self.fail_silently:
                    raise
        return sent
