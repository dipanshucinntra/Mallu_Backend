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
from global_methods import getAllReportingToIds
from .models import *
from TargetVisitor.models import *
from Employee.models import Employee
from Expense.models import *
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

from datetime import datetime

####################################################################################################################


#Attendance API
@api_view(['POST'])
def punch_attendance(request):
    data = request.data
    if "punchin_latitude" in data:
        asp_id = data["asp_id"]
        asp_name = data["asp_name"]
        asp_code = data["asp_code"]
        transport_mode = data["transport_mode"]
        remark = data["punchin_remark"]
        punchin_latitude = data["punchin_latitude"]
        punchin_longitude = data["punchin_longitude"]
        created_by = data["created_by"]
        
        create_date = data["create_date"]
        create_time = data["create_time"]

        service_obj = DailyService(asp_id=asp_id, asp_name=asp_name, asp_code=asp_code, transport_mode=transport_mode, punchin_remark=remark, punchin_latitude=punchin_latitude, punchin_longitude=punchin_longitude, create_date=create_date, create_time=create_time, created_by=created_by)
        service_obj.save()
        
        File = request.data['File']
        attachmentsImage_url = ""
        if File !="" :
            target ='./bridge/static/image/Attachment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge/', '/')
            
            FileName = File.name 

        model=Attachment(File=attachmentsImage_url, LinkType="Service", Caption="PunchIn", LinkID=service_obj.id, CreateDate=create_date, CreateTime=create_time, UpdateDate=create_date, UpdateTime=create_time, FileName = FileName)
        model.save()
        
    if "punchout_latitude" in data:
        fetchid = data["id"]
        asp_id = data["asp_id"]
        asp_name = data["asp_name"]
        asp_code = data["asp_code"]
        total_distance = data["total_distance"]
        punchout_latitude = data["punchout_latitude"]
        punchout_longitude = data["punchout_longitude"]
        remark = data["punchout_remark"]
        created_by = data["created_by"]
        update_date = data["update_date"]
        update_time = data["update_time"]
        if DailyService.objects.filter(id=fetchid).exists():
            service_obj = DailyService.objects.filter(id=fetchid).update(punchout_latitude=punchout_latitude, punchout_longitude=punchout_longitude, punchout_remark=remark, update_date=update_date, update_time=update_time, total_distance=total_distance, created_by=created_by)
            
            File = request.data['File']
            attachmentsImage_url = ""
            if File !="" :
                target ='./bridge/static/image/Attachment'
                os.makedirs(target, exist_ok=True)
                fss = FileSystemStorage()
                file = fss.save(target+"/"+File.name, File)
                productImage_url = fss.url(file)
                attachmentsImage_url = productImage_url.replace('/bridge/', '/')
                
                FileName = File.name 

            model=Attachment(File=attachmentsImage_url, LinkType="Service", Caption="PunchOut", LinkID=fetchid, CreateDate=update_date, CreateTime=update_time, UpdateDate=update_date, UpdateTime=update_time, FileName = FileName)
            model.save()

            service_data = DailyService.objects.get(id=fetchid)
            print("testttttt", service_data)
            trip_name = ""
            type_of_expense = ""
            expense_from = data["update_date"]
            expense_to = service_data.create_date
            totalAmount = float(service_data.total_distance) * 3.0 
            createDate = data["update_date"]
            createTime = data["update_time"]
            createdBy = data["created_by"]
            employeeId = data["created_by"]
            total_distance = float(service_data.total_distance)
            DailyService_id = fetchid
            print("Values..........",expense_to, totalAmount, total_distance, DailyService_id)
            
            exp_model = Expense(DailyService_id=DailyService_id, total_distance=total_distance, trip_name=trip_name, type_of_expense=type_of_expense, expense_from=expense_from, expense_to=expense_to, totalAmount=totalAmount, createDate=createDate, createTime=createTime, createdBy=createdBy, employeeId = employeeId)
            exp_model.save()

    return Response({"message":"successful","status":200, "data":[]})



