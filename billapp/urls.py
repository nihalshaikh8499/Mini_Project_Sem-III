from django.contrib import admin
from django.urls import path, include
from . import views
from .views import (
    CustomerListView, CustomerDetailView, CustomerCreateView,
    CustomerUpdateView, CustomerDeleteView, InvoiceDeleteView
)
from .views import invoice_create, invoice_list, invoice_detail, download_invoice, mark_invoice_mailed, send_invoice_email_view


urlpatterns = [
  path('', views.index, name = 'index'),  
  path('register/',views.register, name = 'register'),
  path('customers/', CustomerListView.as_view(), name='customer_list'),
  path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
  path('customers/create/', CustomerCreateView.as_view(), name='customer_create'),
  path('customers/<int:pk>/update/', CustomerUpdateView.as_view(), name='customer_update'),
  path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
  # path('login/', CustomLoginView.as_view(), name='login'),

  path('invoices/create/', invoice_create, name='invoice_create'),
  path('invoices/', invoice_list, name='invoice_list'),
  path('invoices/<int:pk>/', invoice_detail, name='invoice_detail'),
  path('invoices/<int:pk>/download/', download_invoice, name='download_invoice'),
  path("invoices/<int:pk>/delete/", InvoiceDeleteView.as_view(), name="invoice_delete"),
  path('invoices/<int:pk>/mark-mailed/', mark_invoice_mailed, name='mark_invoice_mailed'),
  path("invoices/<int:pk>/send-email/", send_invoice_email_view, name="send_invoice_email"),
  path("invoices/<int:pk>/update-payment-status/", views.update_payment_status, name="update_payment_status"),

]