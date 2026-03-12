from django.urls import path
from . import views

urlpatterns = [
    # الصفحات العامة
    path('', views.home, name='home'),
    path('categories/', views.main_categories, name='main_categories'),
    path('category/<int:pk>/', views.main_category_detail, name='main_category_detail'),
    path('subcategory/<int:pk>/', views.subcategory_detail, name='subcategory_detail'),
    path('unit/<int:pk>/', views.unit_detail, name='unit_detail'),
    
    # مسارات المصادقة
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # مسارات الإدخال المتسلسل
    path('add/flow/', views.add_unit_flow, name='add_unit_flow'),
    path('add/main-category/', views.add_main_category, name='add_main_category'),
    path('add/choose-subcategory/<int:category_id>/', views.choose_subcategory, name='choose_subcategory'),
    path('add/sub-category/<int:category_id>/', views.add_sub_category, name='add_sub_category'),
    path('add/unit/<int:subcategory_id>/', views.add_unit, name='add_unit'),
    path('add/tenant/', views.add_tenant, name='add_tenant'),
    path('add/contract/', views.add_contract, name='add_contract'),
    path('add/payment/', views.add_payment, name='add_payment'),
    path('add/expense/<int:subcategory_id>/', views.add_expense, name='add_expense'),
    
    # مسارات التقارير
    path('profit-loss/', views.profit_loss_report, name='profit_loss_report'),
    
    # مسارات التعديل (Edit)
    path('edit/main-category/<int:pk>/', views.edit_main_category, name='edit_main_category'),
    path('edit/sub-category/<int:pk>/', views.edit_sub_category, name='edit_sub_category'),
    path('edit/unit/<int:pk>/', views.edit_unit, name='edit_unit'),
    path('edit/tenant/<int:pk>/', views.edit_tenant, name='edit_tenant'),
    path('edit/contract/<int:pk>/', views.edit_contract, name='edit_contract'),
    path('edit/payment/<int:pk>/', views.edit_payment, name='edit_payment'),
    path('edit/expense/<int:pk>/', views.edit_expense, name='edit_expense'),
    
    # مسارات الحذف (Delete)
    path('delete/main-category/<int:pk>/', views.delete_main_category, name='delete_main_category'),
    path('delete/sub-category/<int:pk>/', views.delete_sub_category, name='delete_sub_category'),
    path('delete/unit/<int:pk>/', views.delete_unit, name='delete_unit'),
    path('delete/tenant/<int:pk>/', views.delete_tenant, name='delete_tenant'),
    path('delete/contract/<int:pk>/', views.delete_contract, name='delete_contract'),
    path('delete/payment/<int:pk>/', views.delete_payment, name='delete_payment'),
    path('delete/expense/<int:pk>/', views.delete_expense, name='delete_expense'),
    
    # مسارات التقارير الإضافية
    path('reports/', views.reports_dashboard, name='reports_dashboard'),
    path('reports/rent/', views.rent_report, name='rent_report'),
    path('reports/expense/', views.expense_report, name='expense_report'),
    path('reports/tax/', views.tax_report, name='tax_report'),
    
    # مسارات التصدير
    path('export/rent/excel/', views.export_rent_excel, name='export_rent_excel'),
    path('export/expense/excel/', views.export_expense_excel, name='export_expense_excel'),
    path('export/rent/pdf/', views.export_rent_pdf, name='export_rent_pdf'),
    path('export/expense/pdf/', views.export_expense_pdf, name='export_expense_pdf'),
    
    # مسارات إضافية
    path('search/', views.advanced_search, name='advanced_search'),
    path('add/contract-for-unit/<int:unit_id>/', views.add_contract_for_unit, name='add_contract_for_unit'),
    
    # مسار قائمة المستأجرين (الجديد)
    path('tenants/', views.tenant_list, name='tenant_list'),
]