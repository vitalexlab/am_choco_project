from rest_framework import serializers

from products.models import Products


class ProductSerializerForOrderItem(serializers.ModelSerializer):

    """The serializer for a CRUD Cart operations"""

    class Meta:
        model = Products
        fields = ['id', 'product_type', 'title', 'price', ]


class ProductSerializerForCart(serializers.ModelSerializer):

    """Product serializer for OrderItemCRUDSerializer"""

    class Meta:
        model = Products
        fields = ['id', 'title', 'price']
