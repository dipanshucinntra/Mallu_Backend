from django.conf import settings
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse

from Order.models import Order
from .forms import *  
from .models import *  
from Company.models import Branch  
from Lead.models import Lead
from Employee.models import *
from PaymentTermsTypes.models import PaymentTermsTypes

import requests, json

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from Company.serializers import *
from PaymentTermsTypes.serializers import PaymentTermsTypesSerializer
from Employee.serializers import EmployeeSerializer, TargetSerializer

from rest_framework.parsers import JSONParser

from datetime import date       #added by millan on 12-10-2022
# Create your views here.  

#BusinessPartner Create API
@api_view(['POST'])
def create(request):
    try:
        if request.data['EmailAddress'] != "":
            if BusinessPartner.objects.filter(EmailAddress=request.data['EmailAddress']).exists():
                return Response({"message":"Already exist "+str(request.data['EmailAddress']), "status":"409","data":[]})
        
        if request.data['Phone1'] != "":
            if BusinessPartner.objects.filter(Phone1=request.data['Phone1']).exists():
                return Response({"message":"Already exist "+str(request.data['Phone1']), "status":"409","data":[]})
        
        if BusinessPartner.objects.filter(CardName=request.data['CardName']).exists():
            return Response({"message":"Already exist Card Name","status":"409","data":[]})            
        else:
            try:
                CardName = request.data['CardName']
                Industry = request.data['Industry']
                CardType = request.data['CardType']
                Website = request.data['Website']
                EmailAddress = request.data['EmailAddress']
                Phone1 = request.data['Phone1']
                DiscountPercent = request.data['DiscountPercent']
                Currency = request.data['Currency']
                IntrestRatePercent = request.data['IntrestRatePercent']
                CommissionPercent = request.data['CommissionPercent']
                Notes = request.data['Notes']
                PayTermsGrpCode = request.data['PayTermsGrpCode']
                CreditLimit = request.data['CreditLimit']
                AttachmentEntry = request.data['AttachmentEntry']
                SalesPersonCode = request.data['SalesPersonCode']
                
                ContactPerson = request.data['ContactEmployees'][0]['Name']
                U_PARENTACC = request.data['U_PARENTACC']
                U_BPGRP = request.data['U_BPGRP']
                U_CONTOWNR = request.data['U_CONTOWNR']
                U_RATING = request.data['U_RATING']
                U_TYPE = request.data['U_TYPE']
                U_ANLRVN = request.data['U_ANLRVN']
                U_CURBAL = request.data['U_CURBAL']
                U_ACCNT = request.data['U_ACCNT']
                U_INVNO = request.data['U_INVNO']
                U_Landline = request.data['U_Landline']
                
                U_LEADID = request.data['U_LEADID']
                U_LEADNM = request.data['U_LEADNM']
                
                U_LAT = request.data['U_LAT']
                U_LONG = request.data['U_LONG']
                U_Zone = "North" #request.data['U_Zone']
                
                CreateDate = request.data['CreateDate']
                CreateTime = request.data['CreateTime']
                UpdateDate = request.data['UpdateDate']
                UpdateTime = request.data['UpdateTime']
                
                #added by millan on 27-09-2022
                category = request.data['category']
                intProdCat = request.data['intProdCat']
                intProjCat = request.data['intProjCat']
                #country = request.data['country']
                #country_code = request.data['country_code']
                #state = request.data['state']
                #state_code = request.data['state_code']
                #city = request.data['city']
                source=request.data['source']
                source_id=request.data['source_id']
                bpsource = request.data['bpsource']
                zone=request.data['zone']
                #added by millan on 27-09-2022
                
                CreatedBy = request.data['CreatedBy'] #added by millan on 10 October 2022 to get the name of employee who created customer
                
                # CustomerStatus=request.data['CustomerStatus'] #added by millan on 06-10-2022
                
                custCode = ""
                
                # if CustomerGroup.objects.filter(CustomerGroup=request.data['U_TYPE'].upper()).exists(): 
                #     custCode = CustomerGroup.objects.filter(CustomerGroup=request.data['U_TYPE'].upper()).values('Code')
                
                czone = zone.replace(" Zone", "")
                
                if CustomerZone.objects.filter(CustomerZone=czone).exists(): 
                    custZone = CustomerZone.objects.filter(CustomerZone=czone).values('Code')
                
                if custZone[0]['Code'] == 'E':
                    custZone = 'E1'
                elif custZone[0]['Code'] == 'W':
                    custZone = 'W2'
                elif custZone[0]['Code'] == 'N':
                    custZone = 'N3'
                elif custZone[0]['Code'] == 'S':
                    custZone = 'S4'
                else:
                    custZone = 'n/a'
                
                # BPCustCode = str(custCode[0]['Code']) + '/' + str(custZone)
                BPCustCode = ""
                
                model = BusinessPartner(CardName = CardName, Industry = Industry, CardType = CardType, Website = Website, EmailAddress = EmailAddress, Phone1 = Phone1, DiscountPercent = DiscountPercent, Currency = Currency, IntrestRatePercent = IntrestRatePercent, CommissionPercent = CommissionPercent, Notes = Notes, PayTermsGrpCode = PayTermsGrpCode, CreditLimit = CreditLimit, AttachmentEntry = AttachmentEntry, SalesPersonCode = SalesPersonCode, ContactPerson = request.data['ContactEmployees'][0]['Name'], U_PARENTACC = U_PARENTACC, U_BPGRP = U_BPGRP, U_CONTOWNR = U_CONTOWNR, U_RATING = U_RATING, U_TYPE = U_TYPE, U_ANLRVN = U_ANLRVN, U_CURBAL = U_CURBAL, U_ACCNT = U_ACCNT, U_INVNO = U_INVNO, U_Landline=U_Landline, U_LEADID=U_LEADID, U_LEADNM=U_LEADNM, U_LAT = U_LAT, U_LONG = U_LONG, CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime, category=category, intProdCat=intProdCat, intProjCat=intProjCat, source=source, source_id=source_id, bpsource=bpsource, zone=zone, CreatedBy=CreatedBy, BPCustCode = BPCustCode)
                
                #country=country, country_code=country_code, state=state, state_code=state_code, city=city, 
                
                model.save()
                bpl = Branch.objects.filter(id__in=request.data['BPLID'])
                print(bpl)
                model.BPLID.set(bpl)
                
                bp = BusinessPartner.objects.latest('id')
                CardCode = "CS"+str(format(bp.id, '05'))
                print(CardCode)
                bp.CardCode = CardCode
                bp.save()
                
                #added by millan on 11-10-2022
                if CustomerCode.objects.filter(cc_prefix=bp.BPCustCode).exists(): 
                    counter = CustomerCode.objects.filter(cc_prefix=bp.BPCustCode).order_by('-id')[:1][0].counter
                    
                    counter = int(counter) + 1
                    cmodel = CustomerCode(cc_prefix=bp.BPCustCode, counter=counter)                    
                    cmodel.save()
                else:
                    counter=1
                    cmodel = CustomerCode(cc_prefix=bp.BPCustCode, counter=counter)
                    cmodel.save()
                    
                id=counter
                lead_bpCode = format(id, '04')
                print(lead_bpCode)
                
                bp.BPCustCode = str(bp.BPCustCode) + str(lead_bpCode)
                
                bp.save()
                #added by millan on 11-10-2022
                
                brs = []
                
                for b in request.data['BPLID']:
                    text = {
                        "BPCode": CardCode,
                        "BPLID": b,
                        "DisabledForBP": "tNO"
                    }
                    brs.append(text)
                print(brs)
                
                #return Response({"message":brs,"SAP_error":"", "status":202,"data":[]})
                
                try:
                    bpemp = BPEmployee(U_BPID=bp.id, CardCode=CardCode, MobilePhone=request.data['ContactEmployees'][0]['MobilePhone'], FirstName=request.data['ContactEmployees'][0]['Name'], E_Mail=request.data['ContactEmployees'][0]['E_Mail'], Position=request.data['ContactEmployees'][0]['Position'], CreateDate=CreateDate, CreateTime=CreateTime, UpdateDate=UpdateDate, UpdateTime=UpdateTime)
                    
                    bpemp.save()
                    em = BPEmployee.objects.latest('id')
                    empid = em.id
                except Exception as e:
                    BusinessPartner.objects.get(pk=bp.id).delete()
                    return Response({"message":str(e),"status":201,"data":[{"Error":str(e)}]})
                
                if request.data['BPAddresses'][0]['AddressType']=='bo_BillTo' :
                    bpadd = request.data['BPAddresses'][0]
                    print(request.data['BPAddresses'][0]['AddressType'])
                    try:
                        model_add = BPAddresses(BPID=bp.id, AddressName = bpadd['AddressName'], Street = bpadd['Street'], Block = bpadd['Block'], ZipCode = bpadd['ZipCode'], City = bpadd['City'], Country = bpadd['Country'], AddressType = bpadd['AddressType'], RowNum=0, BPCode = CardCode, U_STATE = bpadd['U_STATE'], State = bpadd['State'], U_COUNTRY = bpadd['U_COUNTRY'], U_SHPTYP = bpadd['U_SHPTYP'], BillToRemark = bpadd['BillToRemark'])
                        model_add.save()
                        lastadd = BPAddresses.objects.latest('id')
                    except Exception as e:
                        BusinessPartner.objects.get(pk=bp.id).delete()
                        BPEmployee.objects.get(pk=em.id).delete()
                        return Response({"message":str(e),"status":201,"data":[{"Error":str(e)}]})    
                
                if request.data['BPAddresses'][1]['AddressType']=='bo_ShipTo' :
                    bpadd1 = request.data['BPAddresses'][1]
                    print(request.data['BPAddresses'][1]['AddressType'])
                    try:
                        model_br = BPBranch(BPID=bp.id, BranchName=CardName, AddressName = bpadd1['AddressName'], Street = bpadd1['Street'], Block = bpadd1['Block'], ZipCode = bpadd1['ZipCode'], City = bpadd1['City'], Country = bpadd1['Country'], AddressType = bpadd1['AddressType'], RowNum=1, BPCode = CardCode, U_STATE = bpadd1['U_STATE'], Default=1, State = bpadd1['State'], U_COUNTRY = bpadd1['U_COUNTRY'], U_SHPTYP = bpadd1['U_SHPTYP'], CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime, ShipToRemark = bpadd1['ShipToRemark'])
                        model_br.save()
                        
                        lastbr = BPBranch.objects.latest('id')
                        brid = lastbr.id
                        emp_obj = BPEmployee.objects.get(pk=empid)
                        emp_obj.U_BRANCHID = brid
                        emp_obj.save()
                        
                    except Exception as e:
                        BusinessPartner.objects.get(pk=bp.id).delete()
                        BPEmployee.objects.get(pk=em.id).delete()
                        BPAddresses.objects.get(pk=lastadd.id).delete()
                        return Response({"message":str(e),"status":201,"data":[{"Error":str(e)}]})    
                                    
                    

                if settings.SAPBP==True:
                    r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
                    token = json.loads(r.text)['SessionId']
                    print(token)
                    
                    addr = request.data['BPAddresses']
                    

                    addr[0].pop('U_SHPTYP')
                    addr[0].pop('U_COUNTRY')
                    addr[0].pop('U_STATE')
                    addr[0]['BPCode']=CardCode


                    addr[1].pop('U_SHPTYP')
                    addr[1].pop('U_COUNTRY')
                    addr[1].pop('U_STATE')
                    addr[1]['BPCode']=CardCode
                    

                    print(addr)
                    print(request.data['PayTermsGrpCode'])

                    bp_data = {
                            "CardCode": CardCode,
                            "CardName": request.data['CardName'],
                            "Industry": request.data['Industry'],
                            "Phone1": request.data['Phone1'],
                            "Website": request.data['Website'],
                            "CardType": request.data['CardType'],
                            "EmailAddress": request.data['EmailAddress'],
                            "SalesPersonCode": request.data['SalesPersonCode'],
                            "ContactPerson": request.data['ContactEmployees'][0]['Name'],
                            "DiscountPercent": request.data['DiscountPercent'],
                            "Currency": request.data['Currency'],
                            "IntrestRatePercent": request.data['IntrestRatePercent'],
                            "CommissionPercent": request.data['CommissionPercent'],
                            "PayTermsGrpCode": request.data['PayTermsGrpCode'],
                            "CreateDate": request.data['CreateDate'],
                            "CreateTime": request.data['CreateTime'],
                            "UpdateDate": request.data['UpdateDate'],
                            "UpdateTime": request.data['UpdateTime'],
                            "U_Zone":U_Zone,
                            "BPBranchAssignment": brs,
                            "ContactEmployees": [
                            {
                                "CardCode": CardCode,
                                "Name": request.data['ContactEmployees'][0]['Name'],
                                "MobilePhone": request.data['ContactEmployees'][0]['MobilePhone'],
                                "Position": request.data['ContactEmployees'][0]['Position']
                            }],
                            
                            "BPAddresses": addr
                            }

                    print(bp_data)
                    #return Response({"message":bp_data,"SAP_error":"", "status":202,"data":[]})
                    print(json.dumps(bp_data))

                    res = requests.post(settings.BASEURL+'/BusinessPartners', data=json.dumps(bp_data), cookies=r.cookies, verify=False)
                    live = json.loads(res.text)
                    print(live)
                    if "ContactEmployees" in live:
                        print("if")
                        InternalCode = live['ContactEmployees'][0]['InternalCode']            
                        bpmodel = BPEmployee.objects.get(id=em.id)
                        bpmodel.InternalCode = InternalCode
                        bpmodel.save()
                        """                    
                        if U_LEADID !=0:
                            leadObj = Lead.objects.get(pk=U_LEADID)
                            leadObj.BPStatus=1
                            leadObj.save()
                        print({"bp_id":bp.id, "CardCode":live['CardCode']})
                        """
                        return Response({"message":"successful","status":200,"data":[{"bp_id":bp.id, "CardCode":live['CardCode']}]})
                    else:
                        print("else")
                        BusinessPartner.objects.get(pk=bp.id).delete()
                        BPEmployee.objects.get(U_BPID=bp.id).delete()
                        BPBranch.objects.get(BPID=bp.id).delete()
                        BPAddresses.objects.get(BPID=bp.id).delete()
                        print(live['error']['message']['value'])
                        SAP_MSG = live['error']['message']['value']
                        print(SAP_MSG)
                        return Response({"message":SAP_MSG,"SAP_error":SAP_MSG, "status":202,"data":[]})
                else:
                    InternalCode = em.id
                    bpmodel = BPEmployee.objects.get(id=em.id)
                    bpmodel.InternalCode = InternalCode
                    bpmodel.save()
                    """                    
                    if U_LEADID !=0:
                        leadObj = Lead.objects.get(pk=U_LEADID)
                        leadObj.BPStatus=1
                        leadObj.save()
                    print({"bp_id":bp.id, "CardCode":live['CardCode']})
                    """
                    return Response({"message":"successful","status":200,"data":[{"bp_id":bp.id, "CardCode":CardCode}]})
            except Exception as e:
                return Response({"message":str(e),"status":201,"data":[{"Error":str(e)}]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[{"Error":str(e)}]})

