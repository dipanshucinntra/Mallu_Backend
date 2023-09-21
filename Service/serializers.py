from rest_framework import serializers
from .models import *

class DailyServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyService
        fields = "__all__"


class DailyCustomerServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyCustomerService
        fields = "__all__"