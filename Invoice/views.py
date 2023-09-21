from django.conf import settings
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse

from Order.models import Order


from .models import *
from Employee.models import Employee

import requests, json

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

from pytz import timezone
from datetime import datetime as dt

date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
yearmonth = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')


# Create your views here.  

#Invoice Create API
@api_view(['POST'])
def create(request):
    TaxDate = request.data['TaxDate']
    DocDueDate = request.data['DocDueDate']
    ContactPersonCode = request.data['ContactPersonCode']
    DiscountPercent = request.data['DiscountPercent']
    DocDate = request.data['DocDate']
    CardCode = request.data['CardCode']
    CardName = request.data['CardName']
    Comments = request.data['Comments']
    SalesPersonCode = request.data['SalesPersonCode']
    CreateDate = request.data['CreateDate']
    CreateTime = request.data['CreateTime']
    UpdateDate = request.data['UpdateDate']
    UpdateTime = request.data['UpdateTime']
    
    PaymentGroupCode = request.data['PaymentGroupCode']
    BPLID = request.data['BPLID']
    U_Term_Condition = request.data['U_Term_Condition']
    
    
    lines = request.data['DocumentLines']
    DocTotal=0
    for line in lines:
        DocTotal = float(DocTotal) + float(line['Quantity']) * float(line['UnitPrice'])
    print(DocTotal)

    model=Invoice(TaxDate = TaxDate, DocDueDate = DocDueDate, ContactPersonCode = ContactPersonCode, DiscountPercent = DiscountPercent, DocDate = DocDate, CardCode = CardCode, CardName = CardName, Comments = Comments, SalesPersonCode = SalesPersonCode, DocumentStatus="bost_Open", DocTotal = DocTotal, CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime, PaymentGroupCode=PaymentGroupCode, BPLID=BPLID,U_Term_Condition=U_Term_Condition)
    
    model.save()
    qt = Invoice.objects.latest('id')
    
    addr = request.data['AddressExtension']
    
    model_add = AddressExtension(InvoiceID = qt.id, BillToBuilding = addr['BillToBuilding'], ShipToState = addr['ShipToState'], BillToCity = addr['BillToCity'], ShipToCountry = addr['ShipToCountry'], BillToZipCode = addr['BillToZipCode'], ShipToStreet = addr['ShipToStreet'], BillToState = addr['BillToState'], ShipToZipCode = addr['ShipToZipCode'], BillToStreet = addr['BillToStreet'], ShipToBuilding = addr['ShipToBuilding'], ShipToCity = addr['ShipToCity'], BillToCountry = addr['BillToCountry'], U_SCOUNTRY = addr['U_SCOUNTRY'], U_SSTATE = addr['U_SSTATE'], U_SHPTYPB = addr['U_SHPTYPB'], U_BSTATE = addr['U_BSTATE'], U_BCOUNTRY = addr['U_BCOUNTRY'], U_SHPTYPS = addr['U_SHPTYPS'])
    
    model_add.save()

    LineNum = 0
    for line in lines:
        model_lines = DocumentLines(LineNum = LineNum, InvoiceID = qt.id, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'], U_FGITEM = line['U_FGITEM'], CostingCode2 = line['CostingCode2'], ProjectCode = line['ProjectCode'], FreeText = line['FreeText'])
        model_lines.save()
        LineNum=LineNum+1
    
    #return Response({"message":"successful","status":200,"data":[{"qt_Id":qt.id}]})
        
        

    
    r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
    token = json.loads(r.text)['SessionId']
    print(token)
    
    qt_data = {
		"TaxDate": request.data['TaxDate'],
		"DocDueDate": request.data['DocDueDate'],
		"ContactPersonCode": request.data['ContactPersonCode'],
		"DiscountPercent": request.data['DiscountPercent'],
		"DocDate": request.data['DocDate'],
		"CardCode": request.data['CardCode'],
		"CardName": request.data['CardName'],
		"Comments": request.data['Comments'],
		"SalesPersonCode": request.data['SalesPersonCode'],
		"BPL_IDAssignedToInvoice": request.data['BPLID'],
		"PaymentGroupCode":request.data['PaymentGroupCode'],
		"U_PORTAL_NO":qt.id,
		"AddressExtension": {
			"BillToBuilding": request.data['AddressExtension']['BillToBuilding'],
			"ShipToState": request.data['AddressExtension']['ShipToState'],
			"BillToCity": request.data['AddressExtension']['BillToCity'],
			"ShipToCountry": request.data['AddressExtension']['ShipToCountry'],
			"BillToZipCode": request.data['AddressExtension']['BillToZipCode'],
			"ShipToStreet": request.data['AddressExtension']['ShipToStreet'],
			"BillToState": request.data['AddressExtension']['BillToState'],
			"ShipToZipCode": request.data['AddressExtension']['ShipToZipCode'],
			"BillToStreet": request.data['AddressExtension']['BillToStreet'],
			"ShipToBuilding": request.data['AddressExtension']['ShipToBuilding'],
			"ShipToCity": request.data['AddressExtension']['ShipToCity'],
			"BillToCountry": request.data['AddressExtension']['BillToCountry']
		},
		"DocumentLines": lines
	}
    
    print(qt_data)
    print(json.dumps(qt_data))

    res = requests.post(settings.BASEURL+'/Invoices', data=json.dumps(qt_data), cookies=r.cookies, verify=False)
    live = json.loads(res.text)
    
    fetchid = qt.id
    
    if "DocEntry" in live:
        print(live['DocEntry'])
        
        model = Invoice.objects.get(pk = fetchid)
        model.DocEntry = live['DocEntry']
        model.save()
        
        return Response({"message":"successful","status":200,"data":[{"qt_Id":qt.id, "DocEntry":live['DocEntry']}]})
    else:
        SAP_MSG = live['error']['message']['value']
        print(SAP_MSG)
        #Invoice.objects.get(pk=qt.id).delete()
        allline = DocumentLines.objects.filter(InvoiceID=qt.id)
        for dcline in allline:
            dcline.delete()
            
        alladd = AddressExtension.objects.filter(InvoiceID=qt.id)
        for ad in alladd:
            ad.delete()
        return Response({"message":SAP_MSG,"SAP_error":SAP_MSG, "status":202,"data":[]})

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
        
        model.PaymentGroupCode = request.data['PaymentGroupCode']
        model.U_Term_Condition = request.data['U_Term_Condition']
        model.BPLID = request.data['BPLID']
        
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
                
                model_line.ProjectCode=line['ProjectCode']
                model_line.U_FGITEM=line['U_FGITEM']
                model_line.CostingCode2=line['CostingCode2']
                model_line.FreeText=line['FreeText']               
                model_line.save()
            else:
                lastline = DocumentLines.objects.filter(InvoiceID = fetchid).order_by('-LineNum')[:1]
                NewLine = int(lastline[0].LineNum) + 1
                model_lines = DocumentLines(InvoiceID = fetchid, LineNum=NewLine, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'], U_FGITEM = line['U_FGITEM'], CostingCode2 = line['CostingCode2'], ProjectCode = line['ProjectCode'], FreeText = line['FreeText'])
                model_lines.save()
            
            

        
        r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
        token = json.loads(r.text)['SessionId']
        print(token)
        
        qt_data = {
            "TaxDate": request.data['TaxDate'],
            "DocDueDate": request.data['DocDueDate'],
            "ContactPersonCode": request.data['ContactPersonCode'],
            "DiscountPercent": request.data['DiscountPercent'],
            "DocDate": request.data['DocDate'],
            "Comments": request.data['Comments'],
            "SalesPersonCode": request.data['SalesPersonCode'],
            "BPL_IDAssignedToInvoice": request.data['BPLID'],
            "PaymentGroupCode":request.data['PaymentGroupCode'],
            "U_Term_Condition":request.data['U_Term_Condition'],
            "AddressExtension": {
                "BillToBuilding": request.data['AddressExtension']['BillToBuilding'],
                "ShipToState": request.data['AddressExtension']['ShipToState'],
                "BillToCity": request.data['AddressExtension']['BillToCity'],
                "ShipToCountry": request.data['AddressExtension']['ShipToCountry'],
                "BillToZipCode": request.data['AddressExtension']['BillToZipCode'],
                "ShipToStreet": request.data['AddressExtension']['ShipToStreet'],
                "BillToState": request.data['AddressExtension']['BillToState'],
                "ShipToZipCode": request.data['AddressExtension']['ShipToZipCode'],
                "BillToStreet": request.data['AddressExtension']['BillToStreet'],
                "ShipToBuilding": request.data['AddressExtension']['ShipToBuilding'],
                "ShipToCity": request.data['AddressExtension']['ShipToCity'],
                "BillToCountry": request.data['AddressExtension']['BillToCountry']
            },
            "DocumentLines": lines
        }
        
        print(qt_data)
        print(json.dumps(qt_data))

    
        print("http://122.160.67.60:50001/b1s/v1/Invoices('"+model.DocEntry+"')");
        res = requests.patch("http://122.160.67.60:50001/b1s/v1/Invoices("+model.DocEntry+")", data=json.dumps(qt_data), cookies=r.cookies, verify=False)
        print(res.content)

        if len(res.content) !=0 :
            res1 = json.loads(res.content)
            SAP_MSG = res1['error']['message']['value']
            return Response({"message":"Partely successful","status":202,"SAP_error":SAP_MSG, "data":[request.data]})
        else:
            return Response({"message":"successful","status":200, "data":[json.loads(json.dumps(request.data))]})
    except Exception as e:
        return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})