#Chaeck API
@api_view(['POST'])
def check_attendance(request):
    data = request.data
    DailyService_id = data["DailyService_id"]
    ase_id = data["ase_id"]
    latitude = data["latitude"]
    longitude = data["longitude"]
    created_by = data["created_by"]
    distance = data["distance"]
    type = data["type"]
    contact_person = data["contact_person"]
    source_type = data["source_type"]
    source_name = data["source_name"]
    source_id = data["source_id"]
    address = data["address"]
    remark = data["remark"]
    lunch_status = data["lunch_status"]
    create_date = data["create_date"]
    create_time = data["create_time"]
    
    service_obj = DailyCustomerService(DailyService_id=DailyService_id,distance=distance, ase_id=ase_id,source_type=source_type,address=address, contact_person=contact_person,latitude=latitude, longitude=longitude, create_date=create_date, create_time=create_time, created_by=created_by, type=type, source_id=source_id, source_name=source_name, remark=remark, lunch_status=lunch_status)
    service_obj.save()

    if type == "Stop":
        DailyService.objects.filter(id=DailyService_id).update(total_distance=distance)
    else:
        if TargetVisitor.objects.filter(assigned_to=int(ase_id)).exists():
            vst_val = TargetVisitor.objects.filter(assigned_to=int(ase_id)).first()
            val = int(vst_val.visited) + 1
            TargetVisitor.objects.filter(assigned_to=int(ase_id)).update(visited=val)
        
    return Response({"message":"successful","status":200, "data":[]})



#Detail Attendance API
@api_view(['POST'])
def one_attendance(request):
    emp_id = request.data["Emp_id"]
    list_data = []
    service_obj = DailyService.objects.filter(created_by=emp_id, create_date=datetime.now().date()).order_by("-id")
    for obj in service_obj:
        serializers = DailyServiceSerializer(obj).data
        check_status = DailyCustomerService.objects.filter(DailyService_id=obj.id).order_by("-id")
        last_lat = ""
        last_long = ""
        if check_status.count() >0:
            check_mark = check_status[0].type
            if check_mark == "Start":
                status = "Stop"
            else:
                status = "Start"
            if DailyCustomerService.objects.filter(DailyService_id=obj.id, type="Stop").count() > 0:
                data = DailyCustomerService.objects.filter(DailyService_id=obj.id, type="Stop", lunch_status="").order_by("-id")
                last_lat = data[0].latitude
                last_long = data[0].longitude
            else:
                last_lat = obj.punchin_latitude
                last_long = obj.punchin_longitude   
        else:
            status = "Start"
            last_lat = obj.punchin_latitude
            last_long = obj.punchin_longitude
        serializers["check_mark"] = status
        serializers["last_lat"] = last_lat
        serializers["last_long"] = last_long
        check_data = DailyCustomerService.objects.filter(DailyService_id=obj.id).order_by("-id")
        check_serializer = DailyCustomerServiceSerializer(check_data, many=True).data
        serializers["check_attendance"] = check_serializer
        list_data.append(serializers)
    return Response({"message":"successful","status":200, "data":list_data})


# #Detail Attendance API
# @api_view(['POST'])
# def list_attendance(request):
#     emp_id = request.data["Emp_id"]
#     service_obj = DailyCustomerService.objects.filter(ase_id=emp_id).order_by("-id")
#     serializers = DailyCustomerServiceSerializer(service_obj, many=True).data
#     return Response({"message":"successful","status":200, "data":serializers})


#list Attendance API
@api_view(['POST'])
def list_attendance(request):
    emp_id = request.data["Emp_id"]
    update_date = request.data["update_date"]
    # emp_list = getAllReportingToIds(emp_id)
    if update_date!="":
        # daily_obj = DailyService.objects.filter(created_by=emp_id, update_date=update_date).first()
        service_obj = DailyCustomerService.objects.filter(ase_id=emp_id, create_date=update_date).order_by("-id")
    else:
        service_obj = DailyCustomerService.objects.filter(ase_id=emp_id).order_by("-id")
    serializers = DailyCustomerServiceSerializer(service_obj, many=True).data
    return Response({"message":"successful","status":200, "data":serializers})


