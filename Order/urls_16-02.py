from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
    path('all_filter', all_filter),
	path('delivery', delivery),
	path('delivery_update', delivery_update),
	path('one',one),
	path('cancel',cancel),
    path('update',update),
    path('addendumcreate', addendumcreate),
    path('addendumall', addendumall)
]
