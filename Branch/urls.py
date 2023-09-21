from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
    path('one',one),
    path('update', update),
    path('delete', delete),

    ######################

    path('create_branch', create_branch),
    path('all_branch', all_branch),
    path('one_branch',one_branch),
    path('update_branch', update_branch),
    path('delete_branch', delete_branch)

]
