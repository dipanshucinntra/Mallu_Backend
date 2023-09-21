#from ctypes.wintypes import PINT
import os
from django.conf import settings
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from PaymentTermsTypes.models import PaymentTermsTypes
from PaymentTermsTypes.serializers import PaymentTermsTypesSerializer

from Attachment.models import Attachment
from Attachment.serializers import AttachmentSerializer
from Project.models import Project
from Project.serializers import ProjectSerializer
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

#Quotation Create API
@api_view(['POST'])
def create(request):
    try:
        TaxDate = request.data['TaxDate']
        DocDueDate = request.data['DocDueDate']
        DocDate = request.data['DocDate']
        ContactPersonCode = request.data['ContactPersonCode']
        DiscountPercent = request.data['DiscountPercent']
        CardCode = request.data['CardCode']
        CardName = request.data['CardName']
        Comments = request.data['Comments']
        SalesPersonCode = request.data['SalesPersonCode']
        U_OPPID = request.data['U_OPPID']
        U_OPPRNM = request.data['U_OPPRNM']
        U_QUOTNM = request.data['U_QUOTNM']
        
        U_PREQUOTATION = request.data['U_PREQUOTATION']
        U_PREQTNM = request.data['U_PREQTNM']
        
        U_LEADID = request.data['U_LEADID']
        U_LEADNM = request.data['U_LEADNM']        
        
        PaymentGroupCode = request.data['PaymentGroupCode']
        BPLID = request.data['BPLID']
        U_Term_Condition = request.data['U_Term_Condition']
        U_TermInterestRate = request.data['U_TermInterestRate']
        U_TermPaymentTerm = request.data['U_TermPaymentTerm']
        U_TermDueDate = request.data['U_TermDueDate']
        
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        UpdateDate = request.data['UpdateDate']
        UpdateTime = request.data['UpdateTime']
        

        QuotType    = request.data['QuotType']
        # QTNO        = request.data['QTNO']
        Project     = request.data['Project']
        Attach      = request.data['Attach']
        Caption      = request.data['Caption']
        Subject     = request.data['Subject']
        GST         = request.data['GST']
        Discount    = request.data['Discount']
        Intall      = request.data['Intall']
        DelTerm     = request.data['DelTerm']
        
        #added by millan on 29-09-2022
        QuotStat     = request.data['QuotStat']
        ApprvReq     = request.data['ApprvReq']
        MICharges     = request.data['MICharges']
        LOCharges     = request.data['LOCharges']
        OthInstruct     = request.data['OthInstruct']
        #added by millan on 29-09-2022 
        
        #lines = request.data['DocumentLines']
        lines = json.loads(request.data['DocumentLines'])
        
        DocTotal=0
        for line in lines:
            DocTotal = float(DocTotal) + float(line['Quantity']) * float(line['UnitPrice'])
        print(DocTotal)

        #updated by millan on 02-September-2022
        try:
            model=Quotation(TaxDate = TaxDate, DocDueDate = DocDueDate, ContactPersonCode = ContactPersonCode, DiscountPercent = DiscountPercent, DocDate = DocDate, CardCode = CardCode, CardName = CardName, Comments = Comments, SalesPersonCode = SalesPersonCode, DocumentStatus="bost_Open", CancelStatus="csNo", DocTotal = DocTotal, U_OPPID=U_OPPID, U_OPPRNM=U_OPPRNM, U_QUOTNM=U_QUOTNM, U_PREQUOTATION=U_PREQUOTATION, U_PREQTNM=U_PREQTNM, U_FAV='N', CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime, PaymentGroupCode=PaymentGroupCode, BPLID=BPLID, U_Term_Condition=U_Term_Condition, U_TermInterestRate=U_TermInterestRate, U_TermPaymentTerm=U_TermPaymentTerm, U_TermDueDate=U_TermDueDate, U_LEADID=U_LEADID, U_LEADNM=U_LEADNM, QuotType = QuotType, Project = Project, Subject = Subject, GST = GST, Discount = Discount, Intall = Intall, DelTerm = DelTerm, QuotStat = QuotStat, ApprvReq = ApprvReq, MICharges = MICharges, LOCharges = LOCharges, OthInstruct = OthInstruct)
        
            model.save()
            qt = Quotation.objects.latest('id')
            qt.QTNO = "QOT"+str(format(qt.id, '05'))
            qt.save()
            fetchid = qt.id
            
            #updated by millan on 06-September-2022
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

                att=Attachment(File=attachmentsImage_url, LinkType="Quotation", Caption=Caption, LinkID=fetchid, CreateDate=CreateDate, CreateTime=CreateTime, UpdateDate=UpdateDate, UpdateTime=UpdateTime, FileName = FileName)
                
                att.save()

            # print(Attach)
            # attachmentsImage_url = ""
            # if Attach !="":
                # target ='./bridge/static/image/QuotationImage'
                # os.makedirs(target, exist_ok=True)
                # fss = FileSystemStorage()
                # file = fss.save(target+"/"+Attach.name, Attach)
                # productImage_url = fss.url(file)
                # attachmentsImage_url = productImage_url.replace('/bridge', '')
            
            # att = Attachment(File=attachmentsImage_url, LinkType="Quotation", LinkID=qt.id, CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime)
            # att.save()
            
        except Exception as e:
            return Response({"message":str(e),"status":201, "data":[]})
        
        #updated by millan on 02-September-2022
        try:
            #addr = request.data['AddressExtension']
            addr = json.loads(request.data['AddressExtension']) 
            
            model_add = AddressExtension(QuotationID = qt.id, BillToBuilding = addr['BillToBuilding'], ShipToState = addr['ShipToState'], BillToCity = addr['BillToCity'], ShipToCountry = addr['ShipToCountry'], BillToZipCode = addr['BillToZipCode'], ShipToStreet = addr['ShipToStreet'], BillToState = addr['BillToState'], ShipToZipCode = addr['ShipToZipCode'], BillToStreet = addr['BillToStreet'], ShipToBuilding = addr['ShipToBuilding'], ShipToCity = addr['ShipToCity'], BillToCountry = addr['BillToCountry'], U_SCOUNTRY = addr['U_SCOUNTRY'], U_SSTATE = addr['U_SSTATE'], U_SHPTYPB = addr['U_SHPTYPB'], U_BSTATE = addr['U_BSTATE'], U_BCOUNTRY = addr['U_BCOUNTRY'], U_SHPTYPS = addr['U_SHPTYPS'], BillToRemark =addr['BillToRemark'], ShipToRemark = addr['ShipToRemark']) #updated by millan on 29-09-2022
            model_add.save()
        
        except Exception as e:
            Quotation.objects.filter(pk=qt.id).delete()
            return Response({"message":str(e),"status":201, "data":[]})
        
        #updated by millan on 02-September-2022
        try:
            LineNum = 0
            for line in lines:
                model_lines = DocumentLines(LineNum = LineNum, QuotationID = qt.id, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'], U_FGITEM = line['U_FGITEM'], CostingCode2 = line['CostingCode2'], ProjectCode = line['ProjectCode'], FreeText = line['FreeText'], Tax = line['Tax'],UomNo = line['UomNo'])    #added by millan on 10-10-2022
                
                model_lines.save()
                LineNum=LineNum+1
        except Exception as e:
            DocumentLines.objects.filter(QuotationID=qt.id).delete()
            AddressExtension.objects.filter(QuotationID=qt.id).delete()
            Quotation.objects.filter(pk=qt.id).delete()
            return Response({"message":str(e),"status":201, "data":[]})
        
        # exit for without SAP
        model = Quotation.objects.get(pk = fetchid)
        model.DocEntry = fetchid
        model.save()
        if int(U_LEADID) !=0:
            leadObj = Lead.objects.get(pk=U_LEADID)
            leadObj.QTStatus=1
            leadObj.save()
        if U_OPPID !="":
            oppObj = Opportunity.objects.get(pk=U_OPPID)
            oppObj.QTStatus=1
            oppObj.save()
        
        emp_obj =  Employee.objects.filter(SalesEmployeeCode=SalesPersonCode)[0]
        report_obj = Employee.objects.filter(SalesEmployeeCode=emp_obj.reportingTo)

        level = tree(SalesPersonCode) 
        #level = tree_role(emp_obj) 
        print("Level: "+level)
        slave_obj =  AppSlave.objects.filter(Level=level)
        min = slave_obj[0].Min
        max = slave_obj[0].Max
        print(max)

        if float(DiscountPercent) <=max:
            model.APPROVEID_id = SalesPersonCode
            model.FinalStatus = "Approved"
            if int(level) == 1:
                model.Level1_id = SalesPersonCode
                model.Level1Status = "Approved"
            elif int(level) == 2:
                model.Level2_id = SalesPersonCode
                model.Level2Status = "Approved"
            elif int(level) == 3:
                model.Level3_id = SalesPersonCode
                model.Level3Status = "Approved"
                
            model.save()
        else:
            model.FinalStatus = "Pending"

            if int(level) == 2:
                model.Level2_id = SalesPersonCode
                model.Level2Status = "Approved"
                model.Level1_id = report_obj[0].SalesEmployeeCode
                model.Level1Status = "Pending"
            elif int(level) == 3:
                model.Level3_id = SalesPersonCode
                model.Level3Status = "Approved"
                model.Level2_id = report_obj[0].SalesEmployeeCode
                model.Level2Status = "Pending"
            elif int(level) == 4:
                model.Level3_id = report_obj[0].SalesEmployeeCode
                model.Level3Status = "Pending"
            model.save()        
        
        return Response({"message":"successful","status":200, "data":[]})

        # r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
        # token = json.loads(r.text)['SessionId']
        # print(token)
        
        # qt_data = {
        #     "TaxDate": request.data['TaxDate'],
        #     "DocDueDate": request.data['DocDueDate'],
        #     "DocDate": request.data['DocDate'],
        #     "ContactPersonCode": request.data['ContactPersonCode'],
        #     "DiscountPercent": request.data['DiscountPercent'],
        #     "CardCode": request.data['CardCode'],
        #     "CardName": request.data['CardName'],
        #     "Comments": request.data['Comments'],
        #     "SalesPersonCode": request.data['SalesPersonCode'],
        #     "BPL_IDAssignedToInvoice": request.data['BPLID'],
        #     "PaymentGroupCode":request.data['PaymentGroupCode'],
        #     "U_PORTAL_NO":qt.id,
        #     "AddressExtension": {
        #         "BillToBuilding": request.data['AddressExtension']['BillToBuilding'],
        #         "ShipToState": request.data['AddressExtension']['ShipToState'],
        #         "BillToCity": request.data['AddressExtension']['BillToCity'],
        #         "ShipToCountry": request.data['AddressExtension']['ShipToCountry'],
        #         "BillToZipCode": request.data['AddressExtension']['BillToZipCode'],
        #         "ShipToStreet": request.data['AddressExtension']['ShipToStreet'],
        #         "BillToState": request.data['AddressExtension']['BillToState'],
        #         "ShipToZipCode": request.data['AddressExtension']['ShipToZipCode'],
        #         "BillToStreet": request.data['AddressExtension']['BillToStreet'],
        #         "ShipToBuilding": request.data['AddressExtension']['ShipToBuilding'],
        #         "ShipToCity": request.data['AddressExtension']['ShipToCity'],
        #         "BillToCountry": request.data['AddressExtension']['BillToCountry']
        #     },
        #     "DocumentLines": lines
        # }
        
        # print(qt_data)
        # print(json.dumps(qt_data))

        # res = requests.post(settings.BASEURL+'/Quotations', data=json.dumps(qt_data), cookies=r.cookies, verify=False)
        # live = json.loads(res.text)
        
        
        # if "DocEntry" in live:
        #     print(live['DocEntry'])
            
        #     model = Quotation.objects.get(pk = fetchid)
        #     model.DocEntry = live['DocEntry']
        #     model.save()
        #     if int(U_LEADID) !=0:
        #         leadObj = Lead.objects.get(pk=U_LEADID)
        #         leadObj.QTStatus=1
        #         leadObj.save()
        #     if U_OPPID !="":
        #         oppObj = Opportunity.objects.get(pk=U_OPPID)
        #         oppObj.QTStatus=1
        #         oppObj.save()

        #     emp_obj =  Employee.objects.filter(SalesEmployeeCode=SalesPersonCode)
        #     report_obj = Employee.objects.filter(SalesEmployeeCode=emp_obj[0].reportingTo)

        #     level = tree(SalesPersonCode) 
        #     print("Level: "+level)
        #     slave_obj =  AppSlave.objects.filter(Level=level)
        #     min = slave_obj[0].Min
        #     max = slave_obj[0].Max

        #     if float(DiscountPercent) <=max:
        #         model.APPROVEID_id = SalesPersonCode
        #         model.FinalStatus = "Approved"
        #         if int(level) == 1:
        #             model.Level1_id = SalesPersonCode
        #             model.Level1Status = "Approved"
        #         elif int(level) == 2:
        #             model.Level2_id = SalesPersonCode
        #             model.Level2Status = "Approved"
        #         elif int(level) == 3:
        #             model.Level3_id = SalesPersonCode
        #             model.Level3Status = "Approved"
                    
        #         model.save()
        #     else:
        #         model.FinalStatus = "Pending"

        #         if int(level) == 2:
        #             model.Level2_id = SalesPersonCode
        #             model.Level2Status = "Approved"
        #             model.Level1_id = report_obj[0].SalesEmployeeCode
        #             model.Level1Status = "Pending"
        #         elif int(level) == 3:
        #             model.Level3_id = SalesPersonCode
        #             model.Level3Status = "Approved"
        #             model.Level2_id = report_obj[0].SalesEmployeeCode
        #             model.Level2Status = "Pending"
        #         elif int(level) == 4:
        #             model.Level3_id = report_obj[0].SalesEmployeeCode
        #             model.Level3Status = "Pending"
        # #         model.save()
            
        #     return Response({"message":"successful","status":200,"data":[{"qt_Id":qt.id, "DocEntry":live['DocEntry']}]})
        # else:
        #     SAP_MSG = live['error']['message']['value']
        #     print(SAP_MSG)
        #     Quotation.objects.get(pk=qt.id).delete()
        #     allline = DocumentLines.objects.filter(QuotationID=qt.id)
        #     for dcline in allline:
        #         dcline.delete()
                
        #     alladd = AddressExtension.objects.filter(QuotationID=qt.id)
        #     for ad in alladd:
        #         ad.delete()
        #     return Response({"message":SAP_MSG,"SAP_error":SAP_MSG, "status":202,"data":[]})

    except Exception as e:
        return Response({"message":str(e), "status":202,"data":[]})


#Quotation Fav Update API
@api_view(['POST'])
def fav(request):
    fetchid = request.data['id']
    model = Quotation.objects.get(pk = fetchid)
    model.U_FAV  = request.data['U_FAV']
    model.save()
    return Response({"message":"successful","status":200, "data":[]})

#Quotation Update API
@api_view(['POST'])
def approve(request):
    SalesEmployeeCode = request.data['SalesEmployeeCode']
    qtid = request.data['id']
    FinalStatus = request.data['FinalStatus']
    #SalesEmployeeCode=2 #salesman
    #SalesEmployeeCode=1 #manager
    #SalesEmployeeCode=38 #admin
    try:
        # UPDATE `quotation_quotation` SET `APPROVEID_id`= NULL, `FinalStatus`="", `Level3_id` = NULL, `Level2_id` = NULL, `Level1_id` = NULL, `Level3Status` = "", `Level2Status` = "", `Level1Status` = "" WHERE `quotation_quotation`.`id` = 30;
        level = tree(SalesEmployeeCode) 
        print("Level: "+level)
        slave_obj =  AppSlave.objects.filter(Level=level)
        min = slave_obj[0].Min
        max = slave_obj[0].Max

        print(str(min)+"-"+str(max))

        qt =  Quotation.objects.get(pk=qtid)
        dis=qt.DiscountPercent
        print(str(dis)+"%")
        #FinalStatus = "Approved"
        #FinalStatus = "Rejected"

        #if dis >= float(min) and dis <= float(max):
        if dis <= float(max):
            print("appr")
            print('"ApprovedID":'+str(SalesEmployeeCode)+'')
            qt.APPROVEID_id = SalesEmployeeCode
            qt.FinalStatus = FinalStatus

            if int(level) == 1:
                qt.Level1_id =SalesEmployeeCode
                qt.Level1Status = FinalStatus
            elif int(level) == 2:
                qt.Level2_id =SalesEmployeeCode
                qt.Level2Status = FinalStatus
            elif int(level) == 3:
                qt.Level3_id =SalesEmployeeCode
                qt.Level3Status = FinalStatus
            
            qt.save()

            print('"FinalStatus":'+FinalStatus)
        else:
            #print("send for appr")
            #SELECT * FROM `quotation_appslave` WHERE Min <= 11 and Max >=11;
            slave_obj =  AppSlave.objects.filter(Min__lte=dis, Max__gte=dis)
            #print(slave_obj)
            
            emp_obj =  Employee.objects.filter(SalesEmployeeCode=SalesEmployeeCode)
            report_obj = Employee.objects.filter(SalesEmployeeCode=emp_obj[0].reportingTo)
            #print("Send to Level "+str(slave_obj[0].Level))
            #print("Send to Level "+emp_obj1[0].role)
            print("_____")
            print("Send for Approve -- Role:--" + report_obj[0].role+ "; SalesEmployeeCode:-- "+report_obj[0].SalesEmployeeCode)    
            print("Send for Final -- Level "+str(slave_obj[0].Level))
            print("_____")
            print('"ApprovedID":null')
            print('"FinalStatus":"Pending"')
            if FinalStatus == "Rejected":        
                qt.APPROVEID_id = SalesEmployeeCode
                qt.FinalStatus = FinalStatus
            else:
                qt.FinalStatus = "Pending"

            if int(level) == 1:
                qt.Level1_id =SalesEmployeeCode
                qt.Level1Status = FinalStatus
            elif int(level) == 2:
                qt.Level2_id =SalesEmployeeCode
                qt.Level2Status = FinalStatus
                qt.Level1_id = report_obj[0].SalesEmployeeCode
                qt.Level1Status = "Pending"
            elif int(level) == 3:
                qt.Level3_id =SalesEmployeeCode
                qt.Level3Status = FinalStatus
                qt.Level2_id = report_obj[0].SalesEmployeeCode
                qt.Level2Status = "Pending"
            qt.save()
            print("_____")
        return Response({"message":"Success","status":201,"data":[]})

    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[{"Error":str(e)}]})

