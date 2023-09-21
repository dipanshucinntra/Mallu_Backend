from rest_framework import serializers
from .models import Caller


class CallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caller
        fields = ["LeadId","MobileNumber","CallDuration","Remarks","EmployeeId","CreateTime","CreateDate","EmployeeName","Status","StatusType","Brocher"]


class CallerGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caller
        fields = "__all__"

