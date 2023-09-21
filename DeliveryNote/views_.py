from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from BusinessPartner.models import BPEmployee
from BusinessPartner.serializers import BPEmployeeSerializer

from Employee.serializers import EmployeeSerializer
from PaymentTermsTypes.models import PaymentTermsTypes
from PaymentTermsTypes.serializers import PaymentTermsTypesSerializer
from BusinessPartner.models import BusinessPartner
from global_methods import employeeViewAccess, getAllReportingToIds
from .models import *
from Employee.models import Employee
from Order import views as OrderView
from Order.models import Order
from Order.models import DocumentLines as Order_DocumentLines
from Invoice.models import DocumentLines as Invoice_DocumentLines
from Order.models import AddressExtension as Order_AddressExtension

import requests, json

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

from pytz import timezone
from datetime import datetime as dt

import datetime

date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
yearmonth = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')


# Create your views here.  

#Invoice Create API
@api_view(['POST'])
def create(request):
    invoice_obj = Invoice.objects.filter(OrderID=request.data['oid'])
    if len(invoice_obj) != 0:
        for inv_obj in invoice_obj:
            print(inv_obj.id)
        return Response({"message":"success","status":200,"data":[{"id":inv_obj.id}]})
    else:
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
            SalesPersonCode = odr.SalesPersonCode
            CreateDate = odr.CreateDate
            CreateTime = odr.CreateTime
            UpdateDate = odr.UpdateDate
            UpdateTime = odr.UpdateTime
            OrderID = odr.id
            lines = Order_DocumentLines.objects.filter(OrderID=request.data['oid'])
            DocTotal=0
            for line in lines:
                DocTotal = float(DocTotal) + float(line.Quantity) * float(line.UnitPrice)
            print(DocTotal)

            model=Invoice(TaxDate = TaxDate, DocDueDate = DocDueDate, ContactPersonCode = ContactPersonCode, DiscountPercent = DiscountPercent, DocDate = DocDate, CardCode = CardCode, CardName = CardName, Comments = Comments, SalesPersonCode = SalesPersonCode, DocumentStatus="bost_Open", DocTotal = DocTotal, OrderID = OrderID, CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime)
            
            model.save()
            qt = Invoice.objects.latest('id')    
            #model = Invoice.objects.get(pk = fetchid)
            model.DocEntry = qt.id
            model.save()
            
            addrs = Order_AddressExtension.objects.filter(OrderID=request.data['oid'])
            for addr in addrs:
                model_add = AddressExtension(DeliveryNoteID = qt.id, BillToBuilding = addr.BillToBuilding, ShipToState = addr.ShipToState, BillToCity = addr.BillToCity, ShipToCountry = addr.ShipToCountry, BillToZipCode = addr.BillToZipCode, ShipToStreet = addr.ShipToStreet, BillToState = addr.BillToState, ShipToZipCode = addr.ShipToZipCode, BillToStreet = addr.BillToStreet, ShipToBuilding = addr.ShipToBuilding, ShipToCity = addr.ShipToCity, BillToCountry = addr.BillToCountry, U_SCOUNTRY = addr.U_SCOUNTRY, U_SSTATE = addr.U_SSTATE, U_SHPTYPB = addr.U_SHPTYPB, U_BSTATE = addr.U_BSTATE, U_BCOUNTRY = addr.U_BCOUNTRY, U_SHPTYPS = addr.U_SHPTYPS)
                
                model_add.save()

            LineNum = 0
            for line in lines:
                model_lines = DocumentLines(LineNum = LineNum, InvoiceID = qt.id, Quantity = line.Quantity, UnitPrice = line.UnitPrice, DiscountPercent = line.DiscountPercent, ItemCode = line.ItemCode, ItemDescription = line.ItemDescription, TaxCode = line.TaxCode)
                model_lines.save()
                LineNum=LineNum+1
            
            return Response({"message":"successful","status":200,"data":[{"id":qt.id, "DocEntry":qt.id}]})
        except Exception as e:
            return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})

