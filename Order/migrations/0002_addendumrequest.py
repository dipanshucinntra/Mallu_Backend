# Generated by Django 3.2.13 on 2022-09-06 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddendumRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OrderID', models.CharField(blank=True, max_length=5)),
                ('Date', models.CharField(blank=True, max_length=50)),
                ('Time', models.CharField(blank=True, max_length=50)),
                ('Attachments', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]
