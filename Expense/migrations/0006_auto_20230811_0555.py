# Generated by Django 3.2.13 on 2023-08-11 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Expense', '0005_expensestatusremarks'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='status',
            new_name='accountant_status',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='approvalId',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='approval_remark',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='remarks',
        ),
        migrations.AddField(
            model_name='expense',
            name='accountant_approval',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='expense',
            name='rsm_approval',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='expense',
            name='rsm_status',
            field=models.CharField(blank=True, default='Pending', max_length=200),
        ),
    ]