#BusinessPartner All API
@api_view(["GET"])
def all(request):
    allbp = [];
    businesspartners_obj = BusinessPartner.objects.all().order_by("-id")
    for bp in businesspartners_obj:
        # Business Partner details obj
        bpObj = BusinessPartner.objects.get(pk=bp.id)
        bp_json = BusinessPartnerSerializer(bpObj)
        bpFinalObj = json.loads(json.dumps(bp_json.data))
        
        # Business Partner CreatedBy object added by millan on 10-10-2022
        if bpFinalObj['CreatedBy']!="":
            print(bpFinalObj['CreatedBy'])
            createdPerson = Employee.objects.filter(pk= bpFinalObj['CreatedBy'])
            createdPersonjson = EmployeeSerializer(createdPerson, many=True)
            print(createdPerson)
            bpFinalObj['CreatedBy'] = json.loads(json.dumps(createdPersonjson.data))
        else:
            bpFinalObj['CreatedBy'] = []
        
        # Business Partner Employee obj
        cont = BPEmployee.objects.filter(CardCode=bp.CardCode)
        cont_json = BPEmployeeSerializer(cont, many=True)
        # cont_all = json.loads(json.dumps(cont_json.data))
        bpFinalObj['ContactEmployees'] = json.loads(json.dumps(cont_json.data))

        # Business Partner contact person obj
        if len(cont) > 0:
           ContactPerson = cont[0].FirstName
           print(ContactPerson)
        else:
           ContactPerson = ""
           print(ContactPerson)
        
        bpFinalObj['ContactPerson'] = ContactPerson
        
        # BusinessPartner address obj
        bpaddr = BPAddresses.objects.filter(BPCode=bp.CardCode)
        bpaddr_json = BPAddressesSerializer(bpaddr, many=True)
        jss0 = json.loads(json.dumps(bpaddr_json.data))
        # bpFinalObj['BPAddresses'] = json.loads(json.dumps(bpaddr_json.data))
        
        # Business Partner Branch obj
        bpbr = BPBranch.objects.filter(BPCode=bp.CardCode,Default=1)
        bpbr_json = BPBranchSerializer(bpbr, many=True)
        jss1 = json.loads(json.dumps(bpbr_json.data))
        # bpFinalObj['BPBranch'] = json.loads(json.dumps(bpbr_json.data))

        bpFinalObj['BPAddresses'] = jss0+jss1

        
        # context = {
        #     'id':bp.id,
        #     'CardCode':bp.CardCode,
        #     'CardName':bp.CardName,
        #     'Industry':bp.Industry,
        #     'CardType':bp.CardType,
        #     'Website':bp.Website,
        #     'EmailAddress':bp.EmailAddress,
        #     'Phone1':bp.Phone1,
        #     'DiscountPercent':bp.DiscountPercent,
        #     'Currency':bp.Currency,
        #     'IntrestRatePercent':bp.IntrestRatePercent,
        #     'CommissionPercent':bp.CommissionPercent,
        #     'Notes':bp.Notes,
        #     'PayTermsGrpCode':bp.PayTermsGrpCode,
        #     'BPLID':bp.BPLID,
        #     'CreditLimit':bp.CreditLimit,
        #     'AttachmentEntry':bp.AttachmentEntry,
        #     'SalesPersonCode':bp.SalesPersonCode,
        #     'ContactPerson':ContactPerson,
        #     'U_PARENTACC':bp.U_PARENTACC,
        #     'U_BPGRP':bp.U_BPGRP,
        #     'U_CONTOWNR':bp.U_CONTOWNR,
        #     'U_RATING':bp.U_RATING,
        #     'U_TYPE':bp.U_TYPE,
        #     'U_ANLRVN':bp.U_ANLRVN,
        #     'U_CURBAL':bp.U_CURBAL,
        #     'U_ACCNT':bp.U_ACCNT,
        #     'U_INVNO':bp.U_INVNO,
        #     'U_LAT':bp.U_LAT,
        #     'U_LONG':bp.U_LONG,
        #     'CreateDate':bp.CreateDate,
        #     'CreateTime':bp.CreateTime,
        #     'UpdateDate':bp.UpdateDate,
        #     'UpdateTime':bp.UpdateTime,
        #     'ContactEmployees': cont_all,
        #     'BPAddresses':jss0+jss1
        #     }
            
        allbp.append(bpFinalObj)
        
    return Response({"message": "Success","status": 200,"data":allbp})

