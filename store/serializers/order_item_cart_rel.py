from rest_framework import serializers

from store.models import OrderItemCartRelations


class OrderItemCartRelSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItemCartRelations
        fields = ['order_item_id', 'cart_id']
