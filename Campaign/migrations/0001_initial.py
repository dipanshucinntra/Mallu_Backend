# Generated by Django 3.2.7 on 2022-09-05 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Employee', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CampaignSetName', models.CharField(blank=True, max_length=100)),
                ('CampSetType', models.CharField(default='Undefined', max_length=255)),
                ('CampaignAccess', models.CharField(blank=True, max_length=250)),
                ('Description', models.CharField(blank=True, max_length=250)),
                ('LeadSource', models.CharField(blank=True, max_length=1000)),
                ('LeadPriority', models.CharField(blank=True, max_length=250)),
                ('LeadStatus', models.CharField(blank=True, max_length=250)),
                ('LeadFromDate', models.CharField(blank=True, max_length=100)),
                ('LeadToDate', models.CharField(blank=True, max_length=100)),
                ('LeadZone', models.TextField(blank=True, max_length=1000)),
                ('LeadGroupType', models.TextField(blank=True, max_length=1000)),
                ('LeadCategory', models.TextField(blank=True, max_length=1000)),
                ('OppType', models.CharField(blank=True, max_length=250)),
                ('OppSalePerson', models.CharField(blank=True, max_length=250)),
                ('OppStage', models.CharField(blank=True, max_length=250)),
                ('OppFromDate', models.CharField(blank=True, max_length=100)),
                ('OppToDate', models.CharField(blank=True, max_length=100)),
                ('OppZone', models.TextField(blank=True, max_length=1000)),
                ('OppGroupType', models.TextField(blank=True, max_length=1000)),
                ('OppCategory', models.TextField(blank=True, max_length=1000)),
                ('BPType', models.CharField(blank=True, max_length=250)),
                ('BPSalePerson', models.CharField(blank=True, max_length=250)),
                ('BPCountry', models.CharField(blank=True, max_length=250)),
                ('BPCountryCode', models.CharField(blank=True, max_length=1000)),
                ('BPState', models.CharField(blank=True, max_length=1000)),
                ('BPStateCode', models.CharField(blank=True, max_length=1000)),
                ('BPIndustry', models.TextField(blank=True, max_length=1000)),
                ('BPFromDate', models.CharField(blank=True, max_length=100)),
                ('BPToDate', models.CharField(blank=True, max_length=100)),
                ('BPZone', models.TextField(blank=True, max_length=1000)),
                ('BPGroupType', models.TextField(blank=True, max_length=1000)),
                ('BPCategory', models.TextField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=250)),
                ('intProdCat', models.CharField(blank=True, max_length=250)),
                ('intProjCat', models.CharField(blank=True, max_length=250)),
                ('MemberList', models.CharField(blank=True, max_length=250)),
                ('Status', models.IntegerField(default=1)),
                ('CreateDate', models.CharField(blank=True, max_length=100)),
                ('CreateTime', models.CharField(blank=True, max_length=100)),
                ('AllLead', models.IntegerField(default=0)),
                ('AllOpp', models.IntegerField(default=0)),
                ('AllBP', models.IntegerField(default=0)),
                ('CampaignSetOwner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CampaignSetOwner', to='Employee.employee', to_field='SalesEmployeeCode')),
                ('CreateBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CreateBy', to='Employee.employee', to_field='SalesEmployeeCode')),
            ],
        ),
        migrations.CreateModel(
            name='CampaignSetMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=100)),
                ('Phone', models.CharField(blank=True, max_length=100)),
                ('Email', models.CharField(blank=True, max_length=100)),
                ('CampSetId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Campaign.campaignset')),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CampaignName', models.CharField(blank=True, max_length=100)),
                ('StartDate', models.CharField(blank=True, max_length=100)),
                ('EndDate', models.CharField(blank=True, max_length=100)),
                ('Type', models.CharField(default='Undefined', max_length=255)),
                ('Frequency', models.CharField(default='Undefined', max_length=255)),
                ('WeekDay', models.CharField(blank=True, default='', max_length=255)),
                ('MonthlyDate', models.TextField(blank=True, max_length=255)),
                ('Message', models.TextField(blank=True, max_length=1000)),
                ('QualityResponse', models.CharField(default='Undefined', max_length=255)),
                ('Sent', models.IntegerField(default=0)),
                ('Delivered', models.IntegerField(default=0)),
                ('Opened', models.IntegerField(default=0)),
                ('Responded', models.IntegerField(default=0)),
                ('Status', models.IntegerField(default=1)),
                ('CreateDate', models.CharField(blank=True, max_length=100)),
                ('CreateTime', models.CharField(blank=True, max_length=100)),
                ('Subject', models.CharField(blank=True, max_length=100)),
                ('RunTime', models.CharField(blank=True, max_length=15)),
                ('Attachments', models.TextField(blank=True, max_length=1000)),
                ('CampaignOwner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CampaignOwner', to='Employee.employee', to_field='SalesEmployeeCode')),
                ('CampaignSetId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Campaign.campaignset')),
            ],
        ),
    ]
