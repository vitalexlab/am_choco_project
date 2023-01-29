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

    def create(self, validated_data):
        request_data = self.context['request'].data
        order_items = request_data.get('order_item')
        cart = Cart.objects.create(
            customer_phone=validated_data.get('customer_phone'),
            customer_wishes=validated_data.get('customer_wishes'),
        )
        for item in order_items:
            product_title: str = item.get('product').get('title')
            item_quantity: int = item.get('quantity')
            product = Products.objects.get(title=product_title)
            order_item = OrderItem.objects.get(
                product=product, quantity=item_quantity
            )
            cart.order_item.add(order_item)
        return cart

    class Meta:
        model = Cart
        fields = ['id', 'customer_phone', 'customer_wishes', 'order_item', 'total_cost']
        depth = 1
