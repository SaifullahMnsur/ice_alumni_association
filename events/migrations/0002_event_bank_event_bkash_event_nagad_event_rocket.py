# Generated by Django 5.1.4 on 2024-12-31 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='bank',
            field=models.JSONField(blank=True, default=dict, help_text='Payment details for Bank (all necessary banking details).'),
        ),
        migrations.AddField(
            model_name='event',
            name='bkash',
            field=models.JSONField(blank=True, default=dict, help_text='Payment details for bKash (account number and payment option).'),
        ),
        migrations.AddField(
            model_name='event',
            name='nagad',
            field=models.JSONField(blank=True, default=dict, help_text='Payment details for Nagad (account number and payment option).'),
        ),
        migrations.AddField(
            model_name='event',
            name='rocket',
            field=models.JSONField(blank=True, default=dict, help_text='Payment details for Rocket (account number and payment option).'),
        ),
    ]
