"""bridge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lead/', include('Lead.urls')),
    path('activity/', include('Activity.urls')),
    path('notification/', include('Notification.urls')),
    path('', include('Countries.urls')),
    # path('', include('Countries.urls')),
    path('employee/', include('Employee.urls')),
    path('quotation/', include('Quotation.urls')),
    path('order/', include('Order.urls')),
    path('invoice/', include('Invoice.urls')),
    path('item/', include('Item.urls')),
    path('category/', include('Category.urls')),
    path('industries/', include('Industries.urls')),
    path('paymenttermstypes/', include('PaymentTermsTypes.urls')),
    path('company/', include('Company.urls')),
    path('branch/', include('Branch.urls')),
    path('deliverynote/', include('DeliveryNote.urls')),
    path('', include('Opportunity.urls')),
    path('', include('Tender.urls')),
    path('', include('BusinessPartner.urls')),
    path('', include('Campaign.urls')),
    path('', include('Expense.urls')),
    path('project/', include('Project.urls')),    
    path('attachment/', include('Attachment.urls')),
    path('caller/', include('Caller.urls')),
    path('clientbankdetails/', include('ClientBankDetails.urls')),
    path('', include('Payment.urls')),
    path('', include('TargetVisitor.urls')),
    path('', include('Service.urls')),
    path('dropdown/', include('DropDown.urls')),
]
