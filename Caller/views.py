from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse

from Employee.models import Employee
from .models import Caller  
from Lead.models import Lead  

from django.contrib import messages

from rest_framework.decorators import api_view
from rest_framework import status    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import CallerSerializer, CallerGetSerializer
from rest_framework.parsers import JSONParser

import os
from django.core.files.storage import FileSystemStorage
import json

from global_methods import showEmployeeData

# Create your views here.  


@api_view(["GET"])
def all(request):
    objs = Caller.objects.all().order_by('-id')
    serializer = CallerGetSerializer(objs, many=True)
    return Response({'status':status.HTTP_200_OK,'message':'Success','data':serializer.data})

@api_view(["POST"])
def all_filter(request):
    LeadId= request.data['LeadId']
    lead_obj = Lead.objects.get(id=LeadId).contactPerson
    objs = Caller.objects.filter(LeadId=LeadId).order_by('-id')
    serializer = CallerGetSerializer(objs, many=True)
    return Response({'status':status.HTTP_200_OK,'message':'Success','data':serializer.data, 'extra_data':[{"ContactPerson":lead_obj}]})


# @api_view(["POST"])
# def all_filter_page(request):
#     LeadId= request.data['LeadId']
#     PageNo = request.data['PageNo']
#     search = request.data['SearchText']
#     Status = request.data['Status']
#     StatusType = request.data['StatusType']
#     CreateDate = request.data['CreateDate']
#     Brocher = request.data['Brocher']
#     Call_by = request.data['CalledBy']
#     try:
#         MaxItem = request.data['MaxItem']
#     except:
#         MaxItem = 10
#     endWith = (PageNo * MaxItem)
#     startWith = (endWith - MaxItem)
#     list_data = []
#     if LeadId == 0:
#         objs = Caller.objects.all()
#     if LeadId != 0:
#         objs = Caller.objects.filter(LeadId=LeadId)
#     if Status!="":
#         objs = objs.filter(Status=Status)
#     if StatusType!="":
#         objs = objs.filter(StatusType=StatusType)
#     if CreateDate !="":
#         objs = objs.filter(CreateDate=CreateDate)
#     if Brocher !="":
#         objs = objs.filter(Brocher=Brocher)
#     if Call_by !="":
#         objs = objs.filter(EmployeeId=Call_by)
#     objs = objs.order_by('-id')[startWith:endWith]
#     for obj in objs:
#         Caller_data = CallerGetSerializer(obj).data
#         Caller_data['ContactPerson'] = Lead.objects.get(id=obj.LeadId).contactPerson
#         list_data.append(Caller_data)
#     # lead_obj = Lead.objects.get(id=LeadId).contactPerson
#     # objs = Caller.objects.filter(LeadId=LeadId).order_by('-id')[startWith:endWith]
#     # serializer = CallerGetSerializer(objs, many=True)
#     return Response({'status':status.HTTP_200_OK,'message':'Success','data':list_data})


# @api_view(["POST"])
# def count_all(request):
#     LeadId= request.data['LeadId']
#     search = request.data['SearchText']
#     Status = request.data['Status']
#     StatusType = request.data['StatusType']
#     CreateDate = request.data['CreateDate']
#     Brocher = request.data['Brocher']
#     Call_by = request.data['CalledBy']
#     if LeadId == 0:
#         objs = Caller.objects.all()
#     if LeadId != 0:
#         objs = Caller.objects.filter(LeadId=LeadId)
#     if Status!="":
#         objs = objs.filter(Status=Status)
#     if StatusType!="":
#         objs = objs.filter(StatusType=StatusType)
#     if CreateDate !="":
#         objs = objs.filter(CreateDate=CreateDate)
#     if Brocher !="":
#         objs = objs.filter(Brocher=Brocher)
#     if Call_by !="":
#         objs = objs.filter(EmployeeId=Call_by)
#     objs = objs.count()
#     return Response({'status':status.HTTP_200_OK,'message':'Success','data':[{"total_count":objs}]})