#BusinessPartner All API
@api_view(["GET"])
def all_sk(request):
    allbp = [];
    businesspartners_obj = BusinessPartner.objects.all().order_by("-id")
    for bp in businesspartners_obj:
        
        # Business Partner details obj
        bpObj = BusinessPartner.objects.get(pk=bp.id)
        bp_json = BusinessPartnerSerializer(bpObj)
        bpFinalObj = json.loads(json.dumps(bp_json.data))

        # Business Partner Employee obj
        cont = BPEmployee.objects.filter(CardCode=bp.CardCode)
        cont_json = BPEmployeeSerializer(cont, many=True)
        # cont_all = json.loads(json.dumps(cont_json.data))
        bpFinalObj['BPEmployee'] = json.loads(json.dumps(cont_json.data))

        # Business Partner contact person obj
        if len(cont) > 0:
           ContactPerson = cont[0].FirstName
           print(ContactPerson)
        else:
           ContactPerson = ""
           print(ContactPerson)
        
        bpFinalObj['ContactPerson'] = ContactPerson
        
        # BusinessPartner address obj
        bpaddr = BPAddresses.objects.filter(BPCode=bp.CardCode)
        bpaddr_json = BPAddressesSerializer(bpaddr, many=True)
        # jss0 = json.loads(json.dumps(bpaddr_json.data))
        bpFinalObj['BPAddresses'] = json.loads(json.dumps(bpaddr_json.data))
        
        # Business Partner Branch obj
        bpbr = BPBranch.objects.filter(BPCode=bp.CardCode,Default=1)
        bpbr_json = BPBranchSerializer(bpbr, many=True)
        # jss1 = json.loads(json.dumps(bpbr_json.data))
        bpFinalObj['BPBranch'] = json.loads(json.dumps(bpbr_json.data))
        
        allbp.append(bpFinalObj)
        
    return Response({"message": "Success","status": 200,"data":allbp})

