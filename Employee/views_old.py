from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from Item.serializers import *
from Category.serializers import *
from Order.serializers import *
from Opportunity.serializers import OpportunitySerializer
from Expense.models import Expense
from .serializers import *
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib import messages
from Quotation.models import Quotation, AppSlave
from Invoice.models import Invoice
from Order.models import Order, DocumentLines
from Opportunity.models import Opportunity
from BusinessPartner.models import BusinessPartner
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import EmployeeForm
from .models import *
from Activity.models import Activity
from Lead.models import Lead
from Item.models import Item
from Category.models import *
from Campaign.models import *
from Tender.models import Tender
from Notification.models import Notification
import requests
import json

from django.conf import settings

from django.db.models import Sum, F #added by millan on 05-September-2022

from datetime import date, timedelta
from collections import Counter

from global_fun import *

from pytz import timezone
from datetime import datetime as dt

tdate = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
yearmonth = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')


# Create your views here.
@api_view(["GET"])
def top5itembyamount(request):
    #added by millan on 05-September-2022
    try:
        top2bp = DocumentLines.objects.values('ItemCode').annotate(Total = Sum(F('Quantity')*F('UnitPrice'))).order_by('-Total')[:5]
    
        top5=[]

        for od in top2bp:
            top5dt = DocumentLines.objects.filter(ItemCode = od['ItemCode']).values('ItemDescription')
            for desc in top5dt:
                print(desc)
            top5.append({"ItemCode":od['ItemCode'], "ItemName":desc['ItemDescription'], "Total":od['Total']})
        
        return Response({"message": "Success","status": 200,"data":top5}) #added by millan on 05-September-2022
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

@api_view(["GET"])
def top5bp(request):
    try:
        #added by millan on 05-September-2022
        top2bp = Order.objects.values('CardCode').annotate(Total = Sum(F('DocTotal'))).order_by('-Total')[:5]
        print(top2bp)
        top5=[]
        for od in top2bp:
            try:
                cd = BusinessPartner.objects.filter(CardCode = od['CardCode']).values('CardName')
                for cName in cd:
                    print(cName)
                top5.append({"CardCode":od['CardCode'], "CardName":cName['CardName'], 'Total':od['Total']})
            except Exception as e:
                top5.append({"CardCode":od['CardCode'], "CardName":od['CardCode'], 'Total':od['Total']})
            
        return Response({"message": "Success","status": 200,"data":top5})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})


