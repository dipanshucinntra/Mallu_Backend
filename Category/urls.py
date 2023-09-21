from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('one',one),
    path('all', all),
    path('all_filter', all_filter),
    path('update', update),
]