#BusinessPartner All API
@api_view(["GET"])
def all_old(request):    
    businesspartners_obj = BusinessPartner.objects.all().order_by("-id")
    for bp in businesspartners_obj:
        bpaddr = BPAddresses.objects.filter(BPID=bp.id)
        bpaddr_json = BPAddressesSerializer(bpaddr, many=True)
        
        jss = json.loads(json.dumps(bpaddr_json.data))
        bp.U_BPADDRESS = jss
        
    businesspartner_json = BusinessPartnerSerializer(businesspartners_obj, many=True)
    return Response({"message": "Success","status": 200,"data":businesspartner_json.data})


#Branch by BP All API
@api_view(["POST"])
def branchbybp(request):    
    businesspartners_obj = BusinessPartner.objects.get(CardCode=request.data['CardCode'])
    businesspartner_json = BusinessPartnerSerializer(businesspartners_obj, many=False)
    #print(businesspartner_json.data['BPLID'])
    return Response({"message": "Success","status": 200,"data":businesspartner_json.data['BPLID']})

#BusinessPartner All API
@api_view(["GET"])
def all_bp(request):    
    businesspartners_obj = BusinessPartner.objects.all()
    businesspartners_json = BPSerializer(businesspartners_obj, many=True)
    return Response({"message": "Success","status": 200,"data":businesspartners_json.data})

#BusinessPartner One API
@api_view(["POST"])
def one(request):

    bpFinalObj = []

    # Business Partner details
    CardCode=request.data['CardCode']
    bp = BusinessPartner.objects.get(CardCode=CardCode)
    bp_json = BusinessPartnerSerializer(bp)
    bpFinalObj = json.loads(json.dumps(bp_json.data))
    
    # Business Partner Employee details
    cont = BPEmployee.objects.filter(CardCode=bp.CardCode)
    cont_json = BPEmployeeSerializer(cont, many=True)
    cont_all = json.loads(json.dumps(cont_json.data))
    bpFinalObj['ContactEmployees'] = cont_all
    
    # Business Partner CreatedBy object added by millan on 10-10-2022
    if bpFinalObj['CreatedBy']!="":
        print('ab')
        print(bpFinalObj['CreatedBy'])
        print('bc')
        createdPerson = Employee.objects.filter(pk= int(bpFinalObj['CreatedBy']))
        createdPersonjson = EmployeeSerializer(createdPerson, many=True)
        bpFinalObj['CreatedBy'] = json.loads(json.dumps(createdPersonjson.data))
    else:
        bpFinalObj['CreatedBy'] = []
    
    if Employee.objects.filter(SalesEmployeeCode=bp.SalesPersonCode).exists():
        spObj = Employee.objects.get(SalesEmployeeCode=bp.SalesPersonCode)
        spJson = EmployeeSerializer(spObj, many=False).data
        bpFinalObj['SalesPersonCode'] = spJson
    else:
        bpFinalObj['SalesPersonCode'] = []

    payObj = PaymentTermsTypes.objects.get(GroupNumber=bp.PayTermsGrpCode)
    payJson = PaymentTermsTypesSerializer(payObj, many=False).data
    
    bpFinalObj['PayTermsGrpCode'] = payJson

    print(cont_all)        
    if len(cont) > 0:
       ContactPerson = cont[0].FirstName
       print(ContactPerson)
    else:
       ContactPerson = ""
       print(ContactPerson)
    
    bpFinalObj['ContactPerson'] = ContactPerson

    # Business Partner Address details
    bpaddr = BPAddresses.objects.filter(BPID=bp.id)
    bpaddr_json = BPAddressesSerializer(bpaddr, many=True)
    jss0 = json.loads(json.dumps(bpaddr_json.data))
    # bpFinalObj['BPAddresses'] = jss0

    # Business Partner Branch details
    bpbr = BPBranch.objects.filter(BPCode=bp.CardCode,Default=1)
    bpbr_json = BPBranchSerializer(bpbr, many=True)
    jss1 = json.loads(json.dumps(bpbr_json.data))    
    # bpFinalObj['BPBranch'] = jss1
    bpFinalObj['BPAddresses'] = jss0+jss1

    # context = {
    #     'id':bp.id,
    #     'CardCode':bp.CardCode,
    #     'CardName':bp.CardName,
    #     'Industry':bp.Industry,
    #     'CardType':bp.CardType,
    #     'Website':bp.Website,
    #     'EmailAddress':bp.EmailAddress,
    #     'Phone1':bp.Phone1,
    #     'DiscountPercent':bp.DiscountPercent,
    #     'Currency':bp.Currency,
    #     'IntrestRatePercent':bp.IntrestRatePercent,
    #     'CommissionPercent':bp.CommissionPercent,
    #     'Notes':bp.Notes,
    #     'PayTermsGrpCode':bp.PayTermsGrpCode,
    #     'CreditLimit':bp.CreditLimit,
    #     'AttachmentEntry':bp.AttachmentEntry,
    #     'SalesPersonCode':bp.SalesPersonCode,
    #     'ContactPerson':ContactPerson,
    #     'BPLID':bp.BPLID,
    #     'U_PARENTACC':bp.U_PARENTACC,
    #     'U_BPGRP':bp.U_BPGRP,
    #     'U_CONTOWNR':bp.U_CONTOWNR,
    #     'U_RATING':bp.U_RATING,
    #     'U_TYPE':bp.U_TYPE,
    #     'U_ANLRVN':bp.U_ANLRVN,
    #     'U_CURBAL':bp.U_CURBAL,
    #     'U_ACCNT':bp.U_ACCNT,
    #     'U_INVNO':bp.U_INVNO,
    #     'U_LAT':bp.U_LAT,
    #     'U_LONG':bp.U_LONG,
    #     'CreateDate':bp.CreateDate,
    #     'CreateTime':bp.CreateTime,
    #     'UpdateDate':bp.UpdateDate,
    #     'UpdateTime':bp.UpdateTime,
    #     'ContactEmployees': cont_all,
    #     'BPAddresses':jss0+jss1
    #     }
        
    return Response({"message": "Success","status": 200,"data":[bpFinalObj]})

