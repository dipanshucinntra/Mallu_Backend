# Generated by Django 3.2.13 on 2022-11-08 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0012_order_urn_no'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='urn_no',
            new_name='URN',
        ),
    ]
