# Generated by Django 3.2.13 on 2023-03-20 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0002_item_uomno'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unitquantitycode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uqc_name', models.CharField(blank=True, max_length=200)),
                ('uqc_code', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]