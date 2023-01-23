from django.contrib import admin

from store.models import *

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
