from django.conf import settings
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from Countries.models import States
from PaymentTermsTypes.models import PaymentTermsTypes
from PaymentTermsTypes.serializers import PaymentTermsTypesSerializer
from Branch.serializers import SettingGetBranchSerializer
from Branch.models import SettingBranch
from Project.models import Project
from Project.serializers import ProjectSerializer
from .models import *
from Employee.models import Employee
from BusinessPartner.models import *
from Opportunity.models import *
from Lead.models import Lead
import requests, json
from django.db.models import Q
from Attachment.models import Attachment
from Attachment.serializers import AttachmentSerializer

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

from BusinessPartner.serializers import *
from Employee.serializers import *

from global_methods import *

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
        print("reqyesssssssssssssssssssssssssssssssss", request.data)
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
        SettingBranch_id = request.data['SettingBranch_id']

        technical_details = request.data['technical_details']
        approved_drawing = request.data['approved_drawing']
        addendum = request.data['addendum']
        special_instructions = request.data['special_instructions']

        ######################## NEW KEYS ADD #########################
        BookedOnDate = request.data['BookedOnDate']
        AttendedBy = request.data['AttendedBy']
        Contact1 = request.data['Contact1']
        Contact2 = request.data['Contact2']
        Contact3= request.data['Contact3']
        EmailID= request.data['EmailID']
        FunctionDate= request.data['FunctionDate']
        Occasion= request.data['Occasion']
        Venue= request.data['Venue']
        Menu= request.data['Menu']
        Time= request.data['Time']
        BridelName= request.data['BridelName']
        GroomName= request.data['GroomName']
        HostedBy= request.data['HostedBy']
        FinalizedMenu= request.data['FinalizedMenu']
        Bar= request.data['Bar']
        BarTander= request.data['BarTander']
        LicenceCode= request.data['LicenceCode']
        HiTea = request.data['HiTea']
        DriversFood = request.data['DriversFood']
        Heaters= request.data['Heaters']
        Coolers= request.data['Coolers']
        Decorations= request.data['Decorations']
        DJ= request.data['DJ'] 
        Fans = request.data['Fans']   
        OptionalCustomerName = request.data['OptionalCustomerName']  
        # lines = json.loads(request.data['DocumentLines'])
        DocTotal=0
        # for line in lines:
        #     DocTotal = float(DocTotal) + float(line['Quantity']) * float(line['UnitPrice'])
        # print(DocTotal)
        if SettingBranch_id != "":
            SettingBranch_obj = SettingBranch.objects.filter(id=SettingBranch_id)
            if SettingBranch_obj:
                SettingBranch_obj = SettingBranch_obj.first()
            else:
                SettingBranch_obj = None
        else:
            SettingBranch_obj = None
        try:
            model=Order(OrdNo = OrdNo, PoNo = PoNo, DatePO = DatePO, Project = Project, TaxDate = TaxDate, 
                DocDueDate = DocDueDate, ContactPersonCode = ContactPersonCode, DiscountPercent = DiscountPercent,
                DocDate = DocDate, CardCode = CardCode, CardName = CardName, Comments = Comments, SalesPersonCode = SalesPersonCode, 
                DocumentStatus="bost_Open", CancelStatus="csNo", DocTotal = DocTotal, NetTotal=NetTotal, CreateDate = CreateDate, 
                CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime, PaymentGroupCode=PaymentGroupCode, 
                BPLID=BPLID,U_Term_Condition=U_Term_Condition, U_TermInterestRate=U_TermInterestRate, U_TermPaymentTerm=U_TermPaymentTerm, 
                U_TermDueDate=U_TermDueDate, U_OPPID=U_OPPID, U_OPPRNM=U_OPPRNM, U_QUOTNM=U_QUOTNM, U_QUOTID=U_QUOTID, U_LEADID=U_LEADID, 
                U_LEADNM=U_LEADNM, GroupType=GroupType, POAmount=POAmount, ProjectLocation=ProjectLocation, OPSNumber=OPSNumber,
                UrlNo=UrlNo, OtherInstruction=OtherInstruction, GSTNo=GSTNo, MICharges = MICharges, LOCharges = LOCharges, 
                Intall = Intall, CivWork = CivWork, SSStatus = SSStatus, PlumStatus = PlumStatus, technical_details = technical_details,
                approved_drawing = approved_drawing, addendum = addendum, special_instructions = special_instructions, 
                SettingBranch_id=SettingBranch_obj, BookedOnDate=BookedOnDate, AttendedBy=AttendedBy, Contact1=Contact1, Contact2=Contact2,
                Contact3=Contact3, EmailID=EmailID, FunctionDate=FunctionDate, Occasion=Occasion, Venue=Venue,
                Menu=Menu, Time=Time, BridelName=BridelName, GroomName=GroomName, HostedBy=HostedBy, FinalizedMenu=FinalizedMenu,
                Bar=Bar, BarTander=BarTander, LicenceCode=LicenceCode, HiTea=HiTea, DriversFood=DriversFood, Heaters=Heaters,
                Coolers=Coolers, Decorations=Decorations, DJ=DJ, Fans=Fans, OptionalCustomerName=OptionalCustomerName)
    
            model.save()
            qt = Order.objects.latest('id')
            print("#####################################################################################################",qt)
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
        
        # try:
        #     LineNum = 0
        #     for line in lines:
        #         model_lines = DocumentLines(LineNum = LineNum, OrderID = qt.id, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'], U_FGITEM = line['U_FGITEM'], CostingCode2 = line['CostingCode2'], ProjectCode = line['ProjectCode'], FreeText = line['FreeText'], Tap_Qty = line['Tap_Qty'], Tap_Type = line['Tap_Type'], Ht_Capacity = line['Ht_Capacity'], Ct_Capacity = line['Ct_Capacity'], At_Capacity = line['At_Capacity'], Pro_Capacity = line['Pro_Capacity'], Machine_Dimension = line['Machine_Dimension'], Machine_Colour = line['Machine_Colour'], Type_of_Machine = line['Type_of_Machine'], Machine_Body_Material = line['Machine_Body_Material'], UV_Germ = line['UV_Germ'], Sales_Type = line['Sales_Type'], Special_Remark = line['Special_Remark'], Tax = line['Tax'], UomNo = line['UomNo'], Item_uqc=line['Item_uqc'])
        #         model_lines.save()
        #         LineNum=LineNum+1
        # except Exception as e:
        #     DocumentLines.objects.filter(OrderID=qt.id).delete()
        #     Order.objects.filter(pk=qt.id).delete()
        #     return Response({"message":str(e),"status":201,"data":[]})
        
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
                "DocumentLines": ""
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
                # allline = DocumentLines.objects.filter(OrderID=qt.id)
                # for dcline in allline:
                #     dcline.delete()
                    
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
    print("fetchid ::", fetchid)
    try:
        model = Order.objects.get(pk = fetchid)
        model.DocTotal =0    
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
        SettingBranch_id = request.data['SettingBranch_id']
        ######################## NEW KEYS ADD #########################
        model.BookedOnDate = request.data['BookedOnDate']
        model.AttendedBy = request.data['AttendedBy']
        model.Contact1 = request.data['Contact1']
        model.Contact2 = request.data['Contact2']
        model.Contact3= request.data['Contact3']
        model.EmailID= request.data['EmailID']
        model.FunctionDate= request.data['FunctionDate']
        model.Occasion= request.data['Occasion']
        model.Venue= request.data['Venue']
        model.Menu= request.data['Menu']
        model.Time= request.data['Time']
        model.BridelName= request.data['BridelName']
        model.GroomName= request.data['GroomName']
        model.HostedBy= request.data['HostedBy']
        model.FinalizedMenu= request.data['FinalizedMenu']
        model.Bar= request.data['Bar']
        model.BarTander= request.data['BarTander']
        model.LicenceCode= request.data['LicenceCode']
        model.HiTea = request.data['HiTea']
        model.DriversFood = request.data['DriversFood']
        model.Heaters= request.data['Heaters']
        model.Coolers= request.data['Coolers']
        model.Decorations= request.data['Decorations']
        model.DJ= request.data['DJ']
        model.OptionalCustomerName = request.data['OptionalCustomerName']
        model.save()
        if AddressExtension.objects.filter(id = request.data['AddressExtension']['id']).exists():
            model_add = AddressExtension.objects.get(id = request.data['AddressExtension']['id'])           
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
        return Response({"message":"successful","status":200, "data":[json.loads(json.dumps(request.data))]})
    except Exception as e:
        return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

