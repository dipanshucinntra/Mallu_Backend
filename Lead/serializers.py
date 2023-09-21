from rest_framework import serializers
from .models import *

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        depth = 1


class LeadSortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ["id","companyName"]


class LeadItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadItem
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class ChatterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatter
        fields = "__all__"
        
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = "__all__"
        
# class LeadEmployeeSerializer(serializers.ModelSerializer):
#     SalesEmployeeName = serializers.SerializerMethodField('get_employee_name')
#     class Meta:
#         model = Lead
#         fields = "__all__"
#         extra_fields =['SalesEmployeeName']

#     def get_employee_name(self, obj):
#         print("obj.junk_by :",obj.junk_by)
#         if Employee.objects.filter(SalesEmployeeCode=obj.junk_by).exists():
#             return Employee.objects.get(SalesEmployeeCode=obj.junk_by).SalesEmployeeName
#         else:
#             return ""
