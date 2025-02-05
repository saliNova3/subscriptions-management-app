from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(to_email):
    subject = "Welcome to Subscription Manager"
    message = (
        "Hello!\n\n"
        "Thanks for signing up for our Subscription Manager app. "
        "We hope you enjoy tracking all your subscriptions in one place!"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [to_email]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
