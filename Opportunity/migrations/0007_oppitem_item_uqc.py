# Generated by Django 3.2.13 on 2023-03-21 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Opportunity', '0006_auto_20221103_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='oppitem',
            name='Item_uqc',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]