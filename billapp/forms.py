from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Invoice, Customer, ServiceNote, Machines
from decimal import Decimal
from django.utils import timezone

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields =  ('username', 'email', 'password1', 'password2')

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'gst_number']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-yellow-500',
                'placeholder': 'Enter customer name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-yellow-500',
                'placeholder': 'Enter email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-yellow-500',
                'placeholder': 'Enter phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-[24px] focus:outline-none focus:ring-2 focus:ring-yellow-500',
                'placeholder': 'Enter address',
                'rows': 3
            }),
            'gst_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-yellow-500',
                'placeholder': 'Enter GST number'
            }),
        }

    def clean_gst_number(self):
        gst_number = self.cleaned_data.get('gst_number')
        if gst_number and len(gst_number) != 15:
            raise forms.ValidationError('GST number must be exactly 15 characters long.')
        return gst_number

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')
        return phone


from .models import Invoice, Customer
from decimal import Decimal

class InvoiceForm(forms.Form):
    INVOICE_TYPE_CHOICES = [
        ('BILL', 'Bill'),
        ('QUOTATION', 'Quotation'),
    ]
    
   
    invoice_type = forms.ChoiceField(
        choices=INVOICE_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-yellow-500'
        })
    )
    invoice_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-yellow-500',
            'placeholder': 'Enter invoice number'
        })
    )
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-yellow-500'
        })
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-yellow-500'
        })
    )
    
    
    product_name_1 = forms.CharField(max_length=255, required=False, label='Product 1 Name')
    quantity_1 = forms.IntegerField(min_value=1, required=False, label='Quantity 1')
    rate_1 = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Rate 1')
    
    product_name_2 = forms.CharField(max_length=255, required=False, label='Product 2 Name')
    quantity_2 = forms.IntegerField(min_value=1, required=False, label='Quantity 2')
    rate_2 = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Rate 2')
    
    product_name_3 = forms.CharField(max_length=255, required=False, label='Product 3 Name')
    quantity_3 = forms.IntegerField(min_value=1, required=False, label='Quantity 3')
    rate_3 = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Rate 3')
    
    product_name_4 = forms.CharField(max_length=255, required=False, label='Product 4 Name')
    quantity_4 = forms.IntegerField(min_value=1, required=False, label='Quantity 4')
    rate_4 = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Rate 4')
    
    product_name_5 = forms.CharField(max_length=255, required=False, label='Product 5 Name')
    quantity_5 = forms.IntegerField(min_value=1, required=False, label='Quantity 5')
    rate_5 = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Rate 5')
    
    product_name_6 = forms.CharField(max_length=255, required=False, label='Product 6 Name')
    quantity_6 = forms.IntegerField(min_value=1, required=False, label='Quantity 6')
    rate_6 = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Rate 6')
    
    def clean_invoice_number(self):
        invoice_number = self.cleaned_data.get('invoice_number')
        if Invoice.objects.filter(invoice_number=invoice_number).exists():
            raise forms.ValidationError('Invoice number already exists.')
        return invoice_number
    
    def clean(self):
        cleaned_data = super().clean()
        
        
        has_product = False
        for i in range(1, 7):
            product_name = cleaned_data.get(f'product_name_{i}')
            quantity = cleaned_data.get(f'quantity_{i}')
            rate = cleaned_data.get(f'rate_{i}')
            
            if product_name or quantity or rate:
                has_product = True
                
                if not (product_name and quantity and rate):
                    raise forms.ValidationError(f'For product {i}, all fields (name, quantity, rate) must be filled.')
        
        if not has_product:
            raise forms.ValidationError('At least one product must be added.')
        
        return cleaned_data
    
from .models import Machines

class MachineForm(forms.ModelForm):
    class Meta:
        model = Machines
        fields = ['machine_name', 'machine_type', 'serial_number', 'purchase_date']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500'
            })

class ServiceNoteForm(forms.ModelForm):
    class Meta:
        model = ServiceNote
        fields = ['date_of_service', 'serviceman_name', 'note', 'fee_charged']
        widgets = {
            'date_of_service': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent'
                }
            ),
            'serviceman_name': forms.TextInput(
                attrs={
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                    'placeholder': 'Enter serviceman name'
                }
            ),
            'note': forms.Textarea(
                attrs={
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                    'rows': 5,
                    'placeholder': 'Enter service details, issues found, actions taken, etc.'
                }
            ),
            'fee_charged': forms.NumberInput(
                attrs={
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent text-right',
                    'placeholder': '0.00',
                    'min': '0',
                    'step': '0.01'
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
       
        self.fields['date_of_service'].label = 'Service Date'
        self.fields['serviceman_name'].label = 'Serviceman Name'
        self.fields['note'].label = 'Service Notes'
        self.fields['fee_charged'].label = 'Service Fee (₹)'
        
       
        self.fields['serviceman_name'].required = False
        self.fields['fee_charged'].required = False
        
       
        self.fields['fee_charged'].help_text = 'Optional - Enter the service fee in rupees (e.g., 500.00)'
        
       
        if not self.instance.pk:  # Only for new service notes
            today = timezone.now().date()
            self.fields['date_of_service'].initial = today
           
            self.fields['date_of_service'].widget.attrs['value'] = today.strftime('%Y-%m-%d')

class CopyCounterForm(forms.ModelForm):
    class Meta:
        model = Machines
        fields = ['copy_counter']
        widgets = {
            'copy_counter': forms.NumberInput(
                attrs={
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent text-center text-2xl font-bold',
                    'placeholder': 'Enter new counter value',
                    'min': '0'
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['copy_counter'].label = 'New Copy Counter Value'
        
       
        if self.instance and self.instance.pk:
            current_value = self.instance.copy_counter
            self.fields['copy_counter'].help_text = f'Current counter value: {current_value:,}'