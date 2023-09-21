from django.conf import settings
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import PaymentTermsTypesForm  
from .models import PaymentTermsTypes  
import requests, json

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import PaymentTermsTypesSerializer
from rest_framework.parsers import JSONParser
# Create your views here.  

#PaymentTermsTypes Create API
@api_view(['POST'])
def create(request):
    try:   

        PaymentTermsGroupName = request.data['PaymentTermsGroupName']
        model=PaymentTermsTypes(PaymentTermsGroupName = PaymentTermsGroupName)
        model.save()
        pay = PaymentTermsTypes.objects.latest('id')
        fetchid = pay.id
        
        model = PaymentTermsTypes.objects.get(pk = fetchid)
        model.GroupNumber = pay.id
        model.save()
        return Response({"message":"successful","status":200,"data":[{"id":pay.id, "GroupNumber":pay.id}]})
        
        r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
        token = json.loads(r.text)['SessionId']
        print(token)
        
        pay_data = {
            "PaymentTermsGroupName": request.data['PaymentTermsGroupName']
        }
        
        print(pay_data)
        print(json.dumps(pay_data))

        res = requests.post(settings.BASEURL+'/PaymentTermsTypes', data=json.dumps(pay_data), cookies=r.cookies, verify=False)
        live = json.loads(res.text)
    
        
        if "GroupNumber" in live:
            print(live['GroupNumber'])
            
            model = PaymentTermsTypes.objects.get(pk = fetchid)
            model.GroupNumber = live['GroupNumber']
            model.save()
            
            return Response({"message":"successful","status":200,"data":[{"id":pay.id, "GroupNumber":live['GroupNumber']}]})
        else:
            SAP_MSG = live['error']['message']['value']
            print(SAP_MSG)
            PaymentTermsTypes.objects.filter(pk=fetchid).delete()
            return Response({"message":SAP_MSG,"SAP_error":SAP_MSG, "status":202,"data":[]})
            # if "already exists" in SAP_MSG:
            #     fetchdata=PaymentTermsTypes.objects.filter(pk=fetchid).delete()
            #     return Response({"message":"Not created","SAP_error":SAP_MSG, "status":202,"data":[]})
            # else:
            #     return Response({"message":"Partely successful","SAP_error":SAP_MSG, "status":202,"data":[]})
    except Exception as e:
        return Response({"message":"Error", "status":201, "data":[{"Error":str(e)}]})


#PaymentTermsTypes All API
@api_view(["GET"])
def all(request):
    PaymentTermsTypes_obj = PaymentTermsTypes.objects.all().order_by('-id') 
    industrie_json = PaymentTermsTypesSerializer(PaymentTermsTypes_obj, many=True)
    return Response({"message": "Success","status": 200,"data":industrie_json.data})


#PaymentTermsTypes One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    industrie_obj = PaymentTermsTypes.objects.get(id=id)
    industrie_json = PaymentTermsTypesSerializer(industrie_obj)
    return Response({"message": "Success","status": 200,"data":[industrie_json.data]})

#PaymentTermsTypes Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = PaymentTermsTypes.objects.get(pk = fetchid)
        model.PaymentTermsGroupName = request.data['PaymentTermsGroupName']

        model.save()
        context = {
            "id":request.data['id'],
            'PaymentTermsGroupName':request.data['PaymentTermsGroupName']
            }

        return Response({"message":"successful","status":"200", "data":[context]})
        
        r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
        token = json.loads(r.text)['SessionId']
        print(token)
        
        pay_data = {
            "PaymentTermsGroupName": request.data['PaymentTermsGroupName']
        }
        
        print(pay_data)
        

        print(settings.BASEURL+'/PaymentTermsTypes('+model.GroupNumber+')');
    
        res = requests.patch(settings.BASEURL+'/PaymentTermsTypes('+model.GroupNumber+')', data=json.dumps(pay_data), cookies=r.cookies, verify=False)
        
        if len(res.content) !=0 :
            res1 = json.loads(res.content)
            SAP_MSG = res1['error']['message']['value']
            return Response({"message":"Partely successful","status":"202","SAP_error":SAP_MSG, "data":[context]})
        else:
            return Response({"message":"successful","status":"200", "data":[context]})
    except:
        return Response({"message":"ID Wrong","status":"201","data":[context]})

#PaymentTermsTypes delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        pay=PaymentTermsTypes.objects.get(pk=fetchid)
        GroupNumber = pay.GroupNumber
        
        fetchdata=PaymentTermsTypes.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})
                    
        print(data)
    
        try:
            r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)
            print(settings.BASEURL+'/PaymentTermsTypes('+GroupNumber+')')
            res = requests.delete(settings.BASEURL+'/PaymentTermsTypes('+GroupNumber+')', cookies=r.cookies, verify=False)
            print(res)
            return Response({"message":"successful","status":"200","data":[]})
        except:
            return Response({"message":"successful","status":"200","data":[]})        
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

