from django.contrib import admin

from .models import Category, ProductTypes, Products

admin.site.register(Category)
admin.site.register(ProductTypes)
admin.site.register(Products)
