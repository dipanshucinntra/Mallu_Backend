import calendar
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from camp_fun import sendMail
from .forms import LeadForm  
from .models import *
from Employee.models import Employee  
from Opportunity.models import *
from Campaign.models import *
import json

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser
# Create your views here.  

from datetime import datetime, timedelta, date

#added by millan for multi image store on 21-09-2022
from Attachment.models import Attachment
from Attachment.serializers import AttachmentSerializer
import os
from django.core.files.storage import FileSystemStorage

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")

print("Today date is: ", currentDate)
print("Today day is: ", currentDay)
print("Today Current time: ", currentTime)


#Lead Create API
@api_view(['POST'])
def create(request):
    print(request)
    try:
        leads = request.data
        print(leads)
        print(request.FILES)
        log = []
        log_msg = ""
        i=0
        # for lead in leads:
        date=leads['date']
        location=leads['location']
        companyName=leads['companyName'].lower()
        numOfEmployee = leads['numOfEmployee']
        turnover = leads['turnover']
        source=leads['source']
        source_id=leads['source_id']
        contactPerson=leads['contactPerson']
        designation=leads['designation']
        phoneNumber=leads['phoneNumber']
        message=leads['message']
        email=leads['email']
        productInterest=leads['productInterest']
        assignedTo_id=leads['assignedTo']
        employeeId_id=leads['employeeId']
        timestamp=leads['timestamp']
        status=leads['status']
        tender=leads['tender']
        DivCode=leads['DivCode']
        DivName=leads['DivName']
        leadType=leads['leadType']

        category = leads['category']
        groupType = leads['groupType']
        intProdCat = leads['intProdCat']
        intProjCat = leads['intProjCat']
        country = leads['country']
        country_code = leads['country_code']
        state = leads['state']
        state_code = leads['state_code']
        city = leads['city']
        
        #added by millan on 21-September-2022 for image upload
        Attach = leads['Attach'] 
        Caption = leads['Caption']
        
        print(companyName) 
        #.filter(companyName=companyName.lower()).exclude()
        if (phoneNumber=="" or companyName=="" or contactPerson==""):
            return Response({"message":"Mobile or Person or Company required","status":"201","data":[]})            
        if Lead.objects.filter(phoneNumber=phoneNumber).exists():
            log.append("This Mobile number already exists: "+str(phoneNumber))
        #elif Lead.objects.filter(email=email).exists():
            #log.append("This Email already exists: "+str(email))
        elif Lead.objects.filter(companyName=companyName).exclude(companyName="n/a").exists():
            log.append("This Company already exists: "+str(companyName))
        elif Lead.objects.filter(companyName=companyName).filter(contactPerson=contactPerson).exclude(companyName="n/a").exists():
            log.append("This ContactPerson already exists: "+contactPerson)
        else:
            model=Lead(date=date, DivCode=DivCode, DivName=DivName, tender=tender, location=location, companyName=leads['companyName'], numOfEmployee=numOfEmployee, turnover=turnover, source=source, source_id=source_id, contactPerson=contactPerson, designation=designation, phoneNumber=phoneNumber, message=message, email=email, status=status, leadType=leadType, productInterest=productInterest, assignedTo_id=assignedTo_id, employeeId_id=employeeId_id, timestamp=timestamp, category = category,groupType = groupType,intProdCat = intProdCat,intProjCat = intProjCat,country = country,country_code = country_code,state = state,state_code = state_code,city = city)
            model.save()
            
            LeadID = Lead.objects.latest('id')
            
            # print(LeadID.id)

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # after creating lead mail alert to reporting person
            # if assignedTo_id != "":
            #     empObj = Employee.objects.get(pk = assignedTo_id)
            #     empFirstName = empObj.firstName
            #     empEmail = empObj.Email
            #     mailSubject = "List of Leads for FollowUp, and List of New Leads"
            #     # mailMessage = f"Hi Sir/Mam <b>{empFirstName}</b> you have new assigned Lead {companyName}"
            #     mailMessage = f"""
            #         <div>
            #             Hi Sir/Mam <b>{empFirstName}</b>,<br><br>
            #             You'r assigned lead list are: <br><br>
            #         </div>
            #         <table style="width: 100%">
            #         <tr>
            #             <th>Lead Id</th>
            #             <th>Company Name</th>
            #             <th>Contact Person</th>
            #             <th>Phone Number</th>
            #             <th>Source</th>
            #             <th>Group Type</th>
            #             <th>Interested in Product Category </th>
            #             <th>Interested in Project Category </th>
            #             <th>Zone Stage</th>
            #         </tr>
            #         <tr>
            #             <td>{model.id}</td>
            #             <td>{model.companyName}</td>
            #             <td>{model.contactPerson}</td>
            #             <td>{model.phoneNumber}</td>
            #             <td>{model.source}</td>
            #             <td>{model.groupType}</td>
            #             <td>{model.intProdCat}</td>
            #             <td>{model.intProjCat}</td>
            #             <td>{model.location}</td>
            #         </tr>
            #         </table>"""
            #     mailAttachments = ""
            #     mailResponse = sendMail(toEmail= empEmail, subject = mailSubject, message = mailMessage, attachments = mailAttachments)
            #     print(mailResponse)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            
            date_time = (timestamp.strip()).split(" ")
            
            print(request.FILES.getlist('Attach'))
            # for multi image upload added by millan on 21-09-2022
            # print(request.FILES.getlist('Attach'))
            for File in request.FILES.getlist('Attach'):
                attachmentsImage_url = ""
                target ='./bridge/static/image/Attachment'
                os.makedirs(target, exist_ok=True)
                fss = FileSystemStorage()
                file = fss.save(target+"/"+File.name, File)
                productImage_url = fss.url(file)
                attachmentsImage_url = productImage_url.replace('/bridge', '')
                
                # print(attachmentsImage_url)
                
                FileName = File.name #added by millan on 17-10-2022 for storing file name

                # att=Attachment(File=attachmentsImage_url, Caption=Caption, LinkType="Lead", LinkID=LeadID.id, CreateDate=leads['date'], CreateTime = date_time[1] + " " + date_time[2], UpdateDate=leads['date'], UpdateTime=date_time[1] + " " + date_time[2], FileName = FileName)
                att=Attachment(File=attachmentsImage_url, Caption=Caption, LinkType="Lead", LinkID=LeadID.id, CreateDate=leads['date'], CreateTime = currentTime, UpdateDate=leads['date'], UpdateTime = currentTime, FileName = FileName)
                # att=Attachment(File=attachmentsImage_url, Caption=Caption, LinkType="Lead", LinkID=LeadID.id, CreateDate=leads['date'], CreateTime=date_time[1] + " " + date_time[2], UpdateDate=leads['date'], UpdateTime=date_time[1] + " " + date_time[2])
            
                att.save()
            
                
            if source =='Facebook':
                temp = "FCBK/L"
            elif source =='Linkedin':
                temp = "LIND/L"
            elif source =='Instagram':
                temp = "INST/L"
            elif source =='Website':
                temp = "WBST/L"
            elif source =='Whatsapp':
                temp = "WHAP/L"
            elif source =='Emailer':
                temp = "EMLR/L"
            elif source =='Event':
                temp = "EVNT/L"
            else:
                temp = "EXTR/L"
            model.code = str(temp+str(LeadID.id))
            model.save()
            i=i+1
            print(LeadID.id)

            if len(leads['LeadItem']) == 0:
                if len(log) > 0:
                    log_msg = "\r\n".join(log)
                    print(log_msg)
                    #log_msg = str(log)
                else:
                    log_msg = 'successful'
                if len(leads) == i:
                    return Response({"message":log_msg,"status":"200","data":[]})

            else:
                lines = json.loads(leads['LeadItem'])
                LineNum = 0
                if len(lines)!=0 and lines != "":
                    for line in lines:
                        try:
                            model_lines = LeadItem(LineNum = LineNum, LeadID = LeadID.id, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'], U_FGITEM = line['U_FGITEM'], CostingCode2 = line['CostingCode2'], ProjectCode = line['ProjectCode'], FreeText = line['FreeText'])
                            model_lines.save()
                            LineNum=LineNum+1
                        except Exception as e:
                            Attachment.objects.filter(LinkID=LeadID.id, LinkType='Lead').delete()
                            Lead.objects.filter(pk=LeadID.id).delete()
                            leadItems = LeadItem.objects.filter(LeadID=LeadID.id)
                            for item in leadItems:
                                item.delete()
                                if len(leads) == i:
                                    #return Response({"message":log_msg,"status":"200","data":[]})
                                    return Response({"message":str(e),"status":"202","data":[]})


        print(log)
        if len(log) > 0:
            log_msg = "\r\n".join(log)
            print(log_msg)
            #log_msg = str(log)
        else:
            log_msg = 'successful'
        return Response({"message":log_msg,"status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

#Lead Mark Junk
@api_view(['POST'])
def mark_junk(request):
    fetchids=request.data['id']
    status=request.data['status']
    naid = []
    for fetchid in fetchids:
        print(fetchid)
        if Lead.objects.filter(pk=fetchid).exists():
           fetchdata=Lead.objects.filter(pk=fetchid).update(junk=status)
        else:
            naid.append(fetchid)
    print(str(naid))
    return Response({"message":"successful","status":"200","data":[]})

#Lead Chat Create API
@api_view(['POST'])
def chatter(request):
    try:
        Message = request.data['Message']
        Lead_Id = request.data['Lead_Id']
        Emp_Id = request.data['Emp_Id']
        Emp_Name = request.data['Emp_Name']
        UpdateDate = request.data['UpdateDate']
        UpdateTime = request.data['UpdateTime']

        model = Chatter(Message=Message, Lead_Id=Lead_Id, Emp_Id=Emp_Id, Emp_Name=Emp_Name, UpdateDate=UpdateDate, UpdateTime=UpdateTime)
        
        model.save()
        chat = Chatter.objects.latest('id')
        print(chat.id)
        return Response({"message":"Success","status":200,"data":[{"id":chat.id}]})
    except Exception as e:
        return Response({"message":"Can not create","status":201,"data":[str(e)]})

#Chatter All API
@api_view(["POST"])
def chatter_all(request):
    Lead_Id=request.data['Lead_Id']
    print(Lead_Id)
    chat_obj = Chatter.objects.filter(Lead_Id=Lead_Id).order_by("id")
    chat_json = ChatterSerializer(chat_obj, many=True)
    return Response({"message": "Success","status": 200,"data":chat_json.data})

#Lead All API
@api_view(["GET"])
def all(request):
    leads_obj = Lead.objects.all()        
    #lead_json = LeadSerializer(leads_obj, many=True)
    
    # date_time = (leads_obj.timestamp).split(" ")
    
    
    allld = []
    for obj in leads_obj:
        lead_json = LeadSerializer(obj, many=False)
        lead_json_dump = json.loads(json.dumps(lead_json.data))
        items = LeadItem.objects.filter(LeadID = obj.id)
        item_json = LeadItemSerializer(items, many=True)
        lead_json_dump['LeadItem'] = item_json.data
        allld.append(lead_json_dump)
    return Response({"message": "Success","status": 200,"data":allld})


# {"leadType": "All", "assignedTo": "1"}
#Lead All Filter API
@api_view(["POST"])
def all_filter(request):
    json_data = request.data
    if len(json_data)==1:   #for pagination
        if json_data['assignedTo']!="":
            print('in first condition')
            SalesPersonID = json_data['assignedTo']
            
            emp_obj = Employee.objects.get(pk=SalesPersonID)
            
            if emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                SalesPersonID=[SalesPersonID]
                for emp in emps:
                    SalesPersonID.append(emp.id)
                
            elif emp_obj.role == 'admin' or emp_obj.role == 'ceo':
                emps = Employee.objects.filter(id__gt=0)
                SalesPersonID=[]
                for emp in emps:
                    SalesPersonID.append(emp.id)
            else:
                SalesPersonID = [json_data['assignedTo']]
            
            print(SalesPersonID)
        
        if len(json_data) == 0:
            print('all lead')
            leads_obj = Lead.objects.all(junk=0).order_by("-id")
            leads_json = LeadSerializer(leads_obj, many=True)
            return Response({"message": "Success","status": 200,"data":leads_json.data})
        else:
            print('by filter employee details')
            print(json_data.keys())
            #print(json_data.keys()[0])
            #if json_data['U_FAV']
            allld = []
            for ke in json_data.keys():
                print(ke)
                if ke =='assignedTo' :
                    if json_data['assignedTo'] !='':
                        leads_obj = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID).order_by("-id")
                        if len(leads_obj) ==0:
                            return Response({"message": "Success","status": 200,"data":[]})
                        else:
                            # allld = []
                            for obj in leads_obj:
                                lead_json = LeadSerializer(obj, many=False)
                                lead_json_dump = json.loads(json.dumps(lead_json.data))
                                items = LeadItem.objects.filter(LeadID = obj.id)
                                item_json = LeadItemSerializer(items, many=True)
                                lead_json_dump['LeadItem'] = item_json.data
                                #added by millan on 22-September-2022
                                image = Attachment.objects.filter(LinkID = obj.id, LinkType='Lead')
                                image_json = AttachmentSerializer(image, many=True)
                                lead_json_dump['Attach'] = image_json.data
                                #added by millan on 22-September-2022
                                allld.append(lead_json_dump)
                            # return Response({"message": "Success","status": 200,"data":allld})
                elif ke =='employeeId':
                    if json_data['employeeId'] !='':
                        leads_obj = Lead.objects.filter(junk=0,employeeId=json_data['employeeId']).order_by("-id")
                        
                        if len(leads_obj) ==0:
                            return Response({"message": "Success","status": 200,"data":[]})
                        else:
                            # allld = []
                            for obj in leads_obj:
                                lead_json = LeadSerializer(obj, many=False)
                                lead_json_dump = json.loads(json.dumps(lead_json.data))
                                items = LeadItem.objects.filter(LeadID = obj.id)
                                item_json = LeadItemSerializer(items, many=True)
                                lead_json_dump['LeadItem'] = item_json.data
                                #added by millan on 22-September-2022
                                attach = Attachment.objects.filter(LinkID = obj.id, LinkType='Lead')
                                image_json = AttachmentSerializer(image, many=True)
                                lead_json_dump['Attach'] = image_json.data
                                #added by millan on 22-September-2022
                                allld.append(lead_json_dump)
                            # return Response({"message": "Success","status": 200,"data":allld})
                    # else:
                    #     return Response({"message": "Success","status": 200,"data":[]})
            return Response({"message": "Success","status": 200,"data":allld})
    else:
        print('called')
        PageNo = json_data['PageNo']
        try:
            MaxItem = json_data['MaxItem']
        except:
            MaxItem = 10
        endWith = (PageNo * MaxItem)
        startWith = (endWith - MaxItem)
        if json_data['assignedTo']!="":
            print('in first condition')
            SalesPersonID = json_data['assignedTo']
            
            emp_obj = Employee.objects.get(pk=SalesPersonID)
            
            if emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                SalesPersonID=[SalesPersonID]
                for emp in emps:
                    SalesPersonID.append(emp.id)
                
            elif emp_obj.role == 'admin' or emp_obj.role == 'ceo':
                emps = Employee.objects.filter(id__gt=0)
                SalesPersonID=[]
                for emp in emps:
                    SalesPersonID.append(emp.id)
            else:
                SalesPersonID = [json_data['assignedTo']]
            
            print(SalesPersonID)
        
        if len(json_data) == 0:
            print('all lead')
            leads_obj = Lead.objects.all(junk=0).order_by("-id")
            leads_json = LeadSerializer(leads_obj, many=True)
            return Response({"message": "Success","status": 200,"data":leads_json.data})
        else:
            print('by filter employee details')
            print(json_data.keys())
            #print(json_data.keys()[0])
            #if json_data['U_FAV']
            allld = []
            if json_data['assignedTo'] !='':
                        leads_obj = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID).order_by("-id")[startWith:endWith]
                        if len(leads_obj) ==0:
                            return Response({"message": "Success","status": 200,"data":[]})
                        else:
                            # allld = []
                            for obj in leads_obj:
                                lead_json = LeadSerializer(obj, many=False)
                                lead_json_dump = json.loads(json.dumps(lead_json.data))
                                items = LeadItem.objects.filter(LeadID = obj.id)
                                item_json = LeadItemSerializer(items, many=True)
                                lead_json_dump['LeadItem'] = item_json.data
                                #added by millan on 22-September-2022
                                image = Attachment.objects.filter(LinkID = obj.id, LinkType='Lead')
                                image_json = AttachmentSerializer(image, many=True)
                                lead_json_dump['Attach'] = image_json.data
                                #added by millan on 22-September-2022
                                allld.append(lead_json_dump)
                            return Response({"message": "Success","status": 200,"data":allld})



            # for ke in json_data.keys():
            #     print(ke)
            #     if ke =='assignedTo' :
            #         if json_data['assignedTo'] !='':
            #             leads_obj = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID).order_by("-id")[startWith:endWith]
            #             if len(leads_obj) ==0:
            #                 return Response({"message": "Success","status": 200,"data":[]})
            #             else:
            #                 # allld = []
            #                 for obj in leads_obj:
            #                     lead_json = LeadSerializer(obj, many=False)
            #                     lead_json_dump = json.loads(json.dumps(lead_json.data))
            #                     items = LeadItem.objects.filter(LeadID = obj.id)
            #                     item_json = LeadItemSerializer(items, many=True)
            #                     lead_json_dump['LeadItem'] = item_json.data
            #                     #added by millan on 22-September-2022
            #                     image = Attachment.objects.filter(LinkID = obj.id, LinkType='Lead')
            #                     image_json = AttachmentSerializer(image, many=True)
            #                     lead_json_dump['Attach'] = image_json.data
            #                     #added by millan on 22-September-2022
            #                     allld.append(lead_json_dump)
            #                 # return Response({"message": "Success","status": 200,"data":allld})
            #     elif ke =='employeeId' :
            #         if json_data['employeeId'] !='':
            #             leads_obj = Lead.objects.filter(junk=0,employeeId=json_data['employeeId']).order_by("-id")[startWith:endWith]
                        
            #             if len(leads_obj) ==0:
            #                 return Response({"message": "Success","status": 200,"data":[]})
            #             else:
            #                 # allld = []
            #                 for obj in leads_obj:
            #                     lead_json = LeadSerializer(obj, many=False)
            #                     lead_json_dump = json.loads(json.dumps(lead_json.data))
            #                     items = LeadItem.objects.filter(LeadID = obj.id)
            #                     item_json = LeadItemSerializer(items, many=True)
            #                     lead_json_dump['LeadItem'] = item_json.data
            #                     #added by millan on 22-September-2022
            #                     attach = Attachment.objects.filter(LinkID = obj.id, LinkType='Lead')
            #                     image_json = AttachmentSerializer(image, many=True)
            #                     lead_json_dump['Attach'] = image_json.data
            #                     #added by millan on 22-September-2022
            #                     allld.append(lead_json_dump)
            #                 # return Response({"message": "Success","status": 200,"data":allld})
            #         # else:
            #         #     return Response({"message": "Success","status": 200,"data":[]})
            # return Response({"message": "Success","status": 200,"data":allld})


#Lead All Filter API
@api_view(["POST"])
def count_all(request):
    json_data = request.data
    if json_data['assignedTo']!="":
        SalesPersonID = json_data['assignedTo']
        emp_obj = Employee.objects.get(pk=SalesPersonID)
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
            SalesPersonID=[SalesPersonID]
            for emp in emps:
                SalesPersonID.append(emp.id)
        elif emp_obj.role == 'admin' or emp_obj.role == 'ceo':
            emps = Employee.objects.filter(id__gt=0)
            SalesPersonID=[]
            for emp in emps:
                SalesPersonID.append(emp.id)
        else:
            SalesPersonID = [json_data['assignedTo']]
    if len(json_data) == 0:
        leads_obj = Lead.objects.all(junk=0).count()
        return Response({"message": "Success","status": 200,"data":[{"lead_count":leads_obj}]})
    else:
        if json_data['assignedTo'] !='':
            leads_obj = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID).count()
            if leads_obj ==0:
                return Response({"message": "Success","status": 200,"data":[{"lead_count":0}]})
            else:
                return Response({"message": "Success","status": 200,"data":[{"lead_count":leads_obj}]})