#Invoice Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Invoice.objects.get(pk = fetchid)

        model.TaxDate = request.data['TaxDate']
        model.DocDate = request.data['DocDate']
        model.DocDueDate = request.data['DocDueDate']
        
        model.ContactPersonCode = request.data['ContactPersonCode']
        model.DiscountPercent = request.data['DiscountPercent']
        model.Comments = request.data['Comments']
        model.SalesPersonCode = request.data['SalesPersonCode']
        
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']

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
            
            'DocumentStatus':qt.DocumentStatus,
            'DocCurrency':qt.DocCurrency,
            'DocTotal':qt.DocTotal,
            'VatSum':qt.VatSum,
            'CreationDate':qt.CreationDate,
            
            'AddressExtension':jss0,
            'DocumentLines':jss1,
            
            "CreateDate":qt.CreateDate,
            "CreateTime":qt.CreateTime,
            "UpdateDate":qt.UpdateDate,
            "UpdateTime":qt.UpdateTime
            }
            
        allqt.append(context)
        
    return allqt

@api_view(["POST"])
def delivery(request):

    json_data = request.data
    
    if "SalesEmployeeCode" in json_data:
        print("yes")
        
        if json_data['SalesEmployeeCode']!="":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode=[]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)                    
            elif emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                SalesEmployeeCode=[SalesEmployeeCode]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode=[SalesEmployeeCode]
                # emps = Employee.objects.filter(reportingTo=emp_obj.reportingTo)#.values('id', 'SalesEmployeeCode')
                # SalesEmployeeCode=[]
                # for emp in emps:
                    # SalesEmployeeCode.append(emp.SalesEmployeeCode)
            
            print(SalesEmployeeCode)

            if json_data['Type'] =="over":
                ord = Invoice.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Open", DocDueDate__lt=date)
                allord = InvoiceShow(ord)
                #print(allord)
            elif json_data['Type'] =="open":
                ord = Invoice.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Open", DocDueDate__gte=date)
                allord = InvoiceShow(ord)
                #print(allord)
            else:
                ord = Invoice.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Close")
                allord = InvoiceShow(ord)
                #print(allord)
			
            #{"SalesEmployeeCode":"2"}
            return Response({"message": "Success","status": 200,"data":allord})
            
            #return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
	
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
            quot_obj = Invoice.objects.filter(SalesPersonCode__in=empList).order_by("-id")
            # allqt = InvoiceShow(quot_obj)
            allqt = showInvoice(quot_obj)
            return Response({"message": "Success","status": 200,"data":allqt})
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
        result = showDeliveryNote(del_obj)
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
    

#Invoice delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Invoice.objects.filter(pk=fetchid).delete()
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
        BaseEntry = 0
        paymentType = 0
        
        if BPEmployee.objects.filter(InternalCode = cpcType).exists():
            cpcTypeObj = BPEmployee.objects.filter(InternalCode = cpcType).values("id","FirstName","E_Mail", "MobilePhone")  #updated by millan on 15-09-2022
            cpcTypejson = BPEmployeeSerializer(cpcTypeObj, many = True)
            finalCPCData['ContactPersonCode']=json.loads(json.dumps(cpcTypejson.data))
        else:
            finalCPCData['ContactPersonCode'] = []
            
        if Employee.objects.filter(SalesEmployeeCode = salesType).exists():
            salesTypeObj = Employee.objects.filter(SalesEmployeeCode = salesType).values("id", "SalesEmployeeCode", "SalesEmployeeName", "Email", "Mobile")
            salesTypejson = EmployeeSerializer(salesTypeObj, many=True)
            finalCPCData['SalesPersonCode'] = json.loads(json.dumps(salesTypejson.data))
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
        
        if Order.objects.filter(DocEntry = BaseEntry).exists():
            ordObj = Order.objects.get(DocEntry = BaseEntry)
            finalCPCData['AdditionalCharges'] = ordObj.AdditionalCharges
            finalCPCData['DeliveryCharge'] = ordObj.DeliveryCharge
            finalCPCData['DeliveryTerm'] = ordObj.DeliveryTerm
            paymentType = ordObj.PayTermsGrpCode
        else:
            finalCPCData['AdditionalCharges'] = ""
            finalCPCData['DeliveryCharge'] = ""

        
        if PaymentTermsTypes.objects.filter(GroupNumber = paymentType).exists():
            paymentTypeObj = PaymentTermsTypes.objects.filter(GroupNumber = paymentType)
            paymentjson = PaymentTermsTypesSerializer(paymentTypeObj, many = True)
            finalCPCData['PayTermsGrpCode'] = json.loads(json.dumps(paymentjson.data))
        else:
            finalCPCData['PayTermsGrpCode'] = []

        allInvoice.append(finalCPCData)
    return allInvoice
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# update Category Invoice and Uom
@api_view(['GET'])
def syncInvoice(request):
    # try:
        # Import and sync Invoice
        invoiceFile ="Invoice/INV.py"
        exec(compile(open(invoiceFile, "rb").read(), invoiceFile, 'exec'), {})
        
        # Import and sync Invoice recive payment
        incomingPayments ="Invoice/inv_incoming_payments.py"
        exec(compile(open(incomingPayments, "rb").read(), incomingPayments, 'exec'), {})
       
        # Import and sync Invoice return items or credit note
        creditNotes ="Invoice/inv_credit_notes.py"
        exec(compile(open(creditNotes, "rb").read(), creditNotes, 'exec'), {})

        return Response({"message":"Successful","status":200, "data":[]})
    # except Exception as e:
    #     return Response({"message":str(e),"status":201,"Model": "Invoice" ,"data":[]})

