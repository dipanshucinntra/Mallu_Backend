# Generated by Django 3.2.13 on 2022-09-07 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Opportunity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staticstage',
            name='UTYPE',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
