from email.headerregistry import Group
from django.db import models  

class Category(models.Model):
	Number = models.IntegerField(default=0, unique=True)
	GroupName = models.CharField(max_length=100)
	def __str__ (self):
		return self.GroupName
		