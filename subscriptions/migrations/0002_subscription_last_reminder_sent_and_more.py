# Generated by Django 5.1.5 on 2025-02-06 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='last_reminder_sent',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='reminder_days',
            field=models.IntegerField(choices=[(3, '3 days before'), (5, '5 days before'), (9, '9 days before')], default=3),
        ),
    ]
