from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from store.models import Cart
from store.serializers.cart import CartSerializer


class CartViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
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
         an endpoint <b>/store/add-to-cart/</b>. More info in a
         particular method description
        """
        if request.session.get('cart_id', False):
            return Response(status=status.HTTP_403_FORBIDDEN)
        order_data = request.data.get('order')
        data_to_serialize = {}
        if order_data:
            data_to_serialize.update(
                {'customer_phone': order_data.get('customer_phone')}
            )
            data_to_serialize.update(
                {'customer_wishes': order_data.get('customer_wishes')}
            )
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
        except Cart.DoesNotExist:
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
        return Response(status=status.HTTP_204_NO_CONTENT)