# {"leadType": "All", "assignedTo": "1"}
#Lead All Filter API
@api_view(["POST"])
def search_all_filter(request):
    json_data = request.data
    print('called')
    PageNo = json_data['PageNo']
    SearchText = json_data['SearchText']
    try:
        MaxItem = json_data['MaxItem']
    except:
        MaxItem = 10
    endWith = (PageNo * MaxItem)
    startWith = (endWith - MaxItem)
    if json_data['assignedTo']!="":
        print('in first condition')
        SalesPersonID = json_data['assignedTo']
        
        emp_obj = Employee.objects.get(pk=SalesPersonID)
        
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
            SalesPersonID=[SalesPersonID]
            for emp in emps:
                SalesPersonID.append(emp.id)
            
        elif emp_obj.role == 'admin' or emp_obj.role == 'ceo':
            emps = Employee.objects.filter(id__gt=0)
            SalesPersonID=[]
            for emp in emps:
                SalesPersonID.append(emp.id)
        else:
            SalesPersonID = [json_data['assignedTo']]
        
        print(SalesPersonID)
    
    if len(json_data) == 0:
        print('all lead')
        leads_obj = Lead.objects.all(junk=0).order_by("-id")
        leads_json = LeadSerializer(leads_obj, many=True)
        return Response({"message": "Success","status": 200,"data":leads_json.data})
    else:
        allld = []
        if json_data['assignedTo'] !='':
            leads_obj = Lead.objects.filter(Q(junk=0, companyName__icontains=SearchText, assignedTo__in=SalesPersonID)|Q(junk=0, phoneNumber__icontains=SearchText, assignedTo__in=SalesPersonID)|Q(junk=0, contactPerson__icontains=SearchText, assignedTo__in=SalesPersonID)).order_by("-id")[startWith:endWith]
            print(leads_obj)
            if len(leads_obj) ==0:
                return Response({"message": "Success","status": 200,"data":[]})
            else:
                # allld = []
                for obj in leads_obj:
                    lead_json = LeadSerializer(obj, many=False)
                    lead_json_dump = json.loads(json.dumps(lead_json.data))
                    items = LeadItem.objects.filter(LeadID = obj.id)
                    item_json = LeadItemSerializer(items, many=True)
                    lead_json_dump['LeadItem'] = item_json.data
                    #added by millan on 22-September-2022
                    image = Attachment.objects.filter(LinkID = obj.id, LinkType='Lead')
                    image_json = AttachmentSerializer(image, many=True)
                    lead_json_dump['Attach'] = image_json.data
                    #added by millan on 22-September-2022
                    allld.append(lead_json_dump)
                return Response({"message": "Success","status": 200,"data":allld})



