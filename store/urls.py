"""
Store app URL configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('faq/', views.faq, name='faq'),
    path('error-codes/', views.error_codes, name='error_codes'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('health/', views.health_check, name='health_check'),
    path('errors/<str:code>/', views.simulate_error, name='simulate_error'),
]
