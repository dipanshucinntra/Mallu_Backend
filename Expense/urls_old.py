from django.urls import path,include

from .views import *
from .viewsExpenseType import create as ExpenseTypeCreate
from .viewsExpenseType import all as ExpenseTypeAll
from .viewsExpenseType import one as ExpenseTypeOne
from .viewsExpenseType import update as ExpenseTypeUpdate
from .viewsExpenseType import delete as ExpenseTypeDelete

# import viewsExpenseType as ExpenseType


urlpatterns = [
    # expense paths
    path('expense/create', create),
    path('expense/all', all),
    path('expense/all_filter', all_filter),
    path('expense/one', one),
    path('expense/update', update),
    path('expense/delete', delete),
    path('expense/expense_img_delete', expense_img_delete),

    # expense type paths
    path('expensetype/create', ExpenseTypeCreate),
    path('expensetype/all', ExpenseTypeAll),
    path('expensetype/one', ExpenseTypeOne),
    path('expensetype/update', ExpenseTypeUpdate),
    path('expensetype/delete', ExpenseTypeDelete),
]