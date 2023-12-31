# Generated by Django 4.1.6 on 2023-08-04 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TargetVisitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthly_target', models.IntegerField(blank=True, max_length=200)),
                ('daily_visit', models.IntegerField(blank=True, max_length=200)),
                ('assigned_to', models.IntegerField(blank=True, max_length=200)),
                ('created_by', models.IntegerField(blank=True, max_length=200)),
                ('zone', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