#BusinessPartner Update API
@api_view(['POST'])
def update(request):
    try:
        if request.data['EmailAddress'] != "":
            if BusinessPartner.objects.filter(EmailAddress=request.data['EmailAddress']).exclude(id=request.data['id']).exists():
                return Response({"message":"Already exist Email "+str(request.data['EmailAddress']), "status":"409","data":[]})
        if request.data['Phone1'] != "":
            if BusinessPartner.objects.filter(Phone1=request.data['Phone1']).exclude(id=request.data['id']).exists():
                return Response({"message":"Already exist Phone "+str(request.data['Phone1']), "status":"409","data":[]})
        
        if BusinessPartner.objects.filter(CardName=request.data['CardName']).exclude(id=request.data['id']).exists():
            return Response({"message":"Already exist Card Name","status":"409","data":[]})
        else:
            fetchid = request.data['id']
            model = BusinessPartner.objects.get(pk = fetchid)
            model.CardName = request.data['CardName']
            model.Industry = request.data['Industry']
            model.CardType = request.data['CardType']
            model.Website = request.data['Website']
            model.EmailAddress = request.data['EmailAddress']
            model.Phone1 = request.data['Phone1']
            model.DiscountPercent = request.data['DiscountPercent']
            model.Currency = request.data['Currency']
            model.IntrestRatePercent = request.data['IntrestRatePercent']
            model.CommissionPercent = request.data['CommissionPercent']
            model.Notes = request.data['Notes']
            model.PayTermsGrpCode = request.data['PayTermsGrpCode']
            model.CreditLimit = request.data['CreditLimit']
            model.AttachmentEntry = request.data['AttachmentEntry']
            # model.BPLID = request.data['BPLID']
            model.SalesPersonCode = request.data['SalesPersonCode']
            model.ContactPerson = request.data['ContactEmployees'][0]['Name']
            model.U_PARENTACC = request.data['U_PARENTACC']
            model.U_BPGRP = request.data['U_BPGRP']
            model.U_CONTOWNR = request.data['U_CONTOWNR']
            model.U_RATING = request.data['U_RATING']
            model.U_TYPE = request.data['U_TYPE']
            model.U_ANLRVN = request.data['U_ANLRVN']
            model.U_CURBAL = request.data['U_CURBAL']
            model.U_ACCNT = request.data['U_ACCNT']
            model.U_INVNO = request.data['U_INVNO']
            model.U_Landline = request.data['U_Landline']
            
            model.U_LAT = request.data['U_LAT']
            model.U_LONG = request.data['U_LONG']
            
            model.CreateDate = request.data['CreateDate']
            model.CreateTime = request.data['CreateTime']
            model.UpdateDate = request.data['UpdateDate']
            model.UpdateTime = request.data['UpdateTime']
            
            #added by millan on 27-09-2022
            model.category = request.data['category']
            model.intProdCat = request.data['intProdCat']
            model.intProjCat = request.data['intProjCat']
            #model.country = request.data['country']
            #model.country_code = request.data['country_code']
            #model.state = request.data['state']
            #model.state_code = request.data['state_code']
            #model.city = request.data['city']
            model.source=request.data['source']
            model.source_id=request.data['source_id']
            model.bpsource = request.data['bpsource']
            model.zone=request.data['zone']
            #added by millan on 27-09-2022
            # model.CustomerStatus=request.data['CustomerStatus']     #added by millan on 06-10-2022
            
            #done by millan on 17-10-2022 for updating customercode based on zone and groupcode
            custCode = ""
            # if CustomerGroup.objects.filter(CustomerGroup=request.data['U_TYPE'].upper()).exists(): 
            #     custCode = CustomerGroup.objects.filter(CustomerGroup=request.data['U_TYPE'].upper()).values('Code')
            
            czone = model.zone.replace(" Zone", "")
            
            if CustomerZone.objects.filter(CustomerZone=czone).exists(): 
                custZone = CustomerZone.objects.filter(CustomerZone=czone).values('Code')
                    
            if custZone[0]['Code'] == 'E':
                custZone = 'E1'
            elif custZone[0]['Code'] == 'W':
                custZone = 'W2'
            elif custZone[0]['Code'] == 'N':
                custZone = 'N3'
            elif custZone[0]['Code'] == 'S':
                custZone = 'S4'
            else:
                custZone = 'n/a'
            
            # BPCustCode = str(custCode[0]['Code']) + '/' + str(custZone)
            BPCustCode = ""
            
            if CustomerCode.objects.filter(cc_prefix=BPCustCode).exists(): 
                Cmodel = CustomerCode.objects.filter(cc_prefix=BPCustCode).order_by('-id')[:1][0]
                
                id=Cmodel.counter
                lead_bpCode = format(id, '04')
                
                ExstCustCode = str(Cmodel.cc_prefix) + str(lead_bpCode)
                if model.BPCustCode == ExstCustCode:
                    model.BPCustCode = model.BPCustCode
                else:                    
                    Cmodel.counter = int(Cmodel.counter) + 1
                    model.BPCustCode = ExstCustCode
                        
                Cmodel.save()
                    
                print(lead_bpCode)
                    
                model.BPCustCode = str(BPCustCode) + str(lead_bpCode)

            model.save()
            #done by millan on 17-10-2022 for updating customercode based on zone and groupcode
            
            print(request.data['BPLID'])
            
            bpl = Branch.objects.filter(id__in=request.data['BPLID'])
            print(bpl)
            model.BPLID.set(bpl)
            
            model_add = BPAddresses.objects.get(BPID = model.id)
            
            model_add.AddressName = request.data['BPAddresses'][0]['AddressName']
            model_add.Street = request.data['BPAddresses'][0]['Street']
            model_add.Block = request.data['BPAddresses'][0]['Block']
            model_add.City = request.data['BPAddresses'][0]['City']
            model_add.State = request.data['BPAddresses'][0]['State']
            model_add.ZipCode = request.data['BPAddresses'][0]['ZipCode']
            model_add.Country = request.data['BPAddresses'][0]['Country']

            model_add.U_SHPTYP = request.data['BPAddresses'][0]['U_SHPTYP']
            model_add.U_COUNTRY = request.data['BPAddresses'][0]['U_COUNTRY']
            model_add.U_STATE = request.data['BPAddresses'][0]['U_STATE']
            
            model_add.BillToRemark = request.data['BPAddresses'][0]['BillToRemark']   #added by millan on 29-09-2022
            
            model_add.save()
            
            bpemp = BPEmployee.objects.get(InternalCode = request.data['ContactEmployees'][0]['InternalCode'])
            
            bpemp.MobilePhone=request.data['ContactEmployees'][0]['MobilePhone']
            bpemp.FirstName=request.data['ContactEmployees'][0]['Name']
            bpemp.E_Mail=request.data['ContactEmployees'][0]['E_Mail']
            bpemp.UpdateDate=request.data['UpdateDate']
            bpemp.UpdateTime=request.data['UpdateTime']
            
            bpemp.save()        
            
            #print(bpemp)
            #return;        
            
            model_br = BPBranch.objects.get(BPCode = model.CardCode, Default=1)
            model_br.Default=0
            model_br.save()
            
            model_br = BPBranch.objects.get(pk = request.data['BPAddresses'][1]['id'])
            model_br.Default=1
            model_br.save()
                
            if settings.SAPBP==True:
                r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
                token = json.loads(r.text)['SessionId']
                print(token)

                # addr = request.data['BPAddresses']

                # addr[0].pop('id')
                # addr[0].pop('BPID')
                # addr[0].pop('U_SHPTYP')
                # addr[0].pop('U_COUNTRY')
                # addr[0].pop('U_STATE')

                # addr[1].pop('id')
                # addr[1].pop('BPID')
                # addr[1].pop('U_SHPTYP')
                # addr[1].pop('U_COUNTRY')
                # addr[1].pop('U_STATE')

                # print(addr)
                
                brs = []
                        
                for b in request.data['BPLID']:
                    text = {
                        "BPCode": model.CardCode,
                        "BPLID": b,
                        "DisabledForBP": "tNO"
                    }
                    brs.append(text)
                print(brs)

                bp_data = {
                        "CardName": request.data['CardName'],
                        "Industry": request.data['Industry'],
                        "Phone1": request.data['Phone1'],
                        "Website": request.data['Website'],
                        "CardType": request.data['CardType'],
                        "ContactPerson":request.data['ContactEmployees'][0]['Name'],
                        "EmailAddress": request.data['EmailAddress'],
                        "DiscountPercent": request.data['DiscountPercent'],
                        "Currency": request.data['Currency'],
                        "IntrestRatePercent": request.data['IntrestRatePercent'],
                        "CommissionPercent": request.data['CommissionPercent'],
                        "PayTermsGrpCode": request.data['PayTermsGrpCode'],
                        "CreateDate": request.data['CreateDate'],
                        "CreateTime": request.data['CreateTime'],
                        "UpdateDate": request.data['UpdateDate'],
                        "UpdateTime": request.data['UpdateTime'],
                        "BPBranchAssignment": brs,
                        "ContactEmployees": [
                        {
                            "InternalCode": request.data['ContactEmployees'][0]['InternalCode'],
                            "Name": request.data['ContactEmployees'][0]['Name'],
                            "MobilePhone": request.data['ContactEmployees'][0]['MobilePhone'],
                            "E_Mail": request.data['ContactEmployees'][0]['E_Mail']
                        }],
                        "BPAddresses": [
                            {
                            "BPCode": request.data['BPAddresses'][0]['BPCode'],
                            "RowNum": request.data['BPAddresses'][0]['RowNum'],
                            "AddressType": "bo_BillTo",
                            "AddressName": request.data['BPAddresses'][0]['AddressName'],
                            "Block": request.data['BPAddresses'][0]['Block'],
                            "Street": request.data['BPAddresses'][0]['Street'],
                            "ZipCode": request.data['BPAddresses'][0]['ZipCode'],
                            "City": request.data['BPAddresses'][0]['City'],
                            "State": request.data['BPAddresses'][0]['State'],
                            "Country": request.data['BPAddresses'][0]['Country']
                            }]
                        }
                
                print(json.dumps(bp_data))
            
                print(settings.BASEURL+"/BusinessPartners('"+model.CardCode+"')");
                res = requests.patch(settings.BASEURL+"/BusinessPartners('"+model.CardCode+"')", data=json.dumps(bp_data), cookies=r.cookies, verify=False)
                print(res.content)


                context = {
                        'id':request.data['id'],                
                        'CardCode':model.CardCode,
                        'CardName':request.data['CardName'],
                        'Industry':request.data['Industry'],
                        'CardType':request.data['CardType'],
                        'Website':request.data['Website'],
                        'EmailAddress':request.data['EmailAddress'],
                        'Phone1':request.data['Phone1'],
                        'DiscountPercent':request.data['DiscountPercent'],
                        'Currency':request.data['Currency'],
                        'IntrestRatePercent':request.data['IntrestRatePercent'],
                        'CommissionPercent':request.data['CommissionPercent'],
                        'Notes':request.data['Notes'],
                        'PayTermsGrpCode':request.data['PayTermsGrpCode'],
                        'CreditLimit':request.data['CreditLimit'],
                        'AttachmentEntry':request.data['AttachmentEntry'],
                        'SalesPersonCode':request.data['SalesPersonCode'],
                        'ContactPerson':request.data['ContactEmployees'][0]['Name'],
                        'U_PARENTACC':request.data['U_PARENTACC'],
                        'U_BPGRP':request.data['U_BPGRP'],
                        'U_CONTOWNR':request.data['U_CONTOWNR'],
                        'U_RATING':request.data['U_RATING'],
                        'U_TYPE':request.data['U_TYPE'],
                        'U_ANLRVN':request.data['U_ANLRVN'],
                        'U_CURBAL':request.data['U_CURBAL'],
                        'U_ACCNT':request.data['U_ACCNT'],
                        'U_INVNO':request.data['U_INVNO'],
                        'U_LAT':request.data['U_LAT'],
                        'U_LONG':request.data['U_LONG'],
                        'CreateDate':request.data['CreateDate'],
                        'CreateTime':request.data['CreateTime'],
                        'UpdateDate':request.data['UpdateDate'],
                        'UpdateTime':request.data['UpdateTime'],
                        "BPAddresses": request.data['BPAddresses']
                    }

                if len(res.content) !=0 :
                    res1 = json.loads(res.content)
                    SAP_MSG = res1['error']['message']['value']
                    return Response({"message":SAP_MSG,"status":202,"SAP_error":SAP_MSG, "data":[context]})
                else:
                    return Response({"message":"successful","status":200, "data":[context]})
            else:
                return Response({"message":"successful","status":200, "data":[request.data]})
    except Exception as e:
        #print(e)
        return Response({"message":str(e),"status":201,"data":[{"Error":str(e)}]})

