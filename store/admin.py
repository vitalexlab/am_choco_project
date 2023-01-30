from django.contrib import admin

from store.models import *

admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(OrderItemCartRelations)
