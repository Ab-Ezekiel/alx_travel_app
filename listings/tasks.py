# listings/tasks.py
from __future__ import annotations
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
import logging

from .models import Booking  # adjust import if Booking is in a different app

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_booking_confirmation_email(self, booking_id: int) -> None:
    """
    Celery task to send booking confirmation email.
    Uses Django's EMAIL_BACKEND configured in settings.py.
    """
    try:
        booking = Booking.objects.select_related("user").get(pk=booking_id)
    except Booking.DoesNotExist:
        logger.warning("Booking with id %s does not exist; skipping email.", booking_id)
        return

    # Prepare email context - include booking and user info
    context = {
        "booking": booking,
        "user": getattr(booking, "user", None),
        "site_name": getattr(settings, "SITE_NAME", "alx_travel_app"),
    }

    # Render templates if you have them; fallback to a simple body
    try:
        subject = render_to_string("emails/booking_confirmation_subject.txt", context).strip()
    except Exception:
        subject = f"Booking confirmation — #{booking.pk}"

    try:
        html_body = render_to_string("emails/booking_confirmation.html", context)
    except Exception:
        html_body = None

    try:
        text_body = render_to_string("emails/booking_confirmation.txt", context)
    except Exception:
        text_body = f"Hello,\n\nYour booking (ID: {booking.pk}) is confirmed.\n\nThanks."

    try:
        email = EmailMessage(
            subject=subject,
            body=text_body,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
            to=[booking.user.email] if getattr(booking, "user", None) else [booking.email],
        )
        if html_body:
            email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=False)
        logger.info("Sent booking confirmation email for booking %s", booking_id)
    except Exception as exc:
        logger.exception("Failed to send booking email for %s", booking_id)
        # retry with exponential backoff handled manually via countdown if desired
        raise self.retry(exc=exc)
