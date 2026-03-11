from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum
from datetime import date
import os

# دالة مساعدة لتوليد مسار رفع الصور (يمكن إضافتها إذا كانت مستخدمة، وإلا حذفها)
def tenant_id_path(instance, filename):
    return f'tenants/{instance.identity_number}/{filename}'

class MainCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="اسم الفئة الرئيسية")
    description = models.TextField(blank=True, verbose_name="وصف")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "فئة رئيسية"
        verbose_name_plural = "الفئات الرئيسية"
        ordering = ['name']

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='subcategories', verbose_name="الفئة الرئيسية")
    name = models.CharField(max_length=200, verbose_name="اسم القسم الداخلي")
    location = models.CharField(max_length=300, verbose_name="الموقع", blank=True)
    description = models.TextField(blank=True, verbose_name="وصف")
    is_active = models.BooleanField(default=True, verbose_name="نشط؟")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "قسم داخلي"
        verbose_name_plural = "الأقسام الداخلية"
        ordering = ['main_category', 'name']

    def __str__(self):
        return f"{self.name} ({self.main_category.name})"

    def total_expenses(self, start_date=None, end_date=None):
        qs = self.expenses.all()
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)
        return qs.aggregate(total=Sum('amount'))['total'] or 0

    def total_refundable_tax(self, start_date=None, end_date=None):
        qs = self.expenses.filter(tax_refundable=True)
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)
        total_tax = 0
        for exp in qs:
            if exp.has_tax:
                tax_amount = exp.amount * (exp.tax_rate / 100) / (1 + exp.tax_rate/100)
                total_tax += tax_amount
        return total_tax


class Unit(models.Model):
    UNIT_TYPES = [
        ('shop', 'محل تجاري'),
        ('apartment', 'شقة سكنية'),
        ('room', 'غرفة'),
        ('farm_unit', 'وحدة زراعية'),
        ('office', 'مكتب'),
        ('warehouse', 'مستودع'),
        ('other', 'أخرى'),
    ]
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='units', verbose_name="القسم الداخلي")
    unit_number = models.CharField(max_length=50, verbose_name="رقم/اسم الوحدة")
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPES, verbose_name="نوع الوحدة")
    floor = models.IntegerField(verbose_name="الدور", null=True, blank=True)
    area = models.FloatField(verbose_name="المساحة (م²)", null=True, blank=True)
    is_rented = models.BooleanField(default=False, verbose_name="مؤجرة حالياً؟")
    notes = models.TextField(blank=True, verbose_name="ملاحظات")
    image = models.ImageField(upload_to='units/%Y/%m/', verbose_name="صورة الوحدة", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['sub_category', 'unit_number']
        verbose_name = "وحدة"
        verbose_name_plural = "الوحدات"
        ordering = ['sub_category', 'unit_number']

    def __str__(self):
        return f"{self.get_unit_type_display()} - {self.unit_number} ({self.sub_category.name})"

    @property
    def current_contract(self):
        return self.contracts.filter(is_active=True).first()


class Tenant(models.Model):
    name = models.CharField(max_length=200, verbose_name="الاسم الكامل")
    identity_number = models.CharField(max_length=50, verbose_name="رقم الهوية/الإقامة")
    phone = models.CharField(max_length=20, verbose_name="رقم الجوال")
    phone2 = models.CharField(max_length=20, blank=True, verbose_name="جوال آخر")
    email = models.EmailField(blank=True, verbose_name="البريد الإلكتروني")
    address = models.TextField(blank=True, verbose_name="العنوان")
    id_image = models.ImageField(upload_to=tenant_id_path, verbose_name="صورة الهوية", blank=True, null=True)
    notes = models.TextField(blank=True, verbose_name="ملاحظات")
    is_deleted = models.BooleanField(default=False, verbose_name="محذوف؟")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "مستأجر"
        verbose_name_plural = "المستأجرون"
        ordering = ['name']
    def __str__(self):
        return f"{self.name} - {self.identity_number}"


class Contract(models.Model):
    RENT_TYPE_CHOICES = [
        ('monthly', 'شهري'),
        ('yearly', 'سنوي'),
    ]
    PAYMENT_INTERVAL_CHOICES = [
        ('monthly', 'شهري'),
        ('quarterly', 'ربع سنوي'),
        ('half_yearly', 'نصف سنوي'),
        ('yearly', 'سنوي'),
    ]
    contract_number = models.CharField(max_length=100, unique=True, verbose_name="رقم العقد")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='contracts', verbose_name="الوحدة")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='contracts', verbose_name="المستأجر")
    start_date = models.DateField(verbose_name="تاريخ بداية العقد")
    lease_duration_months = models.PositiveIntegerField(default=12, verbose_name="مدة العقد (بالأشهر)")
    rent_type = models.CharField(max_length=10, choices=RENT_TYPE_CHOICES, default='monthly', verbose_name="نوع الإيجار")
    rent_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="قيمة الإيجار")
    has_tax = models.BooleanField(default=True, verbose_name="تطبق الضريبة؟")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=15.00, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="نسبة الضريبة (%)")
    payment_interval = models.CharField(max_length=20, choices=PAYMENT_INTERVAL_CHOICES, default='monthly', verbose_name="دورة السداد")
    is_active = models.BooleanField(default=True, verbose_name="العقد ساري؟")
    contract_file = models.FileField(upload_to='contracts/%Y/%m/', verbose_name="ملف العقد", blank=True, null=True)
    notes = models.TextField(blank=True, verbose_name="ملاحظات")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grace_period_days = models.PositiveIntegerField(default=0, verbose_name="فترة السماح (أيام)", help_text="عدد الأيام قبل بداية العقد التي لا تحتسب فيها الضريبة")

    class Meta:
        verbose_name = "عقد"
        verbose_name_plural = "العقود"
        ordering = ['-created_at']

    def __str__(self):
        return f"عقد {self.contract_number} - {self.unit}"

    @property
    def end_date(self):
        from dateutil.relativedelta import relativedelta
        return self.start_date + relativedelta(months=self.lease_duration_months) - relativedelta(days=1)

    @property
    def monthly_rent(self):
        if self.rent_type == 'yearly':
            return self.rent_amount / 12
        return self.rent_amount

    @property
    def tax_amount_monthly(self):
        if self.has_tax:
            return self.monthly_rent * (self.tax_rate / 100)
        return 0
    
    def get_tax_from_total(self, total_with_tax):
        if self.has_tax and self.tax_rate > 0:
           return total_with_tax * (self.tax_rate / 100) / (1 + self.tax_rate/100)
        return 0

    @property
    def total_monthly_with_tax(self):
        return self.monthly_rent + self.tax_amount_monthly

    @property
    def duration_months(self):
        return self.lease_duration_months

    @property
    def total_expected(self):
        return self.total_monthly_with_tax * self.duration_months

    @property
    def total_paid(self):
        total = self.payments.aggregate(Sum('amount_paid'))['amount_paid__sum']
        return total or 0

    @property
    def remaining(self):
        return self.total_expected - self.total_paid

    @property
    def total_tax_paid(self):
        total = 0
        for payment in self.payments.all():
            if self.has_tax:
                total += payment.amount_paid * (self.tax_rate / 100) / (1 + self.tax_rate/100)
        return total
    