import pandas as pd
import numpy as np

#Pendig Delivery
@api_view(["POST"])
def pending(request):
    try:
        PageNo = int(request.data['PageNo'])
        MaxSize = request.data['MaxSize']
        Ods = Order.objects.filter(DocumentStatus="bost_Open", CancelStatus="csNo")
        if MaxSize != "All":
            size = int(MaxSize)
            endWith = (PageNo * size)
            startWith = (endWith - size)
            Ods = Ods[startWith:endWith]
            
        allord = pending_order(Ods)        
        pd_ods = pd.DataFrame(allord, columns=['OrderID', 'OrderDocEntry', 'CardCode', 'CardName', 'PendingAmount', 'PendingQty'])
        df = pd_ods.groupby(['CardCode', 'CardName'], as_index=False)['PendingAmount'].sum()
        
        Total = pd_ods['PendingAmount'].sum()
        
        pd_dict = df.to_dict('records')
        json_obj = json.loads(json.dumps(pd_dict))
        allod=[]
        for obj in json_obj:            
            cc_ods = pd_ods.loc[pd_ods['CardCode']==obj['CardCode']]
            ods_dict = cc_ods.to_dict('records')
            obj['Orderwise']=ods_dict
            allod.append(obj)
        #return Response({"message": "Success","status": 200,"data":[{"Total":Total, "Partywise":pd_dict}]})
        return Response({"message": "Success","status": 200,"data":[{"Total":Total, "Partywise":allod}]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})


#Pendig Delivery
@api_view(["POST"])
def pending_orderwise(request):
    try:
        Ods = Order.objects.filter(CardCode=request.data["CardCode"],DocumentStatus = 'bost_Open', CancelStatus="csNo")
        allord = pending_order(Ods)        
        pd_ods = pd.DataFrame(allord, columns=['OrderID', 'OrderDocEntry', 'CardCode', 'CardName', 'PendingAmount', 'PendingQty'])
        df = pd_ods.groupby(['CardCode', 'CardName'], as_index=False)['PendingAmount'].sum()
        
        Total = pd_ods['PendingAmount'].sum()
        
        pd_dict = df.to_dict('records')
        json_obj = json.loads(json.dumps(pd_dict))
        allod=[]
        for obj in json_obj:            
            cc_ods = pd_ods.loc[pd_ods['CardCode']==obj['CardCode']]
            ods_dict = cc_ods.to_dict('records')
            obj['Orderwise']=ods_dict
            allod.append(obj)
        #return Response({"message": "Success","status": 200,"data":[{"Total":Total, "Partywise":pd_dict}]})
        return Response({"message": "Success","status": 200,"data":{"orderwise":ods_dict}})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":{"orderwise":[]}})



#Pendig Delivery
@api_view(["POST"])
def pending_bybp(request):
    try:
        Ods = Order.objects.filter(DocumentStatus="bost_Open", CancelStatus="csNo", CardCode=request.data['CardCode'])
        allord = pending_order(Ods)        
        print(allord)
        #allord = OrderView.OrderShow(Ods)
        #return Response({"message": "Success","status": 200,"data":allord})
        return Response({"message": "Success","status": 200,"data":allord})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})


#Pendig Delivery
@api_view(["POST"])
def pending_byorder(request):
    try:
        Od = Order.objects.get(pk=request.data['OrderID'])
        allitem = pending_item(Od)        
        print(allitem)
        #allord = OrderView.OrderShow(Ods)
        #return Response({"message": "Success","status": 200,"data":allord})
        return Response({"message": "Success","status": 200,"data":allitem})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})


