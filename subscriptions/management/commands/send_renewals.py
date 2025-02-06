from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from subscriptions.models import Subscription
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send reminder emails for subscriptions that are nearing renewal'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        subscriptions = Subscription.objects.all()
        
        for sub in subscriptions:
            # Calculate when the reminder should be sent
            reminder_date = sub.next_renewal - timedelta(days=sub.reminder_days)
            
            # Check if today is the reminder day
            # Also check if we haven't already sent a reminder for this renewal period.
            if reminder_date == today and (not sub.last_reminder_sent or sub.last_reminder_sent < sub.next_renewal):
                subject = f"Reminder: {sub.name} is renewing soon!"
                message = (
                    f"Hello,\n\n"
                    f"This is a reminder that your subscription to {sub.name} renews on {sub.next_renewal}.\n"
                    f"Cost: ${sub.cost}\n"
                    "Thank you for using Subscription Manager!"
                )
                recipient_email = sub.user.email  
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [recipient_email],
                        fail_silently=False,
                    )
                    # Mark that the reminder was sent today
                    sub.last_reminder_sent = today
                    sub.save()
                    self.stdout.write(f"Sent reminder email for subscription {sub.id} to {recipient_email}")
                except Exception as e:
                    self.stderr.write(f"Failed to send email for subscription {sub.id}: {str(e)}")