def InvoiceShow(Invoices_obj):
    allqt = [];
    for qt in Invoices_obj:
        # invoice
        invoice_obj = InvoiceSerializer(qt, many=False)
        finalInvoice = json.loads(json.dumps(invoice_obj.data))

        # invoice order
        qtaddr = AddressExtension.objects.filter(InvoiceID=qt.id)
        qtaddr_json = AddressExtensionSerializer(qtaddr, many=True)
        jss_ = json.loads(json.dumps(qtaddr_json.data))

        for j in jss_:
            jss0=j
            finalInvoice['AddressExtension'] = ""
        
        # invoice document line
        lines = DocumentLines.objects.filter(InvoiceID=qt.id)
        lines_json = DocumentLinesSerializer(lines, many=True)
        finalInvoice['DocumentLines'] = json.loads(json.dumps(lines_json.data))
        order_obj = Order.objects.filter(id=qt.OrderID).first()
        if order_obj:
            companymobile_obj = BusinessPartner.objects.filter(CardCode = order_obj.CardCode).values('EmailAddress','Phone1')
            if companymobile_obj:
                finalInvoice['BPEmail'] = companymobile_obj[0]['EmailAddress']
                finalInvoice['BPMobile'] = companymobile_obj[0]['Phone1']
            else:
                finalInvoice['BPEmail'] = ""
                finalInvoice['BPMobile'] = ""
        else:
            finalInvoice['BPEmail'] = ""
            finalInvoice['BPMobile'] = ""

        # context = {
        #     'id':qt.id,
        #     'DocEntry':qt.DocEntry,
        #     'DocDueDate':qt.DocDueDate,
        #     'DocDate':qt.DocDate,
        #     'TaxDate':qt.TaxDate,
        #     'ContactPersonCode':qt.ContactPersonCode,
        #     'DiscountPercent':qt.DiscountPercent,
        #     'CardCode':qt.CardCode,
        #     'CardName':qt.CardName,
        #     'Comments':qt.Comments,
        #     'SalesPersonCode':qt.SalesPersonCode,
            
        #     'DocumentStatus':qt.DocumentStatus,
        #     'DocCurrency':qt.DocCurrency,
        #     'DocTotal':qt.DocTotal,
        #     'VatSum':qt.VatSum,
            
        #     'PaymentGroupCode':qt.PaymentGroupCode,
        #     'U_Term_Condition':qt.U_Term_Condition,
        #     'BPLID':qt.BPLID,
            
        #     'CreationDate':qt.CreationDate,
            
        #     'AddressExtension':jss0,
        #     'DocumentLines':jss1,
            
        #     "CreateDate":qt.CreateDate,
        #     "CreateTime":qt.CreateTime,
        #     "UpdateDate":qt.UpdateDate,
        #     "UpdateTime":qt.UpdateTime
        #     }
            
        allqt.append(finalInvoice)
        
    return allqt

