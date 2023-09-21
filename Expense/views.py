import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Expense.models import Expense, ExpenseStatusRemarks, ExpenseType
from Expense.serializers import ExpenseApprovalSerializer, ExpenseSerializer, ExpenseTypeSerializer
from BusinessPartner.models import BPEmployee
from BusinessPartner.serializers import BPEmployeeSerializer

from Attachment.models import Attachment
from Attachment.serializers import AttachmentSerializer
import os
from django.core.files.storage import FileSystemStorage

from Employee.models import Employee
from Employee.serializers import EmployeeSerializer

from global_methods import *

#Expense Create API
@api_view(['POST'])
def create(request):
    try:
        trip_name = request.data['trip_name']
        type_of_expense = request.data['type_of_expense']
        expense_from = request.data['expense_from']
        expense_to = request.data['expense_to']
        totalAmount = request.data['totalAmount']
        createDate = request.data['createDate']
        createTime = request.data['createTime']
        createdBy = request.data['createdBy']
        remarks = request.data['remarks']
        employeeId = request.data['employeeId']
        
        Attach = request.data['Attach']

        model = Expense(remarks=remarks, trip_name=trip_name, type_of_expense=type_of_expense, expense_from=expense_from, expense_to=expense_to, totalAmount=totalAmount, createDate=createDate, createTime=createTime, createdBy=createdBy, employeeId = employeeId)

        model.save()
        
        ExpenseID = Expense.objects.latest('id')
        
        print(request.FILES.getlist('Attach'))
        for File in request.FILES.getlist('Attach'):
            attachmentsImage_url = ""
            target ='./bridge/static/image/Expense'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge', '')
            
            print(attachmentsImage_url)

            att=Attachment(File=attachmentsImage_url, LinkType="Expense", LinkID=ExpenseID.id, CreateDate=createDate, CreateTime=createTime)
        
            att.save()
        
        return Response({"message": "successful", "status": "200", "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": []})

#Expense All API
@api_view(["GET"])
def all(request):
    expn_obj = Expense.objects.all().order_by("-id")
    result = showExpense(expn_obj)
    return Response({"message": "Success","status": 200,"data":result})

#Expense All API
@api_view(["POST"])
def all_filter(request):
    try:  
        employeeId = request.data['employeeId']
        if Employee.objects.filter(SalesEmployeeCode = employeeId).exists():
            expn_obj = Expense.objects.filter(employeeId = employeeId).order_by("-id")
            result = showExpense(expn_obj)
            return Response({"message": "Success","status": 200,"data":result})
        else:
            return Response({"message": "Invalid Employee Id","status": 201,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})



#Expense All API
@api_view(["POST"])
def all_filter_page(request):
    try:  
        PageNo = request.data['PageNo']
        MaxItem = request.data['MaxItem']
        if MaxItem!="All":
            endWith = (PageNo * MaxItem)
            startWith = (endWith - MaxItem)

        employeeId = request.data['employeeId']
        if Employee.objects.filter(SalesEmployeeCode = employeeId).exists():
            emps = showEmployeeData(employeeId)
            exp_count = Expense.objects.filter(employeeId__in = emps).count()
            if MaxItem != "All":
                expn_obj = Expense.objects.filter(employeeId__in = emps).order_by("-id")[startWith:endWith]
            else:
                expn_obj = Expense.objects.filter(employeeId__in = emps).order_by("-id")

            res_data = showExpense(expn_obj)
            return Response({"message": "Success","status": 200,"data":res_data, "extra":{"total_count":exp_count}})
        else:
            return Response({"message": "Invalid Employee Id","status": 201,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})




#Expense One API
@api_view(["POST"])
def one(request):
    try:
        id = request.data['id']
        if Expense.objects.filter(pk=request.data['id']).exists():
            expn_obj = Expense.objects.filter(pk=request.data['id'])
            result = showExpense(expn_obj)
            return Response({"message": "Success","status": 200,"data":result})
        else:
            return Response({"message": "Id Doesn't Exist", "status": 201, "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": 201, "data": []})

#Expense Update API
@api_view(['POST'])
def update(request):
    try:
        fetchid = request.data['id']
        model = Expense.objects.get(pk = fetchid)
        model.remarks = request.data['remarks']
        model.trip_name = request.data['trip_name']
        model.type_of_expense = request.data['type_of_expense']
        model.expense_from = request.data['expense_from']
        model.expense_to = request.data['expense_to']
        model.totalAmount = request.data['totalAmount']
        model.updateDate = request.data['updateDate']
        model.updateTime = request.data['updateTime']
        model.updatedBy = request.data['updatedBy']
        model.employeeId = request.data['employeeId']
        
        Attach = request.data['Attach']  
        for File in request.FILES.getlist('Attach'):
            attachmentsImage_url = ""
            target ='./bridge/static/image/Expense'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge', '')
            
            print(attachmentsImage_url)

            att=Attachment(File=attachmentsImage_url, LinkType="Expense", LinkID=fetchid, CreateDate=model.updateDate, CreateTime=model.updateTime)
        
            att.save()

        model.save()

        return Response({"message":"successful","status":200,"data":[]})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})
    
#Expense Delete API
@api_view(['POST'])
def delete(request):
    fetchids= request.data['id']
    try:
        for ids in fetchids:
            Expense.objects.filter(pk=ids).delete()
            
        return Response({"message":"successful","status":"200","data":[]})   
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

