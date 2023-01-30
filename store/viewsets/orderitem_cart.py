from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from store.models import OrderItemCartRelations
from store.serializers.order_item_cart_rel import OrderItemCartRelSerializer
from store.viewsets.utils import (
    get_valid_cart_id_or_400, get_valid_order_item_pk_or_400
)


class OrderItemCartRelViewset(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Viewset to add or to remove OrderItem instances to a cart

    <b>Make sure the cart is created before using this endpoint</b>
    There are 2 working methods:

    PUT method:
    To add an OrderItem instance to a cart use endpoint
    /store/add-to-cart/{id} - where id is a OrderItem instance
    id to add.

    DELETE method:
    To remove an OrderItem instance from a cart use endpoint
    /store/add-to-cart/{id} - where id is a OrderItem instance
    id to add.
    """


    rel_manager = OrderItemCartRelations.objects
    pref_order_item = rel_manager.prefetch_related('order_item')
    pref_order_item_sel_cart = pref_order_item.select_related('cart')

    queryset = pref_order_item_sel_cart.all()
    serializer_class = OrderItemCartRelSerializer
    permission_classes = (AllowAny, )

    def update(self, request, *args, **kwargs):

        """Method defines an interaction schema

        To update relations between an OrderItem instance and a
        Cart instance pass the OrderItem instance id in the endpoint
        /store/add-to-cart/{id}
        """

        cart_id = get_valid_cart_id_or_400(request)
        order_item_pk = get_valid_order_item_pk_or_400(kwargs)
        data = {
                'cart_id': cart_id,
                'order_item_id': order_item_pk
            }
        rel_object, status_ = OrderItemCartRelations.objects.get_or_create(
            order_item_id=order_item_pk, cart_id=cart_id
        )
        serializer = self.serializer_class(
            instance=rel_object, data=data, partial=False
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):

        """Method defines a removing object schema

        To delete relations between an OrderItem instance and a
        Cart instance pass the OrderItem instance id in the endpoint
        /store/add-to-cart/{id}
        """

        cart_id = get_valid_cart_id_or_400(request)
        order_item_pk = get_valid_order_item_pk_or_400(kwargs)
        try:
            OrderItemCartRelations.objects.get(
                order_item_id=order_item_pk, cart_id=cart_id
            ).delete()
        except OrderItemCartRelations.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)
