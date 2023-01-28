from rest_framework.serializers import ModelSerializer

from store.models import Cart, OrderItem
from products.models import Products


class OrderItemProductSerializer(ModelSerializer):

    class Meta:
        model = Products
        fields = ['id', 'product_type', 'title', 'price']


class OrderItemSerializer(ModelSerializer):

    product = OrderItemProductSerializer(many=False, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'sale', 'product']


class CartSerializer(ModelSerializer):

    order_item = OrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = ['customer_phone', 'customer_wishes', 'order_item', 'total_cost']
        depth = 1
