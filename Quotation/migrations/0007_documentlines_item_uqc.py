# Generated by Django 3.2.13 on 2023-03-21 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quotation', '0006_quotation_bpemail'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentlines',
            name='Item_uqc',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
