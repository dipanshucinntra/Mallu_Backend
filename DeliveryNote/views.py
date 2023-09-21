from threading import activeCount
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from Attachment.serializers import AttachmentSerializer
from BusinessPartner.models import BPEmployee
from BusinessPartner.serializers import BPEmployeeSerializer

from Employee.serializers import EmployeeSerializer
from PaymentTermsTypes.models import PaymentTermsTypes
from PaymentTermsTypes.serializers import PaymentTermsTypesSerializer
from BusinessPartner.models import BusinessPartner
from Quotation.models import Quotation
from global_methods import employeeViewAccess, getAllReportingToIds, showEmployeeData
from .models import *
from Employee.models import Employee
from Order import views as OrderView
from Order.models import Order
from Order.models import DocumentLines as Order_DocumentLines
from DeliveryNote.models import DocumentLines as Invoice_DocumentLines
from Order.models import AddressExtension as Order_AddressExtension
from Attachment.models import *
import requests, json

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

from pytz import timezone
from datetime import datetime as dt

from django.db.models import Q
import os
from django.core.files.storage import FileSystemStorage
import json
import datetime

date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
yearmonth = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')


# Create your views here.  

#Invoice Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = DeliveryNote.objects.get(pk = fetchid)

        model.TaxDate = request.data['TaxDate']
        model.DocDate = request.data['DocDate']
        model.DocDueDate = request.data['DocDueDate']
        
        model.ContactPersonCode = request.data['ContactPersonCode']
        model.DiscountPercent = request.data['DiscountPercent']
        model.Comments = request.data['Comments']
        model.SalesPersonCode = request.data['SalesPersonCode']
        
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']
        model.DelPart = request.data['DelPart']
        model.AwbNo = request.data['AwbNo']

        model.save()
        
        model_add = AddressExtension.objects.get(id = request.data['AddressExtension']['id'])
        print(model_add)
        
        model_add.BillToBuilding = request.data['AddressExtension']['BillToBuilding']
        model_add.ShipToState = request.data['AddressExtension']['ShipToState']
        model_add.BillToCity = request.data['AddressExtension']['BillToCity']
        model_add.ShipToCountry = request.data['AddressExtension']['ShipToCountry']
        model_add.BillToZipCode = request.data['AddressExtension']['BillToZipCode']
        model_add.ShipToStreet = request.data['AddressExtension']['ShipToStreet']
        model_add.BillToState = request.data['AddressExtension']['BillToState']
        model_add.ShipToZipCode = request.data['AddressExtension']['ShipToZipCode']
        model_add.BillToStreet = request.data['AddressExtension']['BillToStreet']
        model_add.ShipToBuilding = request.data['AddressExtension']['ShipToBuilding']
        model_add.ShipToCity = request.data['AddressExtension']['ShipToCity']
        model_add.BillToCountry = request.data['AddressExtension']['BillToCountry']
        model_add.U_SCOUNTRY = request.data['AddressExtension']['U_SCOUNTRY']
        model_add.U_SSTATE = request.data['AddressExtension']['U_SSTATE']
        model_add.U_SHPTYPB = request.data['AddressExtension']['U_SHPTYPB']
        model_add.U_BSTATE = request.data['AddressExtension']['U_BSTATE']
        model_add.U_BCOUNTRY = request.data['AddressExtension']['U_BCOUNTRY']
        model_add.U_SHPTYPS = request.data['AddressExtension']['U_SHPTYPS']
   
        model_add.save()
        print("add save")
        
        lines = request.data['DocumentLines']
        for line in lines:
            if "id" in line:
                model_line = DocumentLines.objects.get(pk = line['id'])
                model_line.Quantity=line['Quantity']
                model_line.UnitPrice=line['UnitPrice']
                model_line.DiscountPercent=line['DiscountPercent']
                model_line.ItemCode=line['ItemCode']
                model_line.ItemDescription=line['ItemDescription']
                model_line.TaxCode=line['TaxCode']            
                model_line.save()
            else:
                lastline = DocumentLines.objects.filter(InvoiceID = fetchid).order_by('-LineNum')[:1]
                NewLine = int(lastline[0].LineNum) + 1
                model_lines = DocumentLines(InvoiceID = fetchid, LineNum=NewLine, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'])
                model_lines.save()
            
        return Response({"message":"successful","status":200, "data":[request.data]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})


@api_view(['POST'])
def change_address_ship_to(request):
    try:
        model_add = AddressExtension.objects.get(id = request.data['AddressExtension']['id'],DeliveryNoteID = request.data['id'])
                
        model_add.ShipToState = request.data['AddressExtension']['ShipToState']
        model_add.ShipToCountry = request.data['AddressExtension']['ShipToCountry']
        model_add.ShipToStreet = request.data['AddressExtension']['ShipToStreet']
        model_add.ShipToZipCode = request.data['AddressExtension']['ShipToZipCode']
        model_add.ShipToBuilding = request.data['AddressExtension']['ShipToBuilding']
        model_add.U_SCOUNTRY = request.data['AddressExtension']['U_SCOUNTRY']
        model_add.U_SSTATE = request.data['AddressExtension']['U_SSTATE']
        model_add.U_SHPTYPS = request.data['AddressExtension']['U_SHPTYPS']

        model_add.save()
            
        return Response({"message":"successful","status":200, "data":[request.data]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})


def InvoiceShow(Invoices_obj):
    allqt = [];
    for qt in Invoices_obj:
        qtaddr = AddressExtension.objects.filter(DeliveryNoteID=qt.id)
        
        qtaddr_json = AddressExtensionSerializer(qtaddr, many=True)
        jss0 = ''
        jss_ = json.loads(json.dumps(qtaddr_json.data))
        for j in jss_:
            jss0=j
        
        lines = DocumentLines.objects.filter(DeliveryNoteID=qt.id)
        
        lines_json = DocumentLinesSerializer(lines, many=True)
        
        jss1 = json.loads(json.dumps(lines_json.data))
        
        if Employee.objects.filter(SalesEmployeeCode=qt.SalesPersonCode).exists():
            SalesPersonName = Employee.objects.filter(SalesEmployeeCode=qt.SalesPersonCode).first()
            SalesPersonName = SalesPersonName.SalesEmployeeName
        else:
            SalesPersonName = ""

        order_obj = Order.objects.filter(id=qt.OrderID).first().U_QUOTID
        if Quotation.objects.filter(id=order_obj).exists():
            quo_obj = Quotation.objects.filter(id=order_obj).first().QTNO
        else:
            quo_obj = ""
        
        context = {
            'id':qt.id,
            'DocEntry':qt.DocEntry,
            'OrderID':qt.OrderID,
            'DocDueDate':qt.DocDueDate,
            'DocDate':qt.DocDate,
            'TaxDate':qt.TaxDate,
            'ContactPersonCode':qt.ContactPersonCode,
            'DiscountPercent':qt.DiscountPercent,
            'CardCode':qt.CardCode,
            'CardName':qt.CardName,
            'Comments':qt.Comments,
            'SalesPersonCode':qt.SalesPersonCode,
            "SalesPersonName":SalesPersonName,
            'DocumentStatus':qt.DocumentStatus,
            'DocCurrency':qt.DocCurrency,
            'DocTotal':qt.DocTotal,
            'NetTotal':qt.NetTotal,
            'VatSum':qt.VatSum,
            'CreationDate':qt.CreationDate,
            'QTNO':quo_obj,
            'AddressExtension':jss0,
            'DocumentLines':jss1,
            
            "CreateDate":qt.CreateDate,
            "CreateTime":qt.CreateTime,
            "UpdateDate":qt.UpdateDate,
            "UpdateTime":qt.UpdateTime,
            "Status":qt.Status,
            "AwbNo":qt.AwbNo,
            "DelPart":qt.DelPart,
            "TaxInvoiceNum":qt.TaxInvoiceNum,
            "TaxInvoiceDate":qt.TaxInvoiceDate
            }
            
        allqt.append(context)
        
    return allqt

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Invoice All API
@api_view(["POST"])
def all_filter(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']
        if Employee.objects.filter(SalesEmployeeCode = SalesPersonCode).exists():
            empList = getAllReportingToIds(SalesPersonCode)
            print("empList: ", empList)
            quot_obj = DeliveryNote.objects.filter(SalesPersonCode__in=empList).order_by("-id")
            # allqt = InvoiceShow(quot_obj)
            allqt = InvoiceShow(quot_obj)
            return Response({"message": "Success","status": 200,"data":allqt})
        else:
            return Response({"message": "Invalid SalesPersonCode","status": 201,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#live filter api
# @api_view(["POST"])
# def all_filter(request):
#     try:
#         SalesPersonCode = request.data['SalesPersonCode']
#         if Employee.objects.filter(SalesEmployeeCode = SalesPersonCode).exists():
#             SalesPersonID = SalesPersonCode
            
#             emp_obj = Employee.objects.get(SalesEmployeeCode=SalesPersonID)
            
#             if emp_obj.role == 'manager':
#                 emps = Employee.objects.filter(reportingTo=SalesPersonID)#.values('id', 'SalesEmployeeCode')
#                 SalesPersonID=[SalesPersonID]
#                 for emp in emps:
#                     SalesPersonID.append(emp.SalesEmployeeCode)
                
#             elif emp_obj.role == 'admin' or emp_obj.role == 'ceo' or emp_obj.role == 'logistic' or emp_obj.role == 'accountant':
#                 emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
#                 SalesPersonID=[]
#                 for emp in emps:
#                     SalesPersonID.append(emp.SalesEmployeeCode)
#             else:
#                 SalesPersonID = [SalesPersonCode]
#             # empList = getAllReportingToIds(SalesPersonCode)
#             # print("empList: ", empList)
#             quot_obj = DeliveryNote.objects.filter(SalesPersonCode__in=SalesPersonID).order_by("-id")
#             # allqt = InvoiceShow(quot_obj)
#             allqt = InvoiceShow(quot_obj)
#             return Response({"message": "Success","status": 200,"data":allqt})
#         else:
#             return Response({"message": "Invalid SalesPersonCode","status": 201,"data":[]})
#     except Exception as e:
#         return Response({"message": str(e),"status": 201,"data":[]})



#Invoice All API
@api_view(["POST"])
def all_filter_page(request):
    print("testeeeeee")
    try:
        SalesPersonCode = request.data['SalesPersonCode']
        PageNo          = request.data['PageNo']
        MaxItem         = request.data['MaxItem']
        card_code         = request.data['CardCode']
        if MaxItem!="All":
            MaxItem = int(MaxItem)
            endWith = (PageNo * MaxItem)
            startWith = (endWith - MaxItem)
        if Employee.objects.filter(SalesEmployeeCode = SalesPersonCode).exists():
            # current_emp = Employee.objects.filter(SalesEmployeeCode = SalesPersonCode).first()
            # role_specific = ["admin","manager","accountant","logistic","Service Head","marketing","HO"]
            # if current_emp.role in role_specific:
            #     emp_all_data = Employee.objects.all()
            #     empList = [emp.SalesEmployeeCode for emp in emp_all_data] 
            #     order_data =  Order.objects.filter(SalesPersonCode__in=empList) 
            #     order_ids = [odr.id for odr in order_data]
            # else:
            #     # empList = getAllReportingToIds(SalesPersonCode)
            #     empList = [SalesPersonCode] 
            #     order_data =  Order.objects.filter(SalesPersonCode__in=empList) 
            #     order_ids = [odr.id for odr in order_data]
            
            empList = showEmployeeData(SalesPersonCode)
            order_data =  Order.objects.filter(SalesPersonCode__in=empList) 
            order_ids = [odr.id for odr in order_data]

            print("empList: ", empList)
            if card_code!="":
                # quot_count = DeliveryNote.objects.filter(SalesPersonCode__in=empList, CardCode=card_code).count()
                quot_count = DeliveryNote.objects.filter(OrderID__in=order_ids, CardCode=card_code).count()
                if MaxItem!="All":
                    quot_obj = DeliveryNote.objects.filter(OrderID__in=order_ids, CardCode=card_code).order_by("-id")[startWith:endWith]
                else:
                    quot_obj = DeliveryNote.objects.filter(OrderID__in=order_ids, CardCode=card_code).order_by("-id")
            else:
                quot_count = DeliveryNote.objects.filter(OrderID__in=order_ids).count()
                if MaxItem!="All":
                    quot_obj = DeliveryNote.objects.filter(OrderID__in=order_ids).order_by("-id")[startWith:endWith]
                else:
                    quot_obj = DeliveryNote.objects.filter(OrderID__in=order_ids).order_by("-id")

            # if card_code!="":
            #     # quot_count = DeliveryNote.objects.filter(SalesPersonCode__in=empList, CardCode=card_code).count()
            #     quot_count = DeliveryNote.objects.filter(SalesPersonCode__in=empList, CardCode=card_code).count()
            #     if MaxItem!="All":
            #         quot_obj = DeliveryNote.objects.filter(SalesPersonCode__in=empList, CardCode=card_code).order_by("-id")[startWith:endWith]
            #     else:
            #         quot_obj = DeliveryNote.objects.filter(SalesPersonCode__in=empList, CardCode=card_code).order_by("-id")
            # else:
            #     quot_count = DeliveryNote.objects.filter(SalesPersonCode__in=empList).count()
            #     if MaxItem!="All":
            #         quot_obj = DeliveryNote.objects.filter(SalesPersonCode__in=empList).order_by("-id")[startWith:endWith]
            #     else:
            #         quot_obj = DeliveryNote.objects.filter(SalesPersonCode__in=empList).order_by("-id")




            # allqt = InvoiceShow(quot_obj)
            print("quotations....",quot_obj)
            allqt = InvoiceShow(quot_obj)
            return Response({"message": "Success","status": 200,"data":allqt, "extra":{"total_count":quot_count}})
        else:
            return Response({"message": "Invalid SalesPersonCode","status": 201,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



#DeliveryNote All API
@api_view(["GET"])
def all(request):
    try:
        del_obj = DeliveryNote.objects.all().order_by("-id")
        result = showDeliveryNote(del_obj)
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
    
#DeliveryNote One API
@api_view(["POST"])
def one(request):
    try:
        id=request.data['id'] 
        del_obj = DeliveryNote.objects.filter(pk=id)
        print("333333id", type(del_obj))
        result = showDeliveryNote(del_obj)
        print("dats",result)
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
    

#Invoice delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=DeliveryNote.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
    
    
# to get invoice contact person details and salesEmployeeDetails
def showDeliveryNote(objs):
    allInvoice = [];
    for obj in objs:
        cpcType = obj.ContactPersonCode
        salesType = obj.SalesPersonCode
        invId = obj.id
        cpcjson = DeliveryNoteSerializer(obj)
        finalCPCData = json.loads(json.dumps(cpcjson.data))
        print(finalCPCData)
        BaseEntry = 0
        paymentType = 0

        if BPEmployee.objects.filter(InternalCode = cpcType).exists():
            cpcTypeObj = BPEmployee.objects.filter(InternalCode = cpcType).values("id","FirstName","E_Mail", "MobilePhone")  #updated by millan on 15-09-2022
            cpcTypejson = BPEmployeeSerializer(cpcTypeObj, many = True)
            finalCPCData['ContactPersonCode']=json.loads(json.dumps(cpcTypejson.data))
        else:
            finalCPCData['ContactPersonCode'] = []
        print("errorr", Employee.objects.filter(SalesEmployeeCode = salesType))
        if Employee.objects.filter(SalesEmployeeCode = salesType).exists():
            salesTypeObj = Employee.objects.filter(SalesEmployeeCode = salesType).values("id", "SalesEmployeeCode", "SalesEmployeeName", "Email", "Mobile")
            salesTypejson = EmployeeSerializer(salesTypeObj, many=True)
            print("fafafa", salesTypejson.data)
            finalCPCData['SalesPersonCode'] = json.loads(json.dumps(salesTypejson.data))
            print("cgcg",json.loads(json.dumps(salesTypejson.data)))
        else:
            finalCPCData['SalesPersonCode'] = []
            
        if AddressExtension.objects.filter(DeliveryNoteID = invId).exists():
            addrObj = AddressExtension.objects.filter(DeliveryNoteID = invId)
            addrjson = AddressExtensionSerializer(addrObj, many=True)
            finalCPCData['AddressExtension'] = json.loads(json.dumps(addrjson.data))
        else:
            finalCPCData['AddressExtension'] = []
            
        if DocumentLines.objects.filter(DeliveryNoteID=invId).exists():
            linesobj = DocumentLines.objects.filter(DeliveryNoteID=invId)
            lines_json = DocumentLinesSerializer(linesobj, many=True)
            BaseEntry = linesobj[0].BaseEntry
            finalCPCData['DocumentLines'] = json.loads(json.dumps(lines_json.data))
        else:
            finalCPCData['DocumentLines'] = []
        print("ffgfgf",BaseEntry, Order.objects.filter(DocEntry = BaseEntry))
        if Order.objects.filter(DocEntry = BaseEntry).exists():
            ordObj = Order.objects.filter(DocEntry = BaseEntry).first()
            # finalCPCData['AdditionalCharges'] = ordObj.AdditionalCharges
            # finalCPCData['DeliveryCharge'] = ordObj.DeliveryCharge
            # finalCPCData['DeliveryTerm'] = ordObj.DeliveryTerm
            finalCPCData['AdditionalCharges'] = ""
            finalCPCData['DeliveryCharge'] = ""
            finalCPCData['DeliveryTerm'] = ""
            # paymentType = ordObj.PayTermsGrpCode
        else:
            finalCPCData['AdditionalCharges'] = ""
            finalCPCData['DeliveryCharge'] = ""
            finalCPCData['DeliveryTerm'] = ""

        
        print("ssss",objs)
        # if PaymentTermsTypes.objects.filter(GroupNumber = paymentType).exists():
            # paymentTypeObj = PaymentTermsTypes.objects.filter(GroupNumber = paymentType)
            # paymentjson = PaymentTermsTypesSerializer(paymentTypeObj, many = True)
            # finalCPCData['PayTermsGrpCode'] = json.loads(json.dumps(paymentjson.data))
        #     finalCPCData['PayTermsGrpCode'] = []
        # else:
        #     finalCPCData['PayTermsGrpCode'] = []

        finalCPCData['PayTermsGrpCode'] = []
        
        if Attachment.objects.filter(LinkType="DeliveryNote", LinkID=obj.id).exists():
            attach_data = Attachment.objects.filter(LinkType="DeliveryNote", LinkID=obj.id)
            attach_ser = AttachmentSerializer(attach_data, many=True)
            finalCPCData['Attach'] = attach_ser.data
        else:
            finalCPCData['Attach'] = []
        allInvoice.append(finalCPCData)
    return allInvoice

# # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # 
# # 
# # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # update Category Invoice and Uom
# @api_view(['GET'])
# def syncInvoice(request):
#     # try:
#         # Import and sync Invoice
#         invoiceFile ="Invoice/INV.py"
#         exec(compile(open(invoiceFile, "rb").read(), invoiceFile, 'exec'), {})
        
#         # Import and sync Invoice recive payment
#         incomingPayments ="Invoice/inv_incoming_payments.py"
#         exec(compile(open(incomingPayments, "rb").read(), incomingPayments, 'exec'), {})
       
#         # Import and sync Invoice return items or credit note
#         creditNotes ="Invoice/inv_credit_notes.py"
#         exec(compile(open(creditNotes, "rb").read(), creditNotes, 'exec'), {})

#         return Response({"message":"Successful","status":200, "data":[]})
#     # except Exception as e:
#     #     return Response({"message":str(e),"status":201,"Model": "Invoice" ,"data":[]})

@api_view(['POST'])
def create_delivery_note(request):
    DelPart = request.data['DelPart']
    AwbNo = request.data['AwbNo']
    TaxInvoiceNum = request.data['TaxInvoiceNum']
    TaxInvoiceDate = request.data['TaxInvoiceDate']
    SalesPersonCode = request.data['SalesPersonCode']
    if AwbNo != "" and DelPart != "":
        Status = "2"
    else:
        Status= "1"
    odr = Order.objects.get(pk=request.data['oid'])
    try:
        TaxDate = odr.TaxDate
        DocDueDate = odr.DocDueDate
        ContactPersonCode = odr.ContactPersonCode
        DiscountPercent = odr.DiscountPercent
        DocDate = odr.DocDate
        CardCode = odr.CardCode
        CardName = odr.CardName
        Comments = odr.Comments
        SalesPersonCode = SalesPersonCode
        DocumentStatus = odr.DocumentStatus
        DocCurrency = odr.DocCurrency
        DocTotal = odr.DocTotal
        NetTotal = odr.NetTotal
        CardName = odr.CardName
        VatSum = odr.VatSum
        CreationDate = odr.CreationDate
        DocEntry = odr.DocEntry
        CreateDate = odr.CreateDate
        CreateTime = odr.CreateTime
        UpdateDate = odr.UpdateDate
        UpdateTime = odr.UpdateTime
        OrderID = odr.id

        model=DeliveryNote(TaxDate = TaxDate, DocDueDate = DocDueDate, ContactPersonCode = ContactPersonCode, DiscountPercent = DiscountPercent, DocDate = DocDate, CardCode = CardCode, CardName = CardName, Comments = Comments, SalesPersonCode = SalesPersonCode, DocumentStatus=DocumentStatus, DocCurrency=DocCurrency, DocTotal = DocTotal, NetTotal=NetTotal, VatSum=VatSum, OrderID = OrderID, Status=Status, CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime, CreationDate=CreationDate, DocEntry=DocEntry, DelPart=DelPart, AwbNo=AwbNo, TaxInvoiceNum=TaxInvoiceNum, TaxInvoiceDate=TaxInvoiceDate)
        
        model.save()
        qt = DeliveryNote.objects.latest('id')

        addrs = Order_AddressExtension.objects.filter(OrderID=request.data['oid'])
        for addr in addrs:
            model_add = AddressExtension(DeliveryNoteID = qt.id, BillToBuilding = addr.BillToBuilding, ShipToState = addr.ShipToState, BillToCity = addr.BillToCity, ShipToCountry = addr.ShipToCountry, BillToZipCode = addr.BillToZipCode, ShipToStreet = addr.ShipToStreet, BillToState = addr.BillToState, ShipToZipCode = addr.ShipToZipCode, BillToStreet = addr.BillToStreet, ShipToBuilding = addr.ShipToBuilding, ShipToCity = addr.ShipToCity, BillToCountry = addr.BillToCountry, U_SCOUNTRY = addr.U_SCOUNTRY, U_SSTATE = addr.U_SSTATE, U_SHPTYPB = addr.U_SHPTYPB, U_BSTATE = addr.U_BSTATE, U_BCOUNTRY = addr.U_BCOUNTRY, U_SHPTYPS = addr.U_SHPTYPS)
            
            model_add.save()

        lines = Order_DocumentLines.objects.filter(OrderID=request.data['oid'])
        LineNum = 0
        for line in lines:
            model_lines = DocumentLines(LineNum = LineNum, DeliveryNoteID = qt.id, Quantity = line.Quantity, UnitPrice = line.UnitPrice, DiscountPercent = line.DiscountPercent, ItemCode = line.ItemCode, ItemDescription = line.ItemDescription, TaxCode = line.TaxCode)
            model_lines.save()
            LineNum=LineNum+1
        LinkType = "DeliveryNote"
        LinkID = qt.id
        Caption = ""
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        UpdateDate = CreateDate
        UpdateTime = CreateTime
        for File in request.FILES.getlist('File'):
            attachmentsImage_url = ""
            if File !="" :
                target ='./bridge/static/image/Attachment'
                os.makedirs(target, exist_ok=True)
                fss = FileSystemStorage()
                file = fss.save(target+"/"+File.name, File)
                productImage_url = fss.url(file)
                attachmentsImage_url = productImage_url.replace('/bridge/', '/')
                print(attachmentsImage_url)
              
            FileName = File.name   

            model=Attachment(File=attachmentsImage_url, LinkType=LinkType, Caption=Caption, LinkID=LinkID, CreateDate=CreateDate, CreateTime=CreateTime, UpdateDate=UpdateDate, UpdateTime=UpdateTime, FileName=FileName)
            
            model.save()
        return Response({"message":"successful","status":200,"data":[{"id":qt.id}]})
    except Exception as e:
        return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})


@api_view(['POST'])
def update_delivery_note(request):
    id = request.data['id']
    DelPart = request.data['DelPart']
    AwbNo = request.data['AwbNo']
    if AwbNo != "" and DelPart != "":
        Status = "2"
    else:
        Status= "1"
    TaxInvoiceNum = request.data['TaxInvoiceNum']
    TaxInvoiceDate = request.data['TaxInvoiceDate']
    CreateDate = request.data['CreateDate']
    CreateTime = request.data['CreateTime']
    DeliveryNote.objects.filter(id=id).update(DelPart=DelPart, AwbNo=AwbNo,Status=Status,TaxInvoiceNum=TaxInvoiceNum, TaxInvoiceDate=TaxInvoiceDate, UpdateDate=CreateDate, UpdateTime=CreateTime)
    return Response({"message":"successful","status":200,"data":[]})


#Change Status API
@api_view(['POST'])
def change_status_delivery(request):
    fetchid = request.data['delivery_id']
    try:
        model = DeliveryNote.objects.get(pk = fetchid)

        model.Status = request.data['Status']

        model.save()
        od = Order.objects.get(pk = model.OrderID)
        od.DocumentStatus = "bost_Close"
        od.save()
            
        return Response({"message":"successful","status":200, "data":[request.data]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

#Change Shipped With API
@api_view(['POST'])
def change_shipped_with(request):
    fetchid = request.data['id']
    try:
        model = DeliveryNote.objects.get(pk = fetchid)

        ShippedWith = request.data['ShippedWith']
        ShippedType = request.data['ShippedType']

        if not ShippedWith:
            ShippedWith = None

        if not ShippedType:
            ShippedType = None

        if ShippedWith is not None:
            model.ShippedWith = ShippedWith

        if ShippedType is not None:
            model.ShippedType = ShippedType

        model.save()
            
        return Response({"message":"successful","status":200, "data":[request.data]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})




    