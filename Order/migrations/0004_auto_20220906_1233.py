# Generated by Django 3.2.13 on 2022-09-06 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0003_auto_20220906_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addendumrequest',
            name='Attachments',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='addendumrequest',
            name='Date',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='addendumrequest',
            name='OrderID',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='addendumrequest',
            name='Time',
            field=models.CharField(max_length=50),
        ),
    ]