#Expense Data for all expenses and one expense
def showExpense(objs):
    allexpn = []
    for obj in objs:
        createPerson = obj.createdBy  
        updatePerson = obj.updatedBy  
        employeePer = obj.employeeId  
        # type_of_expense = obj.type_of_expense  
        rsm_approval = obj.rsm_approval
        accountant_approval = obj.accountant_approval
        
        expn_json = ExpenseSerializer(obj)
        finalExpnData = json.loads(json.dumps(expn_json.data))
            
        # if ExpenseType.objects.filter(pk = type_of_expense).exists():
        #     createPersonObj = ExpenseType.objects.filter(pk = type_of_expense)
        #     createPersonjson = ExpenseTypeSerializer(createPersonObj, many=True)
        #     finalExpnData['type_of_expense'] = createPersonjson.data
        # else:
        #     finalExpnData['type_of_expense'] = []
        
        if Employee.objects.filter(SalesEmployeeCode = createPerson).exists():
            createPersonObj = Employee.objects.filter(SalesEmployeeCode = createPerson).values('id','firstName', 'lastName')
            createPersonjson = EmployeeSerializer(createPersonObj, many=True)
            finalExpnData['createdBy'] = createPersonjson.data
        else:
            finalExpnData['createdBy'] = []
            
        if Employee.objects.filter(SalesEmployeeCode = updatePerson).exists():
            updatePersonObj = Employee.objects.filter(SalesEmployeeCode = updatePerson).values('id','firstName', 'lastName')
            updatePersonjson = EmployeeSerializer(updatePersonObj, many=True)
            finalExpnData['updatedBy'] = updatePersonjson.data
        else:
            finalExpnData['updatedBy'] = []
            
        if Attachment.objects.filter(LinkID = obj.DailyService_id, LinkType="Service").exists():
            Attach_dls = Attachment.objects.filter(LinkID = obj.DailyService_id, LinkType="Service")
            Attach_json = AttachmentSerializer(Attach_dls, many=True)
            finalExpnData['Attach'] = Attach_json.data
        else:
            finalExpnData['Attach'] = []
            
        if Employee.objects.filter(SalesEmployeeCode = employeePer).exists():
            employeePerObj = Employee.objects.filter(SalesEmployeeCode = employeePer).values('id','firstName', 'lastName')
            employeePerjson = EmployeeSerializer(employeePerObj, many=True)
            finalExpnData['employeeId'] = employeePerjson.data
        else:
            finalExpnData['employeeId'] = []
        
        if Employee.objects.filter(SalesEmployeeCode = rsm_approval).exists():
            rsm_approvalObj = Employee.objects.filter(SalesEmployeeCode = rsm_approval).values('id','firstName', 'lastName')
            rsm_approvaljson = EmployeeSerializer(rsm_approvalObj, many=True)
            finalExpnData['rsm_approval'] = rsm_approvaljson.data
        else:
            finalExpnData['rsm_approval'] = []

        if Employee.objects.filter(SalesEmployeeCode = accountant_approval).exists():
            accountant_approvalObj = Employee.objects.filter(SalesEmployeeCode = accountant_approval).values('id','firstName', 'lastName')
            accountant_approvaljson = EmployeeSerializer(accountant_approvalObj, many=True)
            finalExpnData['accountant_approval'] = accountant_approvaljson.data
        else:
            finalExpnData['accountant_approval'] = []
        allexpn.append(finalExpnData)
    return allexpn

#Expense Delete API
@api_view(['POST'])
def expense_img_delete(request):
    expense_id= request.data['id']
    
    image_id = request.data['image_id']
    
    try:
        if Attachment.objects.filter(pk=image_id , LinkID=expense_id).exists():
            Attachment.objects.filter(pk=image_id, LinkID=expense_id).delete()
            
            return Response({"message":"successful","status":"200","data":[]})        
        else:
            return Response({"message":"Id Not Found","status":"201","data":[]})        
    except:
        return Response({"message":"Id wrong","status":"201","data":[]})

#approval expense API
@api_view(['POST'])
def approval_update(request):
    try:
        fetchid = request.data['id']
        model = Expense.objects.get(pk = fetchid)
        model.approval_remark = request.data['approval_remark']
        model.status = request.data['status']
        model.approvalId = request.data['approvalId']
        model.save()
        return Response({"message":"successful","status":200,"data":[]})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})



#create status remark
@api_view(['POST'])
def approval_status(request):
    try:
        Exp_id = request.data['Exp_id']
        SalesEmployeeCode = request.data['SalesEmployeeCode']
        Type = request.data['Type']
        Status = request.data['Status']
        Remarks = request.data['Remarks']
        status_remark = ExpenseStatusRemarks(Expense_id=Exp_id, SalesEmployeeCode=SalesEmployeeCode, Type=Type, Status=Status, Remarks=Remarks)
        status_remark.save()
        
        if Type == "RSM":
            Expense.objects.filter(id=Exp_id).update(rsm_status=Status,rsm_approval=int(SalesEmployeeCode))
        if Type == "ACCOUNTANT":
            Expense.objects.filter(id=Exp_id).update(accountant_status=Status,accountant_approval=int(SalesEmployeeCode))

        return Response({"message":"successful","status":200,"data":[]})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})



#approval expense API
@api_view(['POST'])
def approval_list(request):
    try:
        Exp_id = request.data['Exp_id']
        Type = request.data['Type']
        model = ExpenseStatusRemarks.objects.filter(Expense_id = Exp_id, Type=Type)
        serializers = ExpenseApprovalSerializer(model, many=True).data
        return Response({"message":"successful","status":200,"data":serializers})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})




