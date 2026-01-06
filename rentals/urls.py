from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('properties/', views.property_list, name='property_list'),
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('pay/<int:property_id>/', views.submit_payment, name='submit_payment'),
    path('landlord/add-property/', views.add_property, name='add_property'),
    path('landlord/edit-property/<int:property_id>/', views.edit_property, name='edit_property'),
    path('tenant/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('landlord/dashboard/', views.landlord_dashboard, name='landlord_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/approve-property/<int:property_id>/', views.approve_property, name='approve_property'),
    path('admin/reject-property/<int:property_id>/', views.reject_property, name='reject_property'),
    path('admin/approve-payment/<int:payment_id>/', views.approve_payment, name='approve_payment'),
    path('admin/reject-payment/<int:payment_id>/', views.reject_payment, name='reject_payment'),
]