@api_view(["POST"])
def all_filter_page(request):
    LeadId= request.data['LeadId']
    PageNo = request.data['PageNo']
    search = request.data['SearchText']
    Status = request.data['Status']
    StatusType = request.data['StatusType']
    CreateDate = request.data['CreateDate']
    Brocher = request.data['Brocher']
    Call_by = request.data['CalledBy']
    SalesPersonID = request.data['SalesPersonID']
    try:
        MaxItem = request.data['MaxItem']
    except:
        MaxItem = 10
    endWith = (PageNo * MaxItem)
    startWith = (endWith - MaxItem)
    list_data = []

    emps = showEmployeeData(SalesPersonID)
    ############################################################################
    # emp_obj = Employee.objects.get(pk=SalesPersonID)
    # if emp_obj.role == 'manager':
    #     emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
    #     SalesPersonID=[SalesPersonID]
    #     for emp in emps:
    #         SalesPersonID.append(emp.id)
    # elif emp_obj.role == 'admin' or emp_obj.role == 'ceo':
    #     emps = Employee.objects.filter(id__gt=0)
    #     SalesPersonID=[]
    #     for emp in emps:
    #         SalesPersonID.append(emp.id)
    # else:
    #     SalesPersonID = [SalesPersonID]
    ##########################################################################

    objs = Caller.objects.filter(EmployeeId__in=emps)
    if LeadId == 0:
        objs = objs
    if LeadId != 0:
        objs = objs.filter(LeadId=LeadId)
    if Status!="":
        objs = objs.filter(Status=Status)
    if StatusType!="":
        objs = objs.filter(StatusType=StatusType)
    if CreateDate !="":
        objs = objs.filter(CreateDate=CreateDate)
    if Brocher !="":
        objs = objs.filter(Brocher=Brocher)
    if Call_by !="":
        objs = objs.filter(EmployeeId=Call_by)
    objs = objs.order_by('-id')[startWith:endWith]
    for obj in objs:
        Caller_data = CallerGetSerializer(obj).data
        lead_data = Lead.objects.filter(id=obj.LeadId)
        if lead_data:
            lead_person = lead_data.first().contactPerson
            companyName = lead_data.first().companyName
        else:
            lead_data = ""
            companyName = ""
        Caller_data['ContactPerson'] = lead_person
        Caller_data['companyName'] = companyName
        list_data.append(Caller_data)
    # lead_obj = Lead.objects.get(id=LeadId).contactPerson
    # objs = Caller.objects.filter(LeadId=LeadId).order_by('-id')[startWith:endWith]
    # serializer = CallerGetSerializer(objs, many=True)
    return Response({'status':status.HTTP_200_OK,'message':'Success','data':list_data})


@api_view(["POST"])
def count_all(request):
    LeadId= request.data['LeadId']
    search = request.data['SearchText']
    Status = request.data['Status']
    StatusType = request.data['StatusType']
    CreateDate = request.data['CreateDate']
    Brocher = request.data['Brocher']
    Call_by = request.data['CalledBy']
    SalesPersonID = request.data['SalesPersonID']
    emps = showEmployeeData(SalesPersonID)
    ####################################################################
    # emp_obj = Employee.objects.get(pk=SalesPersonID)
    # if emp_obj.role == 'manager':
    #     emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
    #     SalesPersonID=[SalesPersonID]
    #     for emp in emps:
    #         SalesPersonID.append(emp.id)
    # elif emp_obj.role == 'admin' or emp_obj.role == 'ceo':
    #     emps = Employee.objects.filter(id__gt=0)
    #     SalesPersonID=[]
    #     for emp in emps:
    #         SalesPersonID.append(emp.id)
    # else:
    #     SalesPersonID = [SalesPersonID]
    #####################################################################


    objs = Caller.objects.filter(EmployeeId__in=emps)
    if LeadId == 0:
        objs = objs
    if LeadId != 0:
        objs = objs.filter(LeadId=LeadId)
    if Status!="":
        objs = objs.filter(Status=Status)
    if StatusType!="":
        objs = objs.filter(StatusType=StatusType)
    if CreateDate !="":
        objs = objs.filter(CreateDate=CreateDate)
    if Brocher !="":
        objs = objs.filter(Brocher=Brocher)
    if Call_by !="":
        objs = objs.filter(EmployeeId=Call_by)
    objs = objs.count()
    return Response({'status':status.HTTP_200_OK,'message':'Success','data':[{"total_count":objs}]})


@api_view(["POST"])
def one(request):
    try:
        objs = Caller.objects.get(id=request.data['id'])
        serializer = CallerGetSerializer(objs)
        return Response({'status':status.HTTP_200_OK,'message':'Success','data':[serializer.data]})
    except:
        return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Invalid_data', 'data':[]})

@api_view(["POST"])
def create(request):
    serializer = CallerSerializer(data=request.data)
    if serializer.is_valid(): 
        call_obj = Caller.objects.filter(LeadId=serializer.validated_data["LeadId"], CreateTime=serializer.validated_data["CreateTime"], CreateDate=serializer.validated_data["CreateDate"], CallDuration=serializer.validated_data["CallDuration"])
        if not call_obj:
            obj = serializer.save() 
            objj = serializer.data
            objj["id"] = obj.id
            return Response({'status':status.HTTP_200_OK,'message':'Success', 'data':[objj]})
        return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Invalid_data', 'data':[]})
    return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Invalid_data', 'data':[]})


@api_view(["PUT"])
def update(request):
    try:
        obj = Caller.objects.get(id=request.data['id'])
    except:
        obj = None
    if obj:
        serializer = CallerSerializer(obj, data=request.data)
        if serializer.is_valid(): 
            serializer.save() 
            return Response({'status':status.HTTP_200_OK,'message':'Success', 'data':[]})
    return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Invalid_data', 'data':[]})


@api_view(["POST"])
def delete(request):
    try:
        obj = Caller.objects.get(id=request.data['id'])
    except:
        obj = None
    if obj:
        obj.delete()
        return Response({'status':status.HTTP_200_OK,'message':'Success', 'data':[]})
    return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Invalid_data', 'data':[]})






