from django.urls import path,include
from .views import *
from BusinessPartner import views, viewsBPBranch, viewsBPEmployee, viewsBPDepartment, viewsBPPosition, viewsBPCurrency

urlpatterns = [
    path('businesspartner/create', create),
    path('businesspartner/all', all),
    path('businesspartner/all_filter_page', all_filter_page),
    path('businesspartner/all_filter_page_web', all_filter_page_web),
    path('businesspartner/all_pagination', all_pagination),
    path('businesspartner/count_all', count_all),
    path('businesspartner/all_bp', all_bp),
    path('businesspartner/one', one),
    path('businesspartner/update', update),
    path('businesspartner/delete', delete),
    path('businesspartner/branchbybp', branchbybp),
    path('businesspartner/customer_status', customer_status),
    
    path('businesspartner/branch/create', viewsBPBranch.create),
    path('businesspartner/branch/one', viewsBPBranch.one),
    path('businesspartner/branch/all', viewsBPBranch.all),
    path('businesspartner/branch/update', viewsBPBranch.update),
    path('businesspartner/branch/delete', viewsBPBranch.delete),
    
    path('businesspartner/employee/create', viewsBPEmployee.create),
    path('businesspartner/employee/one', viewsBPEmployee.one),
    path('businesspartner/employee/all', viewsBPEmployee.all),
    path('businesspartner/employee/update', viewsBPEmployee.update),
    path('businesspartner/employee/delete', viewsBPEmployee.delete),
    
    path('businesspartner/department/create', viewsBPDepartment.create),
    path('businesspartner/department/one', viewsBPDepartment.one),
    path('businesspartner/department/all', viewsBPDepartment.all),
    path('businesspartner/department/update', viewsBPDepartment.update),
    path('businesspartner/department/delete', viewsBPDepartment.delete),
    
    path('businesspartner/position/create', viewsBPPosition.create),
    path('businesspartner/position/one', viewsBPPosition.one),
    path('businesspartner/position/all', viewsBPPosition.all),
    path('businesspartner/position/update', viewsBPPosition.update),
    path('businesspartner/position/delete', viewsBPPosition.delete),
    
    path('businesspartner/currency/all', viewsBPCurrency.all),
    
    #added by millan on 11-10-2022
    path('businesspartner/monthlySales', monthlySales),  
    path('businesspartner/employee_target', employee_target), 
    path('businesspartner/target_anu_ach', target_anu_ach), 

    #added by millan on 01-11-2022
    path('businesspartner/all_bpEmployee', all_bpEmployee),  
    
]
