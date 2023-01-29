from rest_framework import serializers

from store.models import OrderItem
from store.serializers.product import ProductSerializerForOrderItem, ProductSerializerForCart


class OrderItemForCartSerializer(serializers.ModelSerializer):
    """The Serializer for CRUD Cart operations"""

    product = ProductSerializerForOrderItem(many=False, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'sale', 'product', ]


class OrderItemCRUDSerializer(serializers.ModelSerializer):

    """The Serializer for CRUD OrderItem operations"""

    product = ProductSerializerForCart(many=False, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'product', ]