# # {"leadType": "All", "assignedTo": "1"}
# #Lead All Filter API
# @api_view(["POST"])
# def all_filter(request):
#     json_data = request.data
        
#     if json_data['assignedTo']!="":
#         print('in first condition')
#         SalesPersonID = json_data['assignedTo']
        
#         emp_obj = Employee.objects.get(pk=SalesPersonID)
        
#         if emp_obj.role == 'manager':
#             emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
#             SalesPersonID=[SalesPersonID]
#             for emp in emps:
#                 SalesPersonID.append(emp.id)
            
#         elif emp_obj.role == 'admin' or emp_obj.role == 'ceo':
#             emps = Employee.objects.filter(id__gt=0)
#             SalesPersonID=[]
#             for emp in emps:
#                 SalesPersonID.append(emp.id)
#         else:
#             SalesPersonID = [json_data['assignedTo']]
        
#         print(SalesPersonID)
    
#     if len(json_data) == 0:
#         print('all lead')
#         leads_obj = Lead.objects.all(junk=0).order_by("-id")
#         leads_json = LeadSerializer(leads_obj, many=True)
#         return Response({"message": "Success","status": 200,"data":leads_json.data})
#     else:
#         print('by filter employee details')
#         print(json_data.keys())
#         #print(json_data.keys()[0])
#         #if json_data['U_FAV']
#         allld = []
#         for ke in json_data.keys():
#             print(ke)
#             if ke =='assignedTo' :
#                 if json_data['assignedTo'] !='':
#                     leads_obj = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID).order_by("-id")
#                     if len(leads_obj) ==0:
#                         return Response({"message": "Success","status": 200,"data":[]})
#                     else:
#                         # allld = []
#                         for obj in leads_obj:
#                             lead_json = LeadSerializer(obj, many=False)
#                             lead_json_dump = json.loads(json.dumps(lead_json.data))
#                             items = LeadItem.objects.filter(LeadID = obj.id)
#                             item_json = LeadItemSerializer(items, many=True)
#                             lead_json_dump['LeadItem'] = item_json.data
#                             #added by millan on 22-September-2022
#                             image = Attachment.objects.filter(LinkID = obj.id, LinkType='Lead')
#                             image_json = AttachmentSerializer(image, many=True)
#                             lead_json_dump['Attach'] = image_json.data
#                             #added by millan on 22-September-2022
#                             allld.append(lead_json_dump)
#                         # return Response({"message": "Success","status": 200,"data":allld})
#             elif ke =='employeeId' :
#                 if json_data['employeeId'] !='':
#                     leads_obj = Lead.objects.filter(junk=0,employeeId=json_data['employeeId']).order_by("-id")
                    
