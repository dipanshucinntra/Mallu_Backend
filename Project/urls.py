from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
    path('allbycp', allbycp),
    path('one',one),
    path('update', update),
    path('delete', delete),
    path('project_all', project_all) # added by millan on 01-November-2022
]
