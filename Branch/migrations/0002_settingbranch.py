# Generated by Django 3.2.13 on 2023-03-22 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Branch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SettingBranch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(blank=True, max_length=200)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('phone', models.CharField(blank=True, max_length=200)),
                ('state', models.CharField(blank=True, max_length=200)),
                ('gst_number', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]
