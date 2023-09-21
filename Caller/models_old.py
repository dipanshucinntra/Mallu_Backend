from django.db import models

# Create your models here.


class Caller(models.Model):
    LeadId = models.IntegerField(default=0)
    MobileNumber = models.CharField(max_length=200, blank=True)
    CallDuration = models.CharField(max_length=200, blank=True)
    Remarks = models.TextField(max_length=200, blank=True)
    EmployeeId = models.IntegerField(default=0)
    EmployeeName = models.CharField(max_length=200, blank=True)
    CreateTime = models.CharField(max_length=200, blank=True)
    CreateDate = models.CharField(max_length=200, blank=True)



