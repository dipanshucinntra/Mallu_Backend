from django.db import models

class ClientBankDetails(models.Model):
    clientName = models.CharField(max_length=100, blank=True)
    clientEmail = models.CharField(max_length=70, blank=True)
    clientMobile = models.CharField(max_length=20, blank=True)
    clientAddress = models.TextField(blank=True)
    clientGST = models.CharField(max_length=30, blank=True)
    bankName = models.CharField(max_length=40, blank=True)
    bankIFSC = models.CharField(max_length=40, blank=True)
    bankAccountNo = models.CharField(max_length=100, blank=True)
    AccountHolderName = models.CharField(max_length=100, blank=True)
    TermsConditions = models.TextField(blank=True)