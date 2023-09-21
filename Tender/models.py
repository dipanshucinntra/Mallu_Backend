from operator import mod
from statistics import mode
from django.db import models

# Create your models here.

class Tender(models.Model):
    
    # Basic Details
    SalesPersonCode = models.CharField(max_length=5, blank=True)
    
    OrganisationChain = models.CharField(max_length=200, blank=True)
    TReferenceNo = models.CharField(max_length=100, blank=True)
    TID = models.CharField(max_length=100, blank=True) #Id
    TType = models.CharField(max_length=100, blank=True) #Type
    TCategoey = models.CharField(max_length=100, blank=True, default="") #Category
    GeneralTechEveAll = models.CharField(max_length=50, blank=True, default="") # General Technical Evaluation Allowed
    PaymentMode = models.CharField(max_length=50, blank=True, default="")
    MultiCurrency = models.CharField(max_length=50, blank=True, default="")
    FormOfContact = models.CharField(max_length=50, blank=True, default="")
    NoOfCovers = models.CharField(max_length=50, blank=True, default="")
    ItemTechEveAll = models.CharField(max_length=50, blank=True, default="")
    MultiCurrencyForBoq = models.CharField(max_length=50, blank=True, default="") # Bill of quantities (BOQ)
    TwoStageBidding = models.CharField(max_length=50, blank=True, default="")


    # Tender Fee Details
    # TenderId = models.ForeignKey(Tender, on_delete=models.CASCADE)
    TenderFee = models.CharField(max_length=100, blank=True, default="")
    PayableTo = models.CharField(max_length=100, blank=True, default="")
    FeeExemptionAllow = models.CharField(max_length=50, blank=True, default="") # yes/no
    FeePayableAt = models.CharField(max_length=100, blank=True, default="")

    # Earnest money deposit (EMD)
    EMDAmount = models.CharField(max_length=100, blank= True, default="") 
    EMDFeeType = models.CharField(max_length=50, blank=True, default="") # type
    EMDPayableTo = models.CharField(max_length=50, blank=True, default="") # person or designation
    EMDPayableAt = models.CharField(max_length=50, blank=True, default="") # place
    EMDExemptionAllow = models.CharField(max_length=50, blank=True, default="") # Yes/No
    EMDPercentage = models.CharField(max_length=50, blank=True, default="")
    
    # Tender Inviting Authority
    InvitingAuthorityName = models.CharField(max_length=100, blank=True, default="")
    InvitingAuthorityAddress = models.CharField(max_length=200, blank=True, default="")

    # Tender Closed
    Status = models.CharField(max_length=50, blank=True, default="")
    Comments = models.CharField(max_length=200, blank=True, default="")

    # status key's
    TenderSubStatus = models.IntegerField( default=0 )
    TenderOpenStatus = models.IntegerField( default=0 )
    TechOpenStatus = models.IntegerField( default=0 )
    LowestOneStatus = models.IntegerField( default=0 )


    U_LEADID = models.IntegerField(default=0)
    U_LEADNM = models.CharField(max_length=150, blank=True)

    U_OPPID = models.CharField(max_length=5, blank=True)
    U_OPPRNM = models.CharField(max_length=100, blank=True)
    


# Payment Instruments
class PaymentInstrument(models.Model):
    TenderId = models.IntegerField(default=0)
    PaymentType = models.CharField(max_length=50, blank=True, default="")
    InstrumentType = models.CharField(max_length=50, blank=True, default="")

# Cover Details
class CoverDetail(models.Model):
    TenderId = models.IntegerField(default=0)
    CoverTitle = models.CharField(max_length=100, blank=True, default="")
    CoverDocType = models.CharField(max_length=100, blank=True, default="")
    CoverDesc = models.CharField(max_length=100, blank=True, default="")

# Work Item Details
class WorkOrItemDetails(models.Model):
    TenderId = models.IntegerField(default=0)
    Title = models.CharField(max_length=200, blank=True)
    Description = models.TextField(blank=True)
    PreQualficationDetails = models.CharField(max_length=200, blank=True, default="")
    Remarks = models.CharField(max_length=200, blank=True, default="")
    TenderValue = models.CharField(max_length=200, blank=True, default="")
    ProductCategory = models.CharField(max_length=200, blank=True, default="")
    ProductSubCategory = models.CharField(max_length=200, blank=True, default="")
    ContactType = models.CharField(max_length=200, blank=True, default="")
    BidValidity = models.CharField(max_length=200, blank=True, default="")
    PeriodOfWork = models.CharField(max_length=200, blank=True, default="")
    Location = models.CharField(max_length=200, blank=True, default="")
    Pincode = models.CharField(max_length=200, blank=True, default="")
    
    PreBidMeetingPlace = models.CharField(max_length=200, blank=True, default="")
    PreBidMeetingAddress = models.CharField(max_length=200, blank=True, default="")
    PreBidMeetingDate = models.CharField(max_length=200, blank=True, default="")
    BidOpeningPlace = models.CharField(max_length=200, blank=True, default="")
    NDATenderAllow = models.CharField(max_length=200, blank=True, default="") #Non-Disclosure Agreement (Yes/No)
    PreferentialBidderAllow = models.CharField(max_length=200, blank=True, default="")

