# Generated by Django 3.2.13 on 2023-01-04 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='country',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='employee',
            name='country_code',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='employee',
            name='state',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='employee',
            name='state_code',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]