#                     if len(leads_obj) ==0:
#                         return Response({"message": "Success","status": 200,"data":[]})
#                     else:
#                         # allld = []
#                         for obj in leads_obj:
#                             lead_json = LeadSerializer(obj, many=False)
#                             lead_json_dump = json.loads(json.dumps(lead_json.data))
#                             items = LeadItem.objects.filter(LeadID = obj.id)
#                             item_json = LeadItemSerializer(items, many=True)
#                             lead_json_dump['LeadItem'] = item_json.data
#                             #added by millan on 22-September-2022
#                             attach = Attachment.objects.filter(LinkID = obj.id, LinkType='Lead')
#                             image_json = AttachmentSerializer(image, many=True)
#                             lead_json_dump['Attach'] = image_json.data
#                             #added by millan on 22-September-2022
#                             allld.append(lead_json_dump)
#                         # return Response({"message": "Success","status": 200,"data":allld})
#                 # else:
#                 #     return Response({"message": "Success","status": 200,"data":[]})
#         return Response({"message": "Success","status": 200,"data":allld})

#Lead All Filter API
@api_view(["POST"])
def all_filter_junk(request):
    json_data = request.data
    
    if len(json_data) == 0:
        leads_obj = Lead.objects.filter(junk=1).order_by("-id")
        #leads_json = LeadSerializer(leads_obj, many=True)
        allld = []
        for obj in leads_obj:
            lead_json = LeadSerializer(obj, many=False)
            lead_json_dump = json.loads(json.dumps(lead_json.data))
            items = LeadItem.objects.filter(LeadID = obj.id)
            item_json = LeadItemSerializer(items, many=True)
            lead_json_dump['LeadItem'] = item_json.data
            allld.append(lead_json_dump)
        return Response({"message": "Success","status": 200,"data":allld})
        #return Response({"message": "Success","status": 200,"data":leads_json.data})
    else:
        SalesPersonID = json_data['assignedTo']         
        print(SalesPersonID)
        emp_obj = Employee.objects.get(pk=SalesPersonID)
        
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
            SalesPersonID=[SalesPersonID]
            for emp in emps:
                SalesPersonID.append(emp.id)
            
        elif emp_obj.role == 'admin' or emp_obj.role == 'ceo':
            emps = Employee.objects.filter(id__gt=0)
            SalesPersonID=[]
            for emp in emps:
                SalesPersonID.append(emp.id)
        else:
            SalesPersonID = [json_data['assignedTo']]
        
        print(SalesPersonID)
        
        leads_obj = Lead.objects.filter(junk=1, assignedTo__in=SalesPersonID).order_by("-id")            
        if len(leads_obj) ==0:
            return Response({"message": "Success","status": 200,"data":[]})
        else:
            #leads_json = LeadSerializer(leads_obj, many=True)
            allld = []
            for obj in leads_obj:
                lead_json = LeadSerializer(obj, many=False)
                lead_json_dump = json.loads(json.dumps(lead_json.data))
                items = LeadItem.objects.filter(LeadID = obj.id)
                item_json = LeadItemSerializer(items, many=True)
                lead_json_dump['LeadItem'] = item_json.data
                allld.append(lead_json_dump)
            return Response({"message": "Success","status": 200,"data":allld})
            #return Response({"message": "Success","status": 200,"data":leads_json.data})            


