from django.db import models  

class Project(models.Model):
    name = models.CharField(max_length=250)
    consultant_code = models.CharField(max_length=100, blank=True)
    consultant_name = models.CharField(max_length=250, blank=True)
    expected_start_date = models.CharField(max_length=50, blank=True)
    details = models.CharField(max_length=1000, blank=True)
    attach = models.CharField(max_length=250, blank=True)
    cardcode = models.CharField(max_length=100, blank=True)
    timestamp = models.CharField(max_length=50)
