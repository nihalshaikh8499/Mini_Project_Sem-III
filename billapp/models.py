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
    date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    file_path = models.FilePathField(path="bills", blank=True)
    mailed = models.BooleanField(default=False)
    ai_summary = models.TextField(blank=True, null=True)

    # Only relevant for bills
    payment_status = models.CharField(
        max_length=10,
        choices=[(PENDING, 'Pending'), (PAID, 'Paid'), (OVERDUE, 'Overdue')],
        blank=True,
        default=PENDING,
        null=True
        
    )

    def save(self, *args, **kwargs):
        if self.invoice_type == self.QUOTATION:
            self.payment_status = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_type} - {self.invoice_number} - {self.payment_status}"
    
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

class Machines(models.Model):
    MACHINE_TYPES = [
        ("PHOTOCOPIER", "Photocopier"),
        ("PRINTER_LASER", "Laser Printer"),
        ("PRINTER_INKJET", "Inkjet Printer"),
        ("MFD", "Multifunction Device"),
        ("SCANNER", "Scanner"),
        ("FAX", "Fax Machine"),

    ]
    
    machine_name = models.CharField(max_length=255)
    machine_type = models.CharField(max_length=50, choices=MACHINE_TYPES)
    serial_number = models.CharField(max_length=255, unique=True)
    purchase_date = models.DateField()
    warranty_expiry = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    copy_counter = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.machine_name
    
    def get_absolute_url(self):
        return reverse("machine_detail", args=[str(self.id)])
    
class ServiceNote(models.Model):
    machine = models.ForeignKey(
        'Machines',
        on_delete=models.CASCADE,
        related_name='service_notes' 
    )
    date_of_service = models.DateField()
    note = models.TextField()
    serviceman_name = models.CharField(max_length=255, blank=True) 
    fee_charged = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    copy_counter_at_service = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.machine.machine_name} on {self.date_of_service}"

    class Meta:
        ordering = ['-created_at']