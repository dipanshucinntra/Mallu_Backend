from rest_framework import serializers
from .models import *

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class AddressExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressExtension
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        
class DocumentLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentLines
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class AddendumSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddendumRequest
        fields = "__all__"


##################################################################################################################


class OrderRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOrder
        fields = "__all__"

class OrderRequestAddressExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddressExtension
        fields = "__all__"
        
class OrderRequestDocumentLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDocumentLines
        fields = "__all__"