from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from products.models import Products
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
        fields = ['id', 'quantity', 'product', 'sale']
        depth = 1

    def create(self, validated_data):
        req_data = self.context['request'].data
        product_id = req_data.get('product_id')
        if not product_id or not isinstance(product_id, int):
            raise ValueError('product_id must be int')
        quantity: int = validated_data.get('quantity')
        try:
            product_obj = Products.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return {'error': 'Product with such id doesn\'t exist'}
        order_item = OrderItem.objects.create(
            product=product_obj, quantity=quantity
        )
        return order_item
