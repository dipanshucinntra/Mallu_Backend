from django.urls import path
from .views import *


urlpatterns = [
    path('all', all),
    path('all_filter', all_filter),
    path('one', one),
    path('create', create),
    path('update', update),
    path('delete', delete),
]