# Critcal Dates
class CritcalDates(models.Model):
    TenderId = models.IntegerField(default=0)
    PublishDate = models.CharField(max_length=200, blank=True)
    BidOpeningDate = models.CharField(max_length=200, blank=True)
    SaleStartDate = models.CharField(max_length=200, blank=True, default="")
    SaleEndDate = models.CharField(max_length=200, blank=True, default="")
    ClarificationStartDate = models.CharField(max_length=200, blank=True, default="")
    ClarificationEndDate = models.CharField(max_length=200, blank=True, default="")
    BidSubStartDate = models.CharField(max_length=200, blank=True, default="")
    BidSubEndDate = models.CharField(max_length=200, blank=True, default="")

class Documents(models.Model):
    TenderId = models.IntegerField(default=0)
    Type = models.CharField(max_length=200, blank=True) # NIT or work or Product documents
    Title = models.CharField(max_length=200, blank=True)
    Description = models.CharField(max_length=200, blank=True, default="")
    File = models.CharField(max_length=200, blank=True, default="")

# currection in tender details
class CorrigendumList(models.Model):
    TenderId = models.IntegerField(default=0)
    Type = models.CharField(max_length=200, blank=True) # NIT or work or Product documents
    Title = models.CharField(max_length=200, blank=True)
    File = models.CharField(max_length=200, blank=True)

class TenderSubmission(models.Model):
    TenderId = models.IntegerField(default=0)
    FeeStatus = models.CharField(max_length=100, blank=True) # tender fee
    PaymentRegNo = models.CharField(max_length=100, blank=True)
    PaymentMode = models.CharField(max_length=100, blank=True)
    FeeAmount = models.CharField(max_length=100, blank=True)
    BankName = models.CharField(max_length=100, blank=True)
    AccountNo = models.CharField(max_length=100, blank=True)
    IFSCCode = models.CharField(max_length=100, blank=True)
    EMDFeeStatus = models.CharField(max_length=100, blank=True) # EMD fee
    EMDTerms = models.CharField(max_length=100, blank=True)
    EMDPaymentMode = models.CharField(max_length=100, blank=True)
    EMDFeeAmount = models.CharField(max_length=100, blank=True)
    EMDBankName = models.CharField(max_length=100, blank=True)
    EMDAccountNo = models.CharField(max_length=100, blank=True)
    EMDIFSCCode = models.CharField(max_length=100, blank=True)

class TenderOpening(models.Model):
    TenderId = models.IntegerField(default=0)
    CompanyName = models.CharField(max_length=200, blank=True)
    QuotedModel = models.CharField(max_length=100, blank=True)
    Part = models.CharField(max_length=100, blank=True)
    Status = models.CharField(max_length=100, blank=True)

class TechnicalOpening(models.Model):
    TenderId = models.IntegerField(default=0)
    CompanyName = models.CharField(max_length=200, blank=True)
    QuotedModel = models.CharField(max_length=100, blank=True)
    Part = models.CharField(max_length=100, blank=True)
    Status = models.CharField(max_length=100, blank=True)

class LowestOne(models.Model):
    TenderId = models.IntegerField(default=0)
    CompanyName = models.CharField(max_length=200, blank=True)
    QuotedModel = models.CharField(max_length=100, blank=True)
    # Price = models.CharField(max_length=100, blank=True)
    Price = models.IntegerField(blank=True, default=0)
    Remarks = models.CharField(max_length=100, blank=True)
    Status = models.CharField(max_length=100, blank=True)
    

# class TenderClosed(models.Model):
#     TenderId = models.IntegerField(default=0)
#     Status = models.CharField(max_length=50, blank=True, default="")
#     Comments = models.CharField(max_length=200, blank=True, default="")

class TenItem(models.Model):
	LineNum = models.IntegerField(default=0)
	TenID = models.CharField(max_length=5, blank=True)
	Quantity = models.IntegerField(default=0)
	UnitPrice = models.FloatField(default=0)
	DiscountPercent = models.FloatField(default=0)
	ItemCode = models.CharField(max_length=20, blank=True)
	ItemDescription = models.CharField(max_length=150, blank=True)
	TaxCode = models.CharField(max_length=10, blank=True)
	U_FGITEM = models.CharField(max_length=20, blank=True)
	CostingCode2 = models.CharField(max_length=20, blank=True)
	ProjectCode = models.CharField(max_length=20, blank=True)
	FreeText = models.CharField(max_length=500, blank=True)

