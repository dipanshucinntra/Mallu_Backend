# Generated by Django 3.2.13 on 2022-09-29 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='architect',
            new_name='completion_date',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='consultant_name',
            new_name='contact_person',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='expected_start_date',
            new_name='start_date',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='mep_consultant',
            new_name='target_date',
        ),
        migrations.RemoveField(
            model_name='project',
            name='consultant_code',
        ),
        migrations.AddField(
            model_name='project',
            name='customer_group_type',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='kit_consultant_code',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='kit_consultant_name',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='mep_consultant_code',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='mep_consultant_name',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='pm_consultant_code',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='pm_consultant_name',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='project',
            name='location',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_cost',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_owner',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='project',
            name='sector',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
