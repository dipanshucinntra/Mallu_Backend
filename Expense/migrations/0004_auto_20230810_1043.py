# Generated by Django 3.2.13 on 2023-08-10 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Expense', '0003_auto_20230209_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='DailyService_id',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='expense',
            name='total_distance',
            field=models.IntegerField(default=0),
        ),
    ]
