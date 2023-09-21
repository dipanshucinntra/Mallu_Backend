from django.db import models  
from Employee.models import *

class DropDown(models.Model):
    DropDownName = models.CharField(max_length=250, blank=True)
    DropDownValue = models.CharField(max_length=250, blank=True)
    DropDownDescription = models.TextField(blank=True)
    CreatedBy = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='CreatedBy', to_field="SalesEmployeeCode")
    UpdatedBy = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='UpdatedBy', to_field="SalesEmployeeCode")
    CreateDate = models.CharField(max_length=100, blank=True)
    CreateTime = models.CharField(max_length=100, blank=True)
    UpdateDate = models.CharField(max_length=100, blank=True)
    UpdateTime = models.CharField(max_length=100, blank=True)	
    Data = models.TextField(blank=True)	
    Parent = models.CharField(max_length=100, blank=True)
    Field1 = models.CharField(max_length=100, blank=True)
    Field2 = models.CharField(max_length=100, blank=True)
    Field3 = models.CharField(max_length=100, blank=True)
    Field4 = models.CharField(max_length=100, blank=True)
    Field5 = models.CharField(max_length=100, blank=True)
    


# class StaticDropDown(models.Model):
#     DropDownName = models.CharField(max_length=250, blank=True)
#     DropDownValue = models.CharField(max_length=250, blank=True)
#     DropDownDescription = models.TextField(blank=True)	
#     Parent = models.CharField(max_length=250, blank=True)
