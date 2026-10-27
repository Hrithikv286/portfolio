"""
Store Admin configuration
"""
from django.contrib import admin
from .models import Category, Brand, Product, FAQ, ErrorCode, SupportTicket


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'stock', 'is_active', 'is_featured', 'rating']
    list_filter = ['is_active', 'is_featured', 'is_new_arrival', 'category']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'is_active', 'is_featured']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']


@admin.register(ErrorCode)
class ErrorCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'severity', 'is_http_standard']
    list_filter = ['severity', 'is_http_standard']


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'user_name', 'user_email', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority']
    search_fields = ['ticket_id', 'user_name', 'user_email', 'user_message']
    readonly_fields = ['ticket_id', 'created_at']
