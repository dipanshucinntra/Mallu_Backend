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

#Category Create API
@api_view(['POST'])
def create(request):
    try:
        GroupName = request.data['GroupName']
        model=Category(GroupName = GroupName)
        model.save()

        cat = Category.objects.latest('id')
        cat.Number = cat.id
        cat.save()

        return Response({"message": "Success","status": 200,"data":[{'id': cat.id}]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[{"Error": str(e)}]})

#Category Create API
@api_view(["POST"])
def update(request):
    try:
        id = request.data['id']
        GroupName = request.data['GroupName']
        if Category.objects.filter(pk = id).exists():
            if Category.objects.filter(GroupName = GroupName).exclude(pk = id):
                return Response({"message": "Category Name already exist","status": 201,"data":[]})
            else:
                Category.objects.filter(pk = id).update(GroupName = GroupName)
                return Response({"message": "Success","status": 200,"data":[]})
        else:
            return Response({"message": "Category id not exist","status": 201,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})



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
            cat_obj = Category.objects.all()
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
