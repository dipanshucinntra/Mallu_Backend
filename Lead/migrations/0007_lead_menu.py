# Generated by Django 3.2.13 on 2023-09-25 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lead', '0006_lead_attendedby_lead_contacttwo_lead_functiondate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='Menu',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
