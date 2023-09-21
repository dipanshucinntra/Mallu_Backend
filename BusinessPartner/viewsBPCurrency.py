from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .models import BPCurrency
import requests, json

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import BPCurrencySerializer
from rest_framework.parsers import JSONParser
# Create your views here.  

#BPCurrency All API
@api_view(["GET"])
def all(request):
    bpcurrency_obj = BPCurrency.objects.all() 
    bpcurrency_json = BPCurrencySerializer(bpcurrency_obj, many=True)
    return Response({"message": "Success","status": 200,"data":bpcurrency_json.data})

