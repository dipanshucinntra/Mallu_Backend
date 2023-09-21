from django.urls import path,include
from .views import *

urlpatterns = [
    path('all', all),
    path('all_filter', all_filter),
    path('one',one)
]
