# Generated by Django 4.2.2 on 2023-06-20 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DeliveryNote', '0004_remove_documentlines_status_deliverynote_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverynote',
            name='ShippedType',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='deliverynote',
            name='ShippedWith',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
