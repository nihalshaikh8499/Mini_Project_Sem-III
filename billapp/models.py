from django.db import models
from django.urls import reverse

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    gst_number = models.CharField(max_length=15)


class Invoice(models.Model):
    BILL = 'BILL'
    QUOTATION = 'QUOTATION'
    TYPE_CHOICES = [(BILL, 'Bill'), (QUOTATION, 'Quotation')]
    PENDING = 'PENDING'
    PAID = 'PAID'
    OVERDUE = 'OVERDUE'


    invoice_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    invoice_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    file_path = models.FilePathField(path="bills", blank=True)
    mailed = models.BooleanField(default=False)
    ai_summary = models.TextField(blank=True, null=True)
    payment_status = models.BooleanField(default=False) 


    def __str__(self):
        return f"{self.invoice_type} - {self.invoice_number}"
    def get_absolute_url(self):
        return reverse("invoice_detail", args=[str(self.pk)])

class LineItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.rate  
        super().save(*args, **kwargs)
