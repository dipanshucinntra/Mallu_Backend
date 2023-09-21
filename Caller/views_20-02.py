from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .models import Caller  
from Lead.models import Lead  

from django.contrib import messages

from rest_framework.decorators import api_view
from rest_framework import status    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import CallerSerializer, CallerGetSerializer
from rest_framework.parsers import JSONParser

import os
from django.core.files.storage import FileSystemStorage
import json

# Create your views here.  


@api_view(["GET"])
def all(request):
    objs = Caller.objects.all().order_by('-id')
    serializer = CallerGetSerializer(objs, many=True)
    return Response({'status':status.HTTP_200_OK,'message':'Success','data':serializer.data})

@api_view(["POST"])
def all_filter(request):
    LeadId= request.data['LeadId']
    lead_obj = Lead.objects.get(id=LeadId).contactPerson
    objs = Caller.objects.filter(LeadId=LeadId).order_by('-id')
    serializer = CallerGetSerializer(objs, many=True)
    return Response({'status':status.HTTP_200_OK,'message':'Success','data':serializer.data, 'extra_data':[{"ContactPerson":lead_obj}]})


@api_view(["POST"])
def all_filter_page(request):
    LeadId= request.data['LeadId']
    PageNo = request.data['PageNo']
    try:
        MaxItem = request.data['MaxItem']
    except:
        MaxItem = 10
    endWith = (PageNo * MaxItem)
    startWith = (endWith - MaxItem)
    lead_obj = Lead.objects.get(id=LeadId).contactPerson
    objs = Caller.objects.filter(LeadId=LeadId).order_by('-id')[startWith:endWith]
    serializer = CallerGetSerializer(objs, many=True)
    return Response({'status':status.HTTP_200_OK,'message':'Success','data':serializer.data, 'extra_data':[{"ContactPerson":lead_obj}]})


@api_view(["POST"])
def count_all(request):
    LeadId= request.data['LeadId']
    objs = Caller.objects.filter(LeadId=LeadId).count()
    return Response({'status':status.HTTP_200_OK,'message':'Success','data':[{"total_count":objs}]})


@api_view(["POST"])
def one(request):
    try:
        objs = Caller.objects.get(id=request.data['id'])
        serializer = CallerGetSerializer(objs)
        return Response({'status':status.HTTP_200_OK,'message':'Success','data':[serializer.data]})
    except:
        return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Invalid_data', 'data':[]})


@api_view(["POST"])
def create(request):
    serializer = CallerSerializer(data=request.data)
    if serializer.is_valid(): 
        serializer.save() 
        return Response({'status':status.HTTP_200_OK,'message':'Success', 'data':[]})
    return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Invalid_data', 'data':[]})


@api_view(["PUT"])
def update(request):
    try:
        obj = Caller.objects.get(id=request.data['id'])
    except:
        obj = None
    if obj:
        serializer = CallerSerializer(obj, data=request.data)
        if serializer.is_valid(): 
            serializer.save() 
            return Response({'status':status.HTTP_200_OK,'message':'Success', 'data':[]})
    return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Invalid_data', 'data':[]})


@api_view(["POST"])
def delete(request):
    try:
        obj = Caller.objects.get(id=request.data['id'])
    except:
        obj = None
    if obj:
        obj.delete()
        return Response({'status':status.HTTP_200_OK,'message':'Success', 'data':[]})
    return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Invalid_data', 'data':[]})






