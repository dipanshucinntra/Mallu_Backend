from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .models import *
from Employee.models import Employee
import requests, json

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser
# Create your views here.  

#Category All API
@api_view(["GET"])
def all(request):
    cat_obj = Category.objects.all()
    cat_json = CategorySerializer(cat_obj, many=True)
    return Response({"message": "Success","status": 200,"data":cat_json.data})

#Category All API
@api_view(["POST"])
def all_filter(request):
    SalesEmployeeCode = request.data['SalesEmployeeCode']
    emp = Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
    if emp.role=='admin':
        cat_obj = Category.objects.all()
        cat_json = CategorySerializer(cat_obj, many=True)
        return Response({"message": "Success","status": 200,"data":cat_json.data})
    else:
        div = emp.div
        try:
            div = div.split(",")
            print(div)
            cat_obj = Category.objects.filter(Number__in=div)
            cat_json = CategorySerializer(cat_obj, many=True)
            return Response({"message": "Success","status": 200,"data":cat_json.data})
        except Exception as e:
            return Response({"message": str(e),"status": 201,"data":[]})


#Category One API
@api_view(["POST"])
def one(request):
    Number=request.data['Number']
    cat_obj = Category.objects.get(Number=Number)
    cat_json = CategorySerializer(cat_obj, many=False)
    return Response({"message": "Success","status": 200,"data":cat_json.data})
