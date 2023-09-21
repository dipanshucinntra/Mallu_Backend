from django.conf import settings
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from PaymentTermsTypes.models import PaymentTermsTypes
from PaymentTermsTypes.serializers import PaymentTermsTypesSerializer

from Project.models import Project
from Project.serializers import ProjectSerializer
from .models import *
from Employee.models import Employee
from BusinessPartner.models import *
from Opportunity.models import *
from Lead.models import Lead
import requests, json

from Attachment.models import Attachment
from Attachment.serializers import AttachmentSerializer

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

from BusinessPartner.serializers import *
from Employee.serializers import *

from pytz import timezone
from datetime import datetime as dt

import os
from django.core.files.storage import FileSystemStorage

date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
yearmonth = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')

# Create your views here.  

#Order Create API
@api_view(['POST'])
def create(request):
    try:
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
        
        OrdNo = request.data['OrdNo']
        PoNo = request.data['PoNo']
        DatePO = request.data['DatePO']
        Attach = request.data['Attach']
        Caption = request.data['Caption']
        Project = request.data['Project']
        
        PaymentGroupCode = request.data['PaymentGroupCode']
        BPLID = request.data['BPLID']
        U_Term_Condition = request.data['U_Term_Condition']
        U_TermInterestRate = request.data['U_TermInterestRate']
        U_TermPaymentTerm = request.data['U_TermPaymentTerm']
        U_TermDueDate = request.data['U_TermDueDate']
        
        U_QUOTNM = request.data['U_QUOTNM']
        U_QUOTID = request.data['U_QUOTID']    
        
        U_OPPID = request.data['U_OPPID']
        U_OPPRNM = request.data['U_OPPRNM']
        
        NetTotal = request.data['NetTotal']
        
        U_LEADID = request.data['U_LEADID']
        U_LEADNM = request.data['U_LEADNM']
        
        #added by millan on 07-10-2022
        GroupType = request.data['GroupType']
        POAmount = request.data['POAmount']
        ProjectLocation = request.data['ProjectLocation']
        OPSNumber = request.data['OPSNumber']
        UrlNo = request.data['UrlNo']
        OtherInstruction = request.data['OtherInstruction']
        GSTNo = request.data['GSTNo']
        #added by millan on 07-10-2022
        
        #added by millan on 11-10-2022
        MICharges = request.data['MICharges']
        LOCharges = request.data['LOCharges']
        Intall = request.data['Intall']
        CivWork = request.data['CivWork']
        SSStatus = request.data['SSStatus']
        PlumStatus = request.data['PlumStatus']
        #added by millan on 11-10-2022
        
        #added by millan on 04-11-2022
        technical_details = request.data['technical_details']
        approved_drawing = request.data['approved_drawing']
        addendum = request.data['addendum']
        special_instructions = request.data['special_instructions']
        #added by millan on 04-11-2022
        
        lines = json.loads(request.data['DocumentLines'])
        DocTotal=0
        for line in lines:
            DocTotal = float(DocTotal) + float(line['Quantity']) * float(line['UnitPrice'])
        print(DocTotal)
        try:
            model=Order(OrdNo = OrdNo, PoNo = PoNo, DatePO = DatePO, Project = Project, TaxDate = TaxDate, DocDueDate = DocDueDate, ContactPersonCode = ContactPersonCode, DiscountPercent = DiscountPercent, DocDate = DocDate, CardCode = CardCode, CardName = CardName, Comments = Comments, SalesPersonCode = SalesPersonCode, DocumentStatus="bost_Open", CancelStatus="csNo", DocTotal = DocTotal, NetTotal=NetTotal, CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime, PaymentGroupCode=PaymentGroupCode, BPLID=BPLID,U_Term_Condition=U_Term_Condition, U_TermInterestRate=U_TermInterestRate, U_TermPaymentTerm=U_TermPaymentTerm, U_TermDueDate=U_TermDueDate, U_OPPID=U_OPPID, U_OPPRNM=U_OPPRNM, U_QUOTNM=U_QUOTNM, U_QUOTID=U_QUOTID, U_LEADID=U_LEADID, U_LEADNM=U_LEADNM, GroupType=GroupType, POAmount=POAmount, ProjectLocation=ProjectLocation, OPSNumber=OPSNumber, UrlNo=UrlNo, OtherInstruction=OtherInstruction, GSTNo=GSTNo, MICharges = MICharges, LOCharges = LOCharges, Intall = Intall, CivWork = CivWork, SSStatus = SSStatus, PlumStatus = PlumStatus, technical_details = technical_details, approved_drawing = approved_drawing, addendum = addendum, special_instructions = special_instructions) #added by millan on 11-10-2022
    
            model.save()
            qt = Order.objects.latest('id')
            fetchid = qt.id
            
            ORD = "ORD"+str(format(fetchid, '05'))
            model = Order.objects.get(pk = fetchid)            
            model.OrdNo = ORD
            model.save()
            
            #added by millan on 12-10-2022
            cc_code = model.CardCode
            if cc_code != "" and BusinessPartner.objects.filter(CardCode = cc_code).exists():
                model = BusinessPartner.objects.get(CardCode = cc_code)
                model.CustomerStatus = 'Customer'
                model.save()
            #added by millan on 12-10-2022
            
            
            print(request.FILES.getlist('Attach'))
            for File in request.FILES.getlist('Attach'):
                attachmentsImage_url = ""
                target ='./bridge/static/image/Attachment'
                os.makedirs(target, exist_ok=True)
                fss = FileSystemStorage()
                file = fss.save(target+"/"+File.name, File)
                productImage_url = fss.url(file)
                attachmentsImage_url = productImage_url.replace('/bridge', '')
                print(attachmentsImage_url)
                
                FileName = File.name #added by millan on 17-10-2022 for storing file name

                att=Attachment(File=attachmentsImage_url, Caption=Caption, LinkType="Order", LinkID=fetchid, CreateDate=CreateDate, CreateTime=CreateTime, UpdateDate=UpdateDate, UpdateTime=UpdateTime, FileName = FileName)
                
                att.save()
            
        except Exception as e:
            return Response({"message":str(e),"status":201,"data":[]})
        try:
            addr = json.loads(request.data['AddressExtension'])
            model_add = AddressExtension(OrderID = qt.id, BillToBuilding = addr['BillToBuilding'], ShipToState = addr['ShipToState'], BillToCity = addr['BillToCity'], ShipToCountry = addr['ShipToCountry'], BillToZipCode = addr['BillToZipCode'], ShipToStreet = addr['ShipToStreet'], BillToState = addr['BillToState'], ShipToZipCode = addr['ShipToZipCode'], BillToStreet = addr['BillToStreet'], ShipToBuilding = addr['ShipToBuilding'], ShipToCity = addr['ShipToCity'], BillToCountry = addr['BillToCountry'], U_SCOUNTRY = addr['U_SCOUNTRY'], U_SSTATE = addr['U_SSTATE'], U_SHPTYPB = addr['U_SHPTYPB'], U_BSTATE = addr['U_BSTATE'], U_BCOUNTRY = addr['U_BCOUNTRY'], U_SHPTYPS = addr['U_SHPTYPS'])
            model_add.save()
        except Exception as e:
            Order.objects.filter(pk=qt.id).delete()
            return Response({"message":str(e),"status":201,"data":[]})
        
        try:
            LineNum = 0
            for line in lines:
                model_lines = DocumentLines(LineNum = LineNum, OrderID = qt.id, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'], U_FGITEM = line['U_FGITEM'], CostingCode2 = line['CostingCode2'], ProjectCode = line['ProjectCode'], FreeText = line['FreeText'], Tap_Qty = line['Tap_Qty'], Tap_Type = line['Tap_Type'], Ht_Capacity = line['Ht_Capacity'], Ct_Capacity = line['Ct_Capacity'], At_Capacity = line['At_Capacity'], Pro_Capacity = line['Pro_Capacity'], Machine_Dimension = line['Machine_Dimension'], Machine_Colour = line['Machine_Colour'], Type_of_Machine = line['Type_of_Machine'], Machine_Body_Material = line['Machine_Body_Material'], UV_Germ = line['UV_Germ'], Sales_Type = line['Sales_Type'], Special_Remark = line['Special_Remark'], Tax = line['Tax'], UomNo = line['UomNo']) #updated by millan on 01-November-2022
                model_lines.save()
                LineNum=LineNum+1
        except Exception as e:
            DocumentLines.objects.filter(OrderID=qt.id).delete()
            Order.objects.filter(pk=qt.id).delete()
            return Response({"message":str(e),"status":201,"data":[]})
        
        #return Response({"message":"successful","status":200,"data":[{"qt_Id":qt.id}]})
            
        if settings.SAPORD == True:
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
                    "BillToBuilding": addr['BillToBuilding'],
                    "ShipToState": addr['ShipToState'],
                    "BillToCity": addr['BillToCity'],
                    "ShipToCountry": addr['ShipToCountry'],
                    "BillToZipCode": addr['BillToZipCode'],
                    "ShipToStreet": addr['ShipToStreet'],
                    "BillToState": addr['BillToState'],
                    "ShipToZipCode": addr['ShipToZipCode'],
                    "BillToStreet": addr['BillToStreet'],
                    "ShipToBuilding": addr['ShipToBuilding'],
                    "ShipToCity": addr['ShipToCity'],
                    "BillToCountry": addr['BillToCountry']
                },
                "DocumentLines": lines
            }
            
            print(qt_data)
            print(json.dumps(qt_data))

            res = requests.post(settings.BASEURL+'/Orders', data=json.dumps(qt_data), cookies=r.cookies, verify=False)
            live = json.loads(res.text)
            
            if "DocEntry" in live:
                print(live['DocEntry'])
                
                model = Order.objects.get(pk = fetchid)
                model.DocEntry = live['DocEntry']
                model.save()
                if int(U_LEADID) !=0:
                    leadObj = Lead.objects.get(pk=U_LEADID)
                    leadObj.ODStatus=1
                    leadObj.save()
                if U_OPPID !="":
                    oppObj = Opportunity.objects.get(pk=U_OPPID)
                    oppObj.ODStatus=1
                    oppObj.save()
                
                return Response({"message":"successful","status":200,"data":[{"qt_Id":qt.id, "DocEntry":live['DocEntry']}]})
            else:
                SAP_MSG = live['error']['message']['value']
                print(SAP_MSG)
                Order.objects.get(pk=qt.id).delete()
                allline = DocumentLines.objects.filter(OrderID=qt.id)
                for dcline in allline:
                    dcline.delete()
                    
                alladd = AddressExtension.objects.filter(OrderID=qt.id)
                for ad in alladd:
                    ad.delete()
                return Response({"message":SAP_MSG,"SAP_error":SAP_MSG, "status":202,"data":[]})
        else:
            model = Order.objects.get(pk = fetchid)
            model.DocEntry = fetchid
            model.save()
            if int(U_LEADID) !=0:
                leadObj = Lead.objects.get(pk=U_LEADID)
                leadObj.ODStatus=1
                leadObj.save()
            if U_OPPID !="":
                oppObj = Opportunity.objects.get(pk=U_OPPID)
                oppObj.ODStatus=1
                oppObj.save()
            return Response({"message":"successful","status":200,"data":[{"qt_Id":qt.id, "DocEntry":qt.id}]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#Order Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Order.objects.get(pk = fetchid)

        model.TaxDate = request.data['TaxDate']
        model.DocDate = request.data['DocDate']
        model.DocDueDate = request.data['DocDueDate']
        
        model.ContactPersonCode = request.data['ContactPersonCode']
        model.DiscountPercent = request.data['DiscountPercent']
        model.Comments = request.data['Comments']
        model.SalesPersonCode = request.data['SalesPersonCode']
        
        model.PaymentGroupCode = request.data['PaymentGroupCode']
        
        
        model.NetTotal = request.data['NetTotal']
        
        model.PoNo = request.data['PoNo']
        model.DatePO = request.data['DatePO']
        model.Attach = request.data['Attach']
        model.Project = request.data['Project']        

        model.U_Term_Condition = request.data['U_Term_Condition']
        model.U_TermInterestRate = request.data['U_TermInterestRate']
        model.U_TermPaymentTerm = request.data['U_TermPaymentTerm']
        model.U_TermDueDate = request.data['U_TermDueDate']
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
                lastline = DocumentLines.objects.filter(OrderID = fetchid).order_by('-LineNum')[:1]
                NewLine = int(lastline[0].LineNum) + 1
                model_lines = DocumentLines(OrderID = fetchid, LineNum=NewLine, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'], U_FGITEM = line['U_FGITEM'], CostingCode2 = line['CostingCode2'], ProjectCode = line['ProjectCode'], FreeText = line['FreeText'])
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

    
        # print(settings.BASEURL+"/Orders('"+model.DocEntry+"')");
        # res = requests.patch(settings.BASEURL+"/Orders("+model.DocEntry+")", data=json.dumps(qt_data), cookies=r.cookies, verify=False)

        print(settings.BASEURL+"/Orders('"+model.DocEntry+"')");
        res = requests.patch(settings.BASEURL+"/Orders("+model.DocEntry+")", data=json.dumps(qt_data), cookies=r.cookies, verify=False)
        print(res.content)

        if len(res.content) !=0 :
            res1 = json.loads(res.content)
            SAP_MSG = res1['error']['message']['value']
            return Response({"message":"Partely successful","status":202,"SAP_error":SAP_MSG, "data":[request.data]})
        else:
            return Response({"message":"successful","status":200, "data":[json.loads(json.dumps(request.data))]})
    except Exception as e:
        return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

def OrderShow(Orders_obj):
    allqt = [];
    for qt in Orders_obj:
        
        order_obj = OrderSerializer(qt)
        finalOrder = json.loads(json.dumps(order_obj.data))

        qtaddr = AddressExtension.objects.filter(OrderID=qt.id)
        qtaddr_json = AddressExtensionSerializer(qtaddr, many=True)
        
        jss_ = json.loads(json.dumps(qtaddr_json.data))
        for j in jss_:
            jss0=j
            finalOrder['AddressExtension'] = jss0
        
        lines = DocumentLines.objects.filter(OrderID=qt.id)
        lines_json = DocumentLinesSerializer(lines, many=True)
        jss1 = json.loads(json.dumps(lines_json.data))
        finalOrder['DocumentLines'] = jss1

        # cont = BPEmployee.objects.filter(InternalCode=qt.ContactPersonCode).values("InternalCode","FirstName")
        cont = BPEmployee.objects.filter(InternalCode=qt.ContactPersonCode)
        cont_json = BPEmployeeSerializer(cont, many=True)
        cont_all = json.loads(json.dumps(cont_json.data))
        
        #added by millan on 12-September-2022
        try:
            if qt.Project != "":
                if Project.objects.filter(id = qt.Project).exists():
                    project_dls = Project.objects.filter(id = qt.Project)
                    project_json = ProjectSerializer(project_dls, many=True)
                    finalOrder['Project'] = project_json.data
                else:
                    finalOrder['Project'] = []
            else:
                finalOrder['Project'] = []        
        except Exception as e:
            return Response({"message": str(e),"status": 201,"data":[]})        

        try:
            if Attachment.objects.filter(LinkID = qt.id, LinkType="Order").exists():
                attachment_dls = Attachment.objects.filter(LinkID = qt.id, LinkType="Order")
                attachment_json = AttachmentSerializer(attachment_dls, many=True)
                finalOrder['Attach'] = attachment_json.data
            else:
                finalOrder['Attach'] = []
        except Exception as e:
            return Response({"message": str(e),"status": 201,"data":[]})
       
        try:
            if qt.PaymentGroupCode != "":
                if PaymentTermsTypes.objects.filter(GroupNumber = qt.PaymentGroupCode).exists():
                    payment_dls = PaymentTermsTypes.objects.filter(GroupNumber = qt.PaymentGroupCode)
                    payment_dls_json = PaymentTermsTypesSerializer(payment_dls, many=True)
                    finalOrder['PaymentGroupCode'] = payment_dls_json.data
                else:
                    finalOrder['PaymentGroupCode'] = []
            else:
                finalOrder['PaymentGroupCode'] = []        
        except Exception as e:
            return Response({"message": str(e),"status": 201,"data":[]})        
        #added by millan on 12-September-2022
        
        #added by millan on 04-November-2022
        # try:
        if qt.CardCode !="":
            if BusinessPartner.objects.filter(CardCode = qt.CardCode).exists():
                BPCustCode = BusinessPartner.objects.filter(CardCode = qt.CardCode).values_list('BPCustCode', flat=True)
                BPCCCode = BPCustCode[0][0:6]
                
                if CustCode.objects.filter(OrderId=qt.id).exists(): 
                    
                    model = CustCode.objects.filter(OrderId=qt.id)
                    
                    BPURN = str(model[0].cc_prefix)+str('/URN1')+str(format(model[0].counter, '04'))
                    print("if BPURN: "+str(BPURN))
                    
                    finalOrder['URN'] = BPURN 
                    
                    OrdUrn = Order.objects.get(pk=qt.id)
                    OrdUrn.URN = BPURN
                    
                    OrdUrn.save()
                    
                else:
                    print(BPCCCode)
                    if CustCode.objects.filter(cc_prefix=BPCCCode).exists():
                        cc = CustCode.objects.filter(cc_prefix=BPCCCode).order_by('-id')[:1][0].counter 
                        
                        counter = int(cc) + 1
                        print("if")
                        model = CustCode(cc_prefix=BPCCCode, counter=counter, CustCodeBp=qt.CardCode, OrderId=qt.id)
                        model.save()

                    else: 
                        print("else")
                        counter =1
                        model = CustCode(cc_prefix=BPCCCode, CustCodeBp=qt.CardCode, counter =counter, OrderId=qt.id)
                        model.save()
                    
                    BPURN= str(BPCCCode)+str('/URN1')+str(format(counter, '04'))
                    finalOrder['URN'] = BPURN
                    print("else BPURN: "+str(BPURN))
                    
                    OrdUrn = Order.objects.get(pk=qt.id)
                    OrdUrn.URN = BPURN
                    OrdUrn.save()
                    
        else:
            return Response({"message": "Customer Card Must Exist","status": 201,"data":[]})     
                
        # except Exception as e:
        #     return Response({"message": str(e),"status": 201,"data":[]}) 
        #added by millan on 04-November-2022
        
        # print(cont_all)
        if len(cont) > 0:
            #ContactPerson = cont[0].FirstName
            ContactPerson = cont_json.data
            # print(ContactPerson)
        else:
            ContactPerson = ""
            

        sobj = Employee.objects.filter(SalesEmployeeCode=qt.SalesPersonCode).values("SalesEmployeeCode","EmployeeID","SalesEmployeeName", "lastName")
        sobj_json = EmployeeSerializer(sobj, many=True)
        sobj_all = json.loads(json.dumps(sobj_json.data))
        SalesPerson = sobj_json.data

        finalOrder['ContactPersonCode'] = ContactPerson
        finalOrder['SalesPersonCode'] = SalesPerson
        
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
        #     'CancelStatus':qt.CancelStatus,
        #     'DocCurrency':qt.DocCurrency,
        #     'DocTotal':qt.DocTotal,
        #     'VatSum':qt.VatSum,
            
        #     'PaymentGroupCode':qt.PaymentGroupCode,
        #     'U_Term_Condition':qt.U_Term_Condition,
        #     'U_TermInterestRate':qt.U_TermInterestRate,
        #     'U_TermPaymentTerm':qt.U_TermPaymentTerm,
        #     'U_TermDueDate':qt.U_TermDueDate,
        #     'U_LEADID':qt.U_LEADID,
        #     'U_LEADNM':qt.U_LEADNM,
        #     'BPLID':qt.BPLID,
            
        #     'CreationDate':qt.CreationDate,
            
        #     'AddressExtension':jss0,
        #     'DocumentLines':jss1,
            
        #     "CreateDate":qt.CreateDate,
        #     "CreateTime":qt.CreateTime,
        #     "UpdateDate":qt.UpdateDate,
        #     "UpdateTime":qt.UpdateTime
        #     }
            
        allqt.append(finalOrder)
        
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
                ord = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Open", DocDueDate__lt=date)
                allord = OrderShow(ord)
                #print(allord)
            elif json_data['Type'] =="open":
                ord = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Open", DocDueDate__gte=date)
                allord = OrderShow(ord)
                #print(allord)
            else:
                ord = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Close")
                allord = OrderShow(ord)
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
                SalesPersonID = [json_data['SalesPersonCode']]
            
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
                    quot_obj = Order.objects.filter(SalesPersonCode__in=SalesPersonID).order_by("-id")
                    allqt = OrderShow(quot_obj)
                        
                    return Response({"message": "Success","status": 200,"data":allqt})
            
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})

#Order All API
@api_view(["GET"])
def all(request):
    Orders_obj = Order.objects.all().order_by("-id")
    allqt = OrderShow(Orders_obj)
    return Response({"message": "Success","status": 200,"data":allqt})

#Order One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    
    Orders_obj = Order.objects.filter(id=id)
    
    allqt = OrderShow(Orders_obj)
    return Response({"message": "Success","status": 200,"data":allqt})


#Order delete
@api_view(['POST'])
def cancel(request):
    fetchid=request.data['DocEntry']
    try:
        odr=Order.objects.get(DocEntry=fetchid)
        odr.DocumentStatus='bost_Close'
        odr.CancelStatus='csYes'
        odr.save()            
        if settings.SAP==True:    
            try:
                r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
                token = json.loads(r.text)['SessionId']
                print(token)
                res = requests.post(settings.BASEURL+'/Orders('+fetchid+')/Cancel', cookies=r.cookies, verify=False)
                return Response({"message":"successful","status":200,"data":[]})
            except:
                return Response({"message":"successful","status":200,"data":[]})        
        else:
            return Response({"message":"successful","status":200,"data":[]})        
    except:
         return Response({"message":"Id wrong","status":201,"data":[]})

#update delivery
@api_view(['POST'])
def delivery_update(request):
   id = request.data['id']
   DelStatus = request.data['DelStatus']
   Obj = Order.objects.get(pk=id)
   Obj.DelStatus = DelStatus
   Obj.save()
   return Response({"message":"successful", "status":200, "data":[]})
   
#added by millan on 06-09-2022

#addendum create api
@api_view(['POST'])   
def addendumcreate(request):
    try:
        if request.data['OrderID'] == "":
            return Response({"message":"Order Id Can't be Empty","status":201,"data":[]})
        elif request.data['Date'] == "":
            return Response({"message":"Date Can't be Empty","status":201,"data":[]})
        elif request.data['Time'] == "":
            return Response({"message":"Time Can't be Empty","status":201,"data":[]})
        elif request.data['Attachments'] == "":
            return Response({"message":"Attachments Can't be Empty","status":201,"data":[]})
        else:
            OrderID = request.data['OrderID']
            Date = request.data['Date']
            Time = request.data['Time']
            Attachments = request.data['Attachments']
            
            attachmentsImage_url = ""
            if Attachments:
                target ='./bridge/static/image/addendumorder'
                os.makedirs(target, exist_ok=True)
                fss = FileSystemStorage()
                file = fss.save(target+"/"+Attachments.name, Attachments)
                productImage_url = fss.url(file)
                attachmentsImage_url = productImage_url.replace('/bridge', '')
            print(attachmentsImage_url)
            
            model = AddendumRequest(OrderID=OrderID, Date=Date, Time=Time, Attachments=attachmentsImage_url)
            model.save()

            addendumId = AddendumRequest.objects.latest('id')
            print(addendumId)
            
            return Response({"message":"success","status":200,"data":[]})
        
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})
        
#addendum All API 
@api_view(["POST"])
def addendumall(request):
    try:
        fetchid = request.data['OrderID']
        if AddendumRequest.objects.filter(OrderID=fetchid).exists():
            Addendum_obj = AddendumRequest.objects.filter(OrderID=fetchid)
            addn_obj = AddendumSerializer(Addendum_obj, many=True)
            finalAddendum = json.loads(json.dumps(addn_obj.data))
            #print(finalAddendum)
            return Response({"message": "Success","status": 200,"data":finalAddendum})
        else:
            return Response({"message": "Enter a Valid OrderID","status": 201,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
        