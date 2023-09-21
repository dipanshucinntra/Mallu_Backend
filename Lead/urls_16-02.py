from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
    path('all_filter', all_filter),
    path('count_all', count_all),
    path('search_all_filter', search_all_filter),
    path('one',one),
    path('update', update),
    path('delete', delete),
    path('assign', assign),
    path('mark_junk', mark_junk),
    path('all_filter_junk', all_filter_junk),
    
    path('chatter', chatter),
    path('chatter_all', chatter_all),
    
    path('type_create', type_create),
    path('type_all', type_all),
    path('type_delete', type_delete),
    
    path('source_create', source_create),
    path('source_update', source_update),
    path('source_all', source_all),
    path('source_one', source_one),
    path('source_delete', source_delete),
    path('lead_dashboard', lead_dashboard),
    path('qualified_lead_y', qualified_lead_y),
    path('qualified_lead_w', qualified_lead_w),
    
    #added by millan on 21-09-2022 
    path('create_by_excel', create_by_excel),
    
]
