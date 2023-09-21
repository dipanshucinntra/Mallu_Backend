from statistics import mode
from django.conf import settings
from django.shortcuts import render, redirect  
from django.db.models import Max
from django.http import JsonResponse, HttpResponse

from Project.models import Project
from Project.serializers import ProjectSerializer
from .models import *
from Employee.models import Employee
from Attachment.models import Attachment
from Attachment.serializers import AttachmentSerializer

import requests, json
import os
from django.core.files.storage import FileSystemStorage
from Lead.models import Lead
from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

from global_methods import *
# Create your views here.  

#Opportunity All API
@api_view(["GET"])
def all(request):
    
    opps_obj = Opportunity.objects.all().order_by("-id")
    #opps_json = OpportunitySerializer(opps_obj, many=True)
    #return Response({"message": "Success","status": 200,"data":opps_json.data})
    allopp = []
    for obj in opps_obj:
        opp_json = OpportunitySerializer(obj, many=False)
        opp_json_dump = json.loads(json.dumps(opp_json.data))
        items = OppItem.objects.filter(OppID = obj.id)
        item_json = OppItemSerializer(items, many=True)
        opp_json_dump['OppItem'] = item_json.data
        #added by millan on 12-September-2022
        try:
            if obj.ProjectCode != "":
                if Project.objects.filter(id = obj.ProjectCode).exists():
                    project_dls = Project.objects.filter(id = obj.ProjectCode)
                    project_json = ProjectSerializer(project_dls, many=True)
                    opp_json_dump['ProjectCode'] = project_json.data
                else:
                    opp_json_dump['ProjectCode'] = []
            else:
                opp_json_dump['ProjectCode'] = []
        except Exception as e:
            return Response({"message": str(e),"status": 201,"data":[]})        
        #added by millan on 12-September-2022
        allopp.append(opp_json_dump)
    return Response({"message": "Success","status": 200,"data":allopp})

#Opportunity All API
@api_view(["GET"])
def all_opp_old(request):
    opps_obj = Opportunity.objects.all().order_by("-id")
    opps_json = OppSerializer(opps_obj, many=True)
    return Response({"message": "Success","status": 200,"data":opps_json.data})

#Opportunity All API
@api_view(["POST"])
def all_opp(request):
    json_data = request.data
    
    if "SalesPerson" in json_data:
        print("yes")
        
        if json_data['SalesPerson']!="":
            SalesPersonID = json_data['SalesPerson']
            
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
                SalesPersonID = [json_data['SalesPerson']]
            
            print(SalesPersonID)
            
            opps_obj = Opportunity.objects.filter(SalesPerson__in=SalesPersonID).order_by("-id")
            opps_json = OppSerializer(opps_obj, many=True)
            return Response({"message": "Success","status": 200,"data":opps_json.data})
            
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPerson?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPerson?"}]})

#Opportunity All API
@api_view(["POST"])
def all_filter(request):
    json_data = request.data
    # print(json_data)
    # allopp = []
    if "SalesPerson" in json_data:
        # print("yes")
        
        if json_data['SalesPerson']!="":
            SalesPersonID = json_data['SalesPerson']
            
            if Employee.objects.filter(SalesEmployeeCode=SalesPersonID).exists(): # added by millan on 12-09-2022
                emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesPersonID)
                print(emp_obj)
                if emp_obj.role == 'manager' or emp_obj.role == "Sales Manager":
                    emps = Employee.objects.filter(reportingTo=SalesPersonID)#.values('id', 'SalesEmployeeCode')
                    SalesPersonID=[SalesPersonID]
                    for emp in emps:
                        SalesPersonID.append(emp.SalesEmployeeCode)
                    
                elif emp_obj.role == 'admin' or emp_obj.role == 'ceo' or emp_obj.role == 'Service Head' or emp_obj.role == "marketing" or emp_obj.role == "HO":
                    emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                    SalesPersonID=[]
                    for emp in emps:
                        SalesPersonID.append(emp.SalesEmployeeCode)
                else:
                    # SalesPersonID = [json_data['SalesPerson']]
                    SalesPersonID = showEmployeeData(json_data['SalesPerson'])
                
                # print(SalesPersonID)
            else:
                return Response({"message": "Sales Employee Code Not Found","status": 201,"data":[]})
            
            for ke in json_data.keys():
                print(ke)
                if ke =='U_FAV' :
                    if json_data['U_FAV'] !='':
                        opps_obj = Opportunity.objects.filter(SalesPerson__in=SalesPersonID, U_FAV=json_data['U_FAV']).order_by("-id")
                        if len(opps_obj) ==0:
                            return Response({"message": "Not Available","status": 201,"data":[]})
                        else:
                            allopp = []
                            for obj in opps_obj:
                                opp_json = OpportunitySerializer(obj, many=False)
                                opp_json_dump = json.loads(json.dumps(opp_json.data))
                                items = OppItem.objects.filter(OppID = obj.id)
                                item_json = OppItemSerializer(items, many=True)
                                opp_json_dump['OppItem'] = item_json.data
                                try:
                                    if obj.ProjectCode!= "":
                                        project_dls = Project.objects.filter(id = obj.ProjectCode)
                                        project_json = ProjectSerializer(project_dls, many=True)
                                        opp_json_dump['ProjectCode'] = project_json.data
                                    else:
                                        opp_json_dump['ProjectCode'] = []
                                except Exception as e:
                                    return Response({"message": str(e),"status": 201,"data":[]})
                                
                                try:
                                    if Attachment.objects.filter(LinkID = obj.id, LinkType="Opportunity").exists():
                                        attachment_dls = Attachment.objects.filter(LinkID = obj.id, LinkType="Opportunity")
                                        attachment_json = AttachmentSerializer(attachment_dls, many=True)
                                        opp_json_dump['Attach'] = attachment_json.data
                                    else:
                                        opp_json_dump['Attach'] = []
                                except Exception as e:
                                    return Response({"message": str(e),"status": 201,"data":[]})
                                allopp.append(opp_json_dump)
                            return Response({"message": "Success","status": 200,"data":allopp})
                            #opps_json = OpportunitySerializer(opps_obj, many=True)
                            #return Response({"message": "Success","status": 200,"data":opps_json.data})
                elif ke =='U_TYPE' :
                    if json_data['U_TYPE'] !='':
                        opps_obj = Opportunity.objects.filter(SalesPerson__in=SalesPersonID, U_TYPE=json_data['U_TYPE']).order_by("-id")
                        if len(opps_obj) ==0:
                            return Response({"message": "Not Available","status": 201,"data":[]})
                        else:
                            allopp = []
                            for obj in opps_obj:
                                opp_json = OpportunitySerializer(obj, many=False)
                                opp_json_dump = json.loads(json.dumps(opp_json.data))
                                items = OppItem.objects.filter(OppID = obj.id)
                                item_json = OppItemSerializer(items, many=True)
                                opp_json_dump['OppItem'] = item_json.data
                                try:
                                    if obj.ProjectCode!= "":
                                        project_dls = Project.objects.filter(id = obj.ProjectCode)
                                        project_json = ProjectSerializer(project_dls, many=True)
                                        opp_json_dump['ProjectCode'] = project_json.data
                                    else:
                                        opp_json_dump['ProjectCode'] = []
                                except Exception as e:
                                    return Response({"message": str(e),"status": 201,"data":[]})
                                
                                try:
                                    if Attachment.objects.filter(LinkID = obj.id, LinkType="Opportunity").exists():
                                        attachment_dls = Attachment.objects.filter(LinkID = obj.id, LinkType="Opportunity")
                                        attachment_json = AttachmentSerializer(attachment_dls, many=True)
                                        opp_json_dump['Attach'] = attachment_json.data
                                    else:
                                        opp_json_dump['Attach'] = []
                                except Exception as e:
                                    return Response({"message": str(e),"status": 201,"data":[]})
                                allopp.append(opp_json_dump)
                            return Response({"message": "Success","status": 200,"data":allopp})
                            #opps_json = OpportunitySerializer(opps_obj, many=True)
                            #return Response({"message": "Success","status": 200,"data":opps_json.data})
                elif ke =='Status' :
                    if json_data['Status'] !='':
                        opps_obj = Opportunity.objects.filter(SalesPerson__in=SalesPersonID, Status=json_data['Status']).order_by("-id")
                        if len(opps_obj) ==0:
                            return Response({"message": "Not Available","status": 201,"data":[]})
                        else:
                            allopp = []
                            for obj in opps_obj:
                                opp_json = OpportunitySerializer(obj, many=False)
                                opp_json_dump = json.loads(json.dumps(opp_json.data))
                                items = OppItem.objects.filter(OppID = obj.id)
                                item_json = OppItemSerializer(items, many=True)
                                opp_json_dump['OppItem'] = item_json.data
                                try:
                                    if obj.ProjectCode!= "":
                                        project_dls = Project.objects.filter(id = obj.ProjectCode)
                                        project_json = ProjectSerializer(project_dls, many=True)
                                        opp_json_dump['ProjectCode'] = project_json.data
                                    else:
                                        opp_json_dump['ProjectCode'] = []
                                except Exception as e:
                                    return Response({"message": str(e),"status": 201,"data":[]})
                                
                                try:
                                    if Attachment.objects.filter(LinkID = obj.id, LinkType="Opportunity").exists():
                                        attachment_dls = Attachment.objects.filter(LinkID = obj.id, LinkType="Opportunity")
                                        attachment_json = AttachmentSerializer(attachment_dls, many=True)
                                        opp_json_dump['Attach'] = attachment_json.data
                                    else:
                                        opp_json_dump['Attach'] = []
                                except Exception as e:
                                    return Response({"message": str(e),"status": 201,"data":[]})
                                allopp.append(opp_json_dump)
                            return Response({"message": "Success","status": 200,"data":allopp})
                            #opps_json = OpportunitySerializer(opps_obj, many=True)
                            #return Response({"message": "Success","status": 200,"data":opps_json.data})
                else:
                    print("no filter")
                    opps_obj = Opportunity.objects.filter(SalesPerson__in=SalesPersonID).order_by("-id")
                    allopp = []
                    for obj in opps_obj:
                        opp_json = OpportunitySerializer(obj, many=False)
                        opp_json_dump = json.loads(json.dumps(opp_json.data))
                        items = OppItem.objects.filter(OppID = obj.id)
                        item_json = OppItemSerializer(items, many=True)
                        opp_json_dump['OppItem'] = item_json.data
                        #added by millan on 12-September-2022
                        try:
                            if obj.ProjectCode!= "":
                                project_dls = Project.objects.filter(id = obj.ProjectCode)
                                project_json = ProjectSerializer(project_dls, many=True)
                                opp_json_dump['ProjectCode'] = project_json.data
                            else:
                                opp_json_dump['ProjectCode'] = []
                        except Exception as e:
                            return Response({"message": str(e),"status": 201,"data":[]})
                        
                        try:
                            if Attachment.objects.filter(LinkID = obj.id, LinkType="Opportunity").exists():
                                attachment_dls = Attachment.objects.filter(LinkID = obj.id, LinkType="Opportunity")
                                attachment_json = AttachmentSerializer(attachment_dls, many=True)
                                opp_json_dump['Attach'] = attachment_json.data
                            else:
                                opp_json_dump['Attach'] = []
                        except Exception as e:
                            return Response({"message": str(e),"status": 201,"data":[]})        
                        #added by millan on 12-September-2022
                        allopp.append(opp_json_dump)
                    return Response({"message": "Success","status": 200,"data":allopp})
                    #opps_json = OpportunitySerializer(opps_obj, many=True)
                    #return Response({"message": "Success","status": 200,"data":opps_json.data})
            
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPerson?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPerson?"}]})



