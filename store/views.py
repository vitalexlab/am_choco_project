import datetime

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from store.models import Cart, OrderItem
from store.serializers.cart import CartSerializer
from store.serializers.order_item import OrderItemCRUDSerializer


class CartViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Creates, retrieves models from DB and delivers data to client

    There is no list Cart instances
    """
    queryset = Cart.objects.all().prefetch_related('order_item').order_by('-time_created')
    serializer_class = CartSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        """Method to create a new cart

        <ul>Parameters
        <li>customer_phone - string in a format like: +375297777777</li>
        <li>customer_wishes - (string) an additional data from a customer
        to the bakery</li>

        This POST method creates a cart without any OrderItem instances.
        To add any OrderItem instances to the cart use POST method for
         an endpoint <b>/store/add-order-item/</b>. More info in a
         particular method description
        """
        if request.session.get('cart_id', False):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        order_data = request.data.get('order')
        order_items = request.data.get('order_item')
        data_to_serialize = {}
        if order_data:
            data_to_serialize.update(
                {'customer_phone': order_data.get('customer_phone')}
            )
            data_to_serialize.update(
                {'customer_wishes': order_data.get('wishes')}
            )
        if order_items:
            data_to_serialize.update({'order_item': order_items})
        serializer = self.get_serializer(data=data_to_serialize)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        request.session['cart_id'] = serializer.data.get('id')
        request.session.modified = True
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """Get method

        To get the data from the DB use endpoint:
        /store/cart/{id} where id is a cart id
        """

        cart_id = kwargs['pk']
        try:
            queryset = Cart.objects.get(id=cart_id)
            serializer = CartSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        """DELETE method

        Deletes a sessionid and a cart instance from the DB
        by using id of cart /store/cart/{id} where id is a cart id
        """

        cart_id = kwargs['pk']
        try:
            Cart.objects.get(pk=cart_id).delete()
            del request.session['cart_id']
        except KeyError:
            pass
        return Response(status=status.HTTP_200_OK)

#
# class AddOrDeleteOrderItemFromCart(
#     mixins.UpdateModelMixin, mixins.DestroyModelMixin,
#     viewsets.GenericViewSet
# ):
#
#     def update(self, request, *args, **kwargs):
#         order_item_id = kwargs['id']
#
#         return Response(status=status.HTTP_202_ACCEPTED)


class OrderItemViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):

    queryset = OrderItem.objects.all().select_related(
        'product'
    ).order_by('-time_added')
    serializer_class = OrderItemCRUDSerializer
    permission_classes = (AllowAny, )
