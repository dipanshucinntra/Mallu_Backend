# Generated by Django 3.2.13 on 2022-10-10 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartner', '0007_auto_20221010_0725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesspartner',
            name='intProdCat',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='businesspartner',
            name='intProjCat',
            field=models.TextField(blank=True),
        ),
    ]