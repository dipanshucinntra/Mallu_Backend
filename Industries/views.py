from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import IndustriesForm  
from .models import Industries  
import requests, json

from django.contrib import messages

from django.conf import settings 

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import IndustriesSerializer
from rest_framework.parsers import JSONParser
# Create your views here.  

from bridge import settings

#Industries Create API
@api_view(['POST'])
def create(request):

    try:
            
        IndustryDescription = request.data['IndustryDescription']
        IndustryName = request.data['IndustryName']

        model=Industries(IndustryDescription = IndustryDescription, IndustryName = IndustryName)
        
        model.save()
        inds = Industries.objects.latest('id')
        fetchid = inds.id

        if settings.SAP == True:
        
            r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)
            
            inds_data = {
                        "IndustryDescription": request.data['IndustryDescription'],
                        "IndustryName": request.data['IndustryName']
                    }
            
            print(inds_data)
            print(json.dumps(inds_data))

            res = requests.post(settings.BASEURL+'/Industries', data=json.dumps(inds_data), cookies=r.cookies, verify=False)
            live = json.loads(res.text)
            
            
            
            if "IndustryCode" in live:
                print(live['IndustryCode'])
                
                model = Industries.objects.get(pk = fetchid)
                model.IndustryCode = live['IndustryCode']
                model.save()
                
                return Response({"message":"successful","status":200,"data":[{"Inds_Id":inds.id, "IndustryCode":live['IndustryCode']}]})
            else:
                SAP_MSG = live['error']['message']['value']
                print(SAP_MSG)
                fetchdata=Industries.objects.filter(pk=fetchid).delete()
                return Response({"message":SAP_MSG,"SAP_error":SAP_MSG, "status":202,"data":[]})
                # if "already exists" in SAP_MSG:
                #     fetchdata=Industries.objects.filter(pk=fetchid).delete()
                #     return Response({"message":"Not created","SAP_error":SAP_MSG, "status":202,"data":[]})
                # else:
                #     return Response({"message":"Partely successful","SAP_error":SAP_MSG, "status":202,"data":[]})
        else:
            model = Industries.objects.get(pk = fetchid)
            model.IndustryCode = fetchid
            model.save()
                
            return Response({"message":"successful","status":200,"data":[{"Inds_Id":inds.id, "IndustryCode":fetchid}]})

    except Exception as e:
        return Response({"message":"Error", "status":201, "data":[{"Error":str(e)}]})

#Industries All API
@api_view(["GET"])
def all(request):
    industries_obj = Industries.objects.all() 
    industrie_json = IndustriesSerializer(industries_obj, many=True)
    return Response({"message": "Success","status": 200,"data":industrie_json.data})


#Industries One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    industrie_obj = Industries.objects.get(id=id)
    industrie_json = IndustriesSerializer(industrie_obj)
    return Response({"message": "Success","status": 200,"data":[industrie_json.data]})

#Industries Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Industries.objects.get(pk = fetchid)
        model.IndustryDescription = request.data['IndustryDescription']
        model.IndustryName = request.data['IndustryName']
        model.IndustryCode = request.data['IndustryCode']

        model.save()
        context = {
            "id":request.data['id'],
            'IndustryDescription':request.data['IndustryDescription'],
            'IndustryName':request.data['IndustryName'],
            'IndustryCode':request.data['IndustryCode']
            }
        if settings.SAP == True:
            r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)
            
            inds_data = {
                "IndustryDescription": request.data['IndustryDescription'],
                "IndustryName": request.data['IndustryName']
            }
            
            print(inds_data)
            

            print(settings.BASEURL+'/Industries('+model.IndustryCode+')');
        
            res = requests.patch(settings.BASEURL+'/Industries('+model.IndustryCode+')', data=json.dumps(inds_data), cookies=r.cookies, verify=False)
            
            if len(res.content) !=0 :
                res1 = json.loads(res.content)
                SAP_MSG = res1['error']['message']['value']
                return Response({"message":"Partely successful","status":202,"SAP_error":SAP_MSG, "data":[context]})
            else:
                return Response({"message":"successful","status":200, "data":[context]})
        else:
            return Response({"message":"successful","status":200, "data":[context]})
        #return Response({"message":"successful","status":"200","data":[context]})
    except:
        return Response({"message":"ID Wrong","status":"201","data":[context]})

#Industries delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        inds=Industries.objects.get(pk=fetchid)
        IndustryCode = inds.IndustryCode
        
        fetchdata=Industries.objects.filter(pk=fetchid).delete()
        if settings.SAP == True:

            try:
                r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
                token = json.loads(r.text)['SessionId']
                print(token)
                res = requests.delete(settings.BASEURL+'/Industries('+IndustryCode+')', cookies=r.cookies, verify=False)
                return Response({"message":"successful","status":"200","data":[]})
            except:
                return Response({"message":"successful","status":"200","data":[]})        
        else:
            return Response({"message":"successful","status":"200","data":[]})        
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

