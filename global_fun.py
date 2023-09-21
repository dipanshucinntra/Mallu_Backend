from Employee.models import *

#for 3 role without ceo
def tree(SalesEmployeeCode):
        emp_obj =  Employee.objects.filter(SalesEmployeeCode=SalesEmployeeCode)
        print(emp_obj[0].role)
        i=1
        while int(emp_obj[0].reportingTo) !=0:
            emp_obj = Employee.objects.filter(SalesEmployeeCode=emp_obj[0].reportingTo)
            
            i=i+1
        return str(i)

#for 4 role with ceo
"""
def tree(SalesEmployeeCode):
        emp_obj =  Employee.objects.filter(SalesEmployeeCode=SalesEmployeeCode)
        print(emp_obj[0].role)
        i=1
        while int(emp_obj[0].reportingTo) !=0:
            emp_obj = Employee.objects.filter(SalesEmployeeCode=emp_obj[0].reportingTo)
            if emp_obj[0].role == 'admin':
                i=i+0
            else:
                i=i+1
        print(str(i))
        return str(i)
    #return Response({"message":"Success", "status":200, "data":[{"Level":str(i)}]})
"""

def tree_role(employee_obj):
    if employee_obj.role == 'admin' or employee_obj.role == 'ceo':
        lev = 1
    elif employee_obj.role == 'manager':
        lev = 2
    else:
        lev = 3
    return str(lev)
    