# subscriptions/management/commands/send_renewals.py

import datetime
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings

from subscriptions.models import Subscription

class Command(BaseCommand):
    help = 'Send email reminders for subscriptions renewing soon'

    def handle(self, *args, **options):
        """
        Find subscriptions with next_renewal in the next 7 days
        and send an email reminder to the user.
        """
        now = timezone.now().date()
        in_7_days = now + datetime.timedelta(days=7)

        upcoming_subs = Subscription.objects.filter(next_renewal__range=(now, in_7_days))

        for sub in upcoming_subs:
            user_email = sub.user.email
            if user_email:
                subject = f"Reminder: {sub.name} renews soon"
                message = (
                    f"Hello {sub.user.username},\n\n"
                    f"This is a reminder that your subscription to {sub.name} "
                    f"will renew on {sub.next_renewal}.\n\n"
                    "Kind regards,\n"
                    "Subscription Manager Team"
                )

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user_email],
                    fail_silently=False
                )

        self.stdout.write(self.style.SUCCESS("Successfully sent subscription renewal reminders"))
