# Generated by Django 3.2.13 on 2022-10-11 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0005_project_grouptype'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='arch_consultant_code',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='arch_consultant_name',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='arch_contact_person',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='cli_consultant_code',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='cli_consultant_name',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='cli_contact_person',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='contr_consultant_code',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='contr_consultant_name',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='contr_contact_person',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='fcm_consultant_code',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='fcm_consultant_name',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='fcm_contact_person',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='oth_consultant_code',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='oth_consultant_name',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='project',
            name='oth_contact_person',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]