class Payment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='payments', verbose_name="العقد")
    payment_date = models.DateField(verbose_name="تاريخ الدفع")
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="المبلغ المدفوع")
    for_period_start = models.DateField(verbose_name="بداية الفترة المدفوعة")
    for_period_end = models.DateField(verbose_name="نهاية الفترة المدفوعة")
    payment_method = models.CharField(
        max_length=30,
        choices=[('cash', 'نقدي'), ('bank', 'تحويل بنكي'), ('check', 'شيك')],
        default='cash',
        verbose_name="طريقة الدفع"
    )
    reference_number = models.CharField(max_length=100, blank=True, verbose_name="رقم المرجع/الشيك")
    receipt_image = models.ImageField(upload_to='payments/%Y/%m/', verbose_name="صورة الإيصال", blank=True, null=True)
    notes = models.TextField(blank=True, verbose_name="ملاحظات")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "دفعة"
        verbose_name_plural = "الدفعات"
        ordering = ['-payment_date']

    def __str__(self):
        return f"دفعة {self.amount_paid} في {self.payment_date}"


class Expense(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='expenses', verbose_name="القسم الداخلي")
    date = models.DateField(verbose_name="تاريخ المصروف")
    description = models.CharField(max_length=255, verbose_name="البيان")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="المبلغ (شامل الضريبة إن وجدت)")
    has_tax = models.BooleanField(default=False, verbose_name="المبلغ شامل الضريبة؟")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=15.00, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="نسبة الضريبة (%)")
    tax_refundable = models.BooleanField(default=False, verbose_name="الضريبة قابلة للاسترداد؟")
    attachment = models.FileField(upload_to='expenses/%Y/%m/', verbose_name="مرفق (فاتورة)", blank=True, null=True)
    notes = models.TextField(blank=True, verbose_name="ملاحظات")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "مصروف"
        verbose_name_plural = "المصروفات"
        ordering = ['-date']

    def __str__(self):
        return f"{self.description} - {self.amount} ({self.date})"

    @property
    def tax_amount(self):
        if self.has_tax:
            return self.amount * (self.tax_rate / 100) / (1 + self.tax_rate/100)
        return 0

    @property
    def amount_without_tax(self):
        if self.has_tax:
            return self.amount - self.tax_amount
        return self.amount