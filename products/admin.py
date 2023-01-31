from django.contrib import admin

from .models import Category, ProductTypes, Products


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name__startswith',)


@admin.register(ProductTypes)
class ProductTypesAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title__startswith',)


@admin.register(Products)
class ProductTypesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', )
    ordering = ('id', )
    search_fields = (
        'title__startswith', 'category__name__startswith',
        'id', 'price'
    )
    list_filter = ('title', 'price', 'category__name')
    list_display_links = ('category',)
