from django.db import models

# Create your models here.


class DailyService(models.Model):
    asp_id = models.CharField(max_length=200, blank=True)
    asp_name = models.CharField(max_length=200, blank=True)
    asp_code = models.CharField(max_length=200, blank=True)
    transport_mode = models.CharField(max_length=200, blank=True)
    punchin_remark = models.CharField(max_length=200, blank=True)
    punchout_remark = models.CharField(max_length=200, blank=True)
    punchin_latitude = models.CharField(max_length=200, blank=True)
    punchin_longitude = models.CharField(max_length=200, blank=True)
    punchout_latitude = models.CharField(max_length=200, blank=True)
    punchout_longitude = models.CharField(max_length=200, blank=True)
    total_distance = models.CharField(max_length=200, blank=True, default="0")
    created_by = models.CharField(max_length=200, blank=True)
    create_date = models.CharField(max_length=200, blank=True)
    create_time = models.CharField(max_length=200, blank=True)
    update_date = models.CharField(max_length=200, blank=True)
    update_time = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    


class DailyCustomerService(models.Model):
    DailyService_id = models.CharField(max_length=200, blank=True)
    ase_id = models.CharField(max_length=200, blank=True)
    latitude = models.CharField(max_length=200, blank=True)
    longitude = models.CharField(max_length=200, blank=True)
    distance = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=500, blank=True)
    created_by = models.CharField(max_length=200, blank=True)
    type = models.CharField(max_length=200, blank=True)
    source_name = models.CharField(max_length=200, blank=True)
    source_id = models.CharField(max_length=200, blank=True)
    source_type = models.CharField(max_length=200, blank=True)
    remark = models.CharField(max_length=200, blank=True)
    contact_person = models.CharField(max_length=200, blank=True)
    lunch_status = models.CharField(max_length=200, blank=True)
    create_date = models.CharField(max_length=200, blank=True)
    create_time = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    
    