#Quotation pending for approval
@api_view(["POST"])
def pending(request):
    SalesEmployeeCode = request.data['SalesEmployeeCode']
    level = tree(SalesEmployeeCode)
    print(level)
    if int(level) == 3:
        quot_obj = Quotation.objects.filter(Level3_id=SalesEmployeeCode,Level3Status="Pending").order_by("-id")
    elif int(level) == 2:
        quot_obj = Quotation.objects.filter(Level2_id=SalesEmployeeCode,Level2Status="Pending").order_by("-id")
    elif int(level) == 1:
        quot_obj = Quotation.objects.filter(Level1_id=SalesEmployeeCode,Level1Status="Pending").order_by("-id")
    print(quot_obj)

    allqt = QuotationShow(quot_obj)                        
    return Response({"message": "Success","status": 200,"data":allqt})

#Quotation pending for approval
@api_view(["POST"])
def approved(request):
    SalesEmployeeCode = request.data['SalesEmployeeCode']
    level = tree(SalesEmployeeCode)
    print(level)
    if int(level) == 3:
        quot_obj = Quotation.objects.filter(Level3_id=SalesEmployeeCode,Level3Status="Approved").order_by("-id")
    elif int(level) == 2:
        quot_obj = Quotation.objects.filter(Level2_id=SalesEmployeeCode,Level2Status="Approved").order_by("-id")
    elif int(level) == 1:
        quot_obj = Quotation.objects.filter(FinalStatus="Approved").order_by("-id")
    print(quot_obj)

    allqt = QuotationShow(quot_obj)                        
    return Response({"message": "Success","status": 200,"data":allqt})