def OrderShow(Orders_obj):
    allqt = []
    for qt in Orders_obj:
        
        order_obj = OrderSerializer(qt)
        # finalOrder = json.loads(json.dumps(order_obj.data))
        finalOrder = order_obj.data
        if finalOrder["SettingBranch_id"]:
            id=finalOrder["SettingBranch_id"]
            Branch_obj = SettingBranch.objects.get(id=id)
            Branch_json = SettingGetBranchSerializer(Branch_obj)
            finalOrder["SettingBranch_id"] = Branch_json.data
        else:
            finalOrder["SettingBranch_id"] = {}
        qtaddr = AddressExtension.objects.filter(OrderID=qt.id)
        qtaddr_json = AddressExtensionSerializer(qtaddr, many=True)
        
        jss_ = json.loads(json.dumps(qtaddr_json.data))
        for j in jss_:
            state_gst = States.objects.filter(Code=j["BillToState"], Country=j["BillToCountry"]).first()
            jss0=j
            if state_gst:               
                jss0["GST"] = state_gst.GST
            finalOrder['AddressExtension'] = jss0
        
        lines = DocumentLines.objects.filter(OrderID=qt.id)
        if lines:
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
            return Response({"message": "Project : "+str(e),"status": 201,"data":[]})        

        try:
            if Attachment.objects.filter(LinkID = qt.id, LinkType="Order").exists():
                attachment_dls = Attachment.objects.filter(LinkID = qt.id, LinkType="Order")
                attachment_json = AttachmentSerializer(attachment_dls, many=True)
                finalOrder['Attach'] = attachment_json.data
            else:
                finalOrder['Attach'] = []
        except Exception as e:
            return Response({"message": "Attachment :"+str(e),"status": 201,"data":[]})
       
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
            return Response({"message": "PaymentTermsTypes :"+str(e),"status": 201,"data":[]})        

        # try:
        if qt.CardCode !="":
            if BusinessPartner.objects.filter(CardCode = qt.CardCode).exists():
                BPCustCode = BusinessPartner.objects.filter(CardCode = qt.CardCode).values_list('BPCustCode', flat=True)
                BPCCCode = BPCustCode[0][0:6]
                companymobile_obj = BusinessPartner.objects.filter(CardCode = qt.CardCode).values('EmailAddress','Phone1','PAN_Card', 'Adhaar_Number')
                if companymobile_obj:
                    finalOrder['BPEmail'] = companymobile_obj[0]['EmailAddress']
                    finalOrder['BPMobile'] = companymobile_obj[0]['Phone1']
                    finalOrder['PAN_Card'] = companymobile_obj[0]['PAN_Card']
                    finalOrder['Adhaar_Number'] = companymobile_obj[0]['Adhaar_Number']
                else:
                    finalOrder['BPEmail'] = ""
                    finalOrder['BPMobile'] = ""
                    finalOrder['PAN_Card'] = ""
                    finalOrder['Address_Number'] = ""
        #         if CustCode.objects.filter(OrderId=qt.id).exists(): 
                    
        #             model = CustCode.objects.filter(OrderId=qt.id)
                    
        #             BPURN = str(model[0].cc_prefix)+str('/URN1')+str(format(model[0].counter, '04'))
        #             print("if BPURN: "+str(BPURN))
                    
        #             finalOrder['URN'] = BPURN 
                    
        #             OrdUrn = Order.objects.get(pk=qt.id)
        #             OrdUrn.URN = BPURN
                    
        #             OrdUrn.save()
                    
        #         else:
        #             print(BPCCCode)
        #             if CustCode.objects.filter(cc_prefix=BPCCCode).exists():
        #                 cc = CustCode.objects.filter(cc_prefix=BPCCCode).order_by('-id')[:1][0].counter 
                        
        #                 counter = int(cc) + 1
        #                 print("if")
        #                 model = CustCode(cc_prefix=BPCCCode, counter=counter, CustCodeBp=qt.CardCode, OrderId=qt.id)
        #                 model.save()

        #             else: 
        #                 print("else")
        #                 counter =1
        #                 model = CustCode(cc_prefix=BPCCCode, CustCodeBp=qt.CardCode, counter =counter, OrderId=qt.id)
        #                 model.save()
                    
        #             BPURN= str(BPCCCode)+str('/URN1')+str(format(counter, '04'))
        #             finalOrder['URN'] = BPURN
        #             print("else BPURN: "+str(BPURN))
                    
        #             OrdUrn = Order.objects.get(pk=qt.id)
        #             OrdUrn.URN = BPURN
        #             OrdUrn.save()
                    
        # else:
        #     return Response({"message": "Customer Card Must Exist","status": 201,"data":[]})     
        
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
                
            elif emp_obj.role == 'admin' or emp_obj.role == 'ceo' or emp_obj.role == 'logistic' or emp_obj.role == 'accountant':
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


	
#Quotation All API
@api_view(["POST"])
def all_filter_page(request):
    json_data = request.data
    PageNo = json_data['PageNo']
    search = json_data['SearchText']
    MaxItem = json_data['MaxItem']
    endWith = (PageNo * MaxItem)
    startWith = (endWith - MaxItem)
    if "SalesPersonCode" in json_data:
        if json_data['SalesPersonCode']!="":
            SalesPersonID = json_data['SalesPersonCode']
            emp_obj = Employee.objects.get(SalesEmployeeCode=SalesPersonID)
            if emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesPersonID)#.values('id', 'SalesEmployeeCode')
                SalesPersonID=[SalesPersonID]
                for emp in emps:
                    SalesPersonID.append(emp.SalesEmployeeCode)
                
            elif emp_obj.role == 'admin' or emp_obj.role == 'ceo' or emp_obj.role == 'logistic' or emp_obj.role == 'accountant':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesPersonID=[]
                for emp in emps:
                    SalesPersonID.append(emp.SalesEmployeeCode)
            else:
                SalesPersonID = [json_data['SalesPersonCode']]
            
            quot_obj = Order.objects.filter(SalesPersonCode__in=SalesPersonID,CardName__icontains=search).order_by("-id")[startWith:endWith]
            
            allqt = OrderShow(quot_obj)
            return Response({"message": "Success","status": 200,"data":allqt})
            
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})


	
#Quotation All API
@api_view(["POST"])
def count_all(request):
    json_data = request.data
    search = json_data['SearchText']
    if "SalesPersonCode" in json_data:
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
            quot_obj = Order.objects.filter(SalesPersonCode__in=SalesPersonID,CardName__icontains=search).count()
            return Response({"message": "Success","status": 200,"data":[{"total_count":quot_obj}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})



	
#Quotation All API
@api_view(["POST"])
def all_filter_page_web(request):
    json_data = request.data
    PageNo = json_data['PageNo']
    search = json_data['SearchText']
    card_code = json_data['CardCode']
    MaxItem = json_data['MaxItem']
    if MaxItem!="All":
        endWith = (PageNo * int(MaxItem))
        startWith = (endWith - int(MaxItem))
    if "SalesPersonCode" in json_data:
        if json_data['SalesPersonCode']!="":
            SalesPersonID = json_data['SalesPersonCode']
            SalesPersonID = showEmployeeData(SalesPersonID)
            # emp_obj = Employee.objects.get(SalesEmployeeCode=SalesPersonID)
            # if emp_obj.role == 'manager':
            #     emps = Employee.objects.filter(reportingTo=SalesPersonID)#.values('id', 'SalesEmployeeCode')
            #     SalesPersonID=[SalesPersonID]
            #     for emp in emps:
            #         SalesPersonID.append(emp.SalesEmployeeCode)
                
            # elif emp_obj.role == 'admin' or emp_obj.role == 'ceo' or emp_obj.role == 'logistic' or emp_obj.role == 'accountant' or emp_obj.role == 'Service Head' or emp_obj.role == "marketing" or emp_obj.role == "HO":
            #     emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
            #     SalesPersonID=[]
            #     for emp in emps:
            #         SalesPersonID.append(emp.SalesEmployeeCode)
            # else:
            #     SalesPersonID = [json_data['SalesPersonCode']]
            
            if card_code!="":
                quot_count = Order.objects.filter(SalesPersonCode__in=SalesPersonID,CardCode=card_code, CardName__icontains=search).count()
                if MaxItem!="All":
                    quot_obj = Order.objects.filter(SalesPersonCode__in=SalesPersonID, CardCode=card_code, CardName__icontains=search).order_by("-id")[startWith:endWith]
                else:
                    quot_obj = Order.objects.filter(SalesPersonCode__in=SalesPersonID, CardCode=card_code, CardName__icontains=search).order_by("-id")
            else:
                quot_count = Order.objects.filter(SalesPersonCode__in=SalesPersonID,CardName__icontains=search).count()
                if MaxItem!="All":
                    quot_obj = Order.objects.filter(SalesPersonCode__in=SalesPersonID,CardName__icontains=search).order_by("-id")[startWith:endWith]
                else:
                    quot_obj = Order.objects.filter(SalesPersonCode__in=SalesPersonID,CardName__icontains=search).order_by("-id")

            allqt = OrderShow(quot_obj)
            return Response({"message": "Success","status": 200,"data":allqt, "extra":{"total_count":quot_count}})
            
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
    print("allqt ::", allqt)
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

# @api_view(['POST'])
# def delivery_create(request):
#     try:
#         OrderId = request.data['OrderId']
#         CompanyName = request.data['CompanyName']
#         OrderPlacedOn = request.data['OrderPlacedOn']
#         ShipTo = request.data['ShipTo']
#         ExpDel = request.data['ExpDel']
#         DelPart = request.data['DelPart']
#         AwbNo = request.data['AwbNo']

#         try:
#             model=DeliveryCreate(OrderId = OrderId,CompanyName = CompanyName,OrderPlacedOn = OrderPlacedOn,ShipTo = ShipTo,ExpDel = ExpDel,DelPart = DelPart,AwbNo = AwbNo)
#             model.save()
#             return Response({"message":"successful","status":200,"data":[]})
#         except Exception as e:
#             return Response({"message":str(e),"status":201,"data":[]})
        
#     except Exception as e:
#         return Response({"message":str(e),"status":201,"data":[]})

        

#Order request Create API
@api_view(['POST'])
def create_orderRequest(request):
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
        # Attach = request.data['Attach']
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
        GroupType = request.data['GroupType']
        POAmount = request.data['POAmount']
        ProjectLocation = request.data['ProjectLocation']
        OPSNumber = request.data['OPSNumber']
        UrlNo = request.data['UrlNo']
        OtherInstruction = request.data['OtherInstruction']
        GSTNo = request.data['GSTNo']
        MICharges = request.data['MICharges']
        LOCharges = request.data['LOCharges']
        Intall = request.data['Intall']
        CivWork = request.data['CivWork']
        SSStatus = request.data['SSStatus']
        PlumStatus = request.data['PlumStatus']
        SettingBranch_id = request.data['SettingBranch_id']

        technical_details = request.data['technical_details']
        approved_drawing = request.data['approved_drawing']
        addendum = request.data['addendum']
        special_instructions = request.data['special_instructions']
        order_request_name = request.data['order_request_name']
        lines = request.data['DocumentLines']
        DocTotal=0
        for line in lines:
            DocTotal = float(DocTotal) + float(line['Quantity']) * float(line['UnitPrice'])
        print(DocTotal)
        if SettingBranch_id != "":
            SettingBranch_obj = SettingBranch.objects.filter(id=SettingBranch_id)
            if SettingBranch_obj:
                SettingBranch_obj = SettingBranch_obj.first()
            else:
                SettingBranch_obj = None
        else:
            SettingBranch_obj = None
        try:
            model=CustomerOrder(OrdNo = OrdNo, PoNo = PoNo, DatePO = DatePO, Project = Project, TaxDate = TaxDate, DocDueDate = DocDueDate, ContactPersonCode = ContactPersonCode, DiscountPercent = DiscountPercent, DocDate = DocDate, CardCode = CardCode, CardName = CardName, Comments = Comments, SalesPersonCode = SalesPersonCode, DocumentStatus="bost_Open", CancelStatus="csNo", DocTotal = DocTotal, NetTotal=NetTotal, CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime, PaymentGroupCode=PaymentGroupCode, BPLID=BPLID,U_Term_Condition=U_Term_Condition, U_TermInterestRate=U_TermInterestRate, U_TermPaymentTerm=U_TermPaymentTerm, U_TermDueDate=U_TermDueDate, U_OPPID=U_OPPID, U_OPPRNM=U_OPPRNM, U_QUOTNM=U_QUOTNM, U_QUOTID=U_QUOTID, U_LEADID=U_LEADID, U_LEADNM=U_LEADNM, GroupType=GroupType, POAmount=POAmount, ProjectLocation=ProjectLocation, OPSNumber=OPSNumber, UrlNo=UrlNo, OtherInstruction=OtherInstruction, GSTNo=GSTNo, MICharges = MICharges, LOCharges = LOCharges, Intall = Intall, CivWork = CivWork, SSStatus = SSStatus, PlumStatus = PlumStatus, technical_details = technical_details, approved_drawing = approved_drawing, addendum = addendum, special_instructions = special_instructions, SettingBranch_id=SettingBranch_obj, order_request_name=order_request_name)
    
            model.save()
            qt = CustomerOrder.objects.latest('id')
            fetchid = qt.id

        except Exception as e:
            return Response({"message":str(e),"status":201,"data":[]})
        
        try:
            addr = request.data['AddressExtension']
            model_add = CustomerAddressExtension(OrderID = qt.id, BillToBuilding = addr['BillToBuilding'], ShipToState = addr['ShipToState'], BillToCity = addr['BillToCity'], ShipToCountry = addr['ShipToCountry'], BillToZipCode = addr['BillToZipCode'], ShipToStreet = addr['ShipToStreet'], BillToState = addr['BillToState'], ShipToZipCode = addr['ShipToZipCode'], BillToStreet = addr['BillToStreet'], ShipToBuilding = addr['ShipToBuilding'], ShipToCity = addr['ShipToCity'], BillToCountry = addr['BillToCountry'], U_SCOUNTRY = addr['U_SCOUNTRY'], U_SSTATE = addr['U_SSTATE'], U_SHPTYPB = addr['U_SHPTYPB'], U_BSTATE = addr['U_BSTATE'], U_BCOUNTRY = addr['U_BCOUNTRY'], U_SHPTYPS = addr['U_SHPTYPS'])
            model_add.save()
        except Exception as e:
            CustomerOrder.objects.filter(pk=qt.id).delete()
            return Response({"message":str(e),"status":201,"data":[]})
        
        try:
            LineNum = 0
            for line in lines:
                model_lines = CustomerDocumentLines(LineNum = LineNum, OrderID = qt.id, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'], U_FGITEM = line['U_FGITEM'], CostingCode2 = line['CostingCode2'], ProjectCode = line['ProjectCode'], FreeText = line['FreeText'], Tap_Qty = line['Tap_Qty'], Tap_Type = line['Tap_Type'], Ht_Capacity = line['Ht_Capacity'], Ct_Capacity = line['Ct_Capacity'], At_Capacity = line['At_Capacity'], Pro_Capacity = line['Pro_Capacity'], Machine_Dimension = line['Machine_Dimension'], Machine_Colour = line['Machine_Colour'], Type_of_Machine = line['Type_of_Machine'], Machine_Body_Material = line['Machine_Body_Material'], UV_Germ = line['UV_Germ'], Sales_Type = line['Sales_Type'], Special_Remark = line['Special_Remark'], Tax = line['Tax'], UomNo = line['UomNo'], Item_uqc=line['Item_uqc'])
                model_lines.save()
                LineNum=LineNum+1
        except Exception as e:
            CustomerDocumentLines.objects.filter(OrderID=qt.id).delete()
            CustomerOrder.objects.filter(pk=qt.id).delete()
            return Response({"message":str(e),"status":201,"data":[]})

        return Response({"message":"successful","status":200,"data":[{"qt_Id":qt.id, "DocEntry":qt.id}]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})


#Order request all API
@api_view(['POST'])
def all_filter_page_orderRequest(request):
    json_data = request.data
    PageNo = json_data['PageNo']
    search = json_data['SearchText']
    if json_data['MaxItem']!="All":
        MaxItem = int(json_data['MaxItem'])
        endWith = (PageNo * MaxItem)
        startWith = (endWith - MaxItem)
    if "SalesPersonCode" in json_data:
        if json_data['SalesPersonCode']!="":
            SalesPersonID = json_data['SalesPersonCode']
            SalesPersonID = showEmployeeData(SalesPersonID)
            if json_data["CardCode"]!="":
                quot_count = CustomerOrder.objects.filter(SalesPersonCode__in=SalesPersonID,CardCode=json_data["CardCode"],CardName__icontains=search).count()
                if json_data['MaxItem'] != "All":
                    quot_obj = CustomerOrder.objects.filter(SalesPersonCode__in=SalesPersonID,CardCode=json_data["CardCode"],CardName__icontains=search).order_by("-id")[startWith:endWith]
                else:
                    quot_obj = CustomerOrder.objects.filter(SalesPersonCode__in=SalesPersonID,CardCode=json_data["CardCode"],CardName__icontains=search).order_by("-id")

            else:
                quot_count = CustomerOrder.objects.filter(SalesPersonCode__in=SalesPersonID,CardName__icontains=search).count()
                if json_data['MaxItem'] != "All":
                    quot_obj = CustomerOrder.objects.filter(SalesPersonCode__in=SalesPersonID,CardName__icontains=search).order_by("-id")[startWith:endWith]
                else:
                    quot_obj = CustomerOrder.objects.filter(SalesPersonCode__in=SalesPersonID,CardName__icontains=search).order_by("-id")
            allqt = OrderRequestShow(quot_obj)
            return Response({"message": "Success","status": 200,"data":allqt, "extra":{"quot_count":quot_count}})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})

