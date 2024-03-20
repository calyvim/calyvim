from celery import shared_task
from django.template.loader import render_to_string
from django.template.defaultfilters import striptags
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from calyvim.models import User


@shared_task
def send_confirmation_email(email):
    user = User.objects.filter(email=email).first()
    if not user:
        # Log the event
        return

    email_confirmation_url = settings.SITE_URL + reverse(
        "email-confirm",
        kwargs={"token": user.email_confirmation_token()},
    )
    email_template = render_to_string(
        "email/accounts/email_confirmation.html",
        {"user": user, "email_confirmation_url": email_confirmation_url},
    )
    send_mail(
        subject="Calyvim | Email verification",
        html_message=email_template,
        message=striptags(email_template),
        fail_silently=True,
        recipient_list=[user.email],
        from_email="no-reply@calyvim.com",
    )
