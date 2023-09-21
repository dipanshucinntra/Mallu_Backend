import os
from django.conf import settings
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from Countries.models import States
from PaymentTermsTypes.models import PaymentTermsTypes
from Payment.models import Payment
from PaymentTermsTypes.serializers import PaymentTermsTypesSerializer
from Order.models import Order, AddressExtension as OrderAddr, DocumentLines as OrderDoc, CustomerOrder, CustomerAddressExtension, CustomerDocumentLines

from Branch.models import SettingBranch
from Attachment.models import Attachment
from Attachment.serializers import AttachmentSerializer
from Project.models import Project
from Branch.serializers import SettingGetBranchSerializer
from Project.serializers import ProjectSerializer
from Quotation.models import Quotation
from .models import *
from Employee.models import Employee
from BusinessPartner.models import *
from Opportunity.models import *
from Lead.models import Lead
import requests, json
from global_fun import *

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

from BusinessPartner.serializers import *
from Employee.serializers import *
from django.core.files.storage import FileSystemStorage

# Create your views here.

#create target visitor
@api_view(['POST'])
def create(request):
    try:
        monthly_target  =  int(request.data["monthly_target"])
        daily_visit = int(request.data["daily_visit"])
        assigned_to = int(request.data["assigned_to"])
        created_by =  int(request.data["created_by"])
        zone = request.data["zone"]
        target_obj = TargetVisitor(monthly_target=monthly_target, daily_visit=daily_visit, assigned_to=assigned_to, created_by=created_by, zone=zone)
        target_obj.save()
        return Response({"message":"Success","status":200, "data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":400, "data":[]})


# target visitor list
@api_view(['GET'])
def all(request):
    target_all = TargetVisitor.objects.all()
    data = target_detail(target_all)
    return Response({"message":"Success","status":200, "data":data})


# target visitor list
@api_view(['POST'])
def all_filter(request):
    MaxItem = request.data["MaxItem"]
    PageNo = request.data["PageNo"]
    if MaxItem!="All":
        endWith = (PageNo * int(MaxItem))
        startWith = (endWith - int(MaxItem))
    
    target_count = TargetVisitor.objects.all().count()
    if MaxItem!="All":
        target_all = TargetVisitor.objects.all()[startWith:endWith]
    else:
        target_all = TargetVisitor.objects.all()
    data = target_detail(target_all)
    return Response({"message":"Success","status":200, "data":data, "extra":{"total_count":target_count}})

def target_detail(data):
    list_data = []
    for obj in data:
        serializers = TargetVisitorSerializer(obj).data
        emp_obj = Employee.objects.filter(SalesEmployeeCode=obj.assigned_to)
        emp_ser = EmployeeSerializer(emp_obj, many=True).data
        serializers["assigned_to"] = emp_ser
        emp_created = Employee.objects.filter(SalesEmployeeCode=obj.created_by)
        emp_ser_created = EmployeeSerializer(emp_created, many=True).data
        serializers["created_by"] = emp_ser_created
        list_data.append(serializers)
    return list_data


# target visitor update
@api_view(['POST'])
def update(request):
    try:
        target_obj = TargetVisitor.objects.filter(id=request.data["id"]).first()
        target_obj.monthly_target = int(request.data["monthly_target"])
        target_obj.daily_visit = int(request.data["daily_visit"])
        target_obj.assigned_to = int(request.data["assigned_to"])
        target_obj.created_by = int(request.data["created_by"])
        target_obj.zone = request.data["zone"]
        target_obj.save()
        return Response({"message":"Success","status":200, "data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":400, "data":[]})


# target visitor detail
@api_view(['POST'])
def one(request):
    target_all = TargetVisitor.objects.filter(id=request.data["id"])
    data = target_detail(target_all)
    return Response({"message":"Success","status":200, "data":data})





