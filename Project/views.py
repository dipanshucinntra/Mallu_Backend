from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import ProjectForm  
from .models import Project  
import json
from django.contrib import messages
import os
from django.core.files.storage import FileSystemStorage

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import ProjectSerializer
from rest_framework.parsers import JSONParser
from Attachment.models import Attachment
from Attachment.serializers import AttachmentSerializer
from django.db.models import Q

# Create your views here.  

#Project Create API
@api_view(['POST'])
def create(request):
    try:
        name = request.data['name']
        
        kit_consultant_code = request.data['kit_consultant_code']
        kit_consultant_name = request.data['kit_consultant_name']
        kit_contact_person = request.data['kit_contact_person']
        
        mep_consultant_code = request.data['mep_consultant_code']
        mep_consultant_name = request.data['mep_consultant_name']
        mep_contact_person = request.data['mep_contact_person']
        
        pm_consultant_code = request.data['pm_consultant_code']
        pm_consultant_name = request.data['pm_consultant_name']
        pm_contact_person = request.data['pm_contact_person']
        
        customer_group_type = request.data['customer_group_type']
        contact_person = request.data['contact_person']
        start_date = request.data['start_date']
        target_date = request.data['target_date']
        completion_date = request.data['completion_date']
        details = request.data['details']        
        #cardcode = request.data['cardcode']
        CardCode = request.data['CardCode']        
        sector = request.data['sector']
        type = request.data['type']
        location = request.data['location']
        project_owner = request.data['project_owner']
        project_cost = request.data['project_cost']
        project_status = request.data['project_status']
        address = request.data['address']
        
        Attach = request.data['Attach']
        Caption = request.data['Caption']
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        
        GroupType = request.data['GroupType'] #added by millan on 10 October 2022
        
        #added by millan on 11-10-2022
        cli_consultant_code = request.data['cli_consultant_code']
        cli_consultant_name = request.data['cli_consultant_name']
        cli_contact_person = request.data['cli_contact_person']
        
        contr_consultant_code = request.data['contr_consultant_code']
        contr_consultant_name = request.data['contr_consultant_name']
        contr_contact_person = request.data['contr_contact_person']
        
        fcm_consultant_code = request.data['fcm_consultant_code']
        fcm_consultant_name = request.data['fcm_consultant_name']
        fcm_contact_person = request.data['fcm_contact_person']
        
        arch_consultant_code = request.data['arch_consultant_code']
        arch_consultant_name = request.data['arch_consultant_name']
        arch_contact_person = request.data['arch_contact_person']
        
        oth_consultant_code = request.data['oth_consultant_code']
        oth_consultant_name = request.data['oth_consultant_name']
        oth_contact_person =  request.data['oth_contact_person']
        #added by millan on 11-10-2022

        model=Project(name = name, kit_consultant_code = kit_consultant_code, kit_consultant_name = kit_consultant_name, kit_contact_person=kit_contact_person, mep_consultant_code = mep_consultant_code, mep_consultant_name = mep_consultant_name, mep_contact_person=mep_contact_person, pm_consultant_code = pm_consultant_code, pm_consultant_name = pm_consultant_name, pm_contact_person=pm_contact_person, customer_group_type = customer_group_type, contact_person = contact_person, start_date = start_date, target_date = target_date, completion_date = completion_date, details = details, CardCode = CardCode, sector = sector, type = type, location = location, project_owner = project_owner, project_cost = project_cost, project_status = project_status, address = address, CreatedDate = CreateDate, CreatedTime=CreateTime, GroupType = GroupType, cli_consultant_code = cli_consultant_code, cli_consultant_name = cli_consultant_name, cli_contact_person = cli_contact_person, contr_consultant_code = contr_consultant_code, contr_consultant_name = contr_consultant_name, contr_contact_person = contr_contact_person, fcm_consultant_code = fcm_consultant_code, fcm_consultant_name = fcm_consultant_name, fcm_contact_person = fcm_contact_person, arch_consultant_code = arch_consultant_code, arch_consultant_name = arch_consultant_name, arch_contact_person = arch_contact_person, oth_consultant_code = oth_consultant_code, oth_consultant_name = oth_consultant_name, oth_contact_person=oth_contact_person)
        
        model.save()
        qt = Project.objects.latest('id')
        fetchid = qt.id
        
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

            att=Attachment(File=attachmentsImage_url, Caption=Caption, LinkType="Project", LinkID=fetchid, CreateDate=CreateDate, CreateTime=CreateTime, UpdateDate=CreateDate, UpdateTime=CreateTime)
            
            att.save()
        return Response({"message":"successful","status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

#Project All API
@api_view(["POST"])
def all(request):
    try:
        allProject = []
        #cardcode=request.data['cardcode']
        CardCode=request.data['CardCode']
        #Projects_objs = Project.objects.filter(Q(CardCode=CardCode) | Q(kit_consultant_code=cardcode) | Q(mep_consultant_code=cardcode) | Q(pm_consultant_code=cardcode) | Q(cli_consultant_code=cardcode) | Q(contr_consultant_code=cardcode) | Q(fcm_consultant_code=cardcode) | Q(arch_consultant_code=cardcode) | Q(oth_consultant_code=cardcode)).order_by("-id")
        Projects_objs = Project.objects.filter(Q(CardCode=CardCode) | Q(kit_consultant_code=CardCode) | Q(mep_consultant_code=CardCode) | Q(pm_consultant_code=CardCode) | Q(cli_consultant_code=CardCode) | Q(contr_consultant_code=CardCode) | Q(fcm_consultant_code=CardCode) | Q(arch_consultant_code=CardCode) | Q(oth_consultant_code=CardCode)).order_by("-id")
        for Obj in Projects_objs:            
            ObjJson = ProjectSerializer(Obj, many=False)
            ObjJson = json.loads(json.dumps(ObjJson.data))
            #print(ObjJson)

            Attach = Attachment.objects.filter(LinkType="Project", LinkID=Obj.id)
            AttachJson = AttachmentSerializer(Attach, many=True)
            
            ObjJson['Attach'] = AttachJson.data
            print(ObjJson)
            allProject.append(ObjJson)
        return Response({"message": "Success","status": 200,"data":allProject})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

#Project All API
@api_view(["POST"])
def allbycp(request):
    try:
        allProject = []
        contact_person=request.data['contact_person']
        Projects_objs = Project.objects.filter(Q(contact_person=contact_person) | Q(kit_contact_person=contact_person) | Q(mep_contact_person=contact_person) | Q(pm_contact_person=contact_person) | Q(cli_contact_person=contact_person) | Q(contr_contact_person=contact_person) | Q(fcm_contact_person=contact_person) | Q(arch_contact_person=contact_person) | Q(oth_contact_person=contact_person)).order_by("-id")
        for Obj in Projects_objs:            
            ObjJson = ProjectSerializer(Obj, many=False)
            ObjJson = json.loads(json.dumps(ObjJson.data))
            #print(ObjJson)

            Attach = Attachment.objects.filter(LinkType="Project", LinkID=Obj.id)
            AttachJson = AttachmentSerializer(Attach, many=True)
            
            ObjJson['Attach'] = AttachJson.data
            print(ObjJson)
            allProject.append(ObjJson)
        return Response({"message": "Success","status": 200,"data":allProject})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
        
#Project One API
@api_view(["POST"])
def one(request):
    try:
        id=request.data['id']
        Project_obj = Project.objects.get(id=id)
        Project_json = ProjectSerializer(Project_obj)
        return Response({"message": "Success","status": 200,"data":[Project_json.data]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})


#Project Update API
@api_view(['POST'])
def update(request):
    try:
        fetchid = request.data['id']
        model = Project.objects.get(pk = fetchid)

        model.kit_consultant_code = request.data['kit_consultant_code']
        model.kit_consultant_name = request.data['kit_consultant_name']
        model.kit_contact_person = request.data['kit_contact_person']

        model.mep_consultant_code = request.data['mep_consultant_code']
        model.mep_consultant_name = request.data['mep_consultant_name']
        model.mep_contact_person = request.data['mep_contact_person']

        model.pm_consultant_code = request.data['pm_consultant_code']
        model.pm_consultant_name = request.data['pm_consultant_name']
        model.pm_contact_person = request.data['pm_contact_person']

        model.customer_group_type = request.data['customer_group_type']
        model.contact_person = request.data['contact_person']
        model.start_date = request.data['start_date']
        model.target_date = request.data['target_date']
        model.completion_date = request.data['completion_date']
        model.details = request.data['details']
        #model.cardcode = request.data['cardcode']
        model.CardCode = request.data['CardCode']
        model.sector = request.data['sector']
        model.type = request.data['type']
        model.location = request.data['location']
        model.project_owner = request.data['project_owner']
        model.project_cost = request.data['project_cost']
        model.project_status = request.data['project_status']
        model.address = request.data['address']

        model.GroupType = request.data['GroupType'] #added by millan on 10 October 2022
        
        #added by millan on 11-10-2022
        model.cli_consultant_code = request.data['cli_consultant_code']
        model.cli_consultant_name = request.data['cli_consultant_name']
        model.cli_contact_person = request.data['cli_contact_person']
        
        model.contr_consultant_code = request.data['contr_consultant_code']
        model.contr_consultant_name = request.data['contr_consultant_name']
        model.contr_contact_person = request.data['contr_contact_person']
        
        model.fcm_consultant_code = request.data['fcm_consultant_code']
        model.fcm_consultant_name = request.data['fcm_consultant_name']
        model.fcm_contact_person = request.data['fcm_contact_person']
        
        model.arch_consultant_code = request.data['arch_consultant_code']
        model.arch_consultant_name = request.data['arch_consultant_name']
        model.arch_contact_person = request.data['arch_contact_person']
        
        model.oth_consultant_code = request.data['oth_consultant_code']
        model.oth_consultant_name = request.data['oth_consultant_name']
        model.oth_contact_person =  request.data['oth_contact_person']
        #added by millan on 11-10-2022
        
        model.save()
        return Response({"message":"successful","status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

#Project delete
@api_view(['POST'])
def delete(request):
    try:
        fetchid=request.data['id']
        fetchdata=Project.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

#Project Listing Without Condition Added by millan on 01-November-2022
@api_view(["GET"])
def project_all(request):
    try:
        allProject = []
        Projects_objs = Project.objects.all().order_by("-id")
        for Obj in Projects_objs:            
            ObjJson = ProjectSerializer(Obj, many=False)
            ObjJson = json.loads(json.dumps(ObjJson.data))

            Attach = Attachment.objects.filter(LinkType="Project", LinkID=Obj.id)
            AttachJson = AttachmentSerializer(Attach, many=True)
            
            ObjJson['Attach'] = AttachJson.data
            allProject.append(ObjJson)
        return Response({"message": "Success","status": 200,"data":allProject})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
