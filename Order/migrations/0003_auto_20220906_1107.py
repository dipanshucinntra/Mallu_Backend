# Generated by Django 3.2.13 on 2022-09-06 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0002_addendumrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Attach',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='order',
            name='DatePO',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='order',
            name='OrdNo',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='PoNo',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='Project',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
