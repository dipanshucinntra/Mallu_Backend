from django.urls import path,include
from .views import *

urlpatterns = [
    path('all', all),
    path('all1', all1),
    path('one',one),
    path('tax_all', tax_all),
    path('distributionlist',distributionlist),
    
    #added by millan on 03-November-2022
    path('create',create),
    path('update',update),
    path('delete',delete),
    #added by millan on 03-November-2022
]