#Quotation Update API
@api_view(['POST'])
def approve_old(request):
    fetchid = request.data['id']
    try:
        model = Quotation.objects.get(pk = fetchid)
        model.U_APPROVEID = request.data['U_APPROVEID']
        model.U_APPROVENM = request.data['U_APPROVENM']
        model.save()
        return Response({"message":"successful","status":200, "data":[]})
    except Exception as e:
        return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

#Quotation Update API
@api_view(['POST'])
def update(request):
    try:
        fetchid = request.data['id']
        model = Quotation.objects.get(pk = fetchid)
        old_dis = model.DiscountPercent
        new_dis = request.data['DiscountPercent']
        model.TaxDate = request.data['TaxDate']
        model.DocDate = request.data['DocDate']
        model.DocDueDate = request.data['DocDueDate']
        model.ContactPersonCode = request.data['ContactPersonCode']
        model.DiscountPercent = request.data['DiscountPercent']
        model.Comments = request.data['Comments']
        SalesPersonCode_old = model.SalesPersonCode
        model.SalesPersonCode = request.data['SalesPersonCode']

        model.PaymentGroupCode = request.data['PaymentGroupCode']
        
        model.U_Term_Condition = request.data['U_Term_Condition']
        model.U_TermInterestRate = request.data['U_TermInterestRate']
        model.U_TermPaymentTerm = request.data['U_TermPaymentTerm']
        model.U_TermDueDate = request.data['U_TermDueDate']
        
        model.BPLID = request.data['BPLID']
        
        model.U_QUOTNM = request.data['U_QUOTNM']
        model.U_PREQUOTATION = request.data['U_PREQUOTATION']
        
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']
        model.QuotType = request.data['QuotType']
        # model.QTNO = request.data['QTNO']
        if request.data['Project'] != "[]":
            model.Project = request.data['Project']
        else:
            model.Project = ""
        #model.Attach = request.data['Attach']
        model.Subject = request.data['Subject']
        model.GST = request.data['GST']
        model.Discount = request.data['Discount']
        model.Intall = request.data['Intall']
        model.DelTerm = request.data['DelTerm']
        
        #added by millan on 29-09-2022
        model.QuotStat     = request.data['QuotStat']
        model.ApprvReq     = request.data['ApprvReq']
        model.MICharges     = request.data['MICharges']
        model.LOCharges     = request.data['LOCharges']
        model.OthInstruct     = request.data['OthInstruct']
        #added by millan on 29-09-2022 
        
        # Attach = request.data['Attach']
        # print(Attach)
        # attachmentsImage_url = ""
        # if Attach !="":
            # target ='./bridge/static/image/QuotationImage'
            # os.makedirs(target, exist_ok=True)
            # fss = FileSystemStorage()
            # file = fss.save(target+"/"+Attach.name, Attach)
            # productImage_url = fss.url(file)
            # attachmentsImage_url = productImage_url.replace('/bridge', '')
            
            # model.Attach = attachmentsImage_url
            
            # print(attachmentsImage_url)  

        model.save()
        
        
        addr = json.loads(request.data['AddressExtension'])
        
        model_add = AddressExtension.objects.get(id = addr['id'])
        # print(model_add)
        
        model_add.BillToBuilding = addr['BillToBuilding']
        model_add.ShipToState = addr['ShipToState']
        model_add.BillToCity = addr['BillToCity']
        model_add.ShipToCountry = addr['ShipToCountry']
        model_add.BillToZipCode = addr['BillToZipCode']
        model_add.ShipToStreet = addr['ShipToStreet']
        model_add.BillToState = addr['BillToState']
        model_add.ShipToZipCode = addr['ShipToZipCode']
        model_add.BillToStreet = addr['BillToStreet']
        model_add.ShipToBuilding = addr['ShipToBuilding']
        model_add.ShipToCity = addr['ShipToCity']
        model_add.BillToCountry = addr['BillToCountry']
        model_add.U_SCOUNTRY = addr['U_SCOUNTRY']
        model_add.U_SSTATE = addr['U_SSTATE']
        model_add.U_SHPTYPB = addr['U_SHPTYPB']
        model_add.U_BSTATE = addr['U_BSTATE']
        model_add.U_BCOUNTRY = addr['U_BCOUNTRY']
        model_add.U_SHPTYPS = addr['U_SHPTYPS']
        
        #added by millan on 29-09-2022
        model_add.BillToRemark = addr['BillToRemark']
        model_add.ShipToRemark = addr['ShipToRemark']
        #added by millan on 29-09-2022
   
        model_add.save()
        print("add save")
        
        #lines = request.data['DocumentLines']
        lines = json.loads(request.data['DocumentLines'])
        itemLines = []
        for line in lines:
            # if "id" in line:
            if line['id'] != "":
                model_line = DocumentLines.objects.get(pk = line['id'])
                model_line.Quantity=line['Quantity']
                model_line.UnitPrice=line['UnitPrice']
                model_line.DiscountPercent=line['DiscountPercent']
                model_line.ItemCode=line['ItemCode']
                model_line.ItemDescription=line['ItemDescription'] 
                model_line.TaxCode=line['TaxCode']           
                model_line.FreeText=line['FreeText']           
                model_line.U_FGITEM=line['U_FGITEM']  #added by millan on 06-10-2022      
                
                #added by millan on 10-10-2022      
                model_line.Tax = line['Tax']
                model_line.UomNo = line['UomNo']
                #added by millan on 10-10-2022         
                model_line.save()
                #print(DocumentLines.objects.latest('id'))
                itemLines.append(line['id'])
            else:
                lastline = DocumentLines.objects.filter(QuotationID = fetchid).order_by('-LineNum')[:1]
                NewLine = int(lastline[0].LineNum) + 1
                model_lines = DocumentLines(QuotationID = fetchid, LineNum=NewLine, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'],FreeText = line['FreeText'],U_FGITEM=line['U_FGITEM'], Tax=line['Tax'], UomNo=line['UomNo'])
                model_lines.save()
                new_item = DocumentLines.objects.latest('id')
                itemLines.append(new_item.id)
        if len(itemLines) > 0:
            DocumentLines.objects.filter(QuotationID = fetchid).exclude(pk__in = itemLines).delete()    
            
        #return Response({"message":"successful","status":200, "data":[json.loads(json.dumps(request.data))]})
        print("old_dis")
        print(float(old_dis))
        print("request.DiscountPercent---")
        print(float(new_dis))

        SalesPersonCode = request.data['SalesPersonCode']
        if (float(old_dis) != float(new_dis)) or SalesPersonCode != SalesPersonCode_old:
            print("if disc")

            #SalesPersonCode = model.SalesPersonCode
            emp_obj =  Employee.objects.filter(SalesEmployeeCode=SalesPersonCode)
            report_obj = Employee.objects.filter(SalesEmployeeCode=emp_obj[0].reportingTo)

            model.APPROVEID_id = None
            model.FinalStatus = ""
            model.Level1_id = None
            model.Level1Status = ""
            model.Level2_id = None
            model.Level2Status = ""
            model.Level3_id = None
            model.Level3Status = ""
            model.save()

            level = tree(SalesPersonCode) 
            #level = tree_role(emp_obj) 
            print("Level: "+level)
            slave_obj =  AppSlave.objects.filter(Level=level)
            min = slave_obj[0].Min
            max = slave_obj[0].Max

            if float(new_dis) <=max:
                model.APPROVEID_id = SalesPersonCode
                model.FinalStatus = "Approved"
                if int(level) == 1:
                    model.Level1_id = SalesPersonCode
                    model.Level1Status = "Approved"
                elif int(level) == 2:
                    model.Level2_id = SalesPersonCode
                    model.Level2Status = "Approved"
                elif int(level) == 3:
                    model.Level3_id = SalesPersonCode
                    model.Level3Status = "Approved"
                    
                model.save()
            else:
                model.FinalStatus = "Pending"

                if int(level) == 2:
                    model.Level2_id = SalesPersonCode
                    model.Level2Status = "Approved"
                    model.Level1_id = report_obj[0].SalesEmployeeCode
                    model.Level1Status = "Pending"
                elif int(level) == 3:
                    model.Level3_id = SalesPersonCode
                    model.Level3Status = "Approved"
                    model.Level2_id = report_obj[0].SalesEmployeeCode
                    model.Level2Status = "Pending"
                elif int(level) == 4:
                    model.Level3_id = report_obj[0].SalesEmployeeCode
                    model.Level3Status = "Pending"
                model.save()

        return Response({"message":"successful","status":200, "data":[]})
       
        # r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
        # token = json.loads(r.text)['SessionId']
        # print(token)
        
        # qt_data = {
        #     "TaxDate": request.data['TaxDate'],
        #     "DocDueDate": request.data['DocDueDate'],
        #     "DocDate": request.data['DocDate'],
        #     "ContactPersonCode": request.data['ContactPersonCode'],
        #     "DiscountPercent": request.data['DiscountPercent'],
        #     "Comments": request.data['Comments'],
        #     "SalesPersonCode": request.data['SalesPersonCode'],
        #     "BPL_IDAssignedToInvoice": request.data['BPLID'],
        #     "PaymentGroupCode":request.data['PaymentGroupCode'],
        #     "AddressExtension": {
        #         "BillToBuilding": addr['BillToBuilding'],
        #         "ShipToState": addr['ShipToState'],
        #         "BillToCity": addr['BillToCity'],
        #         "ShipToCountry": addr['ShipToCountry'],
        #         "BillToZipCode": addr['BillToZipCode'],
        #         "ShipToStreet": addr['ShipToStreet'],
        #         "BillToState": addr['BillToState'],
        #         "ShipToZipCode": addr['ShipToZipCode'],
        #         "BillToStreet": addr['BillToStreet'],
        #         "ShipToBuilding": addr['ShipToBuilding'],
        #         "ShipToCity": addr['ShipToCity'],
        #         "BillToCountry": addr['BillToCountry']
        #     },
        #     "DocumentLines": lines
        # }
        
        # print(qt_data)
        # print(json.dumps(qt_data))

        # print(settings.BASEURL+"/Quotations('"+model.DocEntry+"')");
        # res = requests.patch(settings.BASEURL+"/Quotations("+model.DocEntry+")", data=json.dumps(qt_data), cookies=r.cookies, verify=False)
        # print(res.content)

        # if len(res.content) !=0 :
        #     res1 = json.loads(res.content)
        #     SAP_MSG = res1['error']['message']['value']
        #     return Response({"message":SAP_MSG,"status":202,"SAP_error":SAP_MSG, "data":[request.data]})
        # else:
        #     return Response({"message":"successful","status":200, "data":[json.loads(json.dumps(request.data))]})
        
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[{"Error":str(e)}]})

