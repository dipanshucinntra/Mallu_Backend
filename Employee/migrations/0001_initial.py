# Generated by Django 3.2.7 on 2022-09-05 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyID', models.CharField(blank=True, max_length=50)),
                ('SalesEmployeeCode', models.CharField(blank=True, max_length=20, unique=True)),
                ('SalesEmployeeName', models.CharField(blank=True, max_length=50)),
                ('EmployeeID', models.CharField(blank=True, max_length=30)),
                ('userName', models.CharField(blank=True, max_length=50)),
                ('password', models.CharField(blank=True, max_length=50)),
                ('firstName', models.CharField(blank=True, max_length=50)),
                ('middleName', models.CharField(blank=True, max_length=50)),
                ('lastName', models.CharField(blank=True, max_length=50)),
                ('Email', models.CharField(blank=True, max_length=50)),
                ('Mobile', models.CharField(blank=True, max_length=15)),
                ('role', models.CharField(blank=True, max_length=50)),
                ('position', models.CharField(blank=True, max_length=50)),
                ('branch', models.CharField(blank=True, max_length=20)),
                ('Active', models.CharField(blank=True, max_length=20)),
                ('salesUnit', models.CharField(blank=True, max_length=50)),
                ('passwordUpdatedOn', models.CharField(blank=True, max_length=30)),
                ('lastLoginOn', models.CharField(blank=True, max_length=30)),
                ('logedIn', models.CharField(blank=True, max_length=20)),
                ('reportingTo', models.CharField(blank=True, max_length=20)),
                ('FCM', models.CharField(blank=True, max_length=250)),
                ('div', models.CharField(blank=True, max_length=250)),
                ('timestamp', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Targetyr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Department', models.CharField(blank=True, max_length=50)),
                ('StartYear', models.IntegerField(default=0)),
                ('EndYear', models.IntegerField(default=0)),
                ('YearTarget', models.BigIntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('CreatedDate', models.CharField(blank=True, max_length=20)),
                ('UpdatedDate', models.CharField(blank=True, max_length=20)),
                ('SalesPersonCode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Employee.employee', to_field='SalesEmployeeCode')),
                ('reportingTo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reportingToTargetyr', to='Employee.employee', to_field='SalesEmployeeCode')),
            ],
        ),
        migrations.CreateModel(
            name='Targetqty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q1', models.BigIntegerField(default=0)),
                ('q2', models.BigIntegerField(default=0)),
                ('q3', models.BigIntegerField(default=0)),
                ('q4', models.BigIntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('CreatedDate', models.CharField(blank=True, max_length=20)),
                ('UpdatedDate', models.CharField(blank=True, max_length=20)),
                ('SalesPersonCode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Employee.employee', to_field='SalesEmployeeCode')),
                ('YearTarget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.targetyr')),
                ('reportingTo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reportingToTargetqty', to='Employee.employee', to_field='SalesEmployeeCode')),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('monthYear', models.CharField(blank=True, max_length=50)),
                ('qtr', models.IntegerField(default=0)),
                ('sale', models.FloatField(default=0)),
                ('sale_diff', models.FloatField(default=0)),
                ('CreatedDate', models.CharField(blank=True, max_length=20)),
                ('UpdatedDate', models.CharField(blank=True, max_length=20)),
                ('SalesPersonCode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Employee.employee', to_field='SalesEmployeeCode')),
                ('YearTarget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='YearTargetTarget', to='Employee.targetyr')),
            ],
        ),
    ]