#Opportunity All API
@api_view(["POST"])
def all_filter_page(request):
    json_data = request.data
    # print(json_data)
    # allopp = []
    PageNo = json_data['PageNo']
    search = json_data['SearchText']
    try:
        MaxItem = json_data['MaxItem']
    except:
        MaxItem = 10
    endWith = (PageNo * MaxItem)
    startWith = (endWith - MaxItem)
    if "SalesPerson" in json_data:
        # print("yes")
        
        if json_data['SalesPerson']!="":
            SalesPersonID = json_data['SalesPerson']
            
            if Employee.objects.filter(SalesEmployeeCode=SalesPersonID).exists(): # added by millan on 12-09-2022
                emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesPersonID)
                print(emp_obj)
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
                    SalesPersonID = [json_data['SalesPerson']]
                
                # print(SalesPersonID)
            else:
                return Response({"message": "Sales Employee Code Not Found","status": 201,"data":[]})
            
            opps_obj = Opportunity.objects.filter(SalesPerson__in=SalesPersonID, OpportunityName__icontains=search).order_by("-id")[startWith:endWith]
            allopp = []
            for obj in opps_obj:
                opp_json = OpportunitySerializer(obj, many=False)
                opp_json_dump = json.loads(json.dumps(opp_json.data))
                items = OppItem.objects.filter(OppID = obj.id)
                item_json = OppItemSerializer(items, many=True)
                opp_json_dump['OppItem'] = item_json.data
                #added by millan on 12-September-2022
                try:
                    if obj.ProjectCode!= "":
                        project_dls = Project.objects.filter(id = obj.ProjectCode)
                        project_json = ProjectSerializer(project_dls, many=True)
                        opp_json_dump['ProjectCode'] = project_json.data
                    else:
                        opp_json_dump['ProjectCode'] = []
                except Exception as e:
                    return Response({"message": str(e),"status": 201,"data":[]})
                
                try:
                    if Attachment.objects.filter(LinkID = obj.id, LinkType="Opportunity").exists():
                        attachment_dls = Attachment.objects.filter(LinkID = obj.id, LinkType="Opportunity")
                        attachment_json = AttachmentSerializer(attachment_dls, many=True)
                        opp_json_dump['Attach'] = attachment_json.data
                    else:
                        opp_json_dump['Attach'] = []
                except Exception as e:
                    return Response({"message": str(e),"status": 201,"data":[]})        
                #added by millan on 12-September-2022
                allopp.append(opp_json_dump)
            return Response({"message": "Success","status": 200,"data":allopp})
            
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPerson?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPerson?"}]})


