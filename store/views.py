import datetime

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from store.models import Cart
from store.serializers import CartSerializer


class CartViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Creates, retrieves models from DB and delivers data to client

    GET:
    To get the data from the DB use schema:
    /store/cart/{id} where id is a cart id
    """
    queryset = Cart.objects.all().prefetch_related('order_item').order_by('-time_created')
    serializer_class = CartSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
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
        cart_id = kwargs['pk']
        try:
            queryset = Cart.objects.get(id=cart_id)
            serializer = CartSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        pass
        return Response(status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        cart_id = kwargs['pk']
        try:
            Cart.objects.get(pk=cart_id).delete()
            del request.session['cart_id']
        except KeyError:
            pass
        return Response(status=status.HTTP_200_OK)

