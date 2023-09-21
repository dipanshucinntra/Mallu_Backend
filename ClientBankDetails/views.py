from django.shortcuts import render
from rest_framework.decorators import api_view

from ClientBankDetails.serializers import ClientBankDetailsSerializer

from .models import ClientBankDetails    

from rest_framework.response import Response
# Create your views here.

#Client Bank Details Create API
@api_view(['POST'])
def create(request):
    try:
        clientName = request.data['clientName']
        clientEmail = request.data['clientEmail']
        clientMobile = request.data['clientMobile']
        clientAddress = request.data['clientAddress']
        clientGST = request.data['clientGST']
        bankName = request.data['bankName']
        bankIFSC = request.data['bankIFSC']
        bankAccountNo = request.data['bankAccountNo']
        AccountHolderName = request.data['AccountHolderName']
        TermsConditions = request.data['TermsConditions']
        
        model=ClientBankDetails(clientName = clientName, clientEmail = clientEmail, clientMobile = clientMobile, clientAddress = clientAddress, clientGST = clientGST, bankName = bankName, bankIFSC = bankIFSC, bankAccountNo = bankAccountNo, AccountHolderName = AccountHolderName, TermsConditions = TermsConditions)
        
        model.save()
        return Response({"message":"successful","status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

#Client Bank Details Fetch API
@api_view(['GET'])
def all(request):
    cbd_obj = ClientBankDetails.objects.all().order_by("-id")
    cbd_json = ClientBankDetailsSerializer(cbd_obj, many=True)
    return Response({"message": "Success","status": 200,"data":cbd_json.data})

#Client Bank Details Update API
@api_view(['POST'])
def update(request):
    try:
        fetchid = request.data['id']
        model = ClientBankDetails.objects.get(pk = fetchid)
        model.clientName = request.data['clientName']
        model.clientEmail = request.data['clientEmail']
        model.clientMobile = request.data['clientMobile']
        model.clientAddress = request.data['clientAddress']
        model.clientGST = request.data['clientGST']
        model.bankName = request.data['bankName']
        model.bankIFSC = request.data['bankIFSC']
        model.bankAccountNo = request.data['bankAccountNo']
        model.AccountHolderName = request.data['AccountHolderName']
        model.TermsConditions = request.data['TermsConditions']
        
        model.save()
        return Response({"message":"successful","status":"200","data":[]})
        
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})