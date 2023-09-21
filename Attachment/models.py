from django.db import models  
class Attachment(models.Model):
	File = models.CharField(max_length=150, blank=True)
	LinkType = models.CharField(max_length=100, blank=True)
	Caption = models.CharField(max_length=500, blank=True)
	LinkID = models.IntegerField(default=0)
	CreateDate = models.CharField(max_length=100, blank=True)
	CreateTime = models.CharField(max_length=100, blank=True)
	UpdateDate = models.CharField(max_length=100, blank=True)
	UpdateTime = models.CharField(max_length=100, blank=True)
	FileName = models.CharField(max_length=255, blank=True)		#added by millan on 17-10-2022 for storing name of file and displaying it
