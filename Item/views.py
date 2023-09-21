from django.conf import settings
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .models import *
import requests, json

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser
# Create your views here.  

#Item All API
@api_view(["POST"])
def all(request):
    ItemsGroupCode = request.data['ItemsGroupCode']
    if ItemsGroupCode !="":
        item_obj = Item.objects.filter(ItemsGroupCode=ItemsGroupCode)
        item_json = ItemSerializer(item_obj, many=True)
        return Response({"message": "Success","status": 200,"data":item_json.data})
    else:
        item_obj = Item.objects.all()
        item_json = ItemSerializer(item_obj, many=True)
        return Response({"message": "Success","status": 200,"data":item_json.data})

#Item All API
@api_view(["POST"])
def all_filter_page(request):
    ItemsGroupCode = request.data['ItemsGroupCode']
    PageNo = request.data['PageNo']
    search = request.data['SearchText']
    try:
        MaxItem = request.data['MaxItem']
    except:
        MaxItem = 10
    endWith = (PageNo * MaxItem)
    startWith = (endWith - MaxItem)
    if ItemsGroupCode !="":
        item_obj = Item.objects.filter(ItemsGroupCode=ItemsGroupCode, ItemName__icontains=search)[startWith:endWith]
        item_json = ItemSerializer(item_obj, many=True)
        return Response({"message": "Success","status": 200,"data":item_json.data})
    else:
        item_obj = Item.objects.all()[startWith:endWith]
        item_json = ItemSerializer(item_obj, many=True)
        return Response({"message": "Success","status": 200,"data":item_json.data})

#Item All API
@api_view(["POST"])
def count_all(request):
    ItemsGroupCode = request.data['ItemsGroupCode']
    search = request.data['SearchText']
    if ItemsGroupCode !="":
        item_obj = Item.objects.filter(ItemsGroupCode=ItemsGroupCode, ItemName__icontains=search).count()
        return Response({"message": "Success","status": 200,"data":[{"total_count":item_obj}]})
    else:
        item_obj = Item.objects.all().count()
        return Response({"message": "Success","status": 200,"data":[{"total_count":item_obj}]})

#Item All API
@api_view(["GET"])
def all1(request):
    #item_obj = Item.objects.filter(pk=10,ItemsGroupCode=110).values("id","ItemCode","ItemName")
    item_obj = Item.objects.all().values("ItemCode","ItemName")
    print(item_obj)
    item_json = ItSerializer(item_obj, many=True)
    return Response({"message": "Success","status": 200,"data":item_json.data})


#Item All API
@api_view(["GET"])
def all1_filter_page(request):
    PageNo = request.data['PageNo']
    try:
        MaxItem = request.data['MaxItem']
    except:
        MaxItem = 10
    endWith = (PageNo * MaxItem)
    startWith = (endWith - MaxItem)
    #item_obj = Item.objects.filter(pk=10,ItemsGroupCode=110).values("id","ItemCode","ItemName")
    item_obj = Item.objects.all().values("ItemCode","ItemName")[startWith:endWith]
    print(item_obj)
    item_json = ItSerializer(item_obj, many=True)
    return Response({"message": "Success","status": 200,"data":item_json.data})



#Item All API
@api_view(["GET"])
def count_all1(request):
    #item_obj = Item.objects.filter(pk=10,ItemsGroupCode=110).values("id","ItemCode","ItemName")
    item_obj = Item.objects.all().count()
    return Response({"message": "Success","status": 200,"data":[{"total_count":item_obj}]})



#Item One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    item_obj = Item.objects.get(id=id)
    item_json = ItemSerializer(item_obj, many=False)
    return Response({"message": "Success","status": 200,"data":item_json.data})

#Tax All API
@api_view(["GET"])
def tax_all(request):
    tax_obj = Tax.objects.all()
    tax_json = TaxSerializer(tax_obj, many=True)
    return Response({"message": "Success","status": 200,"data":tax_json.data})


# function created by abhishek
@api_view(["GET"])
def distributionlist(Request):
    obj = Department.objects.all()
    json = DepartmentSerializer(obj, many=True)
    return Response({"message": "Success","status": 200,"data":json.data})

