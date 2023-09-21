from rest_framework import serializers
from .models import *
from .models import *

class TenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = "__all__"
        depth=1
        
class PaymentInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInstrument
        fields = "__all__"
        depth=1

class CoverDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverDetail
        fields = "__all__"
        depth=1

class WorkOrItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrItemDetails
        fields = "__all__"
        # depth=1


class CritcalDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CritcalDates
        fields = "__all__"
        # depth=1

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = "__all__"
        # depth=1

class CorrigendumListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrigendumList
        fields = "__all__"
        # depth=1

class TenderSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenderSubmission
        fields = "__all__"
        # depth=1


class TenderOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenderOpening
        fields = "__all__"
        # depth=1

class TechnicalOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalOpening
        fields = "__all__"
        # depth=1


class LowestOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = LowestOne
        fields = "__all__"
        # depth=1


# class TenderClosedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TenderClosed
#         fields = "__all__"
#         # depth=1

class TenItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenItem
        fields = "__all__"
