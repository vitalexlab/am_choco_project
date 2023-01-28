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
    # TODO change queryset
    queryset = Cart.objects.all().prefetch_related('order_item').order_by('-time_created')
    serializer_class = CartSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        order_data = request.data['order']
        order_items = request.data['order_item']
        data_to_serialize = {
            'customer_phone': order_data.get('customer_phone'),
            'customer_wishes': order_data.get('wishes'),
            'order_item': order_items
        }
        serializer = self.get_serializer(data=data_to_serialize)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        phone_number = kwargs['pk']
        try:
            queryset = Cart.objects.get(customer_phone=phone_number)
            serializer = CartSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
