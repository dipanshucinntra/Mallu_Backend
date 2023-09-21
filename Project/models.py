from django.db import models  

class Project(models.Model):
    name = models.CharField(max_length=250)
    kit_consultant_code = models.CharField(max_length=250, blank=True)
    kit_consultant_name = models.CharField(max_length=250, blank=True)
    kit_contact_person = models.CharField(max_length=250, blank=True)

    mep_consultant_code = models.CharField(max_length=250, blank=True)
    mep_consultant_name = models.CharField(max_length=250, blank=True)
    mep_contact_person = models.CharField(max_length=250, blank=True)
    
    pm_consultant_code = models.CharField(max_length=250, blank=True)
    pm_consultant_name = models.CharField(max_length=250, blank=True)
    pm_contact_person = models.CharField(max_length=250, blank=True)
    
    customer_group_type = models.CharField(max_length=250, blank=True)
    contact_person = models.CharField(max_length=250, blank=True)
    
    start_date = models.CharField(max_length=50, blank=True)
    target_date = models.CharField(max_length=50, blank=True)
    completion_date = models.CharField(max_length=50, blank=True)    
    details = models.CharField(max_length=1000, blank=True)
    
    #cardcode = models.CharField(max_length=100, blank=True)    
    CardCode = models.CharField(max_length=100, blank=True)    
    sector = models.CharField(max_length=250, blank=True)
    type = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=250, blank=True)
    project_owner = models.CharField(max_length=250, blank=True)
    project_cost = models.CharField(max_length=250, blank=True)
    project_status = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=500, blank=True)

    CreatedDate = models.CharField(max_length=50, blank=True)
    CreatedTime = models.CharField(max_length=50, blank=True)
    
    GroupType = models.CharField(max_length=100, blank=True) #added by millan on 10 October 2022
    
    #added by millan on 11-10-2022
    cli_consultant_code = models.CharField(max_length=250, blank=True)
    cli_consultant_name = models.CharField(max_length=250, blank=True)
    cli_contact_person = models.CharField(max_length=250, blank=True)
    
    contr_consultant_code = models.CharField(max_length=250, blank=True)
    contr_consultant_name = models.CharField(max_length=250, blank=True)
    contr_contact_person = models.CharField(max_length=250, blank=True)
    
    fcm_consultant_code = models.CharField(max_length=250, blank=True)
    fcm_consultant_name = models.CharField(max_length=250, blank=True)
    fcm_contact_person = models.CharField(max_length=250, blank=True)
    
    arch_consultant_code = models.CharField(max_length=250, blank=True)
    arch_consultant_name = models.CharField(max_length=250, blank=True)
    arch_contact_person = models.CharField(max_length=250, blank=True)
    
    oth_consultant_code = models.CharField(max_length=250, blank=True)
    oth_consultant_name = models.CharField(max_length=250, blank=True)
    oth_contact_person = models.CharField(max_length=250, blank=True)
    #added by millan on 11-10-2022