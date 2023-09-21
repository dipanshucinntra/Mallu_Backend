from django.urls import path,include
from .views import *

urlpatterns = [
    #path('create', create),
    path('all', all),
    path('all_filter', all_filter),
    path('all_filter_page', all_filter_page),
	path('one', one),
    path('create_delivery_note', create_delivery_note),
    path('update_delivery_note', update_delivery_note),
    path('update', update),
    path('change_status_delivery', change_status_delivery),
    path('change_address_ship_to',change_address_ship_to),
    path('change_shipped_with',change_shipped_with)
    # new apis
    #path('sync_invoice', syncInvoice),
]