#Quotation All API
@api_view(["GET"])
def all_old(request):
    quot_obj = Quotation.objects.all().order_by("-id")    
    quot_json = QuotationSerializer(quot_obj, many=True)
    return Response({"message": "Success","status": 200,"data":quot_json.data})

#Quotation All API
@api_view(["GET"])
def all(request):
    allqt = [];
    quot_obj = Quotation.objects.all().order_by("-id")    
    allqt = QuotationShow(quot_obj)    
    return Response({"message": "Success","status": 200,"data":allqt})

def QuotationShow(quot_obj):
    allqt = []
    for qt in quot_obj:
        qtobj = Quotation.objects.get(pk=qt.id)
        
        qt_json = QuotationSerializer(qtobj)
        
        quot = json.loads(json.dumps(qt_json.data))
        
        qtaddr = AddressExtension.objects.filter(QuotationID=qt.id)
        if len(qtaddr) > 0:
        
            qtaddr_json = AddressExtensionSerializer(qtaddr, many=True)
        
            quot["AddressExtension"]= qtaddr_json.data[0]
        else:
            quot["AddressExtension"]= {}
        
        lines = DocumentLines.objects.filter(QuotationID=qt.id)
        if len(lines) > 0:
            lines_json = DocumentLinesSerializer(lines, many=True)
        
            quot["DocumentLines"]= lines_json.data
        else:
            quot["DocumentLines"]= []

        cont = BPEmployee.objects.filter(InternalCode=qt.ContactPersonCode).values("InternalCode","FirstName")
        cont_json = BPEmployeeSerializer(cont, many=True)
        cont_all = json.loads(json.dumps(cont_json.data))
        
        # try:
        if qt.PaymentGroupCode != "":
            if PaymentTermsTypes.objects.filter(GroupNumber = qt.PaymentGroupCode).exists():
                payment_dls = PaymentTermsTypes.objects.filter(GroupNumber = qt.PaymentGroupCode)
                payment_dls_json = PaymentTermsTypesSerializer(payment_dls, many=True)
                quot['PaymentGroupCode'] = payment_dls_json.data
            else:
                quot['PaymentGroupCode'] = []
        else:
            quot['PaymentGroupCode'] = []        
        # except Exception as e:
        #     return Response({"message": str(e),"status": 201,"data":[]})

        # try:
        if Attachment.objects.filter(LinkID = qt.id, LinkType="Quotation").exists():
            Attach_dls = Attachment.objects.filter(LinkID = qt.id, LinkType="Quotation")
            Attach_json = AttachmentSerializer(Attach_dls, many=True)
            quot['Attach'] = Attach_json.data
        else:
            quot['Attach'] = []
        # except Exception as e:
        #     return Response({"message": str(e),"status": 201,"data":[]})        
        
        #added by millan on 12-September-2022
        # try:
        if qt.Project != "":
            if Project.objects.filter(id = qt.Project).exists():
                project_dls = Project.objects.filter(id = qt.Project)
                project_json = ProjectSerializer(project_dls, many=True)
                quot['Project'] = project_json.data
            else:
                quot['Project'] = []
        else:
            quot['Project'] = []        
        # except Exception as e:
        #     return Response({"message": str(e),"status": 201,"data":[]})        
        #added by millan on 12-September-2022
        
        #added by millan on 14-11-2022 for showing business partner email based on card code
        if qt.CardCode != "":
            if BusinessPartner.objects.filter(CardCode = qt.CardCode).exists():
                bpemail_dls = BusinessPartner.objects.filter(CardCode = qt.CardCode).values_list('EmailAddress',flat=True)
                quot['BPEmail'] = bpemail_dls[0]
            else:
                quot['BPEmail'] = []
        else:
            quot['BPEmail'] = []
        #added by millan on 14-11-2022 for showing business partner email based on card code
        
        if len(cont) > 0:
            #ContactPerson = cont[0].FirstName
            ContactPerson = cont_json.data
            print(ContactPerson)
        else:
            ContactPerson = []
            print(ContactPerson)

        sobj = Employee.objects.filter(SalesEmployeeCode=qt.SalesPersonCode).values("SalesEmployeeCode","SalesEmployeeName","lastName","Email","Mobile")
        sobj_json = EmployeeSerializer(sobj, many=True)
        sobj_all = json.loads(json.dumps(sobj_json.data))
        SalesPerson = sobj_json.data

        quot["ContactPersonCode"]= ContactPerson
        quot["SalesPersonCode"]= SalesPerson

        allqt.append(quot)
    return allqt

