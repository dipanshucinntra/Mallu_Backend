from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
import requests, json

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from Attachment.models import Attachment
from Attachment.serializers import AttachmentSerializer
import os
from django.core.files.storage import FileSystemStorage
from Payment.models import Payment
from Payment.serializers import PaymentSerializer
from BusinessPartner.models import BPEmployee, BusinessPartner
from BusinessPartner.serializers import BPEmployeeSerializer

from Quotation.models import Quotation
from Invoice.models import Invoice
from Invoice.serializers import InvoiceSerializer
from Employee.models import Employee

from global_methods import *

# Create your views here.  

#Payment Create API
@api_view(['POST'])
def create(request):
    try:
        InvoiceNo = request.data['InvoiceNo']
        TransactId = request.data['TransactId']
        TotalAmt = request.data['TotalAmt']
        TransactMod = request.data['TransactMod'] 
        DueAmount = request.data['DueAmount']
        PaymentDate = request.data['PaymentDate']
        ReceivedAmount = request.data['ReceivedAmount'] 
        Remarks = request.data['Remarks']
        createTime = request.data['createTime']
        createdBy = request.data['createdBy']
        createDate = request.data['createDate']
        
        CardCode = request.data['CardCode']
        
        Attach = request.data['Attach']  
        
        model = Payment(InvoiceNo=InvoiceNo, TransactId=TransactId, TotalAmt=TotalAmt, TransactMod=TransactMod, DueAmount=DueAmount, PaymentDate=PaymentDate, ReceivedAmount=ReceivedAmount, Remarks = Remarks, createTime=createTime, createdBy=createdBy, createDate=createDate, CardCode=CardCode)
        
        model.save()
        
        PaymentID = Payment.objects.latest('id')
        
        for File in request.FILES.getlist('Attach'):
            attachmentsImage_url = ""
            target ='./bridge/static/image/Payment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge', '')
            
            print(attachmentsImage_url)

            att=Attachment(File=attachmentsImage_url, LinkType="Payment", LinkID=PaymentID.id, CreateDate=model.updateDate, CreateTime=model.updateTime)
        
            att.save()
        return Response({"message":"successful","status":200,"data":[]})        

    except Exception as e:
        return Response({"message":"Error","status":201,"data":[{"Error":str(e)}]})


#Payment All API
@api_view(["GET"])
def all(request):
    try:
        payment_obj = Payment.objects.all().order_by("-id")
        result = showPayment(payment_obj)
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

#Payment All Filter API
@api_view(["POST"])
def all_filter_page(request):
    json_data = request.data
    try:
        SalesPersonID = json_data['SalesPersonCode']
        PageNo = json_data['PageNo']
        MaxItem = json_data['MaxItem']
        if MaxItem!="All":
            endWith = (PageNo * int(MaxItem))
            startWith = (endWith - int(MaxItem))
                
        # emp_obj = Employee.objects.get(SalesEmployeeCode=SalesPersonID)
        
        # if emp_obj.role == 'manager':
        #     emps = Employee.objects.filter(reportingTo=SalesPersonID)#.values('id', 'SalesEmployeeCode')
        #     SalesPersonID=[SalesPersonID]
        #     for emp in emps:
        #         SalesPersonID.append(emp.SalesEmployeeCode)
            
        # elif emp_obj.role == 'admin' or emp_obj.role == 'ceo' or emp_obj.role == 'logistic' or emp_obj.role == 'accountant':
        #     emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
        #     SalesPersonID=[]
        #     for emp in emps:
        #             SalesPersonID.append(emp.SalesEmployeeCode)
        # else:
        #     SalesPersonID = [json_data['SalesPersonCode']]

        SalesPersonID = showEmployeeData(SalesPersonID)
        print("emp",SalesPersonID)

        if MaxItem!="All":
            if json_data["CardCode"] != "":
                payment_count = Payment.objects.filter(CardCode=json_data["CardCode"]).count()
                payment_obj = Payment.objects.filter(CardCode=json_data["CardCode"]).order_by("-id")[startWith:endWith]
            else:
                quot_obj = Quotation.objects.filter(SalesPersonCode__in=SalesPersonID)
                quot_list = [str(quot.id) for quot in quot_obj]
                payment_count = Payment.objects.filter(InvoiceNo__in=quot_list).count()
                payment_obj = Payment.objects.filter(InvoiceNo__in=quot_list).order_by("-id")[startWith:endWith]
                print("list",quot_list)
        else:
            if json_data["CardCode"] != "":
                payment_count = Payment.objects.filter(CardCode=json_data["CardCode"]).count()
                payment_obj = Payment.objects.filter(CardCode=json_data["CardCode"]).order_by("-id")
            else:
                quot_obj = Quotation.objects.filter(SalesPersonCode__in=SalesPersonID)
                quot_list = [str(quot.id) for quot in quot_obj]
                print("list",quot_list)
                payment_count = Payment.objects.filter(InvoiceNo__in=quot_list).count()
                payment_obj = Payment.objects.filter(InvoiceNo__in=quot_list).order_by("-id")
        result = showPayment(payment_obj)
        return Response({"message": "Success","status": 200,"data":result, "extra":{"total_count":payment_count}})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

