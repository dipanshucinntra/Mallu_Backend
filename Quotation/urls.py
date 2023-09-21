from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('create_web', create_web),
    path('all', all),
    path('all_filter', all_filter),
    path('all_filter_page', all_filter_page),
    path('count_all', count_all),
    path('all_filter_page_web', all_filter_page_web),
    path('one',one),
    path('update',update),
    path('cancel',cancel),
    path('fav',fav),
    path('approve',approve),
    path('pending',pending),
    path('filter_by_payment',filter_by_payment),    
    path('approved',approved)
]
