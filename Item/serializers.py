from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

class ItSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["ItemCode","ItemName"]

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = "__all__"

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class UQCSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unitquantitycode
        fields = ["uqc_name", "uqc_code"]


class UQCGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unitquantitycode
        fields = ["id","uqc_name", "uqc_code"]
