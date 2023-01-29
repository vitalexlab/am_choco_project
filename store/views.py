from time import timezone

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from store.models import Cart
from store.serializers import CartSerializer


class CartViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    # TODO session_id
    """Creates, retrieves models from DB and delivers data to client

    GET:
    To get the data from the DB use schema:
    /store/cart/{id} where id is a session_id
    """
    # TODO change queryset
    queryset = Cart.objects.all().prefetch_related('order_item').order_by('-time_created')
    serializer_class = CartSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        order_data = request.data.get('order')
        order_items = request.data.get('order_item')
        if not request.session.get('session_id'):
            request.session['session_id'] = hash(timezone.now)
        data_to_serialize = {
            'session_id': request.session['session_id']
        }
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        cart_id = kwargs['pk']
        try:
            queryset = Cart.objects.get(id=cart_id)
            serializer = CartSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

