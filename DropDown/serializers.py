from rest_framework import serializers
from .models import DropDown

class DropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropDown
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        depth=1
        fields = "__all__"

# class StaticDropDownSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StaticDropDown
#         #fields = ['ename',"econtact"]
#         #exclude = ['id']
#         depth=1
#         fields = "__all__"
