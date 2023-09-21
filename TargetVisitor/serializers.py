from rest_framework import serializers
from .models import *


class TargetVisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetVisitor
        fields = "__all__"