#Opportunity All API
@api_view(["POST"])
def count_all(request):
    json_data = request.data
    search = json_data['SearchText']
    if "SalesPerson" in json_data:
        if json_data['SalesPerson']!="":
            SalesPersonID = json_data['SalesPerson']
            if Employee.objects.filter(SalesEmployeeCode=SalesPersonID).exists(): # added by millan on 12-09-2022
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
                    SalesPersonID = [json_data['SalesPerson']]
            else:
                return Response({"message": "Sales Employee Code Not Found","status": 201,"data":[]})
            opps_obj = Opportunity.objects.filter(SalesPerson__in=SalesPersonID, OpportunityName__icontains=search).count()
            return Response({"message": "Success","status": 200,"data":[{"total_count":opps_obj}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPerson?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPerson?"}]})

"""
{
 "U_FAV":"",
 "U_TYPE":"Existing Business", 
 "Status":""
}
"""            

#Opportunity One API
@api_view(["POST"])
def one(request):
    try:
        id=request.data['id']    
        opp_obj = Opportunity.objects.get(id=id)
        opp_json = OpportunitySerializer(opp_obj, many=False)
        opp_json_dump = json.loads(json.dumps(opp_json.data))
        items = OppItem.objects.filter(OppID = opp_obj.id)
        item_json = OppItemSerializer(items, many=True)
        opp_json_dump['OppItem'] = item_json.data
        
        #added by millan on 12-September-2022
        try:
            if opp_obj.ProjectCode == "":
                opp_json_dump['ProjectCode'] = []
            elif Project.objects.filter(id = opp_obj.ProjectCode).exists():
                project_dls = Project.objects.filter(id = opp_obj.ProjectCode)
                project_json = ProjectSerializer(project_dls, many=True)
                opp_json_dump['ProjectCode'] = project_json.data
            else:
                opp_json_dump['ProjectCode'] = []
        except Exception as e:
            return Response({"message": str(e),"status": 201,"data":[]})  
        try:
            if Attachment.objects.filter(LinkID = opp_obj.id, LinkType="Opportunity").exists():
                attachment_dls = Attachment.objects.filter(LinkID = opp_obj.id, LinkType="Opportunity")
                attachment_json = AttachmentSerializer(attachment_dls, many=True)
                opp_json_dump['Attach'] = attachment_json.data
            else:
                opp_json_dump['Attach'] = []
        except Exception as e:
            return Response({"message": str(e),"status": 201,"data":[]})
        #added by millan on 12-September-2022
        return Response({"message": "Success","status": 200,"data":[opp_json_dump]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]}) 

#Opportunity Create API
@api_view(['POST'])
def create(request):
    try:
        CardCode = request.data['CardCode']
        SalesPerson = request.data['SalesPerson']
        SalesPersonName = request.data['SalesPersonName']
        ContactPerson = request.data['ContactPerson']
        ContactPersonName = request.data['ContactPersonName']
        Source = request.data['Source']
        StartDate = request.data['StartDate']
        PredictedClosingDate = request.data['PredictedClosingDate']
        MaxLocalTotal = request.data['MaxLocalTotal']
        MaxSystemTotal = request.data['MaxSystemTotal']
        Remarks = request.data['Remarks']
        
        Status = request.data['Status']
        ReasonForClosing = request.data['ReasonForClosing']
        TotalAmountLocal = request.data['TotalAmountLocal']
        TotalAmounSystem = request.data['TotalAmounSystem']
        
        stg = StaticStage.objects.all().order_by("SequenceNo")[:1]
        
        cur = stg[0].SequenceNo
        cur_num = stg[0].Stageno
        cur_name = stg[0].Name

        CurrentStageNo = cur
        CurrentStageNumber = cur_num
        CurrentStageName = cur_name
        
        OpportunityName = request.data['OpportunityName']
        Industry = request.data['Industry']
        LinkedDocumentType = request.data['LinkedDocumentType']
        DataOwnershipfield = request.data['DataOwnershipfield']
        DataOwnershipName = request.data['DataOwnershipName']
        StatusRemarks = request.data['StatusRemarks']
        ProjectCode = request.data['ProjectCode']
        CustomerName = request.data['CustomerName']
        ClosingDate = request.data['ClosingDate']
        ClosingType = request.data['ClosingType']
        OpportunityType = request.data['OpportunityType']
        UpdateDate = request.data['UpdateDate']
        UpdateTime = request.data['UpdateTime']
        U_TYPE = request.data['U_TYPE']
        U_LSOURCE = request.data['U_LSOURCE']
        U_FAV = request.data['U_FAV']
        U_PROBLTY = request.data['U_PROBLTY']
        U_LEADID = request.data['U_LEADID']
        U_LEADNM = request.data['U_LEADNM']
        
        OppType = request.data['OppType']
        DivCode = request.data['DivCode']
        DivName = request.data['DivName']
        Caption = request.data['Caption']
        SolutionType = request.data['SolutionType']
        try:
            model = Opportunity(SolutionType=SolutionType, OPStatus="Cold", CardCode=CardCode, SalesPerson=SalesPerson, SalesPersonName=SalesPersonName, ContactPerson=ContactPerson, ContactPersonName=ContactPersonName, Source=Source, StartDate=StartDate, PredictedClosingDate=PredictedClosingDate, MaxLocalTotal=MaxLocalTotal, MaxSystemTotal=MaxSystemTotal, Remarks=Remarks, Status=Status, ReasonForClosing=ReasonForClosing, TotalAmountLocal=TotalAmountLocal, TotalAmounSystem=TotalAmounSystem, CurrentStageNo=CurrentStageNo, CurrentStageNumber=CurrentStageNumber, CurrentStageName=CurrentStageName, OpportunityName=OpportunityName, Industry=Industry, LinkedDocumentType=LinkedDocumentType, DataOwnershipfield=DataOwnershipfield, DataOwnershipName=DataOwnershipName, StatusRemarks=StatusRemarks, ProjectCode=ProjectCode, CustomerName=CustomerName, ClosingDate=ClosingDate, ClosingType=ClosingType, OpportunityType=OpportunityType, UpdateDate=UpdateDate, UpdateTime=UpdateTime, U_TYPE=U_TYPE, U_LSOURCE=U_LSOURCE, U_FAV=U_FAV, U_PROBLTY=U_PROBLTY, U_LEADID=U_LEADID, U_LEADNM=U_LEADNM, BPStatus="1", OppType=OppType, DivCode=DivCode, DivName=DivName)

            model.save()
        
            Opp = Opportunity.objects.latest('id')
            print(Opp.id)
            OppID = Opp.id

            print(request.FILES.getlist('Attach'))
            for File in request.FILES.getlist('Attach'):
                attachmentsImage_url = ""
                target ='./bridge/static/image/Attachment'
                os.makedirs(target, exist_ok=True)
                fss = FileSystemStorage()
                file = fss.save(target+"/"+File.name, File)
                productImage_url = fss.url(file)
                attachmentsImage_url = productImage_url.replace('/bridge/', '/')
                print(attachmentsImage_url)
                
                FileName = File.name #added by millan on 17-10-2022 for storing file name

                att=Attachment(File=attachmentsImage_url, LinkType="Opportunity", Caption=Caption, LinkID=OppID, CreateDate=UpdateDate, CreateTime=UpdateTime, UpdateDate=UpdateDate, UpdateTime=UpdateTime, FileName = FileName)
                
                att.save()

        except Exception as e:
            return Response({"message":str(e),"status":201,"data":[]})
        
        if len(json.loads(request.data['OppItem'])) != 0:
            lines = json.loads(request.data['OppItem'])
            LineNum = 0
            for line in lines:
                try:
                    model_lines = OppItem(LineNum = LineNum, OppID = OppID, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'], U_FGITEM = line['U_FGITEM'], CostingCode2 = line['CostingCode2'], ProjectCode = line['ProjectCode'], FreeText = line['FreeText'], Tax = line['Tax'], UomNo = line['UomNo'], Item_uqc=line['Item_uqc']) 
                    model_lines.save()
                    LineNum=LineNum+1
                except Exception as e:
                    Opportunity.objects.filter(pk=OppID).delete()
                    oppItems = OppItem.objects.filter(OppID=OppID)
                    for item in oppItems:
                        item.delete()                           
                    return Response({"message":str(e),"status":"202","data":[]})
        try:
            OppLine = json.loads(request.data['SalesOpportunitiesLines'])
            LineNum = "0"
            SalesPerson = OppLine[0]['SalesPerson']
            ContactPerson = request.data['ContactPerson']
            StartDate = request.data['StartDate']
            MaxLocalTotal = OppLine[0]['MaxLocalTotal']
            MaxSystemTotal = OppLine[0]['MaxSystemTotal']
            Remarks = request.data['Remarks']
            Contact="tNO"
            Status = "so_Open"
            StageKey = cur
            ClosingDate = request.data['ClosingDate']
            #SequenceNo = request.data['SequentialNo']
            Opp_Id = Opp.id
            
            model_line = Line(LineNum=LineNum, SalesPerson=SalesPerson, StartDate=StartDate, StageKey=StageKey, MaxLocalTotal=MaxLocalTotal, MaxSystemTotal=MaxSystemTotal, Remarks=Remarks, Contact=Contact, Status=Status, ContactPerson=ContactPerson, ClosingDate=ClosingDate,Opp_Id=Opp_Id)    
            
            model_line.save()    
        except Exception as e:
            Line.objects.filter(Opp_Id=OppID).delete()
            Opportunity.objects.filter(pk=OppID).delete()
            return Response({"message":str(e),"status":201,"data":[]})
        
        # add all static stages with this Opp
        try:
            staticstage = StaticStage.objects.filter(UTYPE=U_TYPE).order_by("Stageno")
            for ststage in staticstage:
                SequenceNo = ststage.SequenceNo
                Name = ststage.Name
                Stageno = ststage.Stageno
                ClosingPercentage = ststage.ClosingPercentage
                Cancelled = ststage.Cancelled
                IsSales = ststage.IsSales
                IsPurchasing = ststage.IsPurchasing
                Opp_Id = Opp_Id
                CreateDate = StartDate
                UpdateDate = ""
                if(ststage.Stageno == 1):
                    Status = 1
                    UpdateDate = CreateDate
                else:
                    Status = 0
                model = Stage(SequenceNo=SequenceNo, Name=Name, Stageno=Stageno, ClosingPercentage=ClosingPercentage, Cancelled=Cancelled, IsSales=IsSales, IsPurchasing=IsPurchasing, Opp_Id=Opp_Id, Status=Status, CreateDate=CreateDate, UpdateDate=UpdateDate)
                model.save()
        except Exception as e:
            Stage.objects.filter(Opp_Id=OppID).delete()
            Line.objects.filter(Opp_Id=OppID).delete()
            Opportunity.objects.filter(pk=OppID).delete()
            return Response({"message":str(e),"status":201,"data":[]})
            
        if settings.SAPOPP == True:
            r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
            print(r.text)
            token = json.loads(r.text)['SessionId']
            print(token)
            
            opp_data = {
            "CardCode": request.data['CardCode'],
            "PredictedClosingDate": request.data['PredictedClosingDate'],
            "ContactPerson": request.data['ContactPerson'],
            "DataOwnershipfield": request.data['DataOwnershipfield'],
            "MaxLocalTotal": request.data['MaxLocalTotal'],
            "MaxSystemTotal": request.data['MaxSystemTotal'],
            "CurrentStageNumber":cur_num,
            "Remarks": request.data['Remarks'],
            "SalesOpportunitiesLines": [
                {
                "DocumentType": "bodt_MinusOne",
                "MaxLocalTotal": OppLine[0]['MaxLocalTotal'],
                "MaxSystemTotal": OppLine[0]['MaxSystemTotal'],
                "SalesPerson": OppLine[0]['SalesPerson'],
                "StageKey": cur
                }
            ],
            "SalesPerson": request.data['SalesPerson'],
            "StartDate": request.data['StartDate'],
            "OpportunityName": request.data['OpportunityName']
            }
            #print(opp_data)
            
            res = requests.post(settings.BASEURL+'/SalesOpportunities', data=json.dumps(opp_data), cookies=r.cookies, verify=False)
            #print(res.text);
            live = json.loads(res.text)
            
            if "SequentialNo" in live:
                print(live['SequentialNo'])
                
                fetchid = Opp.id
                model = Opportunity.objects.get(pk = fetchid)
                model.SequentialNo = live['SequentialNo']
                model.save()
                
                model = Line.objects.get(LineNum = 0, Opp_Id=Opp.id)
                model.SequenceNo = live['SequentialNo']
                model.save()
                if int(U_LEADID) !=0:
                    leadObj = Lead.objects.get(pk=U_LEADID)
                    leadObj.OPStatus=1
                    leadObj.save()
                return Response({"message":"successful","status":200,"data":[{"Opp_Id":Opp.id, "SequentialNo":live['SequentialNo']}]})
            else:
                Opportunity.objects.get(pk=Opp.id).delete()
                Line.objects.get(Opp_Id=Opp.id).delete()
                allstg = Stage.objects.filter(Opp_Id=Opp.id)
                for stg in allstg:
                    stg.delete()
                
                print(live['error']['message']['value'])
                SAP_MSG = live['error']['message']['value']
                return Response({"message":SAP_MSG,"SAP_error":SAP_MSG, "status":202,"data":[]})
        else:
            fetchid = Opp.id
            model = Opportunity.objects.get(pk = fetchid)
            model.SequentialNo = fetchid
            model.save()
            
            model = Line.objects.get(LineNum = 0, Opp_Id=Opp.id)
            model.SequenceNo = fetchid
            model.save()
            if int(U_LEADID) !=0:
                leadObj = Lead.objects.get(pk=U_LEADID)
                leadObj.OPStatus=1
                leadObj.save()
            return Response({"message":"successful","status":200,"data":[{"Opp_Id":Opp.id, "SequentialNo":fetchid}]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})
    
#Opportunity Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Opportunity.objects.get(pk = fetchid)
        
        model.SequentialNo = request.data['SequentialNo']
        model.CardCode = request.data['CardCode']
        model.SalesPerson = request.data['SalesPerson']
        model.SalesPersonName = request.data['SalesPersonName']
        model.ContactPerson = request.data['ContactPerson']
        model.ContactPersonName = request.data['ContactPersonName']
        model.Source = request.data['Source']
        model.StartDate = request.data['StartDate']
        model.PredictedClosingDate = request.data['PredictedClosingDate']
        model.MaxLocalTotal = request.data['MaxLocalTotal']
        model.MaxSystemTotal = request.data['MaxSystemTotal']
        model.Remarks = request.data['Remarks']
        model.Status = request.data['Status']
        model.ReasonForClosing = request.data['ReasonForClosing']
        model.TotalAmountLocal = request.data['TotalAmountLocal']
        model.TotalAmounSystem = request.data['TotalAmounSystem']
        #model.CurrentStageNo = request.data['CurrentStageNo']
        model.CurrentStageNo = model.CurrentStageNo
        model.CurrentStageNumber = model.CurrentStageNumber
        model.CurrentStageName = model.CurrentStageName
        model.OpportunityName = request.data['OpportunityName']
        model.Industry = request.data['Industry']
        model.LinkedDocumentType = request.data['LinkedDocumentType']
        model.DataOwnershipfield = request.data['DataOwnershipfield']
        model.DataOwnershipName = request.data['DataOwnershipName']
        model.StatusRemarks = request.data['StatusRemarks']
        model.ProjectCode = request.data['ProjectCode']
        model.CustomerName = request.data['CustomerName']
        model.ClosingDate = request.data['ClosingDate']
        model.ClosingType = request.data['ClosingType']
        model.OpportunityType = request.data['OpportunityType']
        model.OppType = request.data['OppType']
        model.DivCode = request.data['DivCode']
        model.DivName = request.data['DivName']
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']
        model.U_TYPE = request.data['U_TYPE']
        model.U_LSOURCE = request.data['U_LSOURCE']
        model.U_FAV = request.data['U_FAV']
        model.U_PROBLTY = request.data['U_PROBLTY']
        model.SolutionType = request.data['SolutionType']

        model.save()
        
        # update by abhishek
        updatedItemIds = []
        if len(request.data['OppItem']) != 0:
            lines = request.data['OppItem']
            for line in lines:
                try:
                    if line["id"] !="":
                    # if "id" in line:
                        print("OppItem Update")
                        itmObj = OppItem.objects.get(pk=line['id'])
                        itmObj.Quantity = line['Quantity']
                        itmObj.UnitPrice = line['UnitPrice']
                        itmObj.DiscountPercent = line['DiscountPercent']
                        itmObj.ItemCode = line['ItemCode']
                        itmObj.ItemDescription = line['ItemDescription']
                        itmObj.TaxCode = line['TaxCode']
                        itmObj.U_FGITEM = line['U_FGITEM']
                        itmObj.CostingCode2 = line['CostingCode2']
                        itmObj.ProjectCode = line['ProjectCode']
                        itmObj.FreeText = line['FreeText']
                        itmObj.Tax = line['Tax']
                        itmObj.UomNo = line['UomNo']
                        itmObj.Item_uqc = line['Item_uqc']
                        itmObj.OppID = fetchid
                        itmObj.save()

                        updatedItemIds.append(line['id'])
                    else:
                        print("OppItem create")
                        LineNum = 0;
                        if OppItem.objects.filter(OppID = fetchid).exists():
                            lastline = OppItem.objects.filter(OppID = fetchid).order_by('-LineNum')[:1]
                            LineNum = int(lastline[0].LineNum) + 1
                        
                        model_lines = OppItem(LineNum = LineNum, OppID = fetchid, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'], U_FGITEM = line['U_FGITEM'], CostingCode2 = line['CostingCode2'], ProjectCode = line['ProjectCode'], FreeText = line['FreeText'], Tax = line['Tax'], UomNo = line['UomNo'],Item_uqc=line['Item_uqc']) #added by millan on 03-November-2022
                        model_lines.save()
                        oppObj = OppItem.objects.latest('id')
                        updatedItemIds.append(oppObj.id)

                except Exception as e:
                    print("Error: "+str(e))
        
        # if len(updatedItemIds) != 0:
        #     print("Item List")
            print(updatedItemIds)
        if OppItem.objects.filter(OppID = fetchid).exclude(id__in = updatedItemIds).exists():
            OppItem.objects.filter(OppID = fetchid).exclude(id__in = updatedItemIds).delete()
            print('delete old itme')
        # update by abhishek

        #print(model)
        #SELECT * FROM `opportunity_line` WHERE `SequenceNo`=5 and StageKey=2 order by LineNum desc limit 1;
        #SELECT * FROM `opportunity_line` WHERE `SequenceNo`=5 order by LineNum desc limit 1;
        
        # get object
        #line = Line.objects.filter(SequenceNo = request.data['SequentialNo']).order_by('-LineNum')[:1] 
        
        try:
            line = Line.objects.filter(SequenceNo = request.data['SequentialNo']).order_by('-LineNum')[:1]
            NewLine = int(line[0].LineNum) + 1
            print(NewLine)
        except:
            NewLine=0
            print(NewLine)
        
        LineNum = NewLine
        SalesPerson = request.data['SalesOpportunitiesLines'][0]['SalesPerson']
        ContactPerson = request.data['ContactPerson']
        StartDate = request.data['StartDate']
        MaxLocalTotal = request.data['SalesOpportunitiesLines'][0]['MaxLocalTotal']
        MaxSystemTotal = request.data['SalesOpportunitiesLines'][0]['MaxSystemTotal']
        Remarks = request.data['Remarks']
        Contact="tNO"
        Status = request.data['Status']
        #StageKey = request.data['SalesOpportunitiesLines'][0]['StageKey']
        StageKey = model.CurrentStageNo
        ClosingDate = request.data['ClosingDate']
        SequenceNo = request.data['SequentialNo']
        Opp_Id = fetchid
        
        model_line = Line(LineNum=LineNum, SalesPerson=SalesPerson, StartDate=StartDate, StageKey=StageKey, MaxLocalTotal=MaxLocalTotal, MaxSystemTotal=MaxSystemTotal, Remarks=Remarks, Contact=Contact, Status=Status, ContactPerson=ContactPerson, ClosingDate=ClosingDate,Opp_Id=Opp_Id)    
        
        model_line.save()  
                    
        if settings.SAPOPP == True:
            r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)
            
            opp_data = {
            "CardCode": request.data['CardCode'],
            "PredictedClosingDate": request.data['PredictedClosingDate'],
            "ContactPerson": request.data['ContactPerson'],
            "DataOwnershipfield": request.data['DataOwnershipfield'],
            "MaxLocalTotal": request.data['MaxLocalTotal'],
            "MaxSystemTotal": request.data['MaxSystemTotal'],
            "Remarks": request.data['Remarks'],
            """ "SalesOpportunitiesLines": [
                {
                "DocumentType": "bodt_MinusOne",
                "MaxLocalTotal": request.data['SalesOpportunitiesLines'][0]['MaxLocalTotal'],
                "MaxSystemTotal": request.data['SalesOpportunitiesLines'][0]['MaxSystemTotal'],
                "SalesPerson": request.data['SalesOpportunitiesLines'][0]['SalesPerson'],
                #"StageKey": request.data['SalesOpportunitiesLines'][0]['StageKey']
                "StageKey": model.CurrentStageNo
                }
            ],"""
            "SalesPerson": request.data['SalesPerson'],
            "StartDate": request.data['StartDate'],
            #"U_TYPE": request.data['U_TYPE'],
            "OpportunityName": request.data['OpportunityName']
            }
            
            print(json.dumps(opp_data))
        
            print(settings.BASEURL+'/SalesOpportunities('+request.data['SequentialNo']+')');
            
            res = requests.patch(settings.BASEURL+'/SalesOpportunities('+request.data['SequentialNo']+')', data=json.dumps(opp_data), cookies=r.cookies, verify=False)


            context = {
                'id':request.data['id'],
                'SequentialNo':request.data['SequentialNo'],
                'CardCode':request.data['CardCode'],
                'SalesPerson':request.data['SalesPerson'],
                'SalesPersonName':request.data['SalesPersonName'],
                'ContactPerson':request.data['ContactPerson'],
                'ContactPersonName':request.data['ContactPersonName'],
                "DataOwnershipfield": request.data['DataOwnershipfield'],
                "DataOwnershipName": request.data['DataOwnershipName'],
                'Source':request.data['Source'],
                'StartDate':request.data['StartDate'],
                'PredictedClosingDate':request.data['PredictedClosingDate'],
                'MaxLocalTotal':request.data['MaxLocalTotal'],
                'MaxSystemTotal':request.data['MaxSystemTotal'],
                'Remarks':request.data['Remarks'],
                'Status':request.data['Status'],
                'ReasonForClosing':request.data['ReasonForClosing'],
                'TotalAmountLocal':request.data['TotalAmountLocal'],
                'TotalAmounSystem':request.data['TotalAmounSystem'],
                'CurrentStageNo':model.CurrentStageNo,
                'CurrentStageNumber':model.CurrentStageNumber,
                'CurrentStageName':model.CurrentStageName,
                'OpportunityName':request.data['OpportunityName'],
                'Industry':request.data['Industry'],
                'LinkedDocumentType':request.data['LinkedDocumentType'],
                'StatusRemarks':request.data['StatusRemarks'],
                'ProjectCode':request.data['ProjectCode'],
                'CustomerName':request.data['CustomerName'],
                'ClosingDate':request.data['ClosingDate'],
                'ClosingType':request.data['ClosingType'],
                'OpportunityType':request.data['OpportunityType'],
                'UpdateDate':request.data['UpdateDate'],
                'UpdateTime':request.data['UpdateTime'],
                'U_TYPE':request.data['U_TYPE'],
                'U_LSOURCE':request.data['U_LSOURCE'],
                'U_FAV':request.data['U_FAV'],
                'U_PROBLTY':request.data['U_PROBLTY']
            }

            if len(res.content) !=0 :
                res1 = json.loads(res.content)
                SAP_MSG = res1['error']['message']['value']
                return Response({"message":SAP_MSG,"status":202,"SAP_error":SAP_MSG, "data":[context]})
            else:
                return Response({"message":"successful","status":200, "data":[context]})
        else:
            return Response({"message":"successful","status":200, "data":[]})
    except Exception as e:
        #print(e)
        return Response({"message":str(e),"status":201,"data":[{"Error":str(e)}]})

#Stage Create API
@api_view(['POST'])
def create_stage(request):

    chk = Stage.objects.filter(Opp_Id = request.data['Opp_Id'], Stageno = request.data['Stageno'])
    if chk[0].Status==2:
        return Response({"message":"Can not create due to CurrentStage already completed","status":201,"data":[]})

    SequenceNo = request.data['SequenceNo']
    Name = request.data['Name']
    Stageno = round(float(request.data['Stageno']) + float(.1),1)
    ClosingPercentage = request.data['ClosingPercentage']
    Cancelled = request.data['Cancelled']
    IsSales = request.data['IsSales']
    IsPurchasing = request.data['IsPurchasing']
    Opp_Id = request.data['Opp_Id']
    CreateDate = request.data['CreateDate']
    UpdateDate = request.data['UpdateDate']

    print(Stageno)
    model = Stage(SequenceNo=SequenceNo, Name=Name, Stageno=Stageno, ClosingPercentage=ClosingPercentage, Cancelled=Cancelled, IsSales=IsSales, IsPurchasing=IsPurchasing, Opp_Id=Opp_Id, CreateDate=CreateDate, UpdateDate=UpdateDate)
    model.save()
    return Response({"message":"successful","status":200,"data":[]})

#Stage All API
@api_view(["POST"])
def all_stage(request):
    Opp_Id=request.data['Opp_Id']    
    stages_obj = Stage.objects.filter(Opp_Id=Opp_Id).order_by("Stageno")        
    stages_json = StageSerializer(stages_obj, many=True)
    return Response({"message": "Success","status": 200,"data":stages_json.data})

#Stage One API
@api_view(["POST"])
def one_stage(request):
    SequenceNo=request.data['SequenceNo']    
    stage_obj = Stage.objects.get(SequenceNo=SequenceNo)
    stage_json = StageSerializer(stage_obj)
    return Response({"message": "Success","status": 200,"data":[stage_json.data]})

#Stage_detail One API
@api_view(["POST"])
def stage_detail(request):
    Opp_Id=request.data['Opp_Id']
    Stageno=request.data['Stageno']
    stage_obj = Stage.objects.filter(Opp_Id=Opp_Id,Stageno=Stageno)
    print(stage_obj);
    stage_json = StageSerializer(stage_obj, many=True)
    return Response({"message": "Success","status": 200,"data":stage_json.data})

#Line All API
@api_view(["POST"])
def all_line(request):
    SequenceNo=request.data['SequenceNo']    
    line_obj = Line.objects.filter(SequenceNo=SequenceNo)
    line_json = LineSerializer(line_obj, many=True)
    return Response({"message": "Success","status": 200,"data":line_json.data})

#Line One API
@api_view(["POST"])
def one_line(request):
    SequenceNo=request.data['SequenceNo']    
    LineNum=request.data['LineNum']    
    line_obj = Line.objects.filter(SequenceNo=SequenceNo, LineNum=LineNum)
    line_json = LineSerializer(line_obj, many=True)
    return Response({"message": "Success","status": 200,"data":line_json.data})

#Opp Stage Update API
@api_view(['POST'])
def change_stage(request):
    fetchid = request.data['Opp_Id']
    print("come 0")
    chk = Stage.objects.filter(Opp_Id = fetchid, Stageno = request.data['Stageno'])
    if chk[0].Status==2:
        return Response({"message":"CurrentStage already completed","status":201,"data":[]})
    
    st_max = Stage.objects.filter(Opp_Id = fetchid).order_by('-Stageno')[:1]
    
    print(st_max[0].Stageno)
    
    if float(request.data['Stageno']) > 1:
        if st_max == float(request.data['Stageno']) :
            cur_stg = float(request.data['Stageno'])
        else:
            next_stg = Stage.objects.filter(Opp_Id = fetchid, Stageno__gt = float(request.data['Stageno'])).order_by('Stageno')[:1]
            #SELECT * FROM `Opportunity_stage` WHERE Opp_Id=8 and Stageno > 1 order by Stageno limit 1
            cur_stg = next_stg[0].Stageno
            cur_name = next_stg[0].Name
    
        opp = Opportunity.objects.get(pk = fetchid)
        opp.CurrentStageNumber = cur_stg
        opp.CurrentStageName = cur_name
        opp.save()
        print(cur_stg)
        
        stg_obj = Stage.objects.filter(Opp_Id = fetchid, Stageno__lte = float(request.data['Stageno'])).order_by('Stageno')
    
        for stg in stg_obj:
            print(stg)
            if(int(stg.Status) != 2):
                print("come")
                stg.Status= 2
                stg.UpdateDate=request.data['UpdateDate']
                
                stg.Comment=request.data['Comment']
                
                stg.save()
                
                try:
                    upload = request.FILES['File']
                    target = 'bridge/static/image/'+fetchid+'/'
                    os.makedirs(target, exist_ok=True)
                    fss = FileSystemStorage()
                    file = fss.save(target+"/"+upload.name, upload)
                    #file_url = fss.url(file)
                    file_url = '/static/image/'+fetchid+'/'+upload.name
                    #file_url = file_url.replace('/bridge','')
                    print(file_url)                
                    stg.File=file_url
                    stg.save()
                except:
                    stg.save()
        
        if float(request.data['Stageno']) != st_max[0].Stageno:
            current = Stage.objects.filter(Opp_Id = fetchid, Stageno__gt = float(request.data['Stageno'])).order_by('Stageno')[:1]
            obj = Stage.objects.get(pk=current[0].id)
            obj.Status = 1
            obj.UpdateDate=request.data['UpdateDate']
            obj.save()
            
        stg_objs = Stage.objects.filter(Opp_Id = fetchid).order_by('Stageno')
        stg_json = StageSerializer(stg_objs, many=True)
        
        print(request.data['Stageno'])
        print(type(request.data['Stageno']))
        
        if type(request.data['Stageno']) == int:
            print("int num")
            
            model = Opportunity.objects.get(pk = request.data['Opp_Id'])        

            r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)
            
            opp_data = {
              "CardCode": model.CardCode,
              "PredictedClosingDate": model.PredictedClosingDate,
              "ContactPerson": int(model.ContactPerson),
              "DataOwnershipfield": int(model.DataOwnershipfield),
              "MaxLocalTotal": float(model.MaxLocalTotal),
              "MaxSystemTotal": float(model.MaxSystemTotal),
              "Remarks": model.Remarks,
              "SalesOpportunitiesLines": [
                {
                  "DocumentType": "bodt_MinusOne",
                  "MaxLocalTotal": float(model.MaxLocalTotal),
                  "MaxSystemTotal": float(model.MaxSystemTotal),
                  "SalesPerson": int(model.SalesPerson),
                  "StageKey": float(request.data['Stageno'])
                }
              ],
              "SalesPerson": int(model.SalesPerson),
              "StartDate": model.StartDate,
              #"U_TYPE": request.data['U_TYPE'],
              "OpportunityName": model.OpportunityName
            }
            
            print(opp_data)
            print(json.dumps(opp_data))

            print(settings.BASEURL+'/SalesOpportunities('+model.SequentialNo+')');
        
            res = requests.patch(settings.BASEURL+'/SalesOpportunities('+model.SequentialNo+')', data=json.dumps(opp_data), cookies=r.cookies, verify=False)
            
            if len(res.content) !=0 :
                res1 = json.loads(res.content)
                SAP_MSG = res1['error']['message']['value']
                return Response({"message":"Partely successful","status":202,"SAP_error":SAP_MSG, "data":stg_json.data})
            else:
                return Response({"message":"successful","status":200, "data":stg_json.data})
        else:
            return Response({"message":"successful","status":200, "data":stg_json.data})

        #return Response({"message": "Success","status": 200,"data":stg_json.data})
    
    else:
    
        if st_max == float(request.data['Stageno']) :
            cur_stg = float(request.data['Stageno'])
        else:
            next_stg = Stage.objects.filter(Opp_Id = fetchid, Stageno__gt = float(request.data['Stageno'])).order_by('Stageno')[:1]
            #SELECT * FROM `Opportunity_stage` WHERE Opp_Id=8 and Stageno > 1 order by Stageno limit 1
            cur_stg = next_stg[0].Stageno
            cur_name = next_stg[0].Name
    
        opp = Opportunity.objects.get(pk = fetchid)
        opp.CurrentStageNumber = cur_stg
        opp.CurrentStageName = cur_name
        opp.save()
        print(cur_stg)
    
        stg_obj = Stage.objects.get(Opp_Id = fetchid, Stageno = float(request.data['Stageno']))
        print("come 1")
        stg_obj.Status=2
        stg_obj.UpdateDate=request.data['UpdateDate']
        stg_obj.Comment=request.data['Comment']

        try:
            upload = request.FILES['File']
            target = 'bridge/static/image/'+fetchid+'/'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+upload.name, upload)
            #file_url = fss.url(file)
            file_url = '/static/image/'+fetchid+'/'+upload.name
            #file_url = file_url.replace('/bridge','')
            print(file_url)                
            stg_obj.File=file_url
            stg_obj.save()
        except:
            stg_obj.save()
        
        #SELECT * FROM `opportunity_stage` WHERE Opp_Id=85 and stageno > 2 order by stageno limit 1;
        current = Stage.objects.filter(Opp_Id = fetchid, Stageno__gt = float(request.data['Stageno'])).order_by('Stageno')[:1]
        obj = Stage.objects.get(pk=current[0].id)
        obj.Status = 1
        obj.UpdateDate=request.data['UpdateDate']
        obj.save()
       
        # for obj in current:
            # obj.Status=1
            # obj.save()
        
        stg_objs = Stage.objects.filter(Opp_Id = fetchid).order_by('Stageno')
        stg_json = StageSerializer(stg_objs, many=True)
        
        
        print(request.data['Stageno'])
        print(type(request.data['Stageno']))
        
        if (type(request.data['Stageno']) == int)==True:
            print("int num")
            
            model = Opportunity.objects.get(pk = request.data['Opp_Id'])        
                                
            r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)
            
            opp_data = {
              "CardCode": model.CardCode,
              "PredictedClosingDate": model.PredictedClosingDate,
              "ContactPerson": int(model.ContactPerson),
              "DataOwnershipfield": int(model.DataOwnershipfield),
              "MaxLocalTotal": float(model.MaxLocalTotal),
              "MaxSystemTotal": float(model.MaxSystemTotal),
              "Remarks": model.Remarks,
              "SalesOpportunitiesLines": [
                {
                  "DocumentType": "bodt_MinusOne",
                  "MaxLocalTotal": float(model.MaxLocalTotal),
                  "MaxSystemTotal": float(model.MaxSystemTotal),
                  "SalesPerson": int(model.SalesPerson),
                  "StageKey": float(request.data['Stageno'])
                }
              ],
              "SalesPerson": int(model.SalesPerson),
              "StartDate": model.StartDate,
              #"U_TYPE": request.data['U_TYPE'],
              "OpportunityName": model.OpportunityName
            }
            
            print(opp_data)
            print(json.dumps(opp_data))

            print(settings.BASEURL+'/SalesOpportunities('+model.SequentialNo+')');
        
            res = requests.patch(settings.BASEURL+'/SalesOpportunities('+model.SequentialNo+')', data=json.dumps(opp_data), cookies=r.cookies, verify=False)
            
            if len(res.content) !=0 :
                res1 = json.loads(res.content)
                SAP_MSG = res1['error']['message']['value']
                return Response({"message":"Partely successful","status":202,"SAP_error":SAP_MSG, "data":stg_json.data})
            else:
                return Response({"message":"successful","status":200, "data":stg_json.data})
        else:
            return Response({"message":"successful","status":200, "data":stg_json.data})
        
        #return Response({"message": "Success","status": 200,"data":stg_json.data})
        
