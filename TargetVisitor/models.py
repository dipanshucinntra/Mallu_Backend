from django.db import models

# Create your models here.

class TargetVisitor(models.Model):
    monthly_target = models.IntegerField(default=0, blank=True)
    daily_visit = models.IntegerField(default=0, blank=True)
    visited = models.IntegerField(default=0, blank=True)
    assigned_to = models.IntegerField(default=0, blank=True)
    created_by = models.IntegerField(default=0, blank=True)
    zone = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)












