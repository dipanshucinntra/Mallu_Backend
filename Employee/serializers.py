from rest_framework import serializers
from .models import *

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = "__all__"
        #depth=1
                
class TargetqtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Targetqty
        fields = "__all__"
        depth=1

class TargetyrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Targetyr
        fields = "__all__"
        depth=1
                