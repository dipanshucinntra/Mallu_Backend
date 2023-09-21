from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
    path('all_filter', all_filter),
    path('all_filter_page', all_filter_page),
    path('count_all', count_all),
    path('all_filter_page_web', all_filter_page_web),
	path('delivery', delivery),
	path('delivery_update', delivery_update),
	path('one',one),
	path('cancel',cancel),
    path('update',update),
    path('addendumcreate', addendumcreate),
    path('addendumall', addendumall),
    path('create_orderRequest', create_orderRequest),
    path('all_filter_page_orderRequest', all_filter_page_orderRequest),
    path('approval_orderRequest', approval_orderRequest),
    path('one_orderRequest', one_orderRequest),
    path('all_pagination', all_pagination),
]
