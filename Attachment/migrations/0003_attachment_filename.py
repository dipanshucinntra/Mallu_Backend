# Generated by Django 3.2.13 on 2022-10-17 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attachment', '0002_attachment_caption'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='FileName',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
