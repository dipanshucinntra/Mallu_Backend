# Generated by Django 3.2.13 on 2022-11-14 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quotation', '0005_auto_20221010_0851'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='BPEmail',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
