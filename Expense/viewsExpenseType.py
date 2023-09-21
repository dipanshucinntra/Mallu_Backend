import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Expense.models import *
from Expense.serializers import *


from Employee.models import Employee
from Employee.serializers import EmployeeSerializer

#Expense Create API
@api_view(['POST'])
def create(request):
    try:
        allobjs = request.data
        for obj in allobjs:
            Name = obj['Name']
            CreatedDate = obj['CreatedDate']
            CreatedTime = obj['CreatedTime']
            
            if ExpenseType.objects.filter(Name = Name).exists():
                print("already exist name")
                # return Response({"message": "ExpenseType already exist", "status": "201", "data": []})
            else:
                ExpenseType(Name = Name,CreatedDate = CreatedDate,CreatedTime = CreatedTime).save()
                print("created")
        return Response({"message": "successful", "status": "200", "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": []})

#Expense All API
@api_view(["GET"])
def all(request):
    expn_obj = ExpenseType.objects.all().order_by("-id")
    expn_json = ExpenseTypeSerializer(expn_obj, many=True)
    return Response({"message": "Success","status": 200,"data":expn_json.data})

#Expense One API
@api_view(["POST"])
def one(request):
    try:
        id = request.data['id']
        if Expense.objects.filter(pk = id).exists():
            expn_obj = ExpenseType.objects.filter(pk = id)
            expn_json = ExpenseTypeSerializer(expn_obj, many=True)
            return Response({"message": "Success","status": 200,"data":expn_json.data})
        else:
            return Response({"message": "Id Doesn't Exist", "status": 201, "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": 201, "data": []})

#Expense Update API
@api_view(['POST'])
def update(request):
    try:
        fetchid = request.data['id']
        model = ExpenseType.objects.get(pk = fetchid)
        model.Name = request.data['Name']
        model.CreatedDate = request.data['CreatedDate']
        model.CreatedTime = request.data['CreatedTime']
        model.save()

        return Response({"message":"successful","status":200,"data":[]})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})
    
#Expense Delete API
@api_view(['POST'])
def delete(request):
    fetchids= request.data['id']
    try:
        for ids in fetchids:
            ExpenseType.objects.filter(pk=ids).delete()
            
        return Response({"message":"successful","status":"200","data":[]})   
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