"""
@api_view(["GET"])
def all(request):
    leads_obj = Lead.objects.all()    
    data = []
    leads_obj1 = Lead.objects.raw("SELECT lead_lead.*, employee_employee.firstName FROM `lead_lead` inner join employee_employee on employeeId_id = employee_employee.id;")    
    
    for obj in leads_obj1:
        obj_serialized = obj.__dict__
        obj_serialized.pop('_state')
        print(obj_serialized)
        #data = data + str(obj.__dict__) working
        data.append(obj_serialized)
        
        #data.append({"id":obj.id, "date":obj.date, "location":obj.location, "companyName":obj.companyName, "source":obj.source, "contactPerson":obj.contactPerson, "phoneNumber":obj.phoneNumber, "message":obj.message, "email":obj.email, "productInterest":obj.productInterest, "assignedTo":obj.assignedTo, "employeeId":obj.firstName, "timestamp":obj.timestamp})
        
    lead_json = LeadSerializer(leads_obj, many=True)
    #print(data)
    #return Response({"message": "Success","status": 200,"data":lead_json.data})
    return Response({"message": "Success","status": 200,"data":data})
"""
"""

@api_view(["GET"])
def all(request):
    leads_obj = Lead.objects.all()
    
    # #leads_obj1 = Lead.objects.raw("SELECT *, employee_employee.firstName FROM `lead_lead` inner join employee_employee on employeeId_id = employee_employee.id")
    leads_obj1 = Lead.objects.raw("SELECT lead_lead.*, employee_employee.firstName FROM `lead_lead` inner join employee_employee on employeeId_id = employee_employee.id;")
    for p in leads_obj1:
        print("___")
        for field in p._meta.get_fields():
            print(field)
    
    lead_json = LeadSerializer(leads_obj, many=True)
    return Response({"message": "Success","status": 200,"data":lead_json.data})
"""
#Lead One API
@api_view(["POST"])
def one(request):
    id=request.data['id']    
    lead_obj = Lead.objects.get(id=id)
    lead_json = LeadSerializer(lead_obj, many=False)
    
    lead_json_dump = json.loads(json.dumps(lead_json.data))
    items = LeadItem.objects.filter(LeadID = lead_obj.id)
    item_json = LeadItemSerializer(items, many=True)
    lead_json_dump['LeadItem'] = item_json.data
    #added by millan on 22-September-2022
    image = Attachment.objects.filter(LinkID = lead_obj.id, LinkType='Lead')
    image_json = AttachmentSerializer(image, many=True)
    lead_json_dump['Attach'] = image_json.data
    #added by millan on 22-September-2022
    
    return Response({"message": "Success","status": 200,"data":[lead_json_dump]})

#Lead Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        if (request.data['phoneNumber']=="" or request.data['companyName']=="" or request.data['contactPerson']==""):
            return Response({"message":"Mobile or Person or Company required","status":"201","data":[]})
        if Lead.objects.filter(phoneNumber=request.data['phoneNumber']).exclude(pk=fetchid).exists():
            return Response({"message":"This Mobile number already exists: "+str(request.data['phoneNumber'])+"","status":"201","data":[]})
        #elif Lead.objects.filter(email=request.data['email']).exclude(pk=fetchid).exists():
            #return Response({"message":"This Email already exists: "+str(request.data['email'])+"","status":"201","data":[]})
        elif Lead.objects.filter(companyName=request.data['companyName'].lower()).exclude(pk=fetchid).exclude(companyName="n/a").exists():
            return Response({"message":"This CompanyName already exists: "+str(request.data['companyName'])+"","status":"201","data":[]})
        elif Lead.objects.filter(companyName=request.data['companyName']).filter(contactPerson=request.data['contactPerson']).exclude(pk=fetchid).exclude(companyName="n/a").exists():
            return Response({"message":"This ContactPerson already exists: "+str(request.data['contactPerson'])+"","status":"201","data":[]})
        else:
            model = Lead.objects.get(pk = fetchid)
            model.date  = request.data['date']
            model.location  = request.data['location']
            model.companyName  = request.data['companyName']
            model.numOfEmployee  = request.data['numOfEmployee']
            model.turnover  = request.data['turnover']
            model.source  = request.data['source']
            model.source_id  = request.data['source_id']
            model.contactPerson  = request.data['contactPerson']
            model.designation  = request.data['designation']
            model.phoneNumber  = request.data['phoneNumber']
            model.message  = request.data['message']
            model.email  = request.data['email']
            model.leadType  = request.data['leadType']
            model.productInterest  = request.data['productInterest']
            model.assignedTo_id  = request.data['assignedTo']
            model.employeeId_id  = request.data['employeeId']
            model.timestamp  = request.data['timestamp']
            model.status  = request.data['status']
            model.DivCode  = request.data['DivCode']
            model.DivName  = request.data['DivName']

            model.category = request.data['category']
            model.groupType = request.data['groupType']
            model.intProdCat = request.data['intProdCat']
            model.intProjCat = request.data['intProjCat']
            model.country = request.data['country']
            model.country_code = request.data['country_code']
            model.state = request.data['state']
            model.state_code = request.data['state_code']
            model.city = request.data['city']

            model.save()
            return Response({"message":"successful","status":200,"data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#Lead delete

@api_view(['POST'])
def delete(request):
    fetchids=request.data['id']
    naid = []
    for fetchid in fetchids:
        if Lead.objects.filter(pk=fetchid).exists():
           fetchdata=Lead.objects.filter(pk=fetchid).delete()
        else:
            naid.append(fetchid)
    print(str(naid))
    return Response({"message":"successful","status":"200","data":[]})
             #return Response({"message":"Id wrong","status":"201","data":[]})




# @api_view(['POST'])
# def delete(request):
    # fetchid=request.data['id']
    # try:
        # fetchdata=Lead.objects.filter(pk=fetchid).delete()
        # return Response({"message":"successful","status":"200","data":[]})
    # except:
         # return Response({"message":"Id wrong","status":"201","data":[]})

#Lead Assign
@api_view(['POST'])
def assign(request):
    try:
        fetchids=request.data['id']
        empid=request.data['employeeId']
        emp=Employee.objects.get(pk=empid)
        naid = []

        leadComArr = []
        leadRow = ""

        for fetchid in fetchids:
            if Lead.objects.filter(pk=fetchid).exists():
                model=Lead.objects.get(pk=fetchid)
                model.assignedTo = emp
                model.save()
                
                # leadRow += f""" 
                #     <tr>
                #         <td>{model.id}</td>
                #         <td>{model.companyName}</td>
                #         <td>{model.contactPerson}</td>
                #         <td>{model.phoneNumber}</td>
                #         <td>{model.source}</td>
                #         <td>{model.groupType}</td>
                #         <td>{model.intProdCat}</td>
                #         <td>{model.intProjCat}</td>
                #         <td>{model.location}</td>
                #     </tr>
                # """
            else:
                naid.append(fetchid)
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # after creating lead mail alert to reporting person
        # empFirstName = emp.firstName
        # empEmail = emp.Email
        # mailSubject = "List of Leads for FollowUp, and List of New Leads"
        # mailMessage = f"""
        # <div>
        #     Hi Sir/Mam <b>{empFirstName}</b>,<br><br>
        #     You'r assigned lead list are: <br><br>
        # </div>
        # <table style="width: 100%">
        # <tr>
        #     <th>Lead Id</th>
        #     <th>Company Name</th>
        #     <th>Contact Person</th>
        #     <th>Phone Number</th>
        #     <th>Source</th>
        #     <th>Group Type</th>
        #     <th>Interested in Product Category </th>
        #     <th>Interested in Project Category </th>
        #     <th>Zone Stage</th>
        # </tr>
        # {leadRow}
        # </table>"""
        # mailResponse = sendMail(toEmail= empEmail, subject = mailSubject, message = mailMessage, attachments = "")
        # print(mailResponse)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        # print(str(naid))
        return Response({"message":"successful","status":200,"data":[]})
    except Exception as e:
        return Response({"message":"error","status":"201","data": str(e)})


#Type Create API
@api_view(['POST'])
def type_create(request):
    try:
        Name = request.data['Name']
        CreatedDate = request.data['CreatedDate']
        CreatedTime = request.data['CreatedTime']

        model=Type(Name = Name, CreatedDate = CreatedDate, CreatedTime = CreatedTime)
        
        model.save()
        
        tp = Type.objects.latest('id')        
        
        return Response({"message":"successful","status":200,"data":[{"id":tp.id}]})
    except Exception as e:
        return Response({"message":"Can not create","status":"201","data":[{"Error":str(e)}]})

#LeadType All API
@api_view(["GET"])
def type_all(request):
    type_obj = Type.objects.all()        
    type_json = TypeSerializer(type_obj, many=True)
    return Response({"message": "Success","status": 200,"data":type_json.data})

#Type delete
@api_view(['POST'])
def type_delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Type.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

#Source Create API
@api_view(['POST'])
def source_create(request):
    Name = request.data['Name']    
    if Source.objects.filter(Name=Name).exists():        
        return Response({"message":"Already exist","status":409,"data":[]})
    else:        
        try:
            CreatedDate = request.data['CreatedDate']
            CreatedTime = request.data['CreatedTime']
            model=Source(Name = Name, CreatedDate = CreatedDate, CreatedTime = CreatedTime)            
            model.save()            
            sc = Source.objects.latest('id')
            return Response({"message":"successful","status":200,"data":[{"id":sc.id}]})
        except Exception as e:
            return Response({"message":"Can not create","status":"201","data":[{"Error":str(e)}]})        

#Type Update API
@api_view(['POST'])
def source_update(request):
    fetchid = request.data['id']
    try:
        model = Source.objects.get(pk = fetchid)
        model.Name  = request.data['Name']
        model.CreatedDate  = request.data['CreatedDate']
        model.CreatedTime  = request.data['CreatedTime']
        model.save()
        return Response({"message":"successful","status":200,"data":[request.data]})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})