#BusinessPartner delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        bp=BusinessPartner.objects.get(pk=fetchid)
        CardCode = bp.CardCode

        fetchdata=BusinessPartner.objects.filter(pk=fetchid).delete()
            
        addr=BPAddresses.objects.filter(BPID=fetchid)
        for add in addr:
            BPAddresses.objects.filter(BPID=add.BPID).delete()

        #print(data)
        if settings.SAPBP == True: 
            r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)
            # print(settings.BASEURL+"/BusinessPartners('"+CardCode+"')")
            
            try:
                res = requests.delete(settings.BASEURL+"/BusinessPartners('"+CardCode+"')", cookies=r.cookies, verify=False)
                print(res.content)
                
                return Response({"message":"successful","status":"200","data":[]})
            except:
                return Response({"message":"successful","status":"200","data":[]})        
        else:
            return Response({"message":"successful","status":"200","data":[]})
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

#added by millan on 12-10-2022 to get sales of each particular month based on sales employee code
@api_view(["POST"])
def monthlySales(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']        
            
        emp_obj = Employee.objects.get(SalesEmployeeCode=SalesPersonCode)
        print(emp_obj.role)
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=SalesPersonCode)#.values('id', 'SalesEmployeeCode')
            SalesPersonCode_arr=[]
            SalesPersonCode_arr.append(str(SalesPersonCode))
            for emp in emps:
                SalesPersonCode_arr.append(emp.SalesEmployeeCode)
            
        elif emp_obj.role == 'admin' or emp_obj.role == 'ceo':
            emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
            SalesPersonCode_arr=[]
            for emp in emps:
                SalesPersonCode_arr.append(emp.SalesEmployeeCode)
        else:
            SalesPersonCode_arr=[]
            SalesPersonCode_arr.append(str(SalesPersonCode))
        
        print("SalesPersonCode")
        print(SalesPersonCode_arr)
        SalesPersonCode_list = ",".join(SalesPersonCode_arr)
        print(SalesPersonCode_list)
        
        
        todays_date = date.today()
        CurrYr = todays_date.year
        NextYr = todays_date.year +1
        FinanYr = str(CurrYr) + '-' + str(NextYr)
        #monSales = []
        monSales = [
                {
                    "MonthlySales": 0,
                    "FinanYr": FinanYr,
                    "Month": str("Jan") + "-" + str(NextYr),
                    "MonthlyCount": 0,
                    "Year": 2023
                },
                {
                    "MonthlySales": 0,
                    "FinanYr": FinanYr,
                    "Month": str("Feb") + "-" + str(NextYr),
                    "MonthlyCount": 0,
                    "Year": 2023
                },
                {
                    "MonthlySales": 0,
                    "FinanYr": FinanYr,
                    "Month": str("Mar") + "-" + str(NextYr),
                    "MonthlyCount": 0,
                    "Year": 2023
                },
                {
                    "MonthlySales": 0,
                    "FinanYr": FinanYr,
                    "Month": str("Apr") + "-" + str(CurrYr),
                    "MonthlyCount": 0,
                    "Year": 2022
                },
                {
                    "MonthlySales": 0,
                    "FinanYr": FinanYr,
                    "Month": str("May") + "-" + str(CurrYr),
                    "MonthlyCount": 0,
                    "Year": 2022
                },
                {
                    "MonthlySales": 0,
                    "FinanYr": FinanYr,
                    "Month": str("Jun") + "-" + str(CurrYr),
                    "MonthlyCount": 0,
                    "Year": 2022
                },
                {
                    "MonthlySales": 0,
                    "FinanYr": FinanYr,
                    "Month": str("Jul") + "-" + str(CurrYr),
                    "MonthlyCount": 0,
                    "Year": 2022
                },
                {
                    "MonthlySales": 0,
                    "FinanYr": FinanYr,
                    "Month": str("Aug") + "-" + str(CurrYr),
                    "MonthlyCount": 0,
                    "Year": 2022
                },
                {
                    "MonthlySales": 0,
                    "FinanYr": FinanYr,
                    "Month": str("Sep") + "-" + str(CurrYr),
                    "MonthlyCount": 0,
                    "Year": 2022
                },
                {
                    "MonthlySales": 0,
                    "FinanYr": FinanYr,
                    "Month": str("Oct") + "-" + str(CurrYr),
                    "MonthlyCount": 2,
                    "Year": 2022
                },
                {
                    "MonthlySales": 0,
                    "FinanYr": FinanYr,
                    "Month": str("Nov") + "-" + str(CurrYr),
                    "MonthlyCount": 0,
                    "Year": 2022
                },
                {
                    "MonthlySales": 0,
                    "FinanYr": FinanYr,
                    "Month": str("Dec") + "-" + str(CurrYr),
                    "MonthlyCount": 0,
                    "Year": 2022
                }
                
            ]
        MonthlySales = MonthlyCount = 0
        if Order.objects.filter(SalesPersonCode__in = SalesPersonCode_arr).exists():
            
            sql_query = f"SELECT id, CreateDate, SUBSTR(CreateDate,1,7) monYr, Sum(DocTotal) as MonthlySales, Count(DocTotal) as MonthlyCount FROM `Order_order` where SalesPersonCode IN ({SalesPersonCode_list})  and (SUBSTR(CreateDate,1,4) IN ({CurrYr}, {NextYr})) group by monYr"
            print(sql_query)
            monsl = Order.objects.raw(sql_query)
            for desc in monsl:
                monthYear = desc.monYr.split('-')
                month = int(monthYear[1])
                print(month)
                nextyear = int(monthYear[0])+1
                if month == 1:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Jan") + "-" + str(nextyear)
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : NextYr})
                elif month == 2:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Feb") + "-" + str(nextyear)
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : NextYr})
                elif month == 3:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Mar") + "-" + str(nextyear)
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : NextYr})
                elif month == 4:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Apr") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                elif month == 5:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("May") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                elif month == 6:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Jun") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                elif month == 7:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Jul") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                elif month == 8:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Aug") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                elif month == 9:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Sep") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                elif month == 10:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Oct") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                elif month == 11:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Nov") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                elif month == 12:
                    MonthlySales = desc.MonthlySales
                    MonthlyCount = desc.MonthlyCount
                    Month = str("Dec") + "-" + str(monthYear[0])
                    monSales[month-1].update({"MonthlySales": MonthlySales, "FinanYr":FinanYr, "Month":Month, "MonthlyCount":MonthlyCount, "Year" : CurrYr})
                else:
                    print(month)
            
            monSales = ser(monSales)
            return Response({"message": "success","status": 200,"data":monSales})
        else:
            monSales = ser(monSales)
            return Response({"message": "SalesPersonCode Not Found","status": 201,"data":monSales})
    except Exception as e: 
        return Response({"message": "Error","status": 201,"data":str(e)})