# function created by abhishek
@api_view(["GET"])
def distributionlist_old(Request):
    try:
        # with open("./bridge/db.json") as f:
            
            # 

            


        # Loin to create session variable
        loginResponse = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False, timeout=3)
        token = json.loads(loginResponse.text)['SessionId']
        print(token)

        # get number of data exist in Distribution table
        dlist = requests.get(settings.BASEURL+'/DistributionRules?$select=FactorCode,FactorDescription&$filter=InWhichDimension eq 2', cookies=loginResponse.cookies, verify=False)
        print(dlist.json())
        totalRow = dlist.json()
        return Response({"message":"successful","status":"200","data":totalRow['value']})
    except Exception as e:
        return Response({"message":"Error","status":"201","data":[str(e)]})


#added by millan for item create on 11-10-2022        
@api_view(['POST'])
def create(request):
    try:
        UnitPrice = request.data['UnitPrice']
        Currency = request.data['Currency']
        DiscountPercent = request.data['DiscountPercent']
        ItemCode = request.data['ItemCode']
        ItemName = request.data['ItemName']
        TaxCode = request.data['TaxCode']
        U_DIV = request.data['U_DIV']
        InStock = request.data['InStock']
        ItemsGroupCode = request.data['ItemsGroupCode']
        UomNo = request.data['UomNo']
        UQC = request.data['UQC_Code']
        
        model = Item(UnitPrice = UnitPrice, Currency = Currency, DiscountPercent = DiscountPercent, ItemCode = ItemCode, ItemName = ItemName, TaxCode = TaxCode, U_DIV = U_DIV, InStock = InStock, ItemsGroupCode_id = ItemsGroupCode, UomNo = UomNo, UQC_Code=UQC)
        
        model.save()
        
        itm_id = Item.objects.latest('id')
        ItCode = "IT"+str(format(itm_id.id, '04'))
        itm_id.ItemCode = ItCode
        itm_id.save()
        
        return Response({"message":"success","status":200,"data":[]}) 
        
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})    
    
#Item Update API created by millan on 03-November-2022
@api_view(['POST'])
def update(request):
    try:
        fetchid = request.data['id']
        model = Item.objects.get(pk = fetchid)
        model.UnitPrice = request.data['UnitPrice']
        model.Currency = request.data['Currency']
        model.DiscountPercent = request.data['DiscountPercent']
        model.ItemCode = request.data['ItemCode']
        model.ItemName = request.data['ItemName']
        model.TaxCode = request.data['TaxCode']
        model.U_DIV = request.data['U_DIV']
        model.InStock = request.data['InStock']
        model.ItemsGroupCode_id = request.data['ItemsGroupCode']
        model.UomNo = request.data['UomNo']
        model.UQC_Code = request.data['UQC_Code']
        model.save()
        
        context = {
            "UnitPrice"   : request.data['UnitPrice'],
            "Currency"    : request.data['Currency'],
            "DiscountPercent" : request.data['DiscountPercent'],
            "ItemCode"    : request.data['ItemCode'],
            "ItemName"    : request.data['ItemName'],
            "TaxCode" : request.data['TaxCode'],
            "U_DIV"   : request.data['U_DIV'],
            "InStock" : request.data['InStock'],
            "ItemsGroupCode"  : request.data['ItemsGroupCode'],
            "UomNo"   : request.data['UomNo'],
            "UQC_Code"   : request.data['UQC_Code']
        }
        
        return Response({"message":"success","status":200,"data":[context]}) 
    
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]}) 

#Item Delete API by millan on 03-November-2022
@api_view(['POST'])
def delete(request):
    fetchid= request.data['id']
    try:
        Item.objects.filter(pk=fetchid).delete()
             
        return Response({"message":"successful","status":"200","data":[]})   
    except:
        return Response({"message":"Id wrong","status":"201","data":[]})
    
    
@api_view(['POST'])
def uqc_create(request):
    serializer = UQCSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"successful","status":"200","data":[]})
    return Response({"message":"Failed","status":"201","data":[]})
    
@api_view(['POST'])
def uqc_update(request):
    uid = request.data["id"]
    uobj = Unitquantitycode.objects.filter(id=uid).first()
    if uobj:
        serializer = UQCSerializer(uobj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"successful","status":"200","data":[]})
    return Response({"message":"Failed","status":"201","data":[]})


@api_view(['GET'])
def uqc_all(request):
    data = Unitquantitycode.objects.all()
    serializer = UQCGetSerializer(data, many=True)
    return Response({"message":"successful","status":"200","data":serializer.data})   


@api_view(['POST'])
def uqc_delete(request):
    uid = request.data["id"]
    uobj = Unitquantitycode.objects.filter(id=uid).first()
    if uobj:
        uobj.delete()
        return Response({"message":"successful","status":"200","data":[]})
    return Response({"message":"Failed","status":"201","data":[]})