@api_view(["POST"])
def delivery(request):

    json_data = request.data
    
    if "SalesEmployeeCode" in json_data:
        print("yes")
        
        if json_data['SalesEmployeeCode']!="":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin' or emp_obj.role == 'ceo':
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
	
	
#Quotation All API
@api_view(["POST"])
def all_filter(request):
    json_data = request.data
    
    # if "U_OPPID" in json_data:
        # if json_data['U_OPPID'] !='':
            
            # quot_obj = Quotation.objects.filter(U_OPPID=json_data['U_OPPID']).order_by("-id")
            # if len(quot_obj) ==0:
                # return Response({"message": "Not Available","status": 201,"data":[]})
            # else:
                
                # allqt = QuotationShow(quot_obj)
                        
            # return Response({"message": "Success","status": 200,"data":allqt})
                
    
    if "SalesPersonCode" in json_data:
        print("yes")
        
        if json_data['SalesPersonCode']!="":
            SalesPersonID = json_data['SalesPersonCode']
            
            emp_obj = Employee.objects.get(SalesEmployeeCode=SalesPersonID)
            
            if emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesPersonID)#.values('id', 'SalesEmployeeCode')
                SalesPersonID=[SalesPersonID]
                for emp in emps:
                    SalesPersonID.append(emp.SalesEmployeeCode)
                
            elif emp_obj.role == 'admin' or emp_obj.role == 'ceo':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesPersonID=[]
                for emp in emps:
                    SalesPersonID.append(emp.SalesEmployeeCode)
            else:
                SalesPersonID = json_data['SalesPersonCode']
            
            print(SalesPersonID)
            
            for ke in json_data.keys():
                if ke =='U_FAV' :
                    print("yes filter")
                    if json_data['U_FAV'] !='':
                        quot_obj = Quotation.objects.filter(SalesPersonCode__in=SalesPersonID, U_FAV=json_data['U_FAV']).order_by("-id")
                        if len(quot_obj) ==0:
                            return Response({"message": "Not Available","status": 201,"data":[]})
                        else:
                            allqt = QuotationShow(quot_obj)
                            return Response({"message": "Success","status": 200,"data":allqt})
                # elif ke =='U_TYPE' :
                    # if json_data['U_TYPE'] !='':
                        # quot_obj = Quotation.objects.filter(SalesPersonCode__in=SalesPersonID, U_TYPE=json_data['U_TYPE']).order_by("-id")
                        # if len(quot_obj) ==0:
                            # return Response({"message": "Not Available","status": 201,"data":[]})
                        # else:
                            # quot_json = QuotationSerializer(quot_obj, many=True)
                            # return Response({"message": "Success","status": 200,"data":quot_json.data})
                # elif ke =='Status' :
                    # if json_data['Status'] !='':
                        # quot_obj = Quotation.objects.filter(SalesPersonCode__in=SalesPersonID, Status=json_data['Status']).order_by("-id")
                        # if len(quot_obj) ==0:
                            # return Response({"message": "Not Available","status": 201,"data":[]})
                        # else:
                            # quot_json = QuotationSerializer(quot_obj, many=True)
                            # return Response({"message": "Success","status": 200,"data":quot_json.data})
                
                else:
                    print("no filter")
                    # qt = Quotation.objects.filter(SalesPersonCode__in=SalesPersonID).order_by("-id")
                    # quot_json = QuotationSerializer(quot_obj, many=True)
                    # return Response({"message": "Success","status": 200,"data":quot_json.data})
                    quot_obj = Invoice.objects.filter(SalesPersonCode__in=SalesPersonID).order_by("-id")
                    allqt = InvoiceShow(quot_obj)
                        
                    return Response({"message": "Success","status": 200,"data":allqt})
            
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})


#Invoice All API
@api_view(["GET"])
def all(request):
    Invoices_obj = Invoice.objects.all().order_by("-id")
    allqt = InvoiceShow(Invoices_obj)
    return Response({"message": "Success","status": 200,"data":allqt})

#Invoice One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    
    Invoices_obj = Invoice.objects.filter(id=id)
    
    allqt = InvoiceShow(Invoices_obj)
    return Response({"message": "Success","status": 200,"data":allqt})


#Invoice delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        emp=Invoice.objects.get(pk=fetchid)
        SalesInvoiceCode = emp.SalesInvoiceCode
        
        fetchdata=Invoice.objects.filter(pk=fetchid).delete()
                    
        

        

        # print(data)
    
        try:
            r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)
            res = requests.delete(settings.BASEURL+'/SalesPersons('+SalesInvoiceCode+')', cookies=r.cookies, verify=False)
            return Response({"message":"successful","status":"200","data":[]})
        except:
            return Response({"message":"successful","status":"200","data":[]})        
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

