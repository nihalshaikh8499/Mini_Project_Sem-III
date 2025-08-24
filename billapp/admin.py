from django.contrib import admin
from .models import Customer, Invoice, LineItem

class LineItemInline(admin.TabularInline):
    model = LineItem
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'invoice_type', 'customer', 'date', 'total_amount', 'mailed')
    list_filter = ('invoice_type', 'mailed', 'date')
    search_fields = ('invoice_number', 'customer__name', 'customer__email')
    inlines = [LineItemInline]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'gst_number')
    search_fields = ('name', 'email', 'phone', 'gst_number')

@admin.register(LineItem)
class LineItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'product_name', 'quantity', 'rate', 'amount')
    list_filter = ('invoice',)