#Opp Fav Update API
@api_view(['POST'])
def fav(request):
    fetchid = request.data['id']
    model = Opportunity.objects.get(pk = fetchid)
    model.U_FAV  = request.data['U_FAV']
    model.save()
    return Response({"message":"successful","status":200, "data":[]})

#Opp Stage Update API
@api_view(['POST'])
def change_stage1(request):
    fetchid = request.data['Opp_Id']
    
    if type(request.data['CurrentStageNo']) == str:
        return Response({"message":"CurrentStageNo should be int or float","status":201,"data":[]})
    else:
        try:
            model = Opportunity.objects.get(pk = fetchid)        
            print(model)
            model.CurrentStageNo  = request.data['CurrentStageNo']
            model.UpdateDate  = request.data['UpdateDate']
            model.UpdateTime  = request.data['UpdateTime']

            model.save()
            
            stage = Stage.objects.get(Opp_Id = fetchid, Stageno=request.data['CurrentStageNo'])
            print(stage)
            
            stage.UpdateDate  = request.data['UpdateDate']
            stage.Status  = 1
            stage.save()

            context = {
                "CurrentStageNo":request.data['CurrentStageNo'],
                "UpdateDate ":request.data['UpdateDate'],
                "UpdateTime ":request.data['UpdateTime']            
            }
            
            if type(request.data['CurrentStageNo']) == int:
                print("int num")

                r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
                token = json.loads(r.text)['SessionId']
                print(token)
                
                opp_data = {
                  "CardCode1": model.CardCode,
                  "PredictedClosingDate": model.PredictedClosingDate,
                  "ContactPerson": int(model.ContactPerson),
                  "DataOwnershipfield": int(model.DataOwnershipfield),
                  "MaxLocalTotal": float(model.MaxLocalTotal),
                  "MaxSystemTotal": float(model.MaxSystemTotal),
                  "Remarks": model.Remarks,
                  "SalesOpportunitiesLines": [
                    {
                      "DocumentType": "bodt_MinusOne",
                      "MaxLocalTotal": float(model.MaxLocalTotal),
                      "MaxSystemTotal": float(model.MaxSystemTotal),
                      "SalesPerson": int(model.SalesPerson),
                      "StageKey": request.data['CurrentStageNo']
                    }
                  ],
                  "SalesPerson": int(model.SalesPerson),
                  "StartDate": model.StartDate,
                  #"U_TYPE": request.data['U_TYPE'],
                  "OpportunityName": model.OpportunityName
                }
                
                print(opp_data)
                print(json.dumps(opp_data))
        
                print(settings.BASEURL+'/SalesOpportunities('+model.SequentialNo+')');
            
                res = requests.patch(settings.BASEURL+'/SalesOpportunities('+model.SequentialNo+')', data=json.dumps(opp_data), cookies=r.cookies, verify=False)
                
                if len(res.content) !=0 :
                    res1 = json.loads(res.content)
                    SAP_MSG = res1['error']['message']['value']
                    return Response({"message":"Partely successful","status":202,"SAP_error":SAP_MSG, "data":[context]})
                else:
                    return Response({"message":"successful","status":200, "data":[context]})
            else:
                return Response({"message":"successful","status":200, "data":[context]})
        except:
            return Response({"message":"ID Wrong","status":201,"data":[]})

