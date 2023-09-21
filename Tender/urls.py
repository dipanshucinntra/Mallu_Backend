from django.urls import path,include
from .views import *

urlpatterns = [
    path('tender/create', create),
    path('tender/addtenderdocuments', addtenderdocuments),
    path('tender/tendersubmission', tendersubmission),
    path('tender/tenderopening', tenderopening),
    path('tender/technicalopening', technicalopening),
    path('tender/lowestone', lowestone),
    path('tender/tenderclosed', tenderclosed),
    path('tender/all', all),
    path('tender/all_filter', all_filter),
    path('tender/one', one),
    
    # update 
    path('tender/update', update),
    path('tender/updatetenderopening', updatetenderopening),
    path('tender/updatetechnicalopening', updatetechnicalopening),
    path('tender/updatelowestone', updatelowestone),
    path('tender/updatestagestatus', updatestagestatus),

    # delete
    path('tender/deletedoc', deletedoc),
    path('tender/deletetenderopening', deletetenderopening),
    path('tender/deletetechopening', deletetechopening),
    path('tender/deletelowestone', deletelowestone),
    path('tender/delete', delete),
]
