from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import BPEmployee
from .models import BPEmployee
import requests
import json

from django.contrib import messages

from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import BPEmployeeSerializer
from rest_framework.parsers import JSONParser
# Create your views here.

#BPEmployee Create API


@api_view(['POST'])
def create(request):
    try:
        Title = request.data['Title']
        FirstName = request.data['FirstName']
        MiddleName = request.data['MiddleName']
        LastName = request.data['LastName']
        Position = request.data['Position']
        Address = request.data['Address']
        MobilePhone = request.data['MobilePhone']
        Fax = request.data['Fax']
        E_Mail = request.data['E_Mail']
        Remarks1 = request.data['Remarks1']
        DateOfBirth = request.data['DateOfBirth']
        Gender = request.data['Gender']
        Profession = request.data['Profession']
        CardCode = request.data['CardCode']

        U_BPID = request.data['U_BPID']
        U_BRANCHID = request.data['U_BRANCHID']
        U_NATIONALTY = request.data['U_NATIONALTY']

        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        UpdateDate = request.data['UpdateDate']
        UpdateTime = request.data['UpdateTime']

        #added by millan on 01-September-2022
        LandlineNo = request.data['LandlineNo']
        LinkProfile = request.data['LinkProfile']
        
        Alternateno = request.data['Alternateno']   #added by millan on 10-October-2022

        model = BPEmployee(U_BRANCHID=U_BRANCHID, U_BPID=U_BPID, CardCode=CardCode, Title=Title, FirstName=FirstName, MiddleName=MiddleName, LastName=LastName, Position=Position, Address=Address, MobilePhone=MobilePhone, Fax=Fax, E_Mail=E_Mail, Remarks1=Remarks1, U_NATIONALTY=U_NATIONALTY,DateOfBirth=DateOfBirth, Gender=Gender, Profession=Profession, CreateDate=CreateDate, CreateTime=CreateTime, UpdateDate=UpdateDate, UpdateTime=UpdateTime, LandlineNo=LandlineNo, LinkProfile=LinkProfile, Alternateno=Alternateno)

        model.save()
        em = BPEmployee.objects.latest('id')

        if settings.SAPBP == True:
            r = requests.post(settings.BASEURL+'/Login',
                              data=json.dumps(settings.SAPDB), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)

            em_data = {
                "ContactEmployees": [
                    {"FirstName": request.data['FirstName'],
                     "MiddleName": request.data['MiddleName'],
                     "LastName": request.data['LastName'],
                     "Name": request.data['FirstName'],
                     "E_Mail": request.data['E_Mail'],
                     "Position": request.data['Position'],
                     "MobilePhone": request.data['MobilePhone'],
                     "Address": request.data['Address'],
                     "Profession": request.data['Profession']
                     }
                ]
            }

            #print(em_data)
            print(json.dumps(em_data))
            # url = settings.BASEURL+"/BusinessPartners('"+CardCode+"')"
            url = settings.BASEURL+"/BusinessPartners('"+CardCode+"')"
            print(url)

            # res = requests.patch(settings.BASEURL+"/BusinessPartners('"+CardCode+"')", data=json.dumps(em_data), cookies=r.cookies, verify=False)

            res = requests.patch(settings.BASEURL+"/BusinessPartners('"+CardCode+"')",
                                 data=json.dumps(em_data), cookies=r.cookies, verify=False)

            if len(res.content) != 0:
                res1 = json.loads(res.content)
                SAP_MSG = res1['error']['message']['value']
                return Response({"message": "Partely successful", "status": 202, "SAP_error": SAP_MSG, "data": []})
            else:
                # bpres = requests.get(settings.BASEURL+"/BusinessPartners('"+CardCode+"')", cookies=r.cookies, verify=False)
                bpres = requests.get(
                    settings.BASEURL+"/BusinessPartners('"+CardCode+"')", cookies=r.cookies, verify=False)
                bpres1 = json.loads(bpres.content)
                lastbp = len(bpres1['ContactEmployees']) - 1
                InternalCode = bpres1['ContactEmployees'][lastbp]['InternalCode']

                bpmodel = BPEmployee.objects.get(id=em.id)
                bpmodel.InternalCode = InternalCode
                bpmodel.save()

                return Response({"message": "successful", "status": 200, "data": [{"id": em.id, "InternalCode": InternalCode}]})
        else:
            bpmodel = BPEmployee.objects.get(id=em.id)
            bpmodel.InternalCode = em.id
            bpmodel.save()
            return Response({"message": "successful", "status": 200, "data": [{"id": em.id, "InternalCode": em.id}]})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": []})

#BPEmployee All API


@api_view(["POST"])
def all(request):
    try:
        CardCode = request.data['CardCode']
        bpemployee_obj = BPEmployee.objects.filter(CardCode=CardCode)
        bpemployee_json = BPEmployeeSerializer(bpemployee_obj, many=True)
        return Response({"message": "Success", "status": 200, "data": bpemployee_json.data})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": []})