#Opp Stage Update API
@api_view(['POST'])
def complete(request):
    fetchid = request.data['Opp_Id']
    try:
        model = Opportunity.objects.get(pk = fetchid)        
        print(model)
        model.Remarks  = request.data['Remarks']
        model.Status  = request.data['Status']
        model.UpdateDate  = request.data['UpdateDate']
        model.UpdateTime  = request.data['UpdateTime']
        
        model.save()
        
        stages = Stage.objects.filter(Opp_Id = fetchid)
        for stage in stages:
            stage.Status  = 2
            stage.save()

        st_max = Stage.objects.filter(Opp_Id = fetchid).order_by('-Stageno')[:1]
    
        cur_stg = st_max[0].Stageno
        cur_name = st_max[0].Name

        opp = Opportunity.objects.get(pk = fetchid)
        opp.CurrentStageNumber = cur_stg
        opp.CurrentStageName = cur_name
        opp.save()

        context = {
            #"CurrentStageNo":request.data['CurrentStageNo'],
            "UpdateDate ":request.data['UpdateDate'],
            "UpdateTime ":request.data['UpdateTime']            
        }

        if settings.SAP == True:

            r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)
            
            opp_data = {
            "Remarks": request.data['Remarks'],
            "Status": request.data['Status']
            }
            
            print(opp_data)
            print(json.dumps(opp_data))

            print(settings.BASEURL+'/SalesOpportunities('+model.SequentialNo+')');
        
            res = requests.patch(settings.BASEURL+'/SalesOpportunities('+model.SequentialNo+')', data=json.dumps(opp_data), cookies=r.cookies, verify=False)
            
            if len(res.content) !=0 :
                res1 = json.loads(res.content)
                SAP_MSG = res1['error']['message']['value']
                return Response({"message":"Partely successful","status":202,"SAP_error":SAP_MSG, "data":[context]})
            else:
                return Response({"message":"successful","status":200, "data":[context]})
        else:
            return Response({"message":"successful","status":200, "data":[context]})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})