def pending_order(Ods):
    allord = []
    i=0
    for od in Ods:
        # print(od)
        print(od.CardCode)
        pending_qty = 0
        pending_amount = 0
        # if DocumentLines.objects.filter(BaseEntry=od.DocEntry).exists():

        od_lines = Order_DocumentLines.objects.filter(OrderID=od.id)
        #check every order item
        for od_line in od_lines:
            od_qty = int(od_line.Quantity)
            # check delivery
            if DocumentLines.objects.filter(ItemCode=od_line.ItemCode, BaseEntry=od.DocEntry).exists():
                print("In Delivery")
                del_lines = DocumentLines.objects.filter(ItemCode=od_line.ItemCode, BaseEntry=od.DocEntry)
                
                del_qty = 0
                for del_line in del_lines:
                    del_qty = del_qty + int(del_line.Quantity)
                if od_qty != del_qty:
                    qty = od_qty - del_qty
                    amount = qty * od_line.UnitPrice                        
                    pending_amount = pending_amount + amount
                    pending_qty = pending_qty + qty
            # check invoice
            elif Invoice_DocumentLines.objects.filter(ItemCode=od_line.ItemCode, BaseEntry=od.DocEntry).exists():
                print("In Invoice")
                del_lines = Invoice_DocumentLines.objects.filter(ItemCode=od_line.ItemCode, BaseEntry=od.DocEntry)
                
                del_qty = 0
                for del_line in del_lines:
                    del_qty = del_qty + int(del_line.Quantity)
                if od_qty != del_qty:
                    qty = od_qty - del_qty
                    amount = qty * od_line.UnitPrice                        
                    pending_amount = pending_amount + amount
                    pending_qty = pending_qty + qty
            else:
                print("only order")
                qty = od_qty
                amount = qty * od_line.UnitPrice                        
                pending_amount = pending_amount + amount
                pending_qty = pending_qty + qty
        
        print("pending_qty:", pending_qty)
        allord.append({
            "OrderID":od.id, 
            "OrderDocEntry":od.DocEntry, 
            "CardCode":od.CardCode, 
            "CardName":od.CardName, 
            "PendingAmount":float(pending_amount), 
            "PendingQty": pending_qty
        })
        # else:
        #     allord.append({"OrderID":od.id, "OrderDocEntry":od.DocEntry, "CardCode":od.CardCode, "CardName":od.CardName, "PendingAmount":float(od.DocTotal)})    
    return allord

def pending_item(od):
    allitem = []
    DocDueDate = od.DocDueDate
    i=0
    pending_amount = 0
    od_lines = Order_DocumentLines.objects.filter(OrderID=od.id)
    for od_line in od_lines:
        od_qty = int(od_line.Quantity)
        if Invoice_DocumentLines.objects.filter(BaseEntry=od.DocEntry, ItemCode=od_line.ItemCode).exists():
            del_lines = Invoice_DocumentLines.objects.filter(ItemCode=od_line.ItemCode, BaseEntry=od.DocEntry)
            
            del_qty = 0
            for del_line in del_lines:
                del_qty = del_qty + int(del_line.Quantity)
                
                if od_qty != del_qty:
                    qty = od_qty - del_qty
                    amount = qty * od_line.UnitPrice                        
                    pending_amount = pending_amount + amount
                    allitem.append({"ItemCode":od_line.ItemCode, "ItemDescription":od_line.ItemDescription, "Quantity":qty, "UnitPrice":od_line.UnitPrice, "PendingAmount":float(pending_amount),"DocDueDate": DocDueDate})
        elif DocumentLines.objects.filter(BaseEntry=od.DocEntry, ItemCode=od_line.ItemCode).exists():
            del_lines = DocumentLines.objects.filter(ItemCode=od_line.ItemCode, BaseEntry=od.DocEntry)
            
            del_qty = 0
            for del_line in del_lines:
                del_qty = del_qty + int(del_line.Quantity)
                
                if od_qty != del_qty:
                    qty = od_qty - del_qty
                    amount = qty * od_line.UnitPrice                        
                    pending_amount = pending_amount + amount
                    allitem.append({"ItemCode":od_line.ItemCode, "ItemDescription":od_line.ItemDescription, "Quantity":qty, "UnitPrice":od_line.UnitPrice, "PendingAmount":float(pending_amount),"DocDueDate": DocDueDate})
        else:
            qty = od_qty
            pending_amount = qty * od_line.UnitPrice                        
            allitem.append({"ItemCode":od_line.ItemCode, "ItemDescription":od_line.ItemDescription, "Quantity":qty, "UnitPrice":od_line.UnitPrice, "PendingAmount":float(pending_amount),"DocDueDate": DocDueDate})
                    
    return allitem
    