@api_view(["POST"])
def opportunity_bystage(request):

    json_data = request.data

    if "SalesEmployeeCode" in json_data:
        print("yes")

        if json_data['SalesEmployeeCode'] != "":
            SalesEmployeeCode = json_data['SalesEmployeeCode']

            emp_obj = Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin' or emp_obj.role == 'ceo':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode = []
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            elif emp_obj.role == 'manager':
                # .values('id', 'SalesEmployeeCode')
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)
                SalesEmployeeCode = [SalesEmployeeCode]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode = [SalesEmployeeCode]
            print(SalesEmployeeCode)

            opp_Lead_count = Opportunity.objects.filter(
                SalesPerson__in=SalesEmployeeCode, CurrentStageName="Lead").count()
            opp_Need_count = Opportunity.objects.filter(
                SalesPerson__in=SalesEmployeeCode, CurrentStageName="Need Analysis").count()
            opp_Quotation_count = Opportunity.objects.filter(
                SalesPerson__in=SalesEmployeeCode, CurrentStageName="Quotation").count()
            opp_Negotiation_count = Opportunity.objects.filter(
                SalesPerson__in=SalesEmployeeCode, CurrentStageName="Negotiation").count()
            opp_Order_count = Opportunity.objects.filter(
                SalesPerson__in=SalesEmployeeCode, CurrentStageName="Order").count()

            opportunity_context = {
                "Lead": opp_Lead_count,
                "NeedAnalysis": opp_Need_count,
                "Quotation": opp_Quotation_count,
                "Negotiation": opp_Negotiation_count,
                "Order": opp_Order_count
            }

            return Response({"message": "Success", "status": 200, "data": [opportunity_context]})
        else:
            return Response({"message": "Unsuccess", "status": 201, "data": [{"error": "SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess", "status": 201, "data": [{"error": "SalesEmployeeCode?"}]})


@api_view(["POST"])
def analytics(request):

    json_data = request.data
    month = int(json_data['month'])

    if "SalesEmployeeCode" in json_data:
        print("yes")

        if json_data['SalesEmployeeCode'] != "":
            SalesEmployeeCode = json_data['SalesEmployeeCode']

            emp_obj = Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin' or emp_obj.role == 'ceo':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode = []
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            elif emp_obj.role == 'manager':
                # .values('id', 'SalesEmployeeCode')
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)
                SalesEmployeeCode = [SalesEmployeeCode]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode = [SalesEmployeeCode]
            print(SalesEmployeeCode)

            tgt_all = Target.objects.filter(SalesPersonCode__in=SalesEmployeeCode).exclude(
                monthYear=yearmonth).order_by("-monthYear")[:month]
            #{"month":"3", "SalesEmployeeCode":"3"}
            amount = sum(tgt_all.values_list('amount', flat=True))
            print(amount)
            #amount = "{:.2f}".format(amount)
            #print(amount)

            sale = sum(tgt_all.values_list('sale', flat=True))
            print(sale)

            sale_diff = sum(tgt_all.values_list('sale_diff', flat=True))
            print(sale_diff)

            notification = Notification.objects.filter(
                Emp=emp_obj.id, CreatedDate=tdate, Read=0).order_by("-id").count()
            print(notification)

            return Response({"message": "Success", "status": 200, "data": [{"notification": notification, "amount": amount, "sale": sale, "sale_diff": sale_diff}]})

            #return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess", "status": 201, "data": [{"error": "SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess", "status": 201, "data": [{"error": "SalesEmployeeCode?"}]})


#Target Create API
@api_view(['POST'])
def target_create(request):
    try:
        TargetFor = request.data['TargetFor']
        amount = request.data['amount']
        monthYear = request.data['monthYear']
        qtr = request.data['qtr']
        department = request.data['department']

        SalesPersonCode = request.data['SalesPersonCode']
        reportingTo = request.data['reportingTo'].strip()
        CreatedDate = request.data['CreatedDate']
        if reportingTo == "":
            model = Target(TargetFor=TargetFor, amount=amount, monthYear=monthYear, qtr=qtr,
                           SalesPersonCode_id=SalesPersonCode, CreatedDate=CreatedDate, UpdatedDate=CreatedDate)
        else:
            model = Target(TargetFor=TargetFor, amount=amount, monthYear=monthYear, qtr=qtr, SalesPersonCode_id=SalesPersonCode,
                           reportingTo_id=reportingTo, CreatedDate=CreatedDate, UpdatedDate=CreatedDate)

        model = Target(TargetFor=TargetFor, amount=amount, monthYear=monthYear, qtr=qtr, SalesPersonCode_id=SalesPersonCode,
                       reportingTo_id=reportingTo, CreatedDate=CreatedDate, UpdatedDate=CreatedDate)
        model.save()

        tgt = Target.objects.latest('id')
        print(tgt.id)
        return Response({"message": "Success", "status": "200", "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": [{"Error": str(e)}]})

# most order item in last 30 days


@api_view(['GET'])
def movingitems(request):
    try:
        fastMovingdate = date.today() - timedelta(days=15)
        slowMovingdate = date.today() - timedelta(days=30)

        print(fastMovingdate)
        print(slowMovingdate)

        itemCodeList = []
        fastMovingItemList = []
        # ----------------------------------------------------------------------------
        # ------------------------- Fast Moving Items --------------------------------
        # ----------------------------------------------------------------------------
        fastMovingOrder_obj = Order.objects.filter(
            CreateDate__gte=fastMovingdate)
        fastMovingItemCodeArr = []
        for order in fastMovingOrder_obj:
            order_id = order.id
            docLineObj = DocumentLines.objects.filter(OrderID=order_id)
            for docLine in docLineObj:
                # print(docLine)
                # docJason = DocumentLinesSerializer(docLine);
                itemCode = docLine.ItemCode
                itemObj = Item.objects.get(ItemCode=itemCode)
                itemJson = ItemSerializer(itemObj)

                if itemCode not in fastMovingItemCodeArr:
                    fastMovingItemList.append(itemJson.data)
                    fastMovingItemCodeArr.append(itemCode)
                    itemCodeList.append(itemCode)

        FastItemsCount = len(fastMovingItemCodeArr)

        # ----------------------------------------------------------------------------
        # ------------------------- Slow Moving Itmes --------------------------------
        # ----------------------------------------------------------------------------
        slowMovingdate_obj = Order.objects.filter(
            CreateDate__lte=fastMovingdate, CreateDate__gte=slowMovingdate)
        slowMovingItemCodeArr = []
        slowMovingItemList = []
        for order in slowMovingdate_obj:
            order_id = order.id
            docLineObj = DocumentLines.objects.filter(OrderID=order_id)
            for docLine in docLineObj:
                # docJason = DocumentLinesSerializer(docLine);
                itemCode = docLine.ItemCode
                itemObj = Item.objects.get(ItemCode=itemCode)
                itemJson = ItemSerializer(itemObj)
                if itemCode not in fastMovingItemCodeArr:
                    slowMovingItemList.append(itemJson.data)
                    slowMovingItemCodeArr.append(itemCode)
                    itemCodeList.append(itemCode)

        SlowItemsCount = len(slowMovingItemCodeArr)

        dictItem = set(itemCodeList)
        # notMovingItemCount = Item.objects.all().exclude(ItemCode__in = dictItem).count()
        notMovingItemObj = Item.objects.all().exclude(ItemCode__in=dictItem)
        notMovingItemJson = ItemSerializer(notMovingItemObj, many=True)
        notMovingItemCount = len(notMovingItemObj)
        context = {
            "FastMovingItemsList": fastMovingItemList,
            "FastItemsCount": FastItemsCount,
            "SlowMovingItemsList": slowMovingItemList,
            "SlowItemsCount": SlowItemsCount,
            "NotMovingItemsList": notMovingItemJson.data,
            "NotMovingItemsCount": notMovingItemCount
        }

        print(FastItemsCount)
        print(SlowItemsCount)
        print(notMovingItemCount)

        return Response({"message": "successful", "status": 200, "data": [context]})
    except Exception as e:
        return Response({"message": "Error", "status": 201, "data": [str(e)]})

# most order item in last 30 days


@api_view(['GET'])
def movingitems_count(request):
    try:
        fastMovingdate = date.today() - timedelta(days=15)
        slowMovingdate = date.today() - timedelta(days=30)
        itemCodeList = []
        # --------------------------------------------------------------------------
        # ------------------------- Fast Moving Items ------------------------------
        # --------------------------------------------------------------------------
        fastMovingOrder_obj = Order.objects.filter(
            CreateDate__gte=fastMovingdate)
        fastMovingItemCodeArr = []
        for order in fastMovingOrder_obj:
            order_id = order.id
            docLineObj = DocumentLines.objects.filter(OrderID=order_id)
            for docLine in docLineObj:
                itemCode = docLine.ItemCode
                if itemCode not in fastMovingItemCodeArr:
                    fastMovingItemCodeArr.append(itemCode)
                    itemCodeList.append(itemCode)

        FastItemsCount = len(fastMovingItemCodeArr)

        # ----------------------------------------------------------------------------
        # ------------------------- Slow Moving Itmes --------------------------------
        # ----------------------------------------------------------------------------
        slowMovingdate_obj = Order.objects.filter(
            CreateDate__lte=fastMovingdate, CreateDate__gte=slowMovingdate)
        slowMovingItemCodeArr = []
        # slowMovingItemList = []
        for order in slowMovingdate_obj:
            order_id = order.id
            docLineObj = DocumentLines.objects.filter(OrderID=order_id)
            for docLine in docLineObj:
                itemCode = docLine.ItemCode
                if itemCode not in fastMovingItemCodeArr:
                    slowMovingItemCodeArr.append(itemCode)
                    itemCodeList.append(itemCode)

        SlowItemsCount = len(slowMovingItemCodeArr)
        dictItem = set(itemCodeList)
        notMovingItemCount = Item.objects.all().exclude(ItemCode__in=dictItem).count()

        context = {
            # "FastMovingItemsList": fastMovingItemList,
            "FastItemsCount": FastItemsCount,
            # "SlowMovingItemsList": slowMovingItemList,
            "SlowItemsCount": SlowItemsCount,
            "NotMovingItemsCount": notMovingItemCount
            # "NotMovingItemsList": notMovingItemJson.data
        }

        return Response({"message": "successful", "status": 200, "data": [context]})
    except Exception as e:
        return Response({"message": str(e), "status": 201, "data": [str(e)]})


@api_view(["POST"])
def dashboard(request):

    json_data = request.data

    if "SalesEmployeeCode" in json_data:
        print("yes")

        if json_data['SalesEmployeeCode'] != "":
            SalesEmployeeCode = json_data['SalesEmployeeCode']

            emp_obj = Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin' or emp_obj.role == 'ceo':
                #emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                emps = Employee.objects.all()
                SalesEmployeeCode = []
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            elif emp_obj.role == 'manager':
                # .values('id', 'SalesEmployeeCode')
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)
                SalesEmployeeCode = [SalesEmployeeCode]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode = [SalesEmployeeCode]
                # emps = Employee.objects.filter(reportingTo=emp_obj.reportingTo)#.values('id', 'SalesEmployeeCode')
                # SalesEmployeeCode=[]
                # for emp in emps:
                # SalesEmployeeCode.append(emp.SalesEmployeeCode)

            print(SalesEmployeeCode)

            emp_ids = Employee.objects.filter(
                SalesEmployeeCode__in=SalesEmployeeCode).values_list('id', flat=True)
            print(emp_ids)
            #{"SalesEmployeeCode":4}

            lead_all = Lead.objects.filter(assignedTo__in=emp_ids).count()
            print(lead_all)
            from django.db.models import Q

            lead_prod = Lead.objects.filter(
                assignedTo__in=emp_ids).filter(~Q(intProdCat="")).count()
            print("lead_prod")
            print(lead_prod)

            lead_proj = Lead.objects.filter(
                assignedTo__in=emp_ids).filter(~Q(intProjCat="")).count()
            print("lead_proj")
            print(lead_proj)

            opp_all = Opportunity.objects.filter(
                SalesPerson__in=SalesEmployeeCode).count()
            #print(opp_all)

            quot_all = Quotation.objects.filter(
                SalesPersonCode__in=SalesEmployeeCode).count()
            #print(quot_all)

            ord_all = Order.objects.filter(
                SalesPersonCode__in=SalesEmployeeCode).count()
            #print(ord_all)

            inv_all = Invoice.objects.filter(
                SalesPersonCode__in=SalesEmployeeCode).count()
            #print(inv_all)

            tnd_all = Tender.objects.filter(
                SalesPersonCode__in=SalesEmployeeCode).count()
            print(tnd_all)

            #bp_all = BusinessPartner.objects.filter(SalesPersonCode__in=SalesEmployeeCode).count()
            bp_all = BusinessPartner.objects.all().count()
            #print(bp_all)

            tgt_all = Target.objects.filter(
                SalesPersonCode__in=SalesEmployeeCode, monthYear=yearmonth)

            amount = sum(tgt_all.values_list('amount', flat=True))
            print(amount)
            #amount = "{:.2f}".format(amount)
            #print(amount)

            sale = sum(tgt_all.values_list('sale', flat=True))
            print(sale)

            sale_diff = sum(tgt_all.values_list('sale_diff', flat=True))
            print(sale_diff)

            notification = Notification.objects.filter(
                Emp=emp_obj.id, CreatedDate=tdate, Read=0).order_by("-id").count()
            print(notification)

            ord_over = Order.objects.filter(
                SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Open", DocDueDate__lt=tdate).count()
            print(ord_over)
            print(tdate)

            ord_open = Order.objects.filter(
                SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Open", DocDueDate__gte=tdate).count()
            print(ord_open)

            ord_close = Order.objects.filter(
                SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Close").count()
            print(ord_close)

            camp_all = Campaign.objects.filter(
                CampaignOwner__in=SalesEmployeeCode).count()
            print(camp_all)

            expense_count = Expense.objects.filter(employeeId__in = SalesEmployeeCode).count()
            print(expense_count)
            
            context = {
                "notification": notification,
                "amount": amount,
                "sale": sale,
                "sale_diff": sale_diff,
                "Opportunity": opp_all,
                "Quotation": quot_all,
                "Order": ord_all,
                "Invoice": inv_all,
                "Tender": tnd_all,
                "Customer": bp_all,
                "Leads": lead_all,
                "Leads_Product": lead_prod,
                "Leads_Project": lead_proj,
                "Over": ord_over,
                "Open": ord_open,
                "Close": ord_close,
                "Campaign": camp_all,
                "Expense": expense_count
            }
            #{"SalesEmployeeCode":"2"}
            return Response({"message": "Success", "status": 200, "data": [context]})

            #return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess", "status": 201, "data": [{"error": "SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess", "status": 201, "data": [{"error": "SalesEmployeeCode?"}]})


@api_view(["POST"])
def invoice_counter(request):
    json_data = request.data

    if "SalesEmployeeCode" in json_data:
        print("yes")

        if json_data['SalesEmployeeCode'] != "":
            SalesEmployeeCode = json_data['SalesEmployeeCode']

            emp_obj = Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin' or emp_obj.role == 'ceo':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode = []
                for emp in emps:
                    SalesEmployeeCode.append(str(emp.SalesEmployeeCode))
            elif emp_obj.role == 'manager':
                # .values('id', 'SalesEmployeeCode')
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)
                SalesEmployeeCode = [str(SalesEmployeeCode)]
                for emp in emps:
                    SalesEmployeeCode.append(str(emp.SalesEmployeeCode))
            else:
                SalesEmployeeCode = [str(SalesEmployeeCode)]
                # emps = Employee.objects.filter(reportingTo=emp_obj.reportingTo)#.values('id', 'SalesEmployeeCode')
                # SalesEmployeeCode=[]
                # for emp in emps:
                # SalesEmployeeCode.append(emp.SalesEmployeeCode)

            print(SalesEmployeeCode)

            r = requests.post(settings.BASEURL+'/Login',
                              data=json.dumps(settings.SAPDB), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)

            ps = []
            for s in SalesEmployeeCode:
                print("SalesPersonCode eq "+str(s))
                ps.append("SalesPersonCode eq "+str(s))

            param = " or ".join(ps)
            # addr = settings.BASEURL+"/Invoices/$count?$filter="
            addr = settings.BASEURL+"/Invoices/$count?$filter="
            url = addr+param
            print(url)
            #{"SalesEmployeeCode":"1"}
            #http://103.234.187.35:50001/b1s/v1/Invoices/$count?$filter=SalesPersonCode eq 3 or SalesPersonCode eq 4
            res = requests.get(url, cookies=r.cookies, verify=False)
            live = json.loads(res.text)
            if type(live) == int:
                return Response({"message": "Success", "status": 200, "data": [{"Invoice": live}]})
            else:
                print(live['error']['message']['value'])
                return Response({"message": "Success", "status": 201, "data": [{"SAP_error": live['error']['message']['value']}]})
        else:
            return Response({"message": "Unsuccess", "status": 201, "data": [{"error": "SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess", "status": 201, "data": [{"error": "SalesEmployeeCode?"}]})

#Employee Create API


@api_view(['POST'])
def create(request):
    try:
        if request.data['userName']=='' or request.data['userName']== None :
            return Response({"message": "UserName Can't be Empty", "status": 201, "data": []})
        elif request.data['Email']=='' or request.data['Email']== None :
            return Response({"message": "Email Can't be Empty", "status": 201, "data": []})
        elif request.data['Mobile']=='' or request.data['Mobile']== None :
            return Response({"message": "Mobile Number Can't be Empty", "status": 201, "data": []})
        else:
            if Employee.objects.filter(userName=request.data['userName']).exists():
                return Response({"message": "UserName Already Exists", "status": 201, "data": []})
            elif Employee.objects.filter(Email=request.data['Email']).exists():
                return Response({"message": "Email Already Exists", "status": 201, "data": []})
            elif Employee.objects.filter(Mobile=request.data['Mobile']).exists():
                return Response({"message": "Mobile Number Already Exists", "status": 201, "data": []})
            else:
                companyID = request.data['companyID']
                SalesEmployeeName = request.data['SalesEmployeeName']
                EmployeeID = request.data['EmployeeID']
                userName = request.data['userName']
                password = request.data['password']
                firstName = request.data['firstName']
                middleName = request.data['middleName']
                lastName = request.data['lastName']
                Email = request.data['Email']
                Mobile = request.data['Mobile']
                role = request.data['role']
                position = request.data['position']
                branch = request.data['branch']
                Active = request.data['Active']
                salesUnit = request.data['salesUnit']
                #passwordUpdatedOn = request.data['passwordUpdatedOn']
                #lastLoginOn = request.data['lastLoginOn']
                #logedIn = request.data['logedIn']
                reportingTo = request.data['reportingTo']
                div = request.data['div']
                timestamp = request.data['timestamp']
                country = request.data['country']
                country_code = request.data['country_code']
                state = request.data['state']
                state_code = request.data['state_code']

            try:
                model = Employee(companyID=companyID, SalesEmployeeName=SalesEmployeeName, EmployeeID=EmployeeID, userName=userName, password=password, firstName=firstName, middleName=middleName,lastName=lastName, Email=Email, Mobile=Mobile, role=role, position=position, branch=branch, Active=Active, salesUnit=salesUnit, reportingTo=reportingTo, timestamp=timestamp, div=div, country = country, country_code = country_code, state = state,state_code = state_code)
                model.save()

                sp = Employee.objects.latest('id')

                if settings.SAPSP == True:
                    r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
                    token = json.loads(r.text)['SessionId']
                    print(token)

                    sp_data = {
                        "SalesEmployeeName": request.data['SalesEmployeeName'],
                        "EmployeeID": request.data['EmployeeID'],
                        "Active": "tYES",
                        "Mobile": request.data['Mobile'],
                        "Email": request.data['Email']
                    }

                    #print(sp_data)
                    #print(json.dumps(sp_data))

                    res = requests.post(settings.BASEURL+'/SalesPersons', data=json.dumps(sp_data), cookies=r.cookies, verify=False)
                    live = json.loads(res.text)

                    fetchid = sp.id

                    if "SalesEmployeeCode" in live:
                        print(live['SalesEmployeeCode'])

                        model = Employee.objects.get(pk=fetchid)
                        model.SalesEmployeeCode = live['SalesEmployeeCode']
                        model.save()

                        return Response({"message": "successful", "status": 200, "data": [{"Sp_Id": sp.id, "SalesEmployeeCode": live['SalesEmployeeCode']}]})
                    else:
                        SAP_MSG = live['error']['message']['value']
                        print(SAP_MSG)
                    if "already exists" in SAP_MSG:
                        fetchdata = Employee.objects.filter(pk=fetchid).delete()
                        return Response({"message": live['error']['message']['value'], "SAP_error": SAP_MSG, "status": 202, "data": []})
                    else:
                        fetchdata = Employee.objects.filter(pk=fetchid).delete()
                        return Response({"message": SAP_MSG, "SAP_error": SAP_MSG, "status": 202, "data": []})
                else:
                    model = Employee.objects.get(pk=sp.id)
                    model.SalesEmployeeCode = sp.id
                    model.save()
                    return Response({"message": "successful", "status": 200, "data": [{"Sp_Id": sp.id, "SalesEmployeeCode": sp.id}]})

            except Exception as e:
                return Response({"message": str(e), "status": 200, "data": []})

    except Exception as e:
        return Response({"message": str(e), "status": 200, "data": []})


#Employee All API


@api_view(["GET"])
def all(request):
    emps_obj = Employee.objects.all().order_by("-id")
    emps_json = EmployeeSerializer(emps_obj, many=True)
    emps_json = json.loads(json.dumps(emps_json.data))

    for employee_obj in emps_json:
        print(employee_obj['div'])
        if employee_obj['div'] != "":
            div_arr = employee_obj['div'].split(",")
            div_obj = Category.objects.filter(Number__in=div_arr)
            div_json = CategorySerializer(div_obj, many=True).data
            employee_obj['div'] = div_json
        else:
            employee_obj['div'] = []
    return Response({"message": "Success", "status": 200, "data": emps_json})


@api_view(["POST"])
def all_filter(request):
    json_data = request.data

    if "SalesEmployeeCode" in json_data:
        print("yes")

        if json_data['SalesEmployeeCode'] != "":
            SalesEmployeeCode = json_data['SalesEmployeeCode']

            emp_obj = Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin' or emp_obj.role == 'ceo':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0).order_by("-id")
                SalesEmployeeCode = []
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            elif emp_obj.role == 'manager':
                # .values('id', 'SalesEmployeeCode')
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode).order_by("-id")
                SalesEmployeeCode = [SalesEmployeeCode]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode = [SalesEmployeeCode]
                # emps = Employee.objects.filter(reportingTo=emp_obj.reportingTo)#.values('id', 'SalesEmployeeCode')
                # SalesEmployeeCode=[]
                # for emp in emps:
                # SalesEmployeeCode.append(emp.SalesEmployeeCode)

            print(SalesEmployeeCode)

            emps_all = Employee.objects.filter(
                SalesEmployeeCode__in=SalesEmployeeCode, Active="tYES").order_by("-id")
            emps_json = EmployeeSerializer(emps_all, many=True)

            emps_json = json.loads(json.dumps(emps_json.data))

            for employee_obj in emps_json:
                print(employee_obj['div'])
                if employee_obj['div'] != "":
                    div_arr = employee_obj['div'].split(",")
                    div_obj = Category.objects.filter(Number__in=div_arr)
                    div_json = CategorySerializer(div_obj, many=True).data
                    employee_obj['div'] = div_json
                else:
                    employee_obj['div'] = []

            return Response({"message": "Success", "status": 200, "data": emps_json})
            #return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess", "status": 201, "data": [{"error": "SalesEmployeeCode?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess", "status": 201, "data": [{"error": "SalesEmployeeCode?"}]})

#All Employee by reportingTo


@api_view(["POST"])
def all_filter_reportingto(request):
    json_data = request.data

    if "SalesEmployeeCode" in json_data:
        print("yes")

        if json_data['SalesEmployeeCode'] != "":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            emps_all1 = []
            # .values('id', 'SalesEmployeeCode')
            emps_all = Employee.objects.filter(reportingTo=SalesEmployeeCode)
            print(len(emps_all))
            print(SalesEmployeeCode)

            if len(emps_all) == 0:
                print(SalesEmployeeCode)
                return Response({"message": "Success", "status": 200, "data": []})
            else:
                emps_json = EmployeeSerializer(emps_all, many=True)
            return Response({"message": "Success", "status": 200, "data": emps_json.data})
        else:
            return Response({"message": "Unsuccess", "status": 201, "data": [{"error": "SalesEmployeeCode?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess", "status": 201, "data": [{"error": "SalesEmployeeCode?"}]})


@api_view(["POST"])
def all_filter_assignto(request):
    json_data = request.data

    if "SalesEmployeeCode" in json_data:
        print("yes")

        if json_data['SalesEmployeeCode'] != "":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            emps_all1 = []
            # .values('id', 'SalesEmployeeCode')
            emps_all = Employee.objects.filter(
                reportingTo=SalesEmployeeCode, Active="tYES")
            print(len(emps_all))
            print(SalesEmployeeCode)

            if len(emps_all) == 0:
                print(SalesEmployeeCode)
                emp_obj = Employee.objects.get(
                    SalesEmployeeCode=SalesEmployeeCode)
                # .values('id', 'SalesEmployeeCode')
                emps_all = Employee.objects.filter(
                    reportingTo=emp_obj.reportingTo, Active="tYES")
                emps_json = EmployeeSerializer(emps_all, many=True)
            else:
                #emps_json = EmployeeSerializer(emps_all, many=True)
                print("come")
                emp_obj = Employee.objects.get(
                    SalesEmployeeCode=SalesEmployeeCode)
                siblings = Employee.objects.filter(
                    reportingTo=emp_obj.reportingTo, Active="tYES")
                if len(siblings) != 0:
                    for sibling in siblings:
                        emps_all1.append(sibling)
                else:
                    emps_all1.append(emp_obj)

                for emps in emps_all:
                    emps_all1.append(emps)
                    emps_all_tree = Employee.objects.filter(
                        reportingTo=emps.SalesEmployeeCode, Active="tYES")  # .values('id',
                    print(emps.SalesEmployeeCode)
                    print("Code" + str(emps.SalesEmployeeCode))
                    print("Len" + str(len(emps_all_tree)))
                    if len(emps_all_tree) != 0:
                        for all_tree in emps_all_tree:
                            emps_all_tree1 = Employee.objects.filter(
                                reportingTo=all_tree.SalesEmployeeCode, Active="tYES")
                            if len(emps_all_tree1) != 0:
                                print("Code" + str(all_tree.SalesEmployeeCode))
                                print("Len" + str(len(emps_all_tree1)))
                                for all_tree1 in emps_all_tree1:
                                    print(
                                        "Code" + str(all_tree1.SalesEmployeeCode))
                                    emps_all1.append(all_tree1)
                            emps_all1.append(all_tree)
                emps_json = EmployeeSerializer(emps_all1, many=True)
            return Response({"message": "Success", "status": 200, "data": emps_json.data})

            #return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess", "status": 201, "data": [{"error": "SalesEmployeeCode?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess", "status": 201, "data": [{"error": "SalesEmployeeCode?"}]})


#Employee All Filter API
@api_view(["POST"])
def all_filter_old(request):
    json_data = request.data

    if len(json_data) == 0:
        emps_obj = Employee.objects.all().order_by("-id")
        emps_json = EmployeeSerializer(emps_obj, many=True)
        return Response({"message": "Success", "status": 200, "data": emps_json.data})
    else:
        #print(json_data.keys()[0])
        #if json_data['U_FAV']
        for ke in json_data.keys():
            if ke == 'reportingTo':
                if json_data['reportingTo'] != '':
                    emps_obj = Employee.objects.filter(
                        reportingTo=json_data['reportingTo']).order_by("-id")
                    if len(emps_obj) == 0:
                        return Response({"message": "Not Available", "status": 201, "data": []})
                    else:
                        emps_json = EmployeeSerializer(emps_obj, many=True)
                        return Response({"message": "Success", "status": 200, "data": emps_json.data})
            elif ke == 'role':
                if json_data['role'] != '':
                    emps_obj = Employee.objects.filter(
                        role=json_data['role']).order_by("-id")
                    if len(emps_obj) == 0:
                        return Response({"message": "Not Available", "status": 201, "data": []})
                    else:
                        emps_json = EmployeeSerializer(emps_obj, many=True)
                        return Response({"message": "Success", "status": 200, "data": emps_json.data})
            else:
                return Response({"message": "Not Available", "status": 201, "data": []})

#Employee One API


@api_view(["POST"])
def one(request):
    try:
        if "SalesEmployeeCode" in request.data:
            employee_obj = Employee.objects.get(SalesEmployeeCode=request.data['SalesEmployeeCode'])
        else:
            employee_obj = Employee.objects.get(id=request.data['id'])
        employee_json = json.loads(json.dumps(EmployeeSerializer(employee_obj).data))
        if employee_obj.div != "":
            div_arr = employee_obj.div.split(",")
            div_obj = Category.objects.filter(Number__in=div_arr)
            div_json = CategorySerializer(div_obj, many=True).data
            employee_json['div'] = div_json
        else:
            employee_json['div'] = []
        
        #{"SalesEmployeeCode": "37"}
        if employee_obj.reportingTo =="" or employee_obj.reportingTo=="0":
            repoto = ""
            repoRole = ""
        else:
            if Employee.objects.filter(SalesEmployeeCode=employee_obj.reportingTo).exists():
                rm = Employee.objects.get(SalesEmployeeCode=employee_obj.reportingTo)
                repoto = rm.SalesEmployeeName
                repoRole = rm.role
            else:
                repoto = employee_obj.reportingTo
                repoRole = employee_obj.reportingTo
        
        levdis = {"reportingName": repoto, "reportingRole": repoRole}
        print(levdis)        
        employee_json.update(levdis)

        return Response({"message": "Success", "status": 200, "data": [employee_json]})
    except Exception as e:
        return Response({"message": str(e), "status": 201, "data": []})

#Employee Login API
@api_view(["POST"])
def login(request):

    try:
        #added by millan for showing active users only
        if Employee.objects.filter(userName=request.data['userName'], Active="tYES").exists():
            userName = request.data['userName']
            password = request.data['password']
            FCM = request.data['FCM']

            if Employee.objects.filter(userName=userName, password=password).exists():
                print("uname")
                employee_obj = Employee.objects.get(
                    userName=userName, password=password)
            elif Employee.objects.filter(Email=userName, password=password).exists():
                print("email")
                employee_obj = Employee.objects.get(
                    Email=userName, password=password)
            else:
                print("incorrect")
                return Response({"message": "Username or password is incorrect", "status": 200, "data": [], "SAP": []})
            if FCM != "":
                employee_obj.FCM = FCM
                employee_obj.save()
            employee_json = EmployeeSerializer(employee_obj)

            if employee_obj.reportingTo == "0" or employee_obj.reportingTo == "":
                print("if")
                print(employee_obj.reportingTo)
                repoto = ""
                repoRole = ""
                print(repoto)
            else:
                print(employee_obj.reportingTo)
                print("else")
                repoto = Employee.objects.get(SalesEmployeeCode=employee_obj.reportingTo).SalesEmployeeName
                repoRole = Employee.objects.get(SalesEmployeeCode=employee_obj.reportingTo).role
                print(repoto)

            lev = tree(employee_obj.SalesEmployeeCode)
            #lev = tree_role(employee_obj)
            print(lev)
            json_ob = json.dumps(employee_json.data)
            json_obj = json.loads(json_ob)
            #print(json_obj)
            slave_obj = AppSlave.objects.filter(Level=lev)
            #print(slave_obj[0].Max)

            levdis = {"reportingName": repoto, "reportingRole": repoRole, "level": int(
                lev), "discount": slave_obj[0].Max}
            #print(levdis)
            json_obj.update(levdis)
            #print(json_obj)
            #print(employee_obj.div)
            if employee_obj.role == 'admin' or employee_obj.role == 'ceo':
                div_obj = Category.objects.all()
                div_json = CategorySerializer(div_obj, many=True).data
                print(div_json)
                json_obj['div'] = div_json
            else:  # employee_obj.div !="":
                div_arr = employee_obj.div.split(",")
                div_obj = Category.objects.filter(Number__in=div_arr)
                div_json = CategorySerializer(div_obj, many=True).data
                print(div_json)
                json_obj['div'] = div_json
            return Response({"message": "Success", "status": 200, "data": json_obj, "SAP": settings.SAPDB})
        else:
            return Response({"message": "User is InActive", "status": 201, "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": [{"Error": str(e)}]})

#Employee Update API


@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Employee.objects.get(pk=fetchid)

        model.companyID = request.data['companyID']
        model.SalesEmployeeName = request.data['SalesEmployeeName']
        model.EmployeeID = request.data['EmployeeID']
        model.userName = request.data['userName']
        model.password = request.data['password']
        model.firstName = request.data['firstName']
        model.middleName = request.data['middleName']
        model.lastName = request.data['lastName']
        model.Email = request.data['Email']
        model.Mobile = request.data['Mobile']
        model.role = request.data['role']
        model.position = request.data['position']
        model.branch = request.data['branch']
        model.Active = request.data['Active']
        model.salesUnit = request.data['salesUnit']
        model.reportingTo = request.data['reportingTo']
        model.div = 100  # request.data['div']
        model.country = request.data['country']
        model.country_code = request.data['country_code']
        model.state = request.data['state']
        model.state_code = request.data['state_code']

        model.save()
        if settings.SAPSP == True:
            context = {
                "id": request.data['id'],
                'companyID': request.data['companyID'],
                'SalesEmployeeCode': request.data['SalesEmployeeCode'],
                'SalesEmployeeName': request.data['SalesEmployeeName'],
                'EmployeeID': request.data['EmployeeID'],
                'userName': request.data['userName'],
                'password': request.data['password'],
                'firstName': request.data['firstName'],
                'middleName': request.data['middleName'],
                'lastName': request.data['lastName'],
                'Email': request.data['Email'],
                'Mobile': request.data['Mobile'],
                'role': request.data['role'],
                'position': request.data['position'],
                'branch': request.data['branch'],
                'Active': request.data['Active'],
                'salesUnit': request.data['salesUnit'],
                'reportingTo': request.data['reportingTo']
            }

            r = requests.post(settings.BASEURL+'/Login',
                              data=json.dumps(settings.SAPDB), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)

            sp_data = {
                "SalesEmployeeName": request.data['SalesEmployeeName'],
                "EmployeeID": request.data['EmployeeID'],
                "Active": request.data['Active'],
                "Mobile": request.data['Mobile'],
                "Email": request.data['Email']
            }

            print(sp_data)
            print(json.dumps(sp_data))

            print(settings.BASEURL+'/SalesPersons(' +
                  request.data['SalesEmployeeCode']+')')

            res = requests.patch(settings.BASEURL+'/SalesPersons(' +
                                 request.data['SalesEmployeeCode']+')', data=json.dumps(sp_data), cookies=r.cookies, verify=False)

            if len(res.content) != 0:
                res1 = json.loads(res.content)
                SAP_MSG = res1['error']['message']['value']
                print(SAP_MSG)
                return Response({"message": "Partely successful", "status": 202, "SAP_error": SAP_MSG, "data": [context]})
            else:
                return Response({"message": "successful", "status": 200, "data": [context]})
        else:
            return Response({"message": "successful", "status": 200, "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": []})

#Employee delete


@api_view(['POST'])
def delete(request):
    try:
        fetchid = request.data['id']
        emp = Employee.objects.get(pk=fetchid)
        SalesEmployeeCode = emp.SalesEmployeeCode

        fetchdata = Employee.objects.filter(pk=fetchid).delete()
        if settings.SAPSP == True:
            # print(data)

            try:
                r = requests.post(settings.BASEURL+'/Login',
                                  data=json.dumps(settings.SAPDB), verify=False)
                token = json.loads(r.text)['SessionId']
                print(token)
                res = requests.delete(
                    settings.BASEURL+'/SalesPersons('+SalesEmployeeCode+')', cookies=r.cookies, verify=False)
                return Response({"message": "successful", "status": "200", "data": []})
            except:
                return Response({"message": "successful", "status": "200", "data": []})
        else:
            return Response({"message": "successful", "status": "200", "data": []})
    except:
        return Response({"message": "Id wrong", "status": "201", "data": []})


def months_check(months, qt1, qt2, qt3, qt4):
    q1 = q2 = q3 = q4 = 0
    for mo in months:
        if mo['qtr'] == 1:
            q1 = q1 + int(mo['amount'])
        elif mo['qtr'] == 2:
            q2 = q2 + int(mo['amount'])
        elif mo['qtr'] == 3:
            q3 = q3 + int(mo['amount'])
        elif mo['qtr'] == 4:
            q4 = q4 + int(mo['amount'])

    if q1 != qt1:
        return {"message": "The months total of Qtr 1 should be equal to Q1 value", "data": q1}
    elif q2 != qt2:
        return {"message": "The months total of Qtr 2 should be equal to Q2 value", "data": q2}
    elif q3 != qt3:
        return {"message": "The months total of Qtr 3 should be equal to Q3 value", "data": q3}
    elif q4 != qt4:
        return {"message": "The months total of Qtr 4 should be equal to Q4 value", "data": q4}
    else:
        return "ok"

#Target Create API


@api_view(['POST'])
def targetqtm_create(request):

    try:
        if request.data['id'] != "":
            #StartYear = int(request.data['StartYear'])
            #EndYear = int(request.data['EndYear'])
            SalesPersonCode = request.data['SalesPersonCode']
            #Department = request.data['Department']
            reportingTo = request.data['reportingTo'].strip()
            YearTarget = request.data['YearTarget']
            q1 = int(request.data['q1'])
            q2 = int(request.data['q2'])
            q3 = int(request.data['q3'])
            q4 = int(request.data['q4'])

            CreatedDate = request.data['CreatedDate']
            UpdatedDate = request.data['UpdatedDate']

            if Targetqty.objects.filter(pk=request.data['id']).exists():
                qtymodel = Targetqty.objects.get(pk=request.data['id'])
            else:
                return Response({"message": "Qtr info does not exists", "status": "201", "data": []})

            YearTargetAmount = Targetyr.objects.get(pk=YearTarget).YearTarget
            print(YearTargetAmount)
            print(q1+q2+q3+q4)

            if YearTargetAmount != (q1+q2+q3+q4):
                return Response({"message": "YearTarget should be equal to all quater", "status": "201", "data": []})
            elif (q1 < 1 or q2 < 1 or q3 < 1 or q4 < 1):
                return Response({"message": "All Qtr should be fill", "status": "201", "data": []})
            elif SalesPersonCode == reportingTo:
                return Response({"message": "SalesPersonCode and reportingTo are same", "status": "201", "data": []})
            else:

                if reportingTo == "" or reportingTo == "0":
                    qtymodel.SalesPersonCode_id = SalesPersonCode
                    qtymodel.YearTarget_id = YearTarget
                    qtymodel.q1 = q1
                    qtymodel.q2 = q2
                    qtymodel.q3 = q3
                    qtymodel.q4 = q4
                    qtymodel.CreatedDate = CreatedDate
                    qtymodel.UpdatedDate = CreatedDate
                else:
                    qtymodel.SalesPersonCode_id = SalesPersonCode
                    qtymodel.reportingTo_id = reportingTo
                    qtymodel.YearTarget_id = YearTarget
                    qtymodel.q1 = q1
                    qtymodel.q2 = q2
                    qtymodel.q3 = q3
                    qtymodel.q4 = q4
                    qtymodel.CreatedDate = CreatedDate
                    qtymodel.UpdatedDate = CreatedDate
                qtymodel.save()
                tgt = Targetqty.objects.latest('id')
                #print(tgt.id)
                if len(request.data['monthly']) == 12:
                    months = request.data['monthly']
                    if months[0]['amount'] < 1 or months[1]['amount'] < 1 or months[2]['amount'] < 1 or months[3]['amount'] < 1 or months[4]['amount'] < 1 or months[5]['amount'] < 1 or months[6]['amount'] < 1 or months[7]['amount'] < 1 or months[8]['amount'] < 1 or months[9]['amount'] < 1 or months[10]['amount'] < 1 or months[11]['amount'] < 1:
                        return Response({"message": "Quaterley saved but monthly try again after fill all months", "status": "201", "data": []})
                    else:

                        chk = months_check(
                            request.data['monthly'], request.data['q1'], request.data['q2'], request.data['q3'], request.data['q4'])

                        if chk == "ok":
                            if request.data['monthly'][0]["id"] != "":
                                for mo in months:
                                    mont = Target.objects.get(pk=mo['id'])
                                    print(mo['id'])
                                    print(mont)
                                    mont.YearTarget_id = YearTarget
                                    mont.amount = mo['amount']
                                    mont.monthYear = mo['monthYear']
                                    mont.SalesPersonCode_id = SalesPersonCode
                                    mont.qtr = mo['qtr']
                                    mont.CreatedDate = mo['CreatedDate']
                                    mont.UpdatedDate = mo['CreatedDate']
                                    mont.save()
                            else:
                                for mo in months:
                                    mont = Target(YearTarget_id=YearTarget, amount=mo['amount'], monthYear=mo['monthYear'],
                                                  SalesPersonCode_id=SalesPersonCode, qtr=mo['qtr'], CreatedDate=mo['CreatedDate'], UpdatedDate=mo['CreatedDate'])
                                    mont.save()
                            return Response({"message": "Success", "status": "200", "data": []})
                        else:
                            print(chk)
                            return Response({"message": chk['message'], "status": "201", "data": chk['data']})

                else:
                    return Response({"message": "Quaterley saved but monthly try again after fill all months", "status": "201", "data": []})
        else:
            #StartYear = int(request.data['StartYear'])
            #EndYear = int(request.data['EndYear'])
            SalesPersonCode = request.data['SalesPersonCode']
            #Department = request.data['Department']
            reportingTo = request.data['reportingTo'].strip()
            YearTarget = request.data['YearTarget']
            q1 = int(request.data['q1'])
            q2 = int(request.data['q2'])
            q3 = int(request.data['q3'])
            q4 = int(request.data['q4'])

            CreatedDate = request.data['CreatedDate']
            UpdatedDate = request.data['UpdatedDate']

            if len(Targetqty.objects.filter(YearTarget=YearTarget, SalesPersonCode=SalesPersonCode)) > 0:
                return Response({"message": "Already exist with this Financial Year", "status": "201", "data": []})
            YearTargetAmount = Targetyr.objects.get(pk=YearTarget).YearTarget
            print(YearTargetAmount)
            print(q1+q2+q3+q4)

            if YearTargetAmount != (q1+q2+q3+q4):
                return Response({"message": "YearTarget should be equal to all quater", "status": "201", "data": []})
            elif (q1 < 1 or q2 < 1 or q3 < 1 or q4 < 1):
                return Response({"message": "All Qtr should be fill", "status": "201", "data": []})
            elif SalesPersonCode == reportingTo:
                return Response({"message": "SalesPersonCode and reportingTo are same", "status": "201", "data": []})
            else:

                if reportingTo == "" or reportingTo == "0":
                    model = Targetqty(SalesPersonCode_id=SalesPersonCode, YearTarget_id=YearTarget,
                                      q1=q1, q2=q2, q3=q3, q4=q4, CreatedDate=CreatedDate, UpdatedDate=CreatedDate)
                else:
                    model = Targetqty(SalesPersonCode_id=SalesPersonCode, reportingTo_id=reportingTo, YearTarget_id=YearTarget,
                                      q1=q1, q2=q2, q3=q3, q4=q4, CreatedDate=CreatedDate, UpdatedDate=CreatedDate)

                    #print("reportingTo_id="+str(reportingTo))

                model.save()
                tgt = Targetqty.objects.latest('id')
                #print(tgt.id)
                if len(request.data['monthly']) == 12:
                    months = request.data['monthly']
                    if months[0]['amount'] < 1 or months[1]['amount'] < 1 or months[2]['amount'] < 1 or months[3]['amount'] < 1 or months[4]['amount'] < 1 or months[5]['amount'] < 1 or months[6]['amount'] < 1 or months[7]['amount'] < 1 or months[8]['amount'] < 1 or months[9]['amount'] < 1 or months[10]['amount'] < 1 or months[11]['amount'] < 1:
                        return Response({"message": "Quaterley saved but monthly try again after fill all months", "status": "201", "data": []})
                    else:
                        chk = months_check(
                            request.data['monthly'], request.data['q1'], request.data['q2'], request.data['q3'], request.data['q4'])

                        if chk == "ok":
                            for mo in months:
                                mont = Target(YearTarget_id=YearTarget, amount=mo['amount'], monthYear=mo['monthYear'],
                                              SalesPersonCode_id=SalesPersonCode, qtr=mo['qtr'], CreatedDate=mo['CreatedDate'], UpdatedDate=mo['CreatedDate'])
                                mont.save()
                            return Response({"message": "Success", "status": "200", "data": []})
                        else:
                            print(chk)
                            return Response({"message": chk['message'], "status": "201", "data": chk['data']})
                else:
                    return Response({"message": "Quaterley saved but monthly try again after fill all months", "status": "201", "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": [{"Error": str(e)}]})


def check_year(yeardata):
    StartYear = yeardata[0]['StartYear']
    EndYear = yeardata[0]['EndYear']
    Department = yeardata[0]['Department']
    reportingTo = yeardata[0]['reportingTo']

    if Targetyr.objects.filter(StartYear=StartYear, EndYear=EndYear, SalesPersonCode=reportingTo, Department=Department).exists():
        YearTarget = Targetyr.objects.get(
            StartYear=StartYear, EndYear=EndYear, SalesPersonCode=reportingTo, Department=Department).YearTarget
        ttl = 0
        for dt in yeardata:
            ttl = ttl+int(dt['YearTarget'])
        if YearTarget == ttl:
            return "ok"
        else:
            return "Team distribution total should be equal to Target Goal"
    else:
        return "ok"

#Target yr Create API


@api_view(['POST'])
def targetyr_create(request):
    try:
        yrs = request.data
        chk = check_year(yrs)
        if chk == "ok":
            for yr in yrs:
                StartYear = int(yr['StartYear'])
                EndYear = int(yr['EndYear'])
                SalesPersonCode = yr['SalesPersonCode']
                Department = yr['Department']
                reportingTo = yr['reportingTo'].strip()
                YearTarget = int(yr['YearTarget'])

                CreatedDate = yr['CreatedDate']
                UpdatedDate = yr['UpdatedDate']

                if len(Targetyr.objects.filter(StartYear=StartYear, EndYear=EndYear, SalesPersonCode=SalesPersonCode, Department=Department)) > 0:
                    return Response({"message": "Already exist with this Financial Year", "status": "201", "data": []})
                print(YearTarget)
                if SalesPersonCode == reportingTo:
                    return Response({"message": "SalesPersonCode and reportingTo are same", "status": "201", "data": []})
                elif StartYear == EndYear:
                    return Response({"message": "StartYear and EndYear are same", "status": "201", "data": []})
                else:

                    if reportingTo == "":
                        model = Targetyr(StartYear=StartYear, EndYear=EndYear, SalesPersonCode_id=SalesPersonCode,
                                         Department=Department, YearTarget=YearTarget, CreatedDate=CreatedDate, UpdatedDate=CreatedDate)
                    else:
                        model = Targetyr(StartYear=StartYear, EndYear=EndYear, SalesPersonCode_id=SalesPersonCode, Department=Department,
                                         reportingTo_id=reportingTo, YearTarget=YearTarget, CreatedDate=CreatedDate, UpdatedDate=CreatedDate)

                    model.save()
                    #tgt = Targetyr.objects.latest('id')
                    #print(tgt.id)
            return Response({"message": "Success", "status": "200", "data": []})
        else:
            return Response({"message": chk, "status": "201", "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": [{"Error": str(e)}]})

#targetqty all API


@api_view(["POST"])
def target_all(request):
    SalesPersonCode = request.data['SalesPersonCode']
    target_obj = Target.objects.filter(SalesPersonCode=SalesPersonCode)
    target_json = TargetSerializer(target_obj, many=True)
    return Response({"message": "Success", "status": 200, "data": target_json.data})

#targetqty all API


@api_view(["POST"])
def targetqtm_all(request):
    YearTarget = request.data['YearTarget']
    targetqty_obj = Targetqty.objects.filter(YearTarget=YearTarget)
    if len(targetqty_obj) > 0:
        targetqty_json = TargetqtySerializer(targetqty_obj, many=True)
        m_obj = Target.objects.filter(YearTarget=YearTarget)
        m_json = TargetSerializer(m_obj, many=True)

        targetqty_json.data[0]["monthly"] = m_json.data

        return Response({"message": "Success", "status": 200, "data": targetqty_json.data})
    else:
        return Response({"message": "Success", "status": 200, "data": []})

#targetqty all API


@api_view(["POST"])
def targetyr_all(request):
    SalesPersonCode = request.data['SalesPersonCode']
    targetyr_obj = Targetyr.objects.filter(SalesPersonCode=SalesPersonCode)
    targetyr_json = TargetyrSerializer(targetyr_obj, many=True)
    return Response({"message": "Success", "status": 200, "data": targetyr_json.data})

#All Employee by reportingTo


@api_view(["POST"])
def targetyr_all_filter(request):
    try:
        dt = request.data
        tgt_obj = Targetyr.objects.filter(
            StartYear=dt['StartYear'], EndYear=dt['EndYear'], Department=dt['Department'], reportingTo=dt['reportingTo'])
        tgt_json = TargetyrSerializer(tgt_obj, many=True)
        return Response({"message": "success", "status": 200, "data": tgt_json.data})
    except Exception as e:
        return Response({"message": str(e), "status": 201, "data": []})

#targetqty close


@api_view(["POST"])
def targetqty_close(request):
    id = request.data["id"]
    try:
        model = Targetqty.objects.filter(pk=id).update(status=1)
        return Response({"message": "Success", "Status": 200, "data": []})
    except Exception as e:
        return Response({"message": str(e), "Status": 200, "data": []})

#targetyr close


@api_view(["POST"])
def targetyr_close(request):
    id = request.data["id"]
    try:
        model = Targetyr.objects.filter(pk=id).update(status=1)
        return Response({"message": "Success", "Status": 200, "data": []})
    except Exception as e:
        return Response({"message": str(e), "Status": 200, "data": []})

#product lead


@api_view(["POST"])
def ProductLead(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']

        emp_obj = Employee.objects.get(SalesEmployeeCode=SalesPersonCode)

        if emp_obj.role == 'manager':
            # .values('id', 'SalesEmployeeCode')
            emps = Employee.objects.filter(reportingTo=SalesPersonCode)
            SalesPersonCode = [SalesPersonCode]
            for emp in emps:
                SalesPersonCode.append(emp.SalesEmployeeCode)

        elif emp_obj.role == 'admin' or emp_obj.role == 'ceo':
            emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
            SalesPersonCode = []
            #{"SalesPersonCode":1}
            for emp in emps:
                SalesPersonCode.append(emp.SalesEmployeeCode)
        else:
            SalesPersonCode = request.data['SalesPersonCode']

        print(SalesPersonCode)

        BFS = Lead.objects.filter(
            assignedTo__in=SalesPersonCode, intProdCat="Bottle Filling Stations").count()
        DWF = Lead.objects.filter(
            assignedTo__in=SalesPersonCode, intProdCat="Drinking Water Fountains").count()
        WC = Lead.objects.filter(
            assignedTo__in=SalesPersonCode, intProdCat="Water Coolers").count()
        WCH = Lead.objects.filter(
            assignedTo__in=SalesPersonCode, intProdCat="Water Chillers").count()
        DWS = Lead.objects.filter(
            assignedTo__in=SalesPersonCode, intProdCat="Drinking Water Stations").count()
        DWT = Lead.objects.filter(
            assignedTo__in=SalesPersonCode, intProdCat="Drinking Water Taps").count()
        WD = Lead.objects.filter(
            assignedTo__in=SalesPersonCode, intProdCat="Water Dispenser").count()
        OZO = Lead.objects.filter(
            assignedTo__in=SalesPersonCode, intProdCat="Ozonators").count()
        return Response({"message": "Success", "Status": 200, "data": [{
            "Bottle Filling Stations": str(BFS), "Drinking Water Fountains": str(DWF), "Water Coolers": str(WC), "Water Chillers": str(WCH), "Drinking Water Stations": str(DWS), "Drinking Water Taps": str(DWT), "Water Dispenser": str(WD), "Ozonators": str(OZO)
        }]})
    except Exception as e:
        return Response({"message": str(e), "Status": 201, "data": []})

#project lead


@api_view(["POST"])
def ProjectLead(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']

        emp_obj = Employee.objects.get(SalesEmployeeCode=SalesPersonCode)

        if emp_obj.role == 'manager':
            # .values('id', 'SalesEmployeeCode')
            emps = Employee.objects.filter(reportingTo=SalesPersonCode)
            SalesPersonCode = [SalesPersonCode]
            for emp in emps:
                SalesPersonCode.append(emp.SalesEmployeeCode)

        elif emp_obj.role == 'admin' or emp_obj.role == 'ceo':
            emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
            SalesPersonCode = []
            for emp in emps:
                SalesPersonCode.append(emp.SalesEmployeeCode)
        else:
            SalesPersonCode = request.data['SalesPersonCode']

        print(SalesPersonCode)
        WTP = Lead.objects.filter(
            assignedTo__in=SalesPersonCode, intProjCat="Water Treatment Plant").count()
        STP = Lead.objects.filter(
            assignedTo__in=SalesPersonCode, intProjCat="Sewage Treatment Plant").count()
        WS = Lead.objects.filter(
            assignedTo__in=SalesPersonCode, intProjCat="Water Softner").count()
        ETP = Lead.objects.filter(
            assignedTo__in=SalesPersonCode, intProjCat="Effluent Treatment Plant").count()
        ROP = Lead.objects.filter(
            assignedTo__in=SalesPersonCode, intProjCat="Reverse Osmosis Plant").count()
        UFP = Lead.objects.filter(
            assignedTo__in=SalesPersonCode, intProjCat="Ultra Filtration Plant").count()
        return Response({"message": "Success", "Status": 200, "data": [{
            "Water Treatment Plant": str(WTP), "Sewage Treatment Plant": str(STP), "Water Softner": str(WS), "Effluent Treatment Plant": str(ETP), "Reverse Osmosis Plant": str(ROP), "Ultra Filtration Plant": str(UFP)
        }]})
    except Exception as e:
        return Response({"message": str(e), "Status": 201, "data": []})
