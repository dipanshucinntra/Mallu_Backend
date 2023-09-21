from rest_framework import serializers
from .models import *

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"
        depth = 1

class ExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = "__all__"
        depth = 1

class ExpenseApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseStatusRemarks
        fields = "__all__"