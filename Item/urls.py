from django.urls import path,include
from .views import *

urlpatterns = [
    path('all', all),
    path('all_filter_page', all_filter_page),
    path('count_all', count_all),
    path('all1', all1),
    path('all1_filter_page', all1_filter_page),
    path('count_all1', count_all1),
    path('one',one),
    path('tax_all', tax_all),
    path('distributionlist',distributionlist),
    
    path('create',create),
    path('update',update),
    path('delete',delete),

    path('uqc_create', uqc_create),
    path('uqc_all', uqc_all),
    path('uqc_update', uqc_update),
    path('uqc_delete', uqc_delete),

]
