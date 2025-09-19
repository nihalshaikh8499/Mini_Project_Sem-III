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

  path('customer/<int:customer_id>/add-machine/', views.add_machine, name='add_machine'),
  path('machine/<int:pk>/update/', views.machine_update, name='machine_update'),
  path('machine/<int:pk>/delete/', views.machine_delete, name='machine_delete'),

  path('machine/<int:pk>/', views.machine_detail, name='machine_detail'),
    
    # Service Note URLs
  path('machine/<int:machine_pk>/add-service-note/', views.add_service_note, name='add_service_note'),
  path('service-note/<int:pk>/update/', views.update_service_note, name='update_service_note'),
  path('service-note/<int:pk>/delete/', views.delete_service_note, name='delete_service_note'),
  path('service-notes/', views.service_notes_view, name='service_notes'),
  path("service-note/select-machine/", views.select_machine_for_note, name="select_machine_for_note"),
  path("api/machines/", views.get_machines, name="get_machines"),
  
  # Copy Counter URLs
  path('machine/<int:machine_pk>/update-counter/', views.update_copy_counter, name='update_copy_counter'),
  path('machine/<int:machine_pk>/reset-counter/', views.reset_copy_counter, name='reset_copy_counter'),


]