#SourceType All API
@api_view(["GET"])
def source_all(request):
    source_obj = Source.objects.all()        
    source_json = SourceSerializer(source_obj, many=True)
    return Response({"message": "Success","status": 200,"data":source_json.data})

#SourceType One API
@api_view(["POST"])
def source_one(request):
    fetch = request.data['id']
    source_obj = Source.objects.filter(pk=fetch)        
    source_json = SourceSerializer(source_obj, many=True)
    return Response({"message": "Success","status": 200,"data":source_json.data})


#Source delete
@api_view(['POST'])
def source_delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Source.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

#------------Lead Dash Board------------------------
@api_view(["POST"])
def lead_dashboard(request):

    json_data = request.data
    
    if "SalesEmployeeCode" in json_data:
        print("yes")
        
        if json_data['SalesEmployeeCode']!="":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin' or emp_obj.role == 'ceo':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode=[]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)                    
            elif emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                SalesEmployeeCode=[SalesEmployeeCode]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode=[SalesEmployeeCode]
                # emps = Employee.objects.filter(reportingTo=emp_obj.reportingTo)#.values('id', 'SalesEmployeeCode')
                # SalesEmployeeCode=[]
                # for emp in emps:
                    # SalesEmployeeCode.append(emp.SalesEmployeeCode)
            
            print(SalesEmployeeCode)
            
            emp_ids = Employee.objects.filter(SalesEmployeeCode__in=SalesEmployeeCode).values_list('id', flat=True)
            print(emp_ids)
            #{"SalesEmployeeCode":4}
            
            lead_all = Lead.objects.filter(assignedTo__in=emp_ids).count()
            print(lead_all)
            
            #----Zonewise------
            lead_east = Lead.objects.filter(assignedTo__in=emp_ids, location='East Zone').count()            
            lead_west = Lead.objects.filter(assignedTo__in=emp_ids, location='West Zone').count()            
            lead_north = Lead.objects.filter(assignedTo__in=emp_ids, location='North Zone').count()            
            lead_south = Lead.objects.filter(assignedTo__in=emp_ids, location='South Zone').count()            
            
            #------Groupwise-------
            # ["Customer","Prospect ","Distibutor","Dealar","Other"]
            Customer = Lead.objects.filter(assignedTo__in=emp_ids, groupType='Customer').count()            
            Prospect = Lead.objects.filter(assignedTo__in=emp_ids, groupType='Prospect').count()            
            Distibutor = Lead.objects.filter(assignedTo__in=emp_ids, groupType='Distibutor').count()            
            Dealar = Lead.objects.filter(assignedTo__in=emp_ids, groupType='Dealar').count()            
            Other = Lead.objects.filter(assignedTo__in=emp_ids, groupType='Other').count()
            
            opp_all = Opportunity.objects.filter(SalesPerson__in=SalesEmployeeCode).count()
            #con_opp = "{:.2f}".format((opp_all*100)/lead_all)
            if lead_all ==0:
                con_opp = 0
            else:
                con_opp = int((opp_all*100)/lead_all)            
            
            camp_all = Campaign.objects.filter(CampaignOwner__in=SalesEmployeeCode).count()
            #print(opp_all)
			
            #{"SalesEmployeeCode":"2"}
            context = {
                "Opportunities":opp_all,
                "Leads":lead_all,
                "Zone": {
                    "East":lead_east,
                    "West":lead_west,
                    "North":lead_north,
                    "South":lead_south
                },
                "Group": {
                    "Customer":Customer,
                    "Prospect":Prospect,
                    "Distibutor":Distibutor,
                    "Dealar":Dealar,
                    "Other":Other
                },
                "Campaigns":camp_all,
                "Converted_Opportunities":con_opp
            }
            return Response({"message": "Success","status": 200,"data":[context]})
            
            #return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
        
        
