from rest_framework import serializers

from store.models import Cart
from store.serializers.order_item import OrderItemForCartSerializer


class CartSerializer(serializers.ModelSerializer):

    """The serializer for a CRUD Cart operations"""

    order_item = OrderItemForCartSerializer(
        read_only=True, many=True
    )

    def create(self, validated_data):
        cart = Cart.objects.create(
            customer_phone=validated_data.get('customer_phone'),
            customer_wishes=validated_data.get('customer_wishes'),
        )
        return cart

    class Meta:
        model = Cart
        fields = [
            'id', 'customer_phone', 'customer_wishes', 'order_item',
            'total_cost',
        ]
        depth = 1
