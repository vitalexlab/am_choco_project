from django.contrib import admin

from store.models import *


@admin.action(description='Сделать все выделенные корзины выполненными')
def make_completed(modeladmin, request, queryset):
    queryset.update(is_completed='True')


@admin.action(description='Сделать все выделенные корзины подтвержденными')
def make_confirmed(modeladmin, request, queryset):
    queryset.update(is_confirmed='True')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product', 'quantity',
        'time_added', 'sale', 'get_cost'
    )
    ordering = ('id', 'product__title', )
    search_fields = (
        'product', 'quantity',
        'time_added', 'sale', 'get_cost'
    )
    list_filter = (
        'product', 'quantity',
        'time_added', 'sale',
    )
    list_display_links = ('product', )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'time_created', 'customer_phone',
        'cart_sale', 'total_cost', 'is_confirmed', 'is_completed',
    )
    ordering = ('id', 'time_created', )
    search_fields = (
        'customer_phone', 'order_item',
        'cart_sale', 'time_created', 'cart_sale',
        'total_cost'
    )
    list_filter = (
        'customer_phone', 'order_item',
        'cart_sale', 'is_confirmed',
        'is_completed', 'time_created',
    )
    actions = [make_completed, make_confirmed]


@admin.register(OrderItemCartRelations)
class OrderItemCartRelationsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'order_item', 'cart', 'created_at', 'updated_at',
    )
    ordering = ('id', 'order_item', 'created_at', 'updated_at', )
    search_fields = ('order_item', 'cart', 'created_at', 'updated_at', )
    list_filter = ('order_item', 'cart', 'created_at', 'updated_at', )
    list_display_links = ('order_item', 'cart', )