def ser(arr):
    """x = arr[3:]
    y = arr[:3]
    z = x+y"""
    #print(arr[3:])# 3 to last =9
    #print("\n-------------\n")
    #print(arr[:3])# first to 3 = 3
    return arr[3:] + arr[:3]


#added by millan on 12-10-2022 to get target of each year based on Sales person and the decide target and achieved target in that financial year
@api_view(["POST"])
def employee_target(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']        
            
        emp_obj = Employee.objects.get(SalesEmployeeCode=SalesPersonCode)
        print(emp_obj.role)
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=SalesPersonCode)#.values('id', 'SalesEmployeeCode')
            SalesPersonCode_arr=[]
            SalesPersonCode_arr.append(str(SalesPersonCode))
            for emp in emps:
                SalesPersonCode_arr.append(emp.SalesEmployeeCode)
            
        elif emp_obj.role == 'admin' or emp_obj.role == 'ceo':
            emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
            SalesPersonCode_arr=[]
            for emp in emps:
                SalesPersonCode_arr.append(emp.SalesEmployeeCode)
        else:
            SalesPersonCode_arr=[]
            SalesPersonCode_arr.append(str(SalesPersonCode))
        
        print("SalesPersonCode")
        print(SalesPersonCode_arr)
        SalesPersonCode_list = ",".join(SalesPersonCode_arr)
        print(SalesPersonCode_list)
        
        todays_date = date.today()
        CurrYr = todays_date.year
        NextYr = todays_date.year +1
        FinanYr = str(CurrYr) + '-' + str(NextYr)
        
        fyTarget =[
                {
                    "MonthlyTargetSales": 0,
                    "Month":  str("Jan") + "-" + str(NextYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Feb") + "-" + str(NextYr) ,
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Mar") + "-" + str(NextYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },        
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Apr") + "-" + str(CurrYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("May") + "-" + str(CurrYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Jun") + "-" + str(CurrYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Jul") + "-" + str(CurrYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Aug") + "-" + str(CurrYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Sep") + "-" + str(CurrYr) ,
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Oct") + "-" + str(CurrYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Nov") + "-" + str(CurrYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                },
                {
                    "MonthlyTargetSales": 0,
                    "Month": str("Dec") + "-" + str(CurrYr),
                    "MonthlyAchievedSales": 0,
                    "FinancialYear": FinanYr
                }
                
            ]
        
        if Target.objects.filter(SalesPersonCode_id = SalesPersonCode).exists():
            
            sql_query = f"SELECT id, amount, Concat(SUBSTR(monthYear,6,7), '-', SUBSTR(monthYear,1,4)) as monYr, monthYear FROM Employee_target where SalesPersonCode_id = {SalesPersonCode} and (SUBSTR(monthYear,1,4) IN ({CurrYr}, {NextYr}) ) "
            print(sql_query)
            
            fytgt = Target.objects.raw(sql_query)
            for fyt in fytgt:
                month = int(fyt.monthYear.split('-')[1])
                fyTarget[month-1]['MonthlyTargetSales'] = fyt.amount
                    
        if Order.objects.filter(SalesPersonCode__in = SalesPersonCode_arr).exists():
            
            #sql_query_ord = f"SELECT Distinct(id), SUM(DocTotal) as OrderAchieved, SUBSTR(CreateDate,1,7) as monYr FROM Order_order where SalesPersonCode = {SalesPersonCode} and (SUBSTR(CreateDate,1,4) IN ({CurrYr}, {NextYr})) and CancelStatus = 'csNo' "
            
            sql_query_ord = f"SELECT id, sum(DocTotal) as OrderAchieved, SUBSTR(CreateDate,1,7) as monYr, SUBSTR(CreateDate,6,2) as month FROM Order_order where SalesPersonCode IN ({SalesPersonCode_list}) and (SUBSTR(CreateDate,1,4) IN ({CurrYr}, {NextYr})) and CancelStatus = 'csNo' group by SUBSTR(CreateDate,6,2);"
            
            print(sql_query_ord)
            
            ord_sl = Order.objects.raw(sql_query_ord)            
            
            for ord in ord_sl:
                fyTarget[int(ord.month)-1]['MonthlyAchievedSales'] = ord.OrderAchieved
                
            fyTarget = ser(fyTarget)
            return Response({"message": "success","status": 200,"data":fyTarget})
        else:
            fyTarget = ser(fyTarget)
            return Response({"message": "SalesPersonCode Not Found","status": 201,"data":fyTarget})

    except Exception as e:
        return Response({"message": "Error","status": 201,"data":str(e)})
    
#added by millan on 13-10-2022 to get annual target, achieved target and order placed in a finanical year 
@api_view(["POST"])
def target_anu_ach(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']        
            
        emp_obj = Employee.objects.get(SalesEmployeeCode=SalesPersonCode)
        print(emp_obj.role)
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=SalesPersonCode)#.values('id', 'SalesEmployeeCode')
            SalesPersonCode_arr=[]
            SalesPersonCode_arr.append(str(SalesPersonCode))
            for emp in emps:
                SalesPersonCode_arr.append(emp.SalesEmployeeCode)
            
        elif emp_obj.role == 'admin' or emp_obj.role == 'ceo':
            emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
            SalesPersonCode_arr=[]
            for emp in emps:
                SalesPersonCode_arr.append(emp.SalesEmployeeCode)
        else:
            SalesPersonCode_arr=[]
            SalesPersonCode_arr.append(str(SalesPersonCode))
        
        print("SalesPersonCode")
        print(SalesPersonCode_arr)
        SalesPersonCode_list = ",".join(SalesPersonCode_arr)
        print(SalesPersonCode_list)
        
        #{"SalesPersonCode":105}
        todays_date = date.today()
        CurrYr = todays_date.year
        NextYr = todays_date.year +1
        FinanYr = str(CurrYr) + '-' + str(NextYr)
        
        TargetFyYr = []
        if Targetyr.objects.filter(SalesPersonCode_id = SalesPersonCode).exists():
            sql_query = f"SELECT id, Sum(YearTarget) YearTarget FROM Employee_targetyr where SalesPersonCode_id = {SalesPersonCode} and StartYear={CurrYr} and EndYear={NextYr}"
            print(sql_query)
            fysl = Targetyr.objects.raw(sql_query)
            print(fysl)
            
            sql_query_ord = f"SELECT id, SUM(NetTotal) AchievedTarget,  Count(CancelStatus) ConfirmedOrder FROM Order_order where SalesPersonCode in ({SalesPersonCode_list}) and (SUBSTR(CreateDate,1,4) IN ({CurrYr})) and CancelStatus = 'csNo' "
            ord_sl = Order.objects.raw(sql_query_ord)
            
            #for fy in fysl:
                
            finalfy = {
                "AnnualTarget": fysl[0].YearTarget,
                "AchievedTarget": 0,
                "ConfirmedOrder": 0,
                "FinancialYear": FinanYr,
            }
                
            for ord in ord_sl:
                finalfy['AchievedTarget'] = ord.AchievedTarget
                finalfy['ConfirmedOrder'] = ord.ConfirmedOrder
                    
                TargetFyYr.append(finalfy)
            return Response({"message": "success","status": 200,"data":TargetFyYr})
        else:
            TargetFyYr = [ 
                {
                    "AnnualTarget": 0,
                    "AchievedTarget": 0,
                    "ConfirmedOrder": 0,
                    "FinancialYear": FinanYr
                }
            ]       
            return Response({"message": "SalesPersonCode Not Found","status": 200,"data":TargetFyYr})
    except Exception as e:
        return Response({"message": "Error","status": 201,"data":str(e)})

#added by millan on 13-10-2022 to get annual target, achieved target and order placed in a finanical year 
@api_view(["POST"])
def target_anu_ach_bkp(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']
        todays_date = date.today()
        CurrYr = todays_date.year
        NextYr = todays_date.year +1
        FinanYr = str(CurrYr) + '-' + str(NextYr)
        TargetFyYr = []
        if Target.objects.filter(SalesPersonCode_id = SalesPersonCode).exists():
            sql_query = f"SELECT id, Sum(amount) AnnualTarget FROM Employee_target where SalesPersonCode_id = {SalesPersonCode} and (SUBSTR(monthYear,1,4) IN ({CurrYr}, {NextYr}) )"
            fysl = Target.objects.raw(sql_query)
            
            sql_query_ord = f"SELECT id, SUM(NetTotal) AchievedTarget,  Count(CancelStatus) ConfirmedOrder FROM Order_order where SalesPersonCode = {SalesPersonCode} and (SUBSTR(CreateDate,1,4) IN ({CurrYr})) and CancelStatus = 'csNo' "
            ord_sl = Order.objects.raw(sql_query_ord)
            
            for fy in fysl:
                
                finalfy = {
                    "AnnualTarget": fy.AnnualTarget,
                    "AchievedTarget": 0,
                    "ConfirmedOrder": 0,
                    "FinancialYear": FinanYr,
                }
                
                for ord in ord_sl:
                    finalfy['AchievedTarget'] = ord.AchievedTarget
                    finalfy['ConfirmedOrder'] = ord.ConfirmedOrder
                        
                    TargetFyYr.append(finalfy)
            return Response({"message": "success","status": 200,"data":TargetFyYr})
        else:
            TargetFyYr = [ 
                {
                    "AnnualTarget": 0,
                    "AchievedTarget": 0,
                    "ConfirmedOrder": 0,
                    "FinancialYear": FinanYr
                }
            ]       
            return Response({"message": "SalesPersonCode Not Found","status": 200,"data":TargetFyYr})
    except Exception as e:
        return Response({"message": "Error","status": 201,"data":str(e)})

#added by millan on 01-November-2022 for fetching businesspartner employee without condition
#BusinessPartner All API

@api_view(["GET"])
def all_bpEmployee(request):    
    bpEmp_obj = BPEmployee.objects.all()
    allbpEmp =[]
    
    for emp in bpEmp_obj:
        bpEmp_json = BPEmployeeSerializer(emp)
        
        bpEmp = json.loads(json.dumps(bpEmp_json.data))
        
        if emp.CardCode != "":
            if BusinessPartner.objects.filter(CardCode=emp.CardCode).exists():
                bp_cardName = BusinessPartner.objects.get(CardCode=emp.CardCode)
                
                bpEmp['CardName'] = bp_cardName.CardName
            else:
                bpEmp['CardName'] = []    
        else:
            bpEmp['CardName'] = []
        
        allbpEmp.append(bpEmp)
    return Response({"message": "Success","status": 200,"data":allbpEmp})   
