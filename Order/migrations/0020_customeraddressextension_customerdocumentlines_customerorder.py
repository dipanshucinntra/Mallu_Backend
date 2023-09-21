# Generated by Django 3.2.13 on 2023-06-26 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Branch', '0002_settingbranch'),
        ('Order', '0019_delete_deliverycreate'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAddressExtension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OrderID', models.CharField(blank=True, max_length=5)),
                ('BillToBuilding', models.CharField(blank=True, max_length=100)),
                ('ShipToState', models.CharField(blank=True, max_length=100)),
                ('BillToCity', models.CharField(blank=True, max_length=100)),
                ('ShipToCountry', models.CharField(blank=True, max_length=100)),
                ('BillToZipCode', models.CharField(blank=True, max_length=100)),
                ('ShipToStreet', models.CharField(blank=True, max_length=100)),
                ('BillToState', models.CharField(blank=True, max_length=100)),
                ('ShipToZipCode', models.CharField(blank=True, max_length=100)),
                ('BillToStreet', models.CharField(blank=True, max_length=100)),
                ('ShipToBuilding', models.CharField(blank=True, max_length=100)),
                ('ShipToCity', models.CharField(blank=True, max_length=100)),
                ('BillToCountry', models.CharField(blank=True, max_length=100)),
                ('U_SCOUNTRY', models.CharField(blank=True, max_length=100)),
                ('U_SSTATE', models.CharField(blank=True, max_length=100)),
                ('U_SHPTYPB', models.CharField(blank=True, max_length=100)),
                ('U_BSTATE', models.CharField(blank=True, max_length=100)),
                ('U_BCOUNTRY', models.CharField(blank=True, max_length=100)),
                ('U_SHPTYPS', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerDocumentLines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LineNum', models.IntegerField(default=0)),
                ('OrderID', models.CharField(blank=True, max_length=5)),
                ('Quantity', models.IntegerField(default=0)),
                ('UnitPrice', models.FloatField(default=0)),
                ('DiscountPercent', models.FloatField(default=0)),
                ('ItemDescription', models.CharField(blank=True, max_length=150)),
                ('ItemCode', models.CharField(blank=True, max_length=20)),
                ('TaxCode', models.CharField(blank=True, max_length=50)),
                ('U_FGITEM', models.CharField(blank=True, max_length=20)),
                ('CostingCode2', models.CharField(blank=True, max_length=20)),
                ('ProjectCode', models.CharField(blank=True, max_length=20)),
                ('FreeText', models.CharField(blank=True, max_length=500)),
                ('Tap_Qty', models.CharField(blank=True, max_length=50)),
                ('Tap_Type', models.CharField(blank=True, max_length=50)),
                ('Ht_Capacity', models.CharField(blank=True, max_length=50)),
                ('Ct_Capacity', models.CharField(blank=True, max_length=50)),
                ('At_Capacity', models.CharField(blank=True, max_length=50)),
                ('Pro_Capacity', models.CharField(blank=True, max_length=50)),
                ('Machine_Dimension', models.CharField(blank=True, max_length=100)),
                ('Machine_Colour', models.CharField(blank=True, max_length=100)),
                ('Type_of_Machine', models.CharField(blank=True, max_length=100)),
                ('Machine_Body_Material', models.CharField(blank=True, max_length=500)),
                ('UV_Germ', models.CharField(blank=True, max_length=500)),
                ('Sales_Type', models.CharField(blank=True, max_length=100)),
                ('Special_Remark', models.CharField(blank=True, max_length=500)),
                ('Tax', models.FloatField(default=0)),
                ('UomNo', models.CharField(blank=True, max_length=100)),
                ('Item_uqc', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TaxDate', models.CharField(blank=True, max_length=30)),
                ('DocDueDate', models.CharField(blank=True, max_length=30)),
                ('ContactPersonCode', models.CharField(blank=True, max_length=5)),
                ('DiscountPercent', models.FloatField(default=0)),
                ('DocDate', models.CharField(blank=True, max_length=30)),
                ('CardCode', models.CharField(blank=True, max_length=30)),
                ('Comments', models.CharField(blank=True, max_length=150)),
                ('SalesPersonCode', models.CharField(blank=True, max_length=5)),
                ('DocumentStatus', models.CharField(blank=True, max_length=50)),
                ('CancelStatus', models.CharField(blank=True, max_length=50)),
                ('DocCurrency', models.CharField(blank=True, max_length=50)),
                ('DocTotal', models.CharField(blank=True, max_length=50)),
                ('NetTotal', models.CharField(blank=True, max_length=50)),
                ('CardName', models.CharField(blank=True, max_length=150)),
                ('VatSum', models.CharField(blank=True, max_length=50)),
                ('CreationDate', models.CharField(blank=True, max_length=50)),
                ('OrdNo', models.CharField(blank=True, max_length=50)),
                ('PoNo', models.CharField(blank=True, max_length=50)),
                ('DatePO', models.CharField(blank=True, max_length=150)),
                ('Attach', models.CharField(blank=True, max_length=250)),
                ('Project', models.CharField(blank=True, max_length=50)),
                ('DocEntry', models.CharField(blank=True, max_length=5)),
                ('PaymentGroupCode', models.CharField(blank=True, max_length=5)),
                ('U_Term_Condition', models.TextField(blank=True)),
                ('U_TermInterestRate', models.FloatField(default=0)),
                ('U_TermPaymentTerm', models.CharField(blank=True, max_length=100)),
                ('U_TermDueDate', models.CharField(blank=True, max_length=100)),
                ('U_QUOTNM', models.CharField(blank=True, max_length=100)),
                ('U_QUOTID', models.IntegerField(default=0)),
                ('U_LEADID', models.IntegerField(default=0)),
                ('U_LEADNM', models.CharField(blank=True, max_length=150)),
                ('U_OPPID', models.CharField(blank=True, max_length=5)),
                ('U_OPPRNM', models.CharField(blank=True, max_length=100)),
                ('BPLID', models.CharField(blank=True, max_length=5)),
                ('DelStatus', models.CharField(blank=True, max_length=50)),
                ('CreateDate', models.CharField(blank=True, max_length=30)),
                ('CreateTime', models.CharField(blank=True, max_length=30)),
                ('UpdateDate', models.CharField(blank=True, max_length=30)),
                ('UpdateTime', models.CharField(blank=True, max_length=30)),
                ('GroupType', models.CharField(blank=True, max_length=100)),
                ('POAmount', models.CharField(blank=True, max_length=100)),
                ('ProjectLocation', models.CharField(blank=True, max_length=100)),
                ('OPSNumber', models.CharField(blank=True, max_length=100)),
                ('UrlNo', models.CharField(blank=True, max_length=100)),
                ('OtherInstruction', models.CharField(blank=True, max_length=100)),
                ('GSTNo', models.CharField(blank=True, max_length=100)),
                ('MICharges', models.CharField(blank=True, max_length=100)),
                ('LOCharges', models.CharField(blank=True, max_length=100)),
                ('Intall', models.CharField(blank=True, max_length=100)),
                ('CivWork', models.CharField(blank=True, max_length=100)),
                ('SSStatus', models.CharField(blank=True, max_length=100)),
                ('PlumStatus', models.CharField(blank=True, max_length=100)),
                ('technical_details', models.CharField(blank=True, max_length=20)),
                ('approved_drawing', models.CharField(blank=True, max_length=20)),
                ('addendum', models.CharField(blank=True, max_length=20)),
                ('special_instructions', models.CharField(blank=True, max_length=20)),
                ('URN', models.CharField(blank=True, max_length=20)),
                ('order_request_name', models.CharField(blank=True, max_length=200)),
                ('SettingBranch_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Branch.settingbranch')),
            ],
        ),
    ]