def OrderRequestShow(Orders_obj):
    allqt = [];
    for qt in Orders_obj:
        
        order_obj = OrderRequestSerializer(qt)
        # finalOrder = json.loads(json.dumps(order_obj.data))
        finalOrder = order_obj.data
        if finalOrder["SettingBranch_id"]:
            id=finalOrder["SettingBranch_id"]
            Branch_obj = SettingBranch.objects.get(id=id)
            Branch_json = SettingGetBranchSerializer(Branch_obj)
            finalOrder["SettingBranch_id"] = Branch_json.data
        else:
            finalOrder["SettingBranch_id"] = {}
        qtaddr = CustomerAddressExtension.objects.filter(OrderID=qt.id)
        qtaddr_json = OrderRequestAddressExtensionSerializer(qtaddr, many=True)
        
        jss_ = json.loads(json.dumps(qtaddr_json.data))
        for j in jss_:
            state_gst = States.objects.filter(Code=j["BillToState"], Country=j["BillToCountry"]).first()
            jss0=j
            jss0["GST"] = state_gst.GST
            finalOrder['AddressExtension'] = jss0
        
        lines = CustomerDocumentLines.objects.filter(OrderID=qt.id)
        lines_json = OrderRequestDocumentLinesSerializer(lines, many=True)
        jss1 = json.loads(json.dumps(lines_json.data))
        finalOrder['DocumentLines'] = jss1

        # # cont = BPEmployee.objects.filter(InternalCode=qt.ContactPersonCode).values("InternalCode","FirstName")
        cont = BPEmployee.objects.filter(InternalCode=qt.ContactPersonCode)
        cont_json = BPEmployeeSerializer(cont, many=True)
        cont_all = json.loads(json.dumps(cont_json.data))       
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
        # # print(cont_all)
        if len(cont) > 0:
            #ContactPerson = cont[0].FirstName
            ContactPerson = cont_json.data
            # print(ContactPerson)
        else:
            ContactPerson = ""
        finalOrder['ContactPersonCode'] = ContactPerson          
        allqt.append(finalOrder)        
    return allqt