#------------Lead Dash Board Qualified Current Year------------------------
@api_view(["POST"])
def qualified_lead_y(request):

    json_data = request.data
    
    if "SalesEmployeeCode" in json_data:
        print("yes")
        
        if json_data['SalesEmployeeCode']!="":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin' or emp_obj.role == 'ceo':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode=[]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)                    
            elif emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                SalesEmployeeCode=[SalesEmployeeCode]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode=[SalesEmployeeCode]
                # emps = Employee.objects.filter(reportingTo=emp_obj.reportingTo)#.values('id', 'SalesEmployeeCode')
                # SalesEmployeeCode=[]
                # for emp in emps:
                    # SalesEmployeeCode.append(emp.SalesEmployeeCode)
            
            print(SalesEmployeeCode)
            
            emp_ids = Employee.objects.filter(SalesEmployeeCode__in=SalesEmployeeCode).values_list('id', flat=True)
            print(emp_ids)
            #{"SalesEmployeeCode":4}
            
            #duration = json_data['duration']
            source = json_data['source']
            #if duration == "weekly":
            
            #----weekly------
            year = 2022
            
            Jan={}
            Feb={}
            Mar={}
            Apr={}
            May={}
            Jun={}
            Jul={}
            Aug={}
            Sep={}
            Oct={}
            Nov={}
            Dec={}
            #fil = "source='Facebook'"
            #ss = Lead.objects.filter(fil).count()
            #print(ss)
            if source =="All":
                Jan['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(year)+'-01-').count()
                Jan['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(year)+'-01-').count()
                
                Feb['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(year)+'-02-').count()
                Feb['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(year)+'-02-').count()
                
                Mar['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(year)+'-03-').count()
                Mar['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(year)+'-03-').count()
                
                Apr['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(year)+'-04-').count()
                Apr['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(year)+'-04-').count()
                
                May['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(year)+'-05-').count()
                May['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(year)+'-05-').count()
                
                Jun['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(year)+'-06-').count()
                Jun['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(year)+'-06-').count()
                
                Jul['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(year)+'-07-').count()
                Jul['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(year)+'-07-').count()
                
                Aug['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(year)+'-08-').count()
                Aug['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(year)+'-08-').count()
                
                Sep['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(year)+'-09-').count()
                Sep['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(year)+'-09-').count()
                
                Oct['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(year)+'-10-').count()
                Oct['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(year)+'-10-').count()
                
                Nov['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(year)+'-11-').count()
                Nov['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(year)+'-11-').count()
                
                Dec['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(year)+'-12-').count()
                Dec['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(year)+'-12-').count()
            else:
                Jan['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(year)+'-01-').count()
                Jan['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(year)+'-01-').count()
                
                Feb['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(year)+'-02-').count()
                Feb['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(year)+'-02-').count()
                
                Mar['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(year)+'-03-').count()
                Mar['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(year)+'-03-').count()
                
                Apr['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(year)+'-04-').count()
                Apr['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(year)+'-04-').count()
                
                May['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(year)+'-05-').count()
                May['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(year)+'-05-').count()
                
                Jun['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(year)+'-06-').count()
                Jun['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(year)+'-06-').count()
                
                Jul['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(year)+'-07-').count()
                Jul['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(year)+'-07-').count()
                
                Aug['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(year)+'-08-').count()
                Aug['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(year)+'-08-').count()
                
                Sep['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(year)+'-09-').count()
                Sep['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(year)+'-09-').count()
                
                Oct['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(year)+'-10-').count()
                Oct['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(year)+'-10-').count()
                
                Nov['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(year)+'-11-').count()
                Nov['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(year)+'-11-').count()
                
                Dec['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(year)+'-12-').count()
                Dec['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(year)+'-12-').count()
            
            #"weekly":{"Mon":mon, "Tue":tue, "Wed":wed, "Thu":thu}, 
            #{"SalesEmployeeCode":"2"}
            return Response({"message": "Success","status": 200,"data":{"Jan":Jan, "Feb":Feb, "Mar":Mar, "Apr":Apr, "May":May, "Jun":Jun, "Jul":Jul, "Aug":Aug, "Sep":Sep, "Oct":Oct, "Nov":Nov, "Dec":Dec}})
            
            #return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
        
#------------Lead Dash Board Qualified Current Weekly------------------------
@api_view(["POST"])
def qualified_lead_w(request):

    json_data = request.data
    
    if "SalesEmployeeCode" in json_data:
        print("yes")
        
        if json_data['SalesEmployeeCode']!="":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin' or emp_obj.role == 'ceo':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode=[]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)                    
            elif emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                SalesEmployeeCode=[SalesEmployeeCode]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode=[SalesEmployeeCode]
                # emps = Employee.objects.filter(reportingTo=emp_obj.reportingTo)#.values('id', 'SalesEmployeeCode')
                # SalesEmployeeCode=[]
                # for emp in emps:
                    # SalesEmployeeCode.append(emp.SalesEmployeeCode)
            
            print(SalesEmployeeCode)
            
            emp_ids = Employee.objects.filter(SalesEmployeeCode__in=SalesEmployeeCode).values_list('id', flat=True)
            print(emp_ids)
            #{"SalesEmployeeCode":4}
            
            source = json_data['source']
            #-- get weekdays ----
            #today = '2022-08-03'    
            today = date.today()
            today = today.strftime("%Y-%m-%d") 
            date_object = datetime.strptime(today, '%Y-%m-%d').date()
            wek_strt = date_object - timedelta(days=date_object.weekday())
            wek_end = wek_strt + timedelta(days=6)
            print(wek_strt, wek_end)
            start_date = date(wek_strt.year, wek_strt.month, wek_strt.day) 
            end_date = date(wek_end.year, wek_end.month, wek_end.day)
            delta = end_date - start_date
            
            Mon={}
            Tue={}
            Wed={}
            Thu={}
            Fri={}
            Sat={}
            Sun={}
            
            dt=[]
            for i in range(delta.days + 1):
                dt.append(start_date + timedelta(days=i))

            if source =="All":
                Mon['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(dt[0])).count()
                Mon['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(dt[0])).count()
                
                Tue['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(dt[1])).count()
                Tue['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(dt[1])).count()
                
                Wed['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(dt[2])).count()
                Wed['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(dt[2])).count()
                
                Thu['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(dt[3])).count()
                Thu['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(dt[3])).count()
                
                Fri['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(dt[4])).count()
                Fri['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(dt[4])).count()
                
                Sat['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(dt[5])).count()
                Sat['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(dt[5])).count()
                
                Sun['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", date__contains=str(dt[6])).count()
                Sun['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", date__contains=str(dt[6])).count()
            else:
                Mon['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(dt[0])).count()
                Mon['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(dt[0])).count()
                
                Tue['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(dt[1])).count()
                Tue['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(dt[1])).count()
                
                Wed['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(dt[2])).count()
                Wed['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(dt[2])).count()
                
                Thu['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(dt[3])).count()
                Thu['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(dt[3])).count()
                
                Fri['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(dt[4])).count()
                Fri['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(dt[4])).count()
                
                Sat['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(dt[5])).count()
                Sat['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(dt[5])).count()
                
                Sun['q'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Qualified", source=source, date__contains=str(dt[6])).count()
                Sun['n'] = Lead.objects.filter(assignedTo__in=emp_ids, status="Not Qualified", source=source, date__contains=str(dt[6])).count()
            
            #"weekly":{"Mon":mon, "Tue":tue, "Wed":wed, "Thu":thu}, 
            #{"SalesEmployeeCode":"2"}
            return Response({"message": "Success","status": 200,"data":{"Mon":Mon, "Tue":Tue, "Wed":Wed, "Thu":Thu, "Fri":Fri, "Sat":Sat, "Sun":Sun}})
            
            #return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})

#Lead Bulk Upload Create API
@api_view(['POST'])
def create_by_excel(request):
    try:
        leads = request.data
        log = []
        log_msg = ""
        i=0
        for lead in leads:
            date=lead['date']
            location=lead['location']
            companyName=lead['companyName']
            numOfEmployee = lead['numOfEmployee']
            turnover = lead['turnover']
            source=lead['source']
            contactPerson=lead['contactPerson']
            designation=lead['designation']
            phoneNumber=lead['phoneNumber']
            message=lead['message']
            email=lead['email']
            productInterest=lead['productInterest']
            assignedTo_id=lead['assignedTo']
            employeeId_id=lead['employeeId']
            timestamp=lead['timestamp']
            status=lead['status']
            tender=lead['tender']
            DivCode=lead['DivCode']
            DivName=lead['DivName']
            leadType=lead['leadType']

            category = lead['category']
            groupType = lead['groupType']
            intProdCat = lead['intProdCat']
            intProjCat = lead['intProjCat']
            country = lead['country']
            country_code = lead['country_code']
            state = lead['state']
            state_code = lead['state_code']
            city = lead['city']
            
            source_id = Source.objects.filter(Name = lead['source'].lower()).values('id') #added by millan on 22-09-2022 to get id based on source name
            
            if (phoneNumber=="" or companyName=="" or contactPerson==""):
                return Response({"message":"Email or Mobile or Person or Company required","status":"201","data":[]})            
            if Lead.objects.filter(phoneNumber=phoneNumber).exists():
                log.append("This Mobile number already exists: "+str(phoneNumber))
            elif email!="":
                if Lead.objects.filter(email=email).exists():
                    log.append("This Email already exists: "+str(email))
            elif Lead.objects.filter(companyName=companyName).exists():
                log.append("This Company already exists: "+str(companyName))
            elif Lead.objects.filter(companyName=companyName).filter(contactPerson=contactPerson).exists():
                log.append("This ContactPerson already exists: "+contactPerson)
            else:
                model=Lead(date=date, DivCode=DivCode, DivName=DivName, tender=tender, location=location, companyName=companyName, numOfEmployee=numOfEmployee, turnover=turnover, source=source, source_id=source_id, contactPerson=contactPerson, designation=designation, phoneNumber=phoneNumber, message=message, email=email, status=status, leadType=leadType, productInterest=productInterest, assignedTo_id=assignedTo_id, employeeId_id=employeeId_id, timestamp=timestamp, category = category,groupType = groupType,intProdCat = intProdCat,intProjCat = intProjCat,country = country,country_code = country_code,state = state,state_code = state_code,city = city)
                model.save()

                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # after creating lead mail alert to reporting person
                # if assignedTo_id != "":
                #     empObj = Employee.objects.get(pk = assignedTo_id)
                #     empFirstName = empObj.firstName
                #     empEmail = empObj.Email
                #     mailSubject = "List of Leads for FollowUp, and List of New Leads"
                #     # mailMessage = f"Hi Sir/Mam <b>{empFirstName}</b> you have new assigned Lead {companyName}"
                #     mailMessage = f"""
                #         <div>
                #             Hi Sir/Mam <b>{empFirstName}</b>,<br><br>
                #             You'r assigned lead list are: <br><br>
                #         </div>
                #         <table style="width: 100%">
                #         <tr>
                #             <th>Lead Id</th>
                #             <th>Company Name</th>
                #             <th>Contact Person</th>
                #             <th>Phone Number</th>
                #             <th>Source</th>
                #             <th>Group Type</th>
                #             <th>Interested in Product Category </th>
                #             <th>Interested in Project Category </th>
                #             <th>Zone Stage</th>
                #         </tr>
                #         <tr>
                #             <td>{model.id}</td>
                #             <td>{model.companyName}</td>
                #             <td>{model.contactPerson}</td>
                #             <td>{model.phoneNumber}</td>
                #             <td>{model.source}</td>
                #             <td>{model.groupType}</td>
                #             <td>{model.intProdCat}</td>
                #             <td>{model.intProjCat}</td>
                #             <td>{model.location}</td>
                #         </tr>
                #         </table>"""
                #     mailAttachments = ""
                #     mailResponse = sendMail(toEmail= empEmail, subject = mailSubject, message = mailMessage, attachments = mailAttachments)
                #     print(mailResponse)
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

                LeadID = Lead.objects.latest('id').id
                
                if source =='Facebook':
                    temp = "FCBK/L"
                elif source =='Linkedin':
                    temp = "LIND/L"
                elif source =='Instagram':
                    temp = "INST/L"
                elif source =='Website':
                    temp = "WBST/L"
                elif source =='Whatsapp':
                    temp = "WHAP/L"
                elif source =='Emailer':
                    temp = "EMLR/L"
                elif source =='Event':
                    temp = "EVNT/L"
                else:
                    temp = "EXTR/L"
                model.code = str(temp+str(LeadID))
                model.save()
                i=i+1
                print(LeadID)

                if len(lead['LeadItem']) == 0:
                    if len(log) > 0:
                        log_msg = "\r\n".join(log)
                        print(log_msg)
                        #log_msg = str(log)
                    else:
                        log_msg = 'successful'
                    if len(leads) == i:
                        return Response({"message":log_msg,"status":"200","data":[]})

                else:
                    lines = json.loads(leads['LeadItem'])
                    LineNum = 0
                    if len(lines)!=0 and lines != "":
                        for line in lines:
                            try:
                                model_lines = LeadItem(LineNum = LineNum, LeadID = LeadID, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'], U_FGITEM = line['U_FGITEM'], CostingCode2 = line['CostingCode2'], ProjectCode = line['ProjectCode'], FreeText = line['FreeText'])
                                model_lines.save()
                                LineNum=LineNum+1
                            except Exception as e:
                                Lead.objects.filter(pk=LeadID).delete()
                                leadItems = LeadItem.objects.filter(LeadID=LeadID)
                                for item in leadItems:
                                    item.delete()
                                    if len(leads) == i:
                                        #return Response({"message":log_msg,"status":"200","data":[]})
                                        return Response({"message":str(e),"status":"202","data":[]})
                
            print(log)
            if len(log) > 0:
                log_msg = "\r\n".join(log)
                print(log_msg)
                #log_msg = str(log)
            else:
                log_msg = 'successful'
        return Response({"message":log_msg,"status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
