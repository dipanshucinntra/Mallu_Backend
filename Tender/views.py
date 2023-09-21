import json
from multiprocessing import context
import os
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from Employee.models import Employee
from Lead.models import Lead
from Opportunity.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view    
from rest_framework import serializers

# added by abhishek
import os
from django.core.files.storage import FileSystemStorage

from Tender.serializers import *
from .models import *

# Create your views here.

@api_view(['POST'])
def create(request):
    try:  
        U_LEADID = request.data['U_LEADID']
        U_LEADNM = request.data['U_LEADNM']
        U_OPPID = request.data['U_OPPID']
        U_OPPRNM = request.data['U_OPPRNM']
        
        SalesPersonCode = request.data['SalesPersonCode']
        OrganisationChain = request.data['OrganisationChain']
        TReferenceNo = request.data['TReferenceNo']
        TID = request.data['TID']
        TType = request.data['TType']
        TCategoey = request.data['TCategoey']
        GeneralTechEveAll = request.data['GeneralTechEveAll']
        PaymentMode = request.data['PaymentMode']
        MultiCurrency = request.data['MultiCurrency']
        FormOfContact = request.data['FormOfContact']
        NoOfCovers = request.data['NoOfCovers']
        ItemTechEveAll = request.data['ItemTechEveAll']
        MultiCurrencyForBoq = request.data['MultiCurrencyForBoq']
        TwoStageBidding = request.data['TwoStageBidding']
        TenderFee = request.data['TenderFee']
        PayableTo = request.data['PayableTo']
        FeeExemptionAllow = request.data['FeeExemptionAllow']
        FeePayableAt = request.data['FeePayableAt']
        EMDAmount = request.data['EMDAmount']
        EMDFeeType = request.data['EMDFeeType']
        EMDPayableTo = request.data['EMDPayableTo']
        EMDPayableAt = request.data['EMDPayableAt']
        EMDExemptionAllow = request.data['EMDExemptionAllow']
        EMDPercentage = request.data['EMDPercentage']
        InvitingAuthorityName = request.data['InvitingAuthorityName']
        InvitingAuthorityAddress = request.data['InvitingAuthorityAddress']

        model = Tender(
            U_LEADID=U_LEADID,
            U_LEADNM=U_LEADNM,
            U_OPPID=U_OPPID,
            U_OPPRNM=U_OPPRNM,            
            SalesPersonCode = SalesPersonCode,
            OrganisationChain = OrganisationChain,
            TReferenceNo = TReferenceNo,
            TID = TID,
            TType = TType,
            TCategoey = TCategoey,
            GeneralTechEveAll = GeneralTechEveAll,
            PaymentMode = PaymentMode,
            MultiCurrency = MultiCurrency,
            FormOfContact = FormOfContact,
            NoOfCovers = NoOfCovers,
            ItemTechEveAll = ItemTechEveAll,
            MultiCurrencyForBoq = MultiCurrencyForBoq,
            TwoStageBidding = TwoStageBidding,
            TenderFee = TenderFee,
            PayableTo = PayableTo,
            FeeExemptionAllow = FeeExemptionAllow,
            FeePayableAt = FeePayableAt,
            EMDAmount = EMDAmount,
            EMDFeeType = EMDFeeType,
            EMDPayableTo = EMDPayableTo,
            EMDPayableAt = EMDPayableAt,
            EMDExemptionAllow = EMDExemptionAllow,
            EMDPercentage = EMDPercentage,
            InvitingAuthorityName = InvitingAuthorityName,
            InvitingAuthorityAddress = InvitingAuthorityAddress
        )
        model.save()

        tenderObj = Tender.objects.latest('id')
        TenderId =  tenderObj.id
        TenID =  tenderObj.id

        paymentInstrument = request.data['PaymentInstrument']
        coverDetails = request.data['CoverDetail']

        # -----------------------------------------------------------------------
        # ---------------------Payment Instrument Details------------------------
        # -----------------------------------------------------------------------
        
        paymentInstrumentID = ""
        if paymentInstrument != "":
            try:
                for payInst in paymentInstrument:
                    print(payInst)
                    PaymentType = payInst['PaymentType']
                    InstrumentType = payInst['InstrumentType']
                    PaymentInstrumentModel = PaymentInstrument(TenderId = int(TenderId), PaymentType = PaymentType, InstrumentType = InstrumentType)
                    PaymentInstrumentModel.save()

                    PaymentInstrumentObj = PaymentInstrument.objects.latest('id')
                    paymentInstrumentID =  PaymentInstrumentObj.id

            except Exception as e:
                Tender.objects.filter(pk=TenderId).delete()
                return Response({"message":"Error","status":201,"Model": "Payment Instrument" ,"data":str(e)})


        # ----------------------------------------------------------
        # ---------------------Cover Details------------------------
        # ----------------------------------------------------------
        coverDetailsID = ""
        if coverDetails != "":
            try:
                for coverDetail in coverDetails:
                    print(payInst)
                    CoverTitle = coverDetail['CoverTitle']
                    CoverDocType = coverDetail['CoverDocType']
                    CoverDesc = coverDetail['CoverDesc']
                    CoverDetailModel = CoverDetail(TenderId = int(TenderId), CoverTitle = CoverTitle, CoverDocType = CoverDocType, CoverDesc = CoverDesc)
                    CoverDetailModel.save()

                    coverObj = CoverDetail.objects.latest('id')
                    coverDetailsID =  coverObj.id
            except Exception as e:
                Tender.objects.filter(pk=TenderId).delete()
                PaymentInstrument.objects.filter(pk=paymentInstrumentID).delete()
                return Response({"message":"Error","status":201,"Model": "coverDetails" ,"data":str(e)})
        
        # ---------------------------------------------------------
        # ---------------------Work Details------------------------
        # ---------------------------------------------------------
        workOrItemDetailsID = ""
        if request.data['WorkOrItemDetails'] != "":
            try:
                # TenderId = request.data['WorkOrItemDetails']['TenderId']
                Title = request.data['WorkOrItemDetails']['Title']
                Description = request.data['WorkOrItemDetails']['Description']
                PreQualficationDetails = request.data['WorkOrItemDetails']['PreQualficationDetails']
                Remarks = request.data['WorkOrItemDetails']['Remarks']
                TenderValue = request.data['WorkOrItemDetails']['TenderValue']
                ProductCategory = request.data['WorkOrItemDetails']['ProductCategory']
                ProductSubCategory = request.data['WorkOrItemDetails']['ProductSubCategory']
                ContactType = request.data['WorkOrItemDetails']['ContactType']
                BidValidity = request.data['WorkOrItemDetails']['BidValidity']
                PeriodOfWork = request.data['WorkOrItemDetails']['PeriodOfWork']
                Location = request.data['WorkOrItemDetails']['Location']
                Pincode = request.data['WorkOrItemDetails']['Pincode']
                PreBidMeetingPlace = request.data['WorkOrItemDetails']['PreBidMeetingPlace']
                PreBidMeetingAddress = request.data['WorkOrItemDetails']['PreBidMeetingAddress']
                PreBidMeetingDate = request.data['WorkOrItemDetails']['PreBidMeetingDate']
                BidOpeningPlace = request.data['WorkOrItemDetails']['BidOpeningPlace']
                NDATenderAllow = request.data['WorkOrItemDetails']['NDATenderAllow']
                PreferentialBidderAllow = request.data['WorkOrItemDetails']['PreferentialBidderAllow']

                # Tender work/item details
                workModel = WorkOrItemDetails(
                    TenderId = int(TenderId),
                    Title = Title,
                    Description = Description,
                    PreQualficationDetails = PreQualficationDetails,
                    Remarks = Remarks,
                    TenderValue = TenderValue,
                    ProductCategory = ProductCategory,
                    ProductSubCategory = ProductSubCategory,
                    ContactType = ContactType,
                    BidValidity = BidValidity,
                    PeriodOfWork = PeriodOfWork,
                    Location = Location,
                    Pincode = Pincode,
                    PreBidMeetingPlace = PreBidMeetingPlace,
                    PreBidMeetingAddress = PreBidMeetingAddress,
                    PreBidMeetingDate = PreBidMeetingDate,
                    BidOpeningPlace = BidOpeningPlace,
                    NDATenderAllow = NDATenderAllow,
                    PreferentialBidderAllow = PreferentialBidderAllow
                )
                workModel.save()

                WorkOrItemDetailsObj = WorkOrItemDetails.objects.latest('id')
                workOrItemDetailsID =  WorkOrItemDetailsObj.id

            except Exception as e:
                Tender.objects.filter(pk=TenderId).delete()
                PaymentInstrument.objects.filter(pk=paymentInstrumentID).delete()
                CoverDetail.objects.filter(pk=coverDetailsID).delete()
                return Response({"message":"Error","status":201,"Model": "workModel" ,"data":str(e)})

        # ------------------------------------------------------------------
        # ---------------------Critcal Dates Details------------------------
        # ------------------------------------------------------------------
        critcalDatesID = 0
        if request.data['CritcalDates'] != "":
            try:
                # TenderId = request.data['TenderId']
                PublishDate = request.data['CritcalDates']['PublishDate']
                BidOpeningDate = request.data['CritcalDates']['BidOpeningDate']
                SaleStartDate = request.data['CritcalDates']['SaleStartDate']
                SaleEndDate = request.data['CritcalDates']['SaleEndDate']
                ClarificationStartDate = request.data['CritcalDates']['ClarificationStartDate']
                ClarificationEndDate = request.data['CritcalDates']['ClarificationEndDate']
                BidSubStartDate = request.data['CritcalDates']['BidSubStartDate']
                BidSubEndDate = request.data['CritcalDates']['BidSubEndDate']

                criticalDateModel = CritcalDates(
                    TenderId = int(TenderId),
                    PublishDate = PublishDate,
                    BidOpeningDate = BidOpeningDate,
                    SaleStartDate = SaleStartDate,
                    SaleEndDate = SaleEndDate,
                    ClarificationStartDate = ClarificationStartDate,
                    ClarificationEndDate = ClarificationEndDate,
                    BidSubStartDate = BidSubStartDate,
                    BidSubEndDate = BidSubEndDate
                )
                criticalDateModel.save()
                # critcalDatesObj = CritcalDates.objects.latest('id')
                # critcalDatesID =  critcalDatesObj.id
            except Exception as e:
                Tender.objects.filter(pk=TenderId).delete()
                PaymentInstrument.objects.filter(pk=paymentInstrumentID).delete()
                CoverDetail.objects.filter(pk=coverDetailsID).delete()
                WorkOrItemDetails.objects.filter(pk=workOrItemDetailsID).delete()
                return Response({"message":"Error","status":201,"Model": "criticalDateModel" ,"data":str(e)})

        if int(U_LEADID) !=0:
            leadObj = Lead.objects.get(pk=U_LEADID)
            leadObj.TDStatus=1
            leadObj.save()
        if U_OPPID !="":
            oppObj = Opportunity.objects.get(pk=U_OPPID)
            oppObj.TDStatus=1
            oppObj.save()
        
        if len(request.data['TenItem']) != 0:
            lines = request.data['TenItem']
            LineNum = 0
            for line in lines:
                try:
                    model_lines = TenItem(LineNum = LineNum, TenID = TenID, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'], U_FGITEM = line['U_FGITEM'], CostingCode2 = line['CostingCode2'], ProjectCode = line['ProjectCode'], FreeText = line['FreeText'])
                    model_lines.save()
                    LineNum=LineNum+1
                except Exception as e:
                   Tender.objects.filter(pk=TenID).delete()
                   tenItems = TenItem.objects.filter(TenID=TenID)
                   for item in tenItems:
                       item.delete()                           
                   return Response({"message":str(e),"status":201,"data":[]})
            
        return Response({"message":"Successful","status":200, "data":[{'TenderId': TenderId}]})
    except Exception as e:
        return Response({"message":"Error","status":201,"Model": "Tender Model" ,"data":str(e)})

@api_view(['POST'])
def tendersubmission(request):
    try: 
        TenderId = request.data['TenderId']

        FeeStatus = request.data['FeeStatus']
        PaymentRegNo = request.data['PaymentRegNo']
        PaymentMode = request.data['PaymentMode']
        FeeAmount = request.data['FeeAmount']
        BankName = request.data['BankName']
        AccountNo = request.data['AccountNo']
        IFSCCode = request.data['IFSCCode']
        EMDFeeStatus = request.data['EMDFeeStatus']
        EMDTerms = request.data['EMDTerms']
        EMDPaymentMode = request.data['EMDPaymentMode']
        EMDFeeAmount = request.data['EMDFeeAmount']
        EMDBankName = request.data['EMDBankName']
        EMDAccountNo = request.data['EMDAccountNo']
        EMDIFSCCode = request.data['EMDIFSCCode']

        type = ""
        if TenderSubmission.objects.filter(TenderId = TenderId).exists():
            model = TenderSubmission.objects.get(TenderId = TenderId)
            model.FeeStatus = FeeStatus
            model.PaymentRegNo = PaymentRegNo
            model.PaymentMode = PaymentMode
            model.FeeAmount = FeeAmount
            model.BankName = BankName
            model.AccountNo = AccountNo
            model.IFSCCode = IFSCCode
            model.EMDFeeStatus = EMDFeeStatus
            model.EMDTerms = EMDTerms
            model.EMDPaymentMode = EMDPaymentMode
            model.EMDFeeAmount = EMDFeeAmount
            model.EMDBankName = EMDBankName
            model.EMDAccountNo = EMDAccountNo
            model.EMDIFSCCode = EMDIFSCCode
            model.save()
            type = 'update'
        else:
            tenderSubmissionModel = TenderSubmission(
                TenderId = TenderId,
                FeeStatus = FeeStatus,
                PaymentRegNo = PaymentRegNo,
                PaymentMode = PaymentMode,
                FeeAmount = FeeAmount,
                BankName = BankName,
                AccountNo = AccountNo,
                IFSCCode = IFSCCode,
                EMDFeeStatus = EMDFeeStatus,
                EMDTerms = EMDTerms,
                EMDPaymentMode = EMDPaymentMode,
                EMDFeeAmount = EMDFeeAmount,
                EMDBankName = EMDBankName,
                EMDAccountNo = EMDAccountNo,
                EMDIFSCCode = EMDIFSCCode
            )
            tenderSubmissionModel.save()
            type = 'insert'
            # TenderSubmissionObj = TenderSubmission.objects.latest('id')
            # tenderSubmissionId =  TenderSubmissionObj.id

        return Response({"message":"Successful","status":200, "data":[{'TenderId': TenderId, 'type': type}]})
    except Exception as e:
        return Response({"message":"Error","status":201,"Model": "Tender Submission" ,"data":str(e)})

@api_view(['POST'])
def tenderopening(request):
    try:
        TenderId = request.data['TenderId']
        CompanyName = request.data['CompanyName']
        QuotedModel = request.data['QuotedModel']
        Part = request.data['Part']
        Status = request.data['Status']

        # Tender opening
        tenderOpeningModel = TenderOpening(TenderId = TenderId, CompanyName = CompanyName, QuotedModel = QuotedModel, Part = Part, Status = Status)
        tenderOpeningModel.save()
        tenderOpeningObj = TenderOpening.objects.latest('id')

        # Technical opening
        technicalOpeningModel = TechnicalOpening(TenderId = TenderId, CompanyName = CompanyName, QuotedModel = QuotedModel, Part = Part, Status = Status)
        technicalOpeningModel.save()
        technicalOpeningObj = TechnicalOpening.objects.latest('id')

        context = {
            'TenderId': TenderId, 
            'TenderOpeningId': tenderOpeningObj.id, 
            'TechnicalOpeningId': technicalOpeningObj.id
        }

        return Response({"message":"Successful","status":200, "data":[context]})
    except Exception as e:
        return Response({"message":"Error","status":201,"Model": "Technical Opening" ,"data":str(e)})

@api_view(['POST'])
def technicalopening(request):
    try:
        TenderId = request.data['TenderId']
        CompanyName = request.data['CompanyName']
        QuotedModel = request.data['QuotedModel']
        Remarks = request.data['Remarks']
        Status = request.data['Status']

        technicalOpeningModel = TechnicalOpening(
            TenderId = TenderId,
            CompanyName = CompanyName,
            QuotedModel = QuotedModel,
            Remarks = Remarks,
            Status = Status
        )
        technicalOpeningModel.save()

        technicalOpeningObj = TechnicalOpening.objects.latest('id')
        technicalOpeningId =  technicalOpeningObj.id

        return Response({"message":"Successful","status":200, "data":[{'TenderId': TenderId, 'TechnicalOpeningId': technicalOpeningId}]})
    except Exception as e:
        return Response({"message":"Error","status":201,"Model": "Technical Opening" ,"data":str(e)})


@api_view(['POST'])
def lowestone(request):
    try:
        TenderId = request.data['TenderId']
        CompanyName = request.data['CompanyName']
        QuotedModel = request.data['QuotedModel']
        Price = request.data['Price']
        Remarks = request.data['Remarks']
        Status = request.data['Status']

        technicalOpeningModel = LowestOne(
            TenderId = TenderId,
            CompanyName = CompanyName,
            QuotedModel = QuotedModel,
            Price = Price,
            Remarks = Remarks,
            Status = Status,
        )
        technicalOpeningModel.save()

        lowestOneObj = LowestOne.objects.latest('id')
        lowestOneId =  lowestOneObj.id

        return Response({"message":"Successful","status":200, "data":[{'TenderId': TenderId, 'LowestOneId': lowestOneId}]})
    except Exception as e:
        return Response({"message":"Error","status":201,"Model": "Lowest One" ,"data":str(e)})


@api_view(['POST'])
def tenderclosed(request):
    try:
        TenderId = request.data['TenderId']
        Status = request.data['Status']
        Comments = request.data['Comments']

        model = Tender.objects.get(pk = TenderId)
        model.Status = Status
        model.Comments = Comments
        model.save()
   
        context = {
            "TenderId" :TenderId,
            "Status" :Status,
            "Comments" :Comments
        }

        return Response({"message":"Successful","status":200, "data":[{'TenderId': TenderId, 'context': context}]})
    except Exception as e:
        return Response({"message":"Error","status":201,"Model": "Tender Closed" ,"data":str(e)})


@api_view(['POST'])
def addtenderdocuments(request):
    try:
        docs = request.data
        print(docs)
        # for doc in docs:
        TenderId = docs['TenderId']
        Type = docs['Type']
        Title = docs['Title']
        Description = docs['Description']
        File = docs['File']

        # upload file
        target = 'bridge/static/tender-files/'
        os.makedirs(target, exist_ok=True)
        fss = FileSystemStorage()
        file = fss.save(target+"/"+File.name, File)

        file_url = fss.url(file)
        Item_image_name = file_url[file_url.rfind('/')+1 : len(file_url)]
        print(Item_image_name)

        documentModel = Documents(
            TenderId = TenderId,
            Type = Type,
            Title = Title,
            Description = Description,
            File = Item_image_name
        )
        documentModel.save()
        documentsObj = Documents.objects.latest('id')
        documentId =  documentsObj.id
    
        return Response({"message":"Successful","status":200, "data":[{'documentId': documentId}]})
    except Exception as e:
        return Response({"message":"Error","status":201,"data":[{str(e)}]})


@api_view(['POST'])
def one(request):
    try:
        id = request.data['id']
        tenderObj = Tender.objects.filter(pk=id)
        # tender_json = TenderSerializer(tenderObj)
        finalData = showtender(tenderObj)
        return Response({"message":"Successful","status":200, "data":finalData})
    except Exception as e:
        return Response({"message":"Error","status":201,"data":[{str(e)}]})


@api_view(['GET'])
def all(request):
    try:
        tenderObj = Tender.objects.all().order_by("-id")
        # tender_json = TenderSerializer(tenderObj, many=True)
        # finalTender = json.loads(json.dumps(tender_json.data))
        finalData = showtender(tenderObj)
        return Response({"message":"Successful","status":200, "data":finalData})
    except Exception as e:
        return Response({"message":"Error","status":201,"data":[{str(e)}]})

@api_view(['POST'])
def all_filter(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']
        if Employee.objects.filter(SalesEmployeeCode = SalesPersonCode, role = "admin").exists():
            tenderObj = Tender.objects.all().order_by("-id")
            finalData = showtender(tenderObj)
            return Response({"message":"Successful","status":200, "data":finalData})
        else:
            tenderObj = Tender.objects.filter(SalesPersonCode = SalesPersonCode).order_by("-id")
            finalData = showtender(tenderObj)
            return Response({"message":"Successful","status":200, "data":finalData})
    except Exception as e:
        return Response({"message":"Error","status":201,"data":[{str(e)}]})

@api_view(['POST'])
def update(request):
    try:
        TenderId = request.data['id']

        # tender model object
        model = Tender.objects.get(pk = TenderId)

        # keys
        model.OrganisationChain = request.data['OrganisationChain']
        model.TReferenceNo = request.data['TReferenceNo']
        model.TID = request.data['TID']
        model.TType = request.data['TType']
        model.TCategoey = request.data['TCategoey']
        model.GeneralTechEveAll = request.data['GeneralTechEveAll']
        model.PaymentMode = request.data['PaymentMode']
        model.MultiCurrency = request.data['MultiCurrency']
        model.FormOfContact = request.data['FormOfContact']
        model.NoOfCovers = request.data['NoOfCovers']
        model.ItemTechEveAll = request.data['ItemTechEveAll']
        model.MultiCurrencyForBoq = request.data['MultiCurrencyForBoq']
        model.TwoStageBidding = request.data['TwoStageBidding']
        model.TenderFee = request.data['TenderFee']
        model.PayableTo = request.data['PayableTo']
        model.FeeExemptionAllow = request.data['FeeExemptionAllow']
        model.FeePayableAt = request.data['FeePayableAt']
        model.EMDAmount = request.data['EMDAmount']
        model.EMDFeeType = request.data['EMDFeeType']
        model.EMDPayableTo = request.data['EMDPayableTo']
        model.EMDPayableAt = request.data['EMDPayableAt']
        model.EMDExemptionAllow = request.data['EMDExemptionAllow']
        model.EMDPercentage = request.data['EMDPercentage']
        model.InvitingAuthorityName = request.data['InvitingAuthorityName']
        model.InvitingAuthorityAddress = request.data['InvitingAuthorityAddress']
        model.save()

        # paymentInstrument = request.data['PaymentInstrument']
        # coverDetails = request.data['CoverDetail']
        # # -----------------------------------------------------------------------
        # # ---------------------Payment Instrument Details------------------------
        # # -----------------------------------------------------------------------
        # if paymentInstrument != "":
        #     try:
        #         for payInst in paymentInstrument:

        #             if PaymentInstrument.objects.filter(TenderId = tender.id).exists():
        #                 paymentInstModel = PaymentInstrument.objects.get(TenderId = TenderId)
        #                 paymentInstModel.PaymentType = payInst['PaymentType']
        #                 paymentInstModel.InstrumentType = payInst['InstrumentType']
        #                 paymentInstModel.save()
        #     except Exception as e:
        #         return Response({"message":"Error","status":201,"Model": "PaymentInstrument" ,"data":str(e)})

        # # ----------------------------------------------------------
        # # ---------------------Cover Details------------------------
        # # ----------------------------------------------------------
        # if coverDetails != "":
        #     try:
        #         for coverDetail in coverDetails:
        #             coverDetailModel = CoverDetail.objects.get(TenderId = TenderId)
        #             coverDetailModel.CoverTitle = coverDetail['CoverTitle']
        #             coverDetailModel.CoverDocType = coverDetail['CoverDocType']
        #             coverDetailModel.CoverDesc = coverDetail['CoverDesc']
        #             coverDetailModel.save()
        #     except Exception as e:
        #         return Response({"message":"Error","status":201,"Model": "CoverDetails" ,"data":str(e)})

        # ---------------------------------------------------------
        # ---------------------Work Details------------------------
        # ---------------------------------------------------------
        if request.data['WorkOrItemDetails'] != "":
            try:
                workModel = WorkOrItemDetails.objects.get(TenderId = TenderId)

                workModel.Title = request.data['WorkOrItemDetails']['Title']
                workModel.Description = request.data['WorkOrItemDetails']['Description']
                workModel.PreQualficationDetails = request.data['WorkOrItemDetails']['PreQualficationDetails']
                workModel.Remarks = request.data['WorkOrItemDetails']['Remarks']
                workModel.TenderValue = request.data['WorkOrItemDetails']['TenderValue']
                workModel.ProductCategory = request.data['WorkOrItemDetails']['ProductCategory']
                workModel.ProductSubCategory = request.data['WorkOrItemDetails']['ProductSubCategory']
                workModel.ContactType = request.data['WorkOrItemDetails']['ContactType']
                workModel.BidValidity = request.data['WorkOrItemDetails']['BidValidity']
                workModel.PeriodOfWork = request.data['WorkOrItemDetails']['PeriodOfWork']
                workModel.Location = request.data['WorkOrItemDetails']['Location']
                workModel.Pincode = request.data['WorkOrItemDetails']['Pincode']
                workModel.PreBidMeetingPlace = request.data['WorkOrItemDetails']['PreBidMeetingPlace']
                workModel.PreBidMeetingAddress = request.data['WorkOrItemDetails']['PreBidMeetingAddress']
                workModel.PreBidMeetingDate = request.data['WorkOrItemDetails']['PreBidMeetingDate']
                workModel.BidOpeningPlace = request.data['WorkOrItemDetails']['BidOpeningPlace']
                workModel.NDATenderAllow = request.data['WorkOrItemDetails']['NDATenderAllow']
                workModel.PreferentialBidderAllow = request.data['WorkOrItemDetails']['PreferentialBidderAllow']

                workModel.save()

            except Exception as e:
                return Response({"message":"Error","status":201,"Model": "WorkModel" ,"data":str(e)})

        
        # ------------------------------------------------------------------
        # ---------------------Critcal Dates Details------------------------
        # ------------------------------------------------------------------
        critcalDatesID = 0
        if request.data['CritcalDates'] != "":
            try:
                criticalDateModel = CritcalDates.objects.get(TenderId = TenderId)

                criticalDateModel.PublishDate = request.data['CritcalDates']['PublishDate']
                criticalDateModel.BidOpeningDate = request.data['CritcalDates']['BidOpeningDate']
                criticalDateModel.SaleStartDate = request.data['CritcalDates']['SaleStartDate']
                criticalDateModel.SaleEndDate = request.data['CritcalDates']['SaleEndDate']
                criticalDateModel.ClarificationStartDate = request.data['CritcalDates']['ClarificationStartDate']
                criticalDateModel.ClarificationEndDate = request.data['CritcalDates']['ClarificationEndDate']
                criticalDateModel.BidSubStartDate = request.data['CritcalDates']['BidSubStartDate']
                criticalDateModel.BidSubEndDate = request.data['CritcalDates']['BidSubEndDate']

                criticalDateModel.save()
            except Exception as e:
                return Response({"message":"Error","status":201,"Model": "CriticalDateModel" ,"data":str(e)})

        return Response({"message":"Successful","status":200, "data": [request.data]})
    except Exception as e:
        return Response({"message":"Error","status":201,"data":[{str(e)}]})



@api_view(['POST'])
def updatetenderopening(request):
    try:
        id = request.data['id']
        model = TenderOpening.objects.get(pk = id)
        
        model.TenderId = request.data['TenderId']
        model.CompanyName = request.data['CompanyName']
        model.QuotedModel = request.data['QuotedModel']
        model.Part = request.data['Part']
        model.Status = request.data['Status']
        model.save()

        return Response({"message":"Successful","status":200, "data": [request.data]})
    except Exception as e:
        return Response({"message":"Error","status":201,"data":[{str(e)}]})

@api_view(['POST'])
def updatetechnicalopening(request):
    try:
        id = request.data['id']
        model = TechnicalOpening.objects.get(pk = id)
        
        model.TenderId = request.data['TenderId']
        model.CompanyName = request.data['CompanyName']
        model.QuotedModel = request.data['QuotedModel']
        model.Part = request.data['Part']
        model.Status = request.data['Status']
        model.save()

        return Response({"message":"Successful","status":200, "data": [request.data]})
    except Exception as e:
        return Response({"message":"Error","status":201,"data":[{str(e)}]})

@api_view(['POST'])
def updatelowestone(request):
    try:
        id = request.data['id']
        model = LowestOne.objects.get(pk = id)

        model.TenderId = request.data['TenderId']
        model.CompanyName = request.data['CompanyName']
        model.QuotedModel = request.data['QuotedModel']
        model.Price = request.data['Price']
        model.Remarks = request.data['Remarks']
        model.Status = request.data['Status']
        model.save()

        return Response({"message":"Successful","status":200, "data": [request.data]})
    except Exception as e:
        return Response({"message":"Error","status":201,"data":[{str(e)}]})

@api_view(['POST'])
def updatestagestatus(request):
    try:
        TenderId = request.data['TenderId']
        StatusType = request.data['StatusType']
        StageStatus = request.data['StageStatus']

        model = Tender.objects.get(pk = TenderId)

        if StatusType == "TenderSubStatus":
            print("TenderSubStatus update")
            model.TenderSubStatus = StageStatus
            model.save()

        elif StatusType == "TenderOpenStatus":
            print("TenderOpenStatus update")
            model.TenderOpenStatus = StageStatus
            model.save()
        
        elif StatusType == "TechOpenStatus":
            print("TenderSubStatus update")
            model.TechOpenStatus = StageStatus
            model.save()
            
        elif StatusType == "LowestOneStatus":
            print("TenderSubStatus update")
            model.LowestOneStatus = StageStatus
            model.save()
        else:
            return Response({"message":"Error","status":201,"data": f"StatusType {StatusType} not exist"})

        return Response({"message":"Successful","status":200, "data": [request.data]})
    except Exception as e:
        return Response({"message":"Error","status":201,"data":[{str(e)}]})

def showtender(obj):
    allTender = []
    for tender in obj:
        try:
            TenderJson = TenderSerializer(tender, many=False)
            finalTender = json.loads(json.dumps(TenderJson.data))
            
            if PaymentInstrument.objects.filter(TenderId = tender.id).exists():
                payInstObj= PaymentInstrument.objects.filter(TenderId = tender.id)
                payInstJson = PaymentInstrumentSerializer(payInstObj, many=True)
                finalTender['PaymentInstrument'] = payInstJson.data
            else:
                finalTender['PaymentInstrument'] = []

            if CoverDetail.objects.filter(TenderId = tender.id).exists():
                coverObj = CoverDetail.objects.filter(TenderId = tender.id)
                coverJson = CoverDetailSerializer(coverObj, many=True)
                finalTender['CoverDetail'] = coverJson.data
            else:
                finalTender['CoverDetail'] = []
                    
            
            if WorkOrItemDetails.objects.filter(TenderId = tender.id).exists():
                WorkOrItemObj = WorkOrItemDetails.objects.get(TenderId = tender.id)
                WorkOrItemJson = WorkOrItemDetailSerializer(WorkOrItemObj)
                finalTender['WorkOrItemDetails'] = WorkOrItemJson.data
            else:
                finalTender['WorkOrItemDetails'] = {
                    "id": 0,
                    "TenderId":0,
                    "Title": "",
                    "Description": "",
                    "PreQualficationDetails": "",
                    "Remarks": "",
                    "TenderValue": "",
                    "ProductCategory": "",
                    "ProductSubCategory": "",
                    "ContactType": "",
                    "BidValidity": "",
                    "PeriodOfWork": "",
                    "Location": "",
                    "Pincode": "",
                    "PreBidMeetingPlace": "",
                    "PreBidMeetingAddress": "",
                    "PreBidMeetingDate": "",
                    "BidOpeningPlace": "",
                    "NDATenderAllow": "",
                    "PreferentialBidderAllow": ""
                }
            
            if CritcalDates.objects.filter(TenderId = tender.id).exists():
                CritcalDateObj = CritcalDates.objects.get(TenderId = tender.id)
                CritcalDatejson = CritcalDateSerializer(CritcalDateObj)
                finalTender['CritcalDates'] = CritcalDatejson.data
            else:
                finalTender['CritcalDates'] = {
                    "id": 0,
                    "TenderId":0,
                    "PublishDate": "",
                    "BidOpeningDate": "",
                    "SaleStartDate": "",
                    "SaleEndDate": "",
                    "ClarificationStartDate": "",
                    "ClarificationEndDate": "",
                    "BidSubStartDate": "",
                    "BidSubEndDate": ""
                }
            
            if Documents.objects.filter(TenderId = tender.id).exists():
                DocumentsObj = Documents.objects.filter(TenderId = tender.id)
                DocumentsJson = DocumentSerializer(DocumentsObj, many=True)
                finalTender['Documents'] = DocumentsJson.data
            else:
                finalTender['Documents'] = []
            
            if TenderSubmission.objects.filter(TenderId = tender.id).exists():
                tenderSubmissionObj = TenderSubmission.objects.get(TenderId = tender.id)
                tenderSubmissionJson = TenderSubmissionSerializer(tenderSubmissionObj)
                finalTender['TenderSubmission'] = tenderSubmissionJson.data
            else:
                finalTender['TenderSubmission'] = {
                    "id": 0,
                    "TenderId":0,
                    "FeeStatus":"",
                    "PaymentRegNo":"",
                    "PaymentMode":"",
                    "EMDFeeStatus":"",
                    "EMDTerms":"",
                    "EMDPaymentMode":""
                }

            if TenderOpening.objects.filter(TenderId = tender.id).exists():
                tenderOpeningObj = TenderOpening.objects.filter(TenderId = tender.id)
                tenderOpeningJson = TenderOpeningSerializer(tenderOpeningObj, many=True)
                finalTender['TenderOpening'] = tenderOpeningJson.data
            else:
                finalTender['TenderOpening'] = []
            
            if TechnicalOpening.objects.filter(TenderId = tender.id).exists():
                technicalOpeningObj = TechnicalOpening.objects.filter(TenderId = tender.id)
                technicalOpeningJson = TechnicalOpeningSerializer(technicalOpeningObj, many=True)
                finalTender['TechnicalOpening'] = technicalOpeningJson.data
            else:
                finalTender['TechnicalOpening'] = []

            if LowestOne.objects.filter(TenderId = tender.id).exists():
                lowestOneObj = LowestOne.objects.filter(TenderId = tender.id).order_by("Price")
                lowestOneJson = LowestOneSerializer(lowestOneObj, many=True)
                finalTender['LowestOne'] = lowestOneJson.data
            else:
                finalTender['LowestOne'] = []
            
            if TenItem.objects.filter(TenID = tender.id).exists():
                tenItemObj = TenItem.objects.filter(TenID = tender.id)
                tenItemJson = TenItemSerializer(tenItemObj, many=True)
                finalTender['TenItem'] = tenItemJson.data
            else:
                finalTender['TenItem'] = []
            
            
            allTender.append(finalTender)
        except Exception as e:
            print(str(e))
    return allTender



@api_view(['POST'])
def deletedoc(request):
    try:
        # tenderId=request.data['TenderId']
        docId=request.data['id']
        if docId != 0:
            if Documents.objects.filter(pk = docId).exists():
                docObj = Documents.objects.get(pk = docId)
                docName = docObj.File

                # File location 
                location = "./bridge/static/tender-files/"
                
                if os.path.exists(f"{location}/{docName}"):
                    path = os.path.join(location, docName)
                    os.remove(path)
                
                docObj.delete()
        return Response({"message":"Successful","status":"200","data":[request.data]})
    except Exception as e:
         return Response({"message":"Error","status":"201","data":[str(e)]})


@api_view(['POST'])
def deletetechopening(request):
    try:
        # tenderId=request.data['TenderId']
        techOpId=request.data['id']
        if TechnicalOpening.objects.filter(pk = techOpId).exists():
            TechnicalOpening.objects.filter(pk = techOpId).delete()
            return Response({"message":"Successful","status":"200","data":[request.data]})
        else:
            return Response({"message":"Warning","status":"201","data":"Technical Opeining id does not exist in db"})
    except Exception as e:
        return Response({"message":"Error","status":"201","data":[str(e)]})

@api_view(['POST'])
def deletetenderopening(request):
    try:
        # tenderId=request.data['TenderId']
        tenderOpId=request.data['id']
        if TenderOpening.objects.filter(pk = tenderOpId).exists():
            TenderOpening.objects.filter(pk = tenderOpId).delete()
            return Response({"message":"Successful","status":"200","data":[request.data]})
        else:
            return Response({"message":"Warning","status":"201","data":"Technical Opeining id does not exist in db"})
    except Exception as e:
        return Response({"message":"Error","status":"201","data":[str(e)]})

@api_view(['POST'])
def deletelowestone(request):
    try:
        # tenderId=request.data['TenderId']
        lowestOneId=request.data['id']
        if LowestOne.objects.filter(pk = lowestOneId).exists():
            LowestOne.objects.filter(pk = lowestOneId).delete()
            return Response({"message":"Successful","status":"200","data":[request.data]})
        else:
            return Response({"message":"Warning","status":"201","data":"Lowest One id does not exist in db"})
    except Exception as e:
        return Response({"message":"Error","status":"201","data":[str(e)]})


@api_view(['POST'])
def delete(request):
    try:
        tenderId = request.data['id']
        if Tender.objects.filter(pk=tenderId).exists():
            
            if PaymentInstrument.objects.filter(TenderId=tenderId).exists():
                PaymentInstrument.objects.filter(TenderId=tenderId).delete()
                print("PaymentInstrument delete")

            if CoverDetail.objects.filter(TenderId=tenderId).exists():
                CoverDetail.objects.filter(TenderId=tenderId).delete()
                print("CoverDetail delete")

            if WorkOrItemDetails.objects.filter(TenderId=tenderId).exists():
                WorkOrItemDetails.objects.filter(TenderId=tenderId).delete()
                print("WorkOrItemDetails delete")

            if CritcalDates.objects.filter(TenderId=tenderId).exists():
                CritcalDates.objects.filter(TenderId=tenderId).delete()
                print("CritcalDates delete")

            if TenderSubmission.objects.filter(TenderId=tenderId).exists():
                TenderSubmission.objects.filter(TenderId=tenderId).delete()
                print("TenderSubmission delete")

            if TenderOpening.objects.filter(TenderId=tenderId).exists():
                TenderOpening.objects.filter(TenderId=tenderId).delete()
                print("TenderOpening delete")
            
            if TechnicalOpening.objects.filter(TenderId=tenderId).exists():
                TechnicalOpening.objects.filter(TenderId=tenderId).delete()
                print("TechnicalOpening delete")

            if LowestOne.objects.filter(TenderId=tenderId).exists():
                LowestOne.objects.filter(TenderId=tenderId).delete()
                print("LowestOne delete")

            if Documents.objects.filter(TenderId=tenderId).exists():
                docObj = Documents.objects.filter(TenderId=tenderId)
                for obj in docObj:
                    docName = obj.File
                    # File location 
                    location = "./bridge/static/tender-files/"
                    if os.path.exists(f"{location}/{docName}"):
                        path = os.path.join(location, docName)
                        os.remove(path)

                    docObj.delete()

                Documents.objects.filter(TenderId=tenderId).delete()
                print("Documents delete")
            Tender.objects.filter(pk=tenderId).delete()
            print("Tender delete")
            return Response({"message":"Successful","status":"200","data":[request.data]})
        else:
            return Response({"message":"Warning","status":"201","data":"TenderId does not exist"})
    except Exception as e:
        return Response({"message":"Error","status":"201","data":[str(e)]})