#Payment One API
@api_view(["POST"])
def one(request):
    try:
        id = request.data['id']
        if Payment.objects.filter(pk=id).exists():
            pay_obj = Payment.objects.filter(pk=id)
            result = showPayment(pay_obj)
            return Response({"message": "Success","status": 200,"data":result})
        else:
            return Response({"message": "Id Doesn't Exist", "status": 201, "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": 201, "data": []})

# #Payment Data for all payments and one payment
# def showPayment(objs):
#     allPayment = [];
#     for obj in objs:
#         createPerson = obj.createdBy  
#         updatePerson = obj.updatedBy  
#         cc = obj.CardCode
        
#         pay_json = PaymentSerializer(obj)
#         finalPayData = json.loads(json.dumps(pay_json.data))
        
#         if BusinessPartner.objects.filter(CardCode=obj.CardCode).exists():
#             bp_card = BusinessPartner.objects.filter(CardCode=obj.CardCode).first()
#             finalPayData['CardName'] = bp_card.CardName
#         else:
#             finalPayData['CardName'] = ""

#         if createPerson > 0:
#             createPersonObj = BPEmployee.objects.filter(pk = createPerson).values("FirstName", "MiddleName","LastName")
#             createPersonjson = BPEmployeeSerializer(createPersonObj, many=True)
#             if len(createPersonjson.data) > 0:
#                 finalPayData['createdBy'] = [json.loads(json.dumps(createPersonjson.data[0]))]   
#             else:
#                 finalPayData['createdBy'] = []
#         else:
#             finalPayData['createdBy'] = []
            
#         if updatePerson > 0:
#             updatePersonObj = BPEmployee.objects.filter(pk = updatePerson).values("FirstName", "MiddleName","LastName")
#             updatePersonjson = BPEmployeeSerializer(updatePersonObj, many=True)
#             if len(updatePersonjson.data) > 0:
#                 finalPayData['updatedBy'] = [json.loads(json.dumps(updatePersonjson.data[0]))]
#             else:
#                 finalPayData['updatedBy'] = []
#         else:
#             finalPayData['updatedBy'] = []
            
#         if Attachment.objects.filter(LinkID = obj.id, LinkType="Payment").exists():
#             Attach_dls = Attachment.objects.filter(LinkID = obj.id, LinkType="Payment")
#             Attach_json = AttachmentSerializer(Attach_dls, many=True)
#             finalPayData['Attach'] = Attach_json.data
#         else:
#             finalPayData['Attach'] = []
            
#         # if cc !="":
#             # ccObj = Invoice.objects.filter(CardCode = cc).values('CardCode')
#             # ccjson = InvoiceSerializer(ccObj, many=True)
#             # if len(ccjson.data) > 0:
#                 # finalPayData['CardCode'] = json.loads(json.dumps(ccjson.data[0]))
#             # else:
#                 # finalPayData['CardCode'] = []
#         # else:
#             # finalPayData['CardCode'] = []
        
#         allPayment.append(finalPayData)
#     return allPayment



