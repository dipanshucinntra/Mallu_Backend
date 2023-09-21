from django.urls import path, include
from .views import *

urlpatterns = [
    path("targetvisitor/create", create),
    path("targetvisitor/all", all),
    path("targetvisitor/all_filter", all_filter),
    path("targetvisitor/one", one),
    path("targetvisitor/update", update),
    

]


