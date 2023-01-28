from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from store.models import Cart
from store.serializers import CartSerializer


# class CartAPIView(views.APIView):
#     def get(self, request, phone):
#         try:
#             queryset = Cart.objects.get(order__consumer_phone=phone)
#             serializer = CartSerializer(queryset)
#             return response.Response(serializer.data, status=status.HTTP_200_OK)
#         except ObjectDoesNotExist:
#             return response.Response(status=status.HTTP_404_NOT_FOUND)
#
#     def post(self, request, phone):
#         request_with_phone = request.data
#         request_with_phone['order'] = {
#             'consumer_phone': phone
#         }
#         serializer = CartSerializer(data=request_with_phone)
#         if serializer.is_valid():
#             print(serializer.validated_data)
#             serializer.save()
#             return response.Response(
#                 serializer.data, status=status.HTTP_201_CREATED
#             )
#         return response.Response(
#             serializer.errors, status=status.HTTP_400_BAD_REQUEST
#         )
class CartViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):

    queryset = Cart.objects.all().prefetch_related('order_item').order_by('-time_created')
    serializer_class = CartSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        # order_data = request.data['order']
        # if order_data['consumer_phone']:
        #     serializer = OrderSerializer(queryset)
        ...

    def retrieve(self, request, *args, **kwargs):
        phone_number = kwargs['pk']
        try:
            queryset = Cart.objects.get(customer_phone=phone_number)
            serializer = CartSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
