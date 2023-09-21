
import json
from .models import DropDown
from rest_framework.decorators import api_view    
from rest_framework.response import Response
from .serializers import DropDownSerializer 
from django.conf import settings
# Create your views here. 

#DropDown Create API
@api_view(['POST'])
def create(request):
    try:
        request.data['Data'] = json.dumps(request.data['Data'])        
        DropDownName= request.data['DropDownName']
        Data= request.data['Data']
        DropDownValue= request.data['DropDownValue']
        DropDownDescription= request.data['DropDownDescription']
        Parent= request.data['Parent']
        Field1= request.data['Field1']
        Field2= request.data['Field2']
        Field3= request.data['Field3']
        Field4= request.data['Field4']
        Field5= request.data['Field5']
        CreatedBy= request.data['CreatedBy']
        CreateDate= request.data['CreateDate']
        CreateTime= request.data['CreateTime']
        UpdateDate= request.data['UpdateDate']
        UpdateTime= request.data['UpdateTime']
        UpdatedBy= request.data['UpdatedBy']
        try:
            model = DropDown(DropDownName=DropDownName, Data=Data, DropDownValue=DropDownValue, DropDownDescription=DropDownDescription, Parent=Parent, Field1=Field1, Field2=Field2, Field3=Field3, Field4=Field4, Field5=Field5, CreatedBy_id=CreatedBy, CreateDate=CreateDate, CreateTime=CreateTime, UpdateDate=UpdateDate, UpdateTime=UpdateTime, UpdatedBy_id=UpdatedBy)
            model.save()        
            return Response({"message":"successful", "status":200,"data":[]})
        except Exception as e:
            print(str(e))
            return Response({"message":"Not valid", "status":201,"data":[]})            
    except Exception as e:
        return Response({"message":str(e), "status":201, "data":[]})

@api_view(["GET"])
def all(request):
    try:
        if request.query_params:
            dds = DropDown.objects.filter(**request.query_params.dict()).order_by('id')
        else:
            dds = DropDown.objects.all().order_by('id')
        
        if dds:
            serializer = DropDownSerializer(dds, many=True)
            return Response({"message": "Success","status": 200,"data":serializer.data})
        else:
            return Response({"message": "Success","status": "200","data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": "201","data":[]})

#DropDown Update API
@api_view(['POST'])
def update(request):
    try:
        fetchid = request.data['id']
        dd = DropDown.objects.get(pk=fetchid)
        data = DropDownSerializer(instance=dd, data=request.data)     
        if data.is_valid():
            data.save()
            return Response({"message":"successful","status":"200","data":[]})
        else:
            return Response({"message":"ID Wrong","status":"201","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

#DropDown delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        DropDown.objects.filter(pk=fetchid).delete()        
        return Response({"message":"successful","status":"200","data":[]})        
    except Exception as e:
         return Response({"message":str(e),"status":"201","data":[]})


# #Static DropDown All API
# @api_view(["GET"])
# def static_all(request):
#     try:
#         if request.query_params:
#             dds = StaticDropDown.objects.filter(**request.query_params.dict()).order_by('id')
#         else:
#             dds = StaticDropDown.objects.all().order_by('-id')
        
#         if dds:
#             serializer = StaticDropDownSerializer(dds, many=True)
#             return Response({"message": "Success","status": 200,"data":serializer.data})
#         else:
#             return Response({"message": "Success","status": "200","data":[]})
#     except Exception as e:
#         return Response({"message": str(e),"status": "201","data":[]})