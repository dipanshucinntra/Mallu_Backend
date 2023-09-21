from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import CompanyForm  
from .models import Company  
import json
from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser
# Create your views here.  

#import pyodbc

#Company Create API
@api_view(['POST'])
def create(request):
    name = request.data['name']
    desc = request.data['desc']
    phone = request.data['phone']
    email = request.data['email']
    
    state = request.data['state']
    city = request.data['city']
    pincode = request.data['pincode']
    address = request.data['address']
    
    natureOfIndustry = request.data['natureOfIndustry']
    ERP = request.data['ERP']
    serverIP = request.data['serverIP']
    port = request.data['port']
    user = request.data['user']
    password = request.data['password']
    
    license_limit = request.data['license_limit']
    active = request.data['active']
    timestamp = request.data['timestamp']

    model=Company(name = name, desc = desc,  phone = phone, email = email, state=state, city=city, pincode=pincode, address=address,  natureOfIndustry = natureOfIndustry, ERP = ERP, serverIP = serverIP, port = port, user = user, password = password, license_limit = license_limit, active = active, timestamp = timestamp)
    
    model.save()
    return Response({"message":"successful","status":"200","data":[]})

#Company All API
@api_view(["GET"])
def all(request):
    companys_obj = Company.objects.all() 
    company_json = CompanySerializer(companys_obj, many=True)
    return Response({"message": "Success","status": 200,"data":company_json.data})

#Company One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    company_obj = Company.objects.get(id=id)
    company_json = CompanySerializer(company_obj)
    return Response({"message": "Success","status": 200,"data":[company_json.data]})


#Company Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Company.objects.get(pk = fetchid)

        model.id = request.data['id']
        model.name = request.data['name']
        model.desc = request.data['desc']
        model.phone = request.data['phone']
        model.email = request.data['email']

        model.state = request.data['state']
        model.city = request.data['city']
        model.pincode = request.data['pincode']
        model.address = request.data['address']
        
        model.natureOfIndustry = request.data['natureOfIndustry']
        model.ERP = request.data['ERP']
        model.serverIP = request.data['serverIP']
        model.port = request.data['port']
        model.user = request.data['user']
        model.password = request.data['password']
        
        model.license_limit = request.data['license_limit']
        model.active = request.data['active']
        model.save()
        context = {
            "id":request.data['id'],
            'name':request.data['name'],
            'desc':request.data['desc'],
            'phone':request.data['phone'],
            'email':request.data['email'],
            'state':request.data['state'],
            'city':request.data['city'],
            'pincode':request.data['pincode'],
            'address':request.data['address'],
            
            'natureOfIndustry':request.data['natureOfIndustry'],
            'ERP':request.data['ERP'],
            'serverIP':request.data['serverIP'],
            'port':request.data['port'],
            'user':request.data['user'],
            'password':request.data['password'],

            'license_limit':request.data['license_limit'],
            'active':request.data['active']
            }

        return Response({"message":"successful","status":"200","data":[context]})
    except:
        return Response({"message":"ID Wrong","status":"201","data":[]})

#Company delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Company.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

#Company All Branch API
@api_view(["GET"])
def branches(request):
    branch_obj = Branch.objects.all() 
    branch_json = BranchSerializer(branch_obj, many=True)
    return Response({"message": "Success","status": 200,"data":branch_json.data})


#Company All Branch API
@api_view(["GET"])
def branches_old(request):

    # Some other example server values are
    # server = 'localhost\sqlexpress' # for a named instance
    server = '122.160.67.60' # to specify an alternate port
    #server = 'tcp:myserver.database.windows.net' 
    database = 'TEST1003' 
    username = 'sa' 
    password = 'vision@1091'

    url = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password
    print(url)
    conn = pyodbc.connect(url)
    cursor = conn.cursor()

    #cursor.execute("SELECT @@version;")
    #cursor.execute("SELECT * from OBPL")
    cursor.execute("SELECT BPLId, BPLName, Address, MainBPL, Disabled, UserSign2, UpdateDate, DflWhs, TaxIdNum, StreetNo, Building, ZipCode, City, State, Country from OBPL where Disabled='N'") 
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    #while rows: 
        #print(rows[0])
        #row = cursor.fetchone()
        #print(row)
    all = []
    i=0;
    for row in rows:
      #print(row)
      row = dict(zip(columns, row))
      all.append(row)
      print(row['BPLId'])
      print(row['BPLName'])

    print(all)
    return Response({"message": "Success","status": 200,"data":all})
