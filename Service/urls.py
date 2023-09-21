from django.urls import path,include
from .views import *

urlpatterns = [

    path('service/punch_attendance', punch_attendance),
    path('service/check_attendance', check_attendance),
    path('service/one_attendance', one_attendance),
    path('service/list_attendance', list_attendance),


]