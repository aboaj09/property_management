from django import forms
from .models import MainCategory, SubCategory, Unit, Tenant, Contract, Payment, Expense
from django.utils.translation import gettext_lazy as _

class MainCategoryForm(forms.ModelForm):
    class Meta:
        model = MainCategory
        fields = ['name', 'description']
        labels = {
            'name': _('اسم الفئة الرئيسية'),
            'description': _('وصف'),
        }

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'location', 'description']
        labels = {
            'name': _('اسم القسم الداخلي'),
            'location': _('الموقع'),
            'description': _('وصف'),
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_number', 'unit_type', 'floor', 'area', 'notes']  # بدون image
        labels = {
            'unit_number': _('رقم/اسم الوحدة'),
            'unit_type': _('نوع الوحدة'),
            'floor': _('الدور'),
            'area': _('المساحة (م²)'),
            'notes': _('ملاحظات'),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['floor'].required = False
        self.fields['area'].required = False
        self.fields['notes'].required = False

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'identity_number', 'phone', 'phone2', 'email', 'address', 'notes']  # بدون id_image
        labels = {
            'name': _('الاسم الكامل'),
            'identity_number': _('رقم الهوية/الإقامة'),
            'phone': _('رقم الجوال'),
            'phone2': _('جوال آخر'),
            'email': _('البريد الإلكتروني'),
            'address': _('العنوان'),
            'notes': _('ملاحظات'),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone2'].required = False
        self.fields['email'].required = False
        self.fields['address'].required = False
        self.fields['notes'].required = False

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['contract_number', 'start_date', 'lease_duration_months', 'rent_type', 'rent_amount', 'has_tax', 'tax_rate', 'payment_interval', 'notes']  # بدون contract_file
        labels = {
            'contract_number': _('رقم العقد'),
            'start_date': _('تاريخ البداية'),
            'lease_duration_months': _('مدة العقد (بالأشهر)'),
            'rent_type': _('نوع الإيجار'),
            'rent_amount': _('قيمة الإيجار'),
            'has_tax': _('تطبق الضريبة؟'),
            'tax_rate': _('نسبة الضريبة (%)'),
            'payment_interval': _('دورة السداد'),
            'notes': _('ملاحظات'),
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'].required = False
        self.fields['tax_rate'].required = False
        self.fields['lease_duration_months'].initial = 12

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_date', 'amount_paid', 'for_period_start', 'for_period_end', 'payment_method', 'reference_number', 'notes']  # بدون receipt_image
        labels = {
            'payment_date': _('تاريخ الدفع'),
            'amount_paid': _('المبلغ المدفوع'),
            'for_period_start': _('بداية الفترة'),
            'for_period_end': _('نهاية الفترة'),
            'payment_method': _('طريقة الدفع'),
            'reference_number': _('رقم المرجع/الشيك'),
            'notes': _('ملاحظات'),
        }
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'for_period_start': forms.DateInput(attrs={'type': 'date'}),
            'for_period_end': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reference_number'].required = False
        self.fields['notes'].required = False

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'description', 'amount', 'has_tax', 'tax_rate', 'tax_refundable', 'attachment', 'notes']  # نبقى على attachment
        labels = {
            'date': _('التاريخ'),
            'description': _('البيان'),
            'amount': _('المبلغ'),
            'has_tax': _('المبلغ شامل الضريبة؟'),
            'tax_rate': _('نسبة الضريبة (%)'),
            'tax_refundable': _('الضريبة قابلة للاسترداد؟'),
            'attachment': _('مرفق (فاتورة)'),
            'notes': _('ملاحظات'),
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'].required = False
        self.fields['tax_rate'].required = False
        self.fields['tax_refundable'].required = False
        self.fields['attachment'].required = False