from rest_framework import serializers
from .models import Branch, SettingBranch

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"



class SettingBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingBranch
        fields = ["branch_name","address","phone","state","gst_number"]


class SettingGetBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingBranch
        fields = "__all__"




