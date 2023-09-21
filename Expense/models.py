from django.db import models

class Expense(models.Model):
    trip_name = models.CharField(max_length=100, blank=True)
    type_of_expense = models.CharField(max_length=100, blank=True) 
    expense_from = models.CharField(max_length=100, blank=True)
    expense_to = models.CharField(max_length=100, blank=True)
    totalAmount = models.IntegerField(default=0)
    createDate = models.CharField(max_length=100, blank=True)
    createTime = models.CharField(max_length=100, blank=True)
    createdBy = models.IntegerField(default=0)
    updateDate = models.CharField(max_length=100, blank=True)
    updateTime = models.CharField(max_length=100, blank=True)
    updatedBy = models.IntegerField(default=0)
    rsm_approval = models.IntegerField(default=0)
    accountant_approval = models.IntegerField(default=0)
    rsm_status = models.CharField(max_length=200, blank=True, default="Pending")
    accountant_status = models.CharField(max_length=200, blank=True, default="Pending")

    employeeId = models.IntegerField(default=0)
    #added
    total_distance = models.IntegerField(default=0)
    DailyService_id = models.CharField(max_length=20, blank=True)    # DailyService id for attachment


class ExpenseType(models.Model):
    Name        = models.CharField(max_length=100, blank=True)
    CreatedDate = models.CharField(max_length=50, blank=True)
    CreatedTime = models.CharField(max_length=50, blank=True)


class ExpenseStatusRemarks(models.Model):
    Expense_id       = models.CharField(max_length=5, blank=True)
    SalesEmployeeCode= models.CharField(max_length=5, blank=True)
    Type             = models.CharField(max_length=200, blank=True)
    Status           = models.CharField(max_length=50, blank=True)
    Remarks          = models.CharField(max_length=255, blank=True)
    Datetime         = models.DateTimeField(auto_now_add=True)


