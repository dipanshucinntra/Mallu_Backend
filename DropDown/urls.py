from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
    path('update', update),
    path('delete', delete),
    # path('static/all', static_all)
]
