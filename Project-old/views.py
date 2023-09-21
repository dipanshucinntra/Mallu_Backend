from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import ProjectForm  
from .models import Project  

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import ProjectSerializer
from rest_framework.parsers import JSONParser
# Create your views here.  

#Project Create API
@api_view(['POST'])
def create(request):
    name = request.data['name']
    consultant_code = request.data['consultant_code']
    consultant_name = request.data['consultant_name']
    expected_start_date = request.data['expected_start_date']
    details = request.data['details']
    attach = request.data['attach']
    cardcode = request.data['cardcode']
    timestamp = request.data['timestamp']

    model=Project(name = name, consultant_code = consultant_code, consultant_name = consultant_name,  expected_start_date = expected_start_date, details = details, attach=attach, cardcode=cardcode, timestamp = timestamp)
    
    model.save()
    return Response({"message":"successful","status":"200","data":[]})

#Project All API
@api_view(["POST"])
def all(request):
    cardcode=request.data['cardcode']
    Projects_obj = Project.objects.filter(cardcode=cardcode) 
    Project_json = ProjectSerializer(Projects_obj, many=True)
    return Response({"message": "Success","status": 200,"data":Project_json.data})

#Project One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    Project_obj = Project.objects.get(id=id)
    Project_json = ProjectSerializer(Project_obj)
    return Response({"message": "Success","status": 200,"data":[Project_json.data]})


#Project Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Project.objects.get(pk = fetchid)
        model.name = request.data['name']
        model.consultant_code = request.data['consultant_code']
        model.consultant_name = request.data['consultant_name']
        model.expected_start_date = request.data['expected_start_date']
        model.details = request.data['details']
        model.attach = request.data['attach']
        model.cardcode = request.data['cardcode']
        model.timestamp = request.data['timestamp']
        model.save()
        return Response({"message":"successful","status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

#Project delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Project.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