#Order request approval API
@api_view(['POST'])
def approval_orderRequest(request):
    id = request.data["id"]
    emp_id = request.data["emp_id"]
    status = request.data["status"]
    CustomerOrder.objects.filter(id=id).update(approval_status=status, approved_by=emp_id)
    return Response({"message":"successful","status":200,"data":[]})

@api_view(['POST'])
def one_orderRequest(request):
    try:
        id = request.data["id"]
        quot_obj = CustomerOrder.objects.filter(id=id)
        allqt = OrderRequestShow(quot_obj)
        return Response({"message":"successful","status":200,"data":allqt})
    except Exception as e:
        return Response({"message":str(e),"status":400,"data":[]})    


#Quotation All API
@api_view(["POST"])
def all_pagination(request):
    try:    
        json_data = request.data
        PageNo = json_data['PageNo']
        SearchText = json_data['SearchText']
        card_code = json_data['CardCode']
        MaxItem = json_data['MaxItem']
        SalesPersonID = json_data['SalesPersonCode']        
        print("SearchText :", SearchText)
        order_obj =Order.objects.all().order_by("-id")
        if SalesPersonID !="":
            SalesPersonID = showEmployeeData(SalesPersonID)
            order_obj = order_obj.filter(SalesPersonCode__in=SalesPersonID)
        if card_code !="":
            order_obj = order_obj.filter(CardCode=card_code)    
        if SearchText !="":
            order_obj = order_obj.filter(Q(CardName__icontains=SearchText)|Q(OrdNo__icontains=SearchText)|Q(Occasion__icontains=SearchText)|Q(Venue__icontains=SearchText))
        count = order_obj.count()
        if MaxItem != "All":
            endWith = (PageNo * int(MaxItem))
            startWith = (endWith - int(MaxItem)) 
            order_obj = order_obj[startWith:endWith]                
        serializer = OrderSerializer(order_obj, many=True)
        return Response({"message": "Success","status": 200,"data":serializer.data, "total_count":count}) 
    except Exception as e:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":str(e)}]})   
    