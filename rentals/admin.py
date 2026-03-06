from django.contrib import admin
from .models import MainCategory, SubCategory, Unit, Tenant, Contract, Payment

@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_category', 'location', 'is_active')
    list_filter = ('main_category', 'is_active')
    search_fields = ('name',)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'sub_category', 'unit_type', 'is_rented', 'area')
    list_filter = ('sub_category__main_category', 'unit_type', 'is_rented')
    search_fields = ('unit_number',)

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'identity_number', 'phone')
    search_fields = ('name', 'identity_number', 'phone')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'unit', 'tenant', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'payment_interval')
    search_fields = ('contract_number',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('contract', 'payment_date', 'amount_paid', 'payment_method')
    list_filter = ('payment_method',)