#Quotation All API
@api_view(["POST"])
def all_filter(request):
    json_data = request.data
    
    if "U_OPPID" in json_data:
        if json_data['U_OPPID'] !='':
            
            quot_obj = Quotation.objects.filter(U_OPPID=json_data['U_OPPID']).order_by("-id")
            if len(quot_obj) ==0:
                return Response({"message": "Success","status": 200,"data":[]})
            else:
                
                allqt = QuotationShow(quot_obj)
                        
            return Response({"message": "Success","status": 200,"data":allqt})
                
    
    if "SalesPersonCode" in json_data:
        print("yes")
        
        if json_data['SalesPersonCode']!="":
            SalesPersonID = json_data['SalesPersonCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesPersonID)
            
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
                
                #added by millan on 12-September-2022           
                elif ke =='Project' :
                    if json_data['Project'] !='':
                        opps_obj = Opportunity.objects.filter(SalesPerson__in=SalesPersonID, Project=json_data['Project']).order_by("-id")
                        if len(opps_obj) ==0:
                            return Response({"message": "Not Available","status": 201,"data":[]})
                        else:
                            allopp = []
                            for obj in opps_obj:
                                try:
                                    if Project.objects.filter(id = obj.ProjectCode).exists():
                                        project_dls = Project.objects.filter(id = obj.ProjectCode)
                                        project_json = ProjectSerializer(project_dls, many=True)
                                        quot_obj['ProjectCode'] = project_json.data
                                    else:
                                        quot_obj['ProjectCode'] = []
                                except Exception as e:
                                    return Response({"message": str(e),"status": 201,"data":[]})        
                                allqt.append(quot_obj)
                            #return Response({"message": "Success","status": 200,"data":allqt})
                #added by millan on 12-September-2022
                
                else:
                    print("no filter")
                    # qt = Quotation.objects.filter(SalesPersonCode__in=SalesPersonID).order_by("-id")
                    # quot_json = QuotationSerializer(quot_obj, many=True)
                    # return Response({"message": "Success","status": 200,"data":quot_json.data})
                    quot_obj = Quotation.objects.filter(SalesPersonCode__in=SalesPersonID).order_by("-id")
                    allqt = QuotationShow(quot_obj)
                        
                    return Response({"message": "Success","status": 200,"data":allqt})
                    
            
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})

#Quotation One API
@api_view(["POST"])
def one(request):
    try:
        id=request.data['id']
        quot_obj = Quotation.objects.filter(id=id)
        allqt = QuotationShow(quot_obj)
        return Response({"message": "Success","status": 200,"data":allqt})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

#Quotation Cancel
@api_view(['POST'])
def cancel(request):
    fetchid=request.data['DocEntry']
    try:
        odr=Quotation.objects.get(DocEntry=fetchid)
        odr.DocumentStatus='bost_Close'
        odr.CancelStatus='csYes'
        odr.FinalStatus='Cancel'
        odr.save()
        try:
            r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)
            res = requests.post(settings.BASEURL+'/Quotations('+fetchid+')/Cancel', cookies=r.cookies, verify=False)
            return Response({"message":"successful","status":200,"data":[]})
        except:
            return Response({"message":"successful","status":200,"data":[]})        
    except:
         return Response({"message":"Id wrong","status":201,"data":[]})