#Payment Data for all payments and one payment
def showPayment(objs):
    allPayment = [];
    for obj in objs:
        createPerson = obj.createdBy  
        updatePerson = obj.updatedBy  
        cc = obj.CardCode
        
        pay_json = PaymentSerializer(obj)
        finalPayData = json.loads(json.dumps(pay_json.data))

        ##################### Added 05-07 #############################
        if BusinessPartner.objects.filter(CardCode=obj.CardCode).exists():
            bp_card = BusinessPartner.objects.filter(CardCode=obj.CardCode).first()
            finalPayData['CardName'] = bp_card.CardName
        else:
            finalPayData['CardName'] = ""
        ###############################################################
        
        if createPerson > 0:
            createPersonObj = BPEmployee.objects.filter(pk = createPerson).values("FirstName", "MiddleName","LastName")
            createPersonjson = BPEmployeeSerializer(createPersonObj, many=True)
            if len(createPersonjson.data) > 0:
                finalPayData['createdBy'] = [json.loads(json.dumps(createPersonjson.data[0]))]   
            else:
                finalPayData['createdBy'] = []
        else:
            finalPayData['createdBy'] = []
            
        if updatePerson > 0:
            updatePersonObj = BPEmployee.objects.filter(pk = updatePerson).values("FirstName", "MiddleName","LastName")
            updatePersonjson = BPEmployeeSerializer(updatePersonObj, many=True)
            if len(updatePersonjson.data) > 0:
                finalPayData['updatedBy'] = [json.loads(json.dumps(updatePersonjson.data[0]))]
            else:
                finalPayData['updatedBy'] = []
        else:
            finalPayData['updatedBy'] = []
            
        if Attachment.objects.filter(LinkID = obj.id, LinkType="Payment").exists():
            Attach_dls = Attachment.objects.filter(LinkID = obj.id, LinkType="Payment")
            Attach_json = AttachmentSerializer(Attach_dls, many=True)
            finalPayData['Attach'] = Attach_json.data
        else:
            finalPayData['Attach'] = []

        if Quotation.objects.filter(pk = obj.InvoiceNo).exists():
            qtno = Quotation.objects.get(pk = obj.InvoiceNo).QTNO
            finalPayData['QTNO'] = qtno
        else:
            finalPayData['QTNO'] = ""
            
        # if cc !="":
            # ccObj = Invoice.objects.filter(CardCode = cc).values('CardCode')
            # ccjson = InvoiceSerializer(ccObj, many=True)
            # if len(ccjson.data) > 0:
                # finalPayData['CardCode'] = json.loads(json.dumps(ccjson.data[0]))
            # else:
                # finalPayData['CardCode'] = []
        # else:
            # finalPayData['CardCode'] = []
        
        allPayment.append(finalPayData)
    return allPayment



#Payment Update API
@api_view(['POST'])
def update(request):
    try:
        fetchid = request.data['id']
        model = Payment.objects.get(pk = fetchid)
        model.InvoiceNo = request.data['InvoiceNo']
        model.TransactId = request.data['TransactId']
        model.TotalAmt = request.data['TotalAmt']
        model.TransactMod = request.data['TransactMod'] 
        model.DueAmount = request.data['DueAmount']
        model.PaymentDate = request.data['PaymentDate']
        model.ReceivedAmount = request.data['ReceivedAmount'] 
        model.Remarks = request.data['Remarks']
        model.updateDate = request.data['updateDate']
        model.updateTime = request.data['updateTime']
        model.updatedBy = request.data['updatedBy']
        model.CardCode = request.data['CardCode']
        
        Attach = request.data['Attach']  
        for File in request.FILES.getlist('Attach'):
            attachmentsImage_url = ""
            target ='./bridge/static/image/Payment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge', '')
            
            print(attachmentsImage_url)

            att=Attachment(File=attachmentsImage_url, LinkType="Payment", LinkID=fetchid, CreateDate=model.updateDate, CreateTime=model.updateTime)
        
            att.save()

        model.save()

        return Response({"message":"successful","status":200,"data":[]})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})
    
#Payment delete
@api_view(['POST'])
def delete(request):
    try:
        fetchids= request.data['id']
        for ids in fetchids:
            if Payment.objects.filter(pk=ids).exists():
                Payment.objects.filter(pk=ids).delete()
            else:
                return Response({"message":"Id Doesn't Exist","status":"405","data":[]}) 
        return Response({"message":"successful","status":"200","data":[]})   
    except:
        return Response({"message":"Id wrong","status":"201","data":[]})

#Payment Image Delete API
@api_view(['POST'])
def payment_img_delete(request):
    pay_id= request.data['id']
    
    image_id = request.data['image_id']
    
    try:
        if Attachment.objects.filter(pk=image_id , LinkID=pay_id).exists():
            Attachment.objects.filter(pk=image_id, LinkID=pay_id).delete()
            
            return Response({"message":"successful","status":"200","data":[]})        
        else:
            return Response({"message":"Id Not Found","status":"201","data":[]})        
    except:
        return Response({"message":"Id wrong","status":"201","data":[]})