#BPEmployee One API
@api_view(["POST"])
def one(request):
    try:
        id = request.data['id']
        bpemployee_obj = BPEmployee.objects.get(id=id)
        bpemployee_json = BPEmployeeSerializer(bpemployee_obj)
        return Response({"message": "Success", "status": 200, "data": [bpemployee_json.data]})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": []})

#BPEmployee Update API


@api_view(['POST'])
def update(request):
    try:
        fetchid = request.data['id']
        model = BPEmployee.objects.get(pk=fetchid)
        model.Title = request.data['Title']
        model.FirstName = request.data['FirstName']
        model.MiddleName = request.data['MiddleName']
        model.LastName = request.data['LastName']
        model.Position = request.data['Position']
        model.Address = request.data['Address']
        model.MobilePhone = request.data['MobilePhone']
        model.Fax = request.data['Fax']
        model.E_Mail = request.data['E_Mail']
        model.Remarks1 = request.data['Remarks1']
        model.DateOfBirth = request.data['DateOfBirth']
        model.Gender = request.data['Gender']
        model.Profession = request.data['Profession']
        model.CardCode = request.data['CardCode']
        model.U_BPID = request.data['U_BPID']
        model.U_BRANCHID = request.data['U_BRANCHID']
        model.U_NATIONALTY = request.data['U_NATIONALTY']
        model.CreateDate = request.data['CreateDate']
        model.CreateTime = request.data['CreateTime']
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']

        #added by millan on 01-September-2022
        model.LandlineNo = request.data['LandlineNo']
        model.LinkProfile = request.data['LinkProfile']
        
        model.Alternateno = request.data['Alternateno']   #added by millan on 10-October-2022

        model.save()
        if settings.SAP == True:

            context = {
                'Title': request.data['Title'],
                'FirstName': request.data['FirstName'],
                'MiddleName': request.data['MiddleName'],
                'LastName': request.data['LastName'],
                'Position': request.data['Position'],
                'Address': request.data['Address'],
                'MobilePhone': request.data['MobilePhone'],
                'Fax': request.data['Fax'],
                'E_Mail': request.data['E_Mail'],
                'Remarks1': request.data['Remarks1'],
                'DateOfBirth': request.data['DateOfBirth'],
                'Gender': request.data['Gender'],
                'Profession': request.data['Profession'],
                'CardCode': request.data['CardCode'],
                'U_BPID': request.data['U_BPID'],
                'U_BRANCHID': request.data['U_BRANCHID'],
                'U_NATIONALTY': request.data['U_NATIONALTY'],
                'CreateDate': request.data['CreateDate'],
                'CreateTime': request.data['CreateTime'],
                'UpdateDate': request.data['UpdateDate'],
                'UpdateTime': request.data['UpdateTime'],
                'LandlineNo': request.data['LandlineNo'],
                'LinkProfile': request.data['LinkProfile'],
                # 'Alternateno': request.data['Alternateno'],
            }

            r = requests.post(settings.BASEURL+'/Login',data=json.dumps(settings.SAPDB), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)

            em_data = {
                "CardCode": request.data['CardCode'],
                "ContactEmployees": [
                    {
                        'Title': request.data['Title'],
                        'FirstName':request.data['FirstName'],
                        'MiddleName':request.data['MiddleName'],
                        'LastName':request.data['LastName'],
                        'Position':request.data['Position'],
                        'Address':request.data['Address'],
                        'MobilePhone':request.data['MobilePhone'],
                        'Fax':request.data['Fax'],
                        'E_Mail':request.data['E_Mail'],
                        'Remarks1':request.data['Remarks1'],
                        'InternalCode':request.data['InternalCode'],
                        'DateOfBirth':request.data['DateOfBirth'],
                        'Gender':request.data['Gender'],
                        'Profession':request.data['Profession'],
                        'CardCode':request.data['CardCode'],
                        'CreateDate':request.data['CreateDate'],
                        'CreateTime':request.data['CreateTime'],
                        'UpdateDate':request.data['UpdateDate'],
                        'UpdateTime':request.data['UpdateTime']
                    }
                ]
            }

            #print(em_data)
            print(json.dumps(em_data))
            # url = settings.BASEURL+"/BusinessPartners('"+model.CardCode+"')"
            url = settings.BASEURL+"/BusinessPartners('"+model.CardCode+"')"
            print(url)

            res = requests.patch(url, data=json.dumps(
                em_data), cookies=r.cookies, verify=False)

            if len(res.content) != 0:
                res1 = json.loads(res.content)
                SAP_MSG = res1['error']['message']['value']
                return Response({"message": "Partely successful", "status": "202", "SAP_error": SAP_MSG, "data": []})
            else:
                return Response({"message": "successful", "status": "200", "data": [context]})
        else:
            return Response({"message": "successful", "status": "200", "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": []})

#BPEmployee delete


@api_view(['POST'])
def delete(request):
    try:
        fetchid = request.data['id']
        fetchdata = BPEmployee.objects.filter(pk=fetchid).delete()
        return Response({"message": "successful", "status": "200", "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": []})
