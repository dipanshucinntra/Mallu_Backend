from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        