#updated by millan on 07-September-2022
#Opportunity stage_complete API
@api_view(['POST'])
def stage_complete(request):
    try:        
        if request.data['id'] == "":
            return Response({"message":"Stage Id Can't be Empty","status":201,"data":[]})
        elif request.data['CreateDate'] == "":
            return Response({"message":"CreateDate Can't be Empty","status":201,"data":[]})
        else:
            id = request.data['id']
            CreateDate = request.data['CreateDate']
            UpdateDate = request.data['UpdateDate']
            Comment = request.data['Comment']
            File = request.data['File']
            
            model = Stage.objects.get(pk=id)
            OppID = model.Opp_Id            

            Status=0
            if UpdateDate !="":
                Status = 1                
            
                if model.UpdateDate =="":
                    OppObj = Opportunity.objects.get(pk=OppID)
                    if model.Name == "Need Analysis":
                        OppObj.OPStatus = "Warm"
                        OppObj.save()
                    elif model.Name == "Evaluating":
                        OppObj.OPStatus = "Hot"
                        OppObj.save()
                    elif model.Name == "Close":
                        OppObj.OPStatus = request.data['OPStatus']
                        OppObj.save()
            else:
                print("Sqno: "+str(model.SequenceNo))
                if model.SequenceNo == '1':
                    return Response({"message":"First Stage Can't be Incomplete","status":201,"data":[]})
                OppObj = Opportunity.objects.get(pk=OppID)
                if model.Name == "Need Analysis":
                    OppObj.OPStatus = "Cold"
                    OppObj.save()
                elif model.Name == "Evaluating":
                    OppObj.OPStatus = "Warm"
                    OppObj.save()

            attachmentsImage_url = ""
            if File !="" :
                target ='./bridge/static/image/opportunitystage'
                os.makedirs(target, exist_ok=True)
                fss = FileSystemStorage()
                file = fss.save(target+"/"+File.name, File)
                productImage_url = fss.url(file)
                attachmentsImage_url = productImage_url.replace('/bridge/', '/')
                model.File = attachmentsImage_url
            print(attachmentsImage_url)

            model.CreateDate = CreateDate
            model.UpdateDate = UpdateDate
            model.Comment = Comment
            model.Status = Status
            model.save()
            
            stg = Stage.objects.filter(Opp_Id=OppID, SequenceNo__gt=model.SequenceNo)[:1]
            print(stg)
            if UpdateDate !="":
                StartDate = UpdateDate
            else:
                pre = Stage.objects.filter(Opp_Id=OppID, SequenceNo__lt=model.SequenceNo)[:1]
                StartDate = pre[0].UpdateDate
                
            for st in stg:
                st.CreateDate = StartDate
                st.save()            
            context = {
                "CreateDate" :model.CreateDate,
                "UpdateDate" : model.UpdateDate,
                "Comment" : model.Comment,
                "File" : model.File,
                "id" : model.id
            }
            
            return Response({"message":"successful","status":200, "data":context})
    except Exception as e:
        #print(e)
        return Response({"message":str(e),"status":201,"data":[{"Error":str(e)}]})

