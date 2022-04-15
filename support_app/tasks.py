from support_site.celery import app
from django.core.mail import send_mail
from support_site.settings import EMAIL_HOST_USER
from .utils import get_prepared_email, EmailType


@app.task(bind=True)
def send_email(self, email_type: EmailType, email_address, *args):
    print("Sending email...")
    print(f"Recipient: {email_address}")
    email_message = get_prepared_email(email_type, *args)
    send_mail(subject='Support service', message=email_message,
              from_email=EMAIL_HOST_USER,
              recipient_list=[email_address])
    print("Sent!")
