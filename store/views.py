import datetime

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from products.models import Products
from store.models import Cart, OrderItem, OrderItemCartRelations
from store.serializers.cart import CartSerializer
from store.serializers.order_item import OrderItemCRUDSerializer
from store.serializers.order_item_cart_rel import OrderItemCartRelSerializer


def get_valid_cart_id_or_400(request) -> [int, Response]:
    cart_id = request.session.get('cart_id', False)
    if not isinstance(cart_id, int):
        return Response(
            {
                'error': 'An incorrect cart_id type: must be int'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    return cart_id


def get_valid_order_item_pk_or_400(kwargs: dict) -> [int, Response]:
    try:
        order_item_pk = int(kwargs.get('pk'))
    except ValueError:
        return Response(
            {'error': 'order_item_pk must be an integer'},
            status=status.HTTP_400_BAD_REQUEST
        )
    return order_item_pk



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
         an endpoint <b>/store/add-order-item/</b>. More info in a
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
                {'customer_wishes': order_data.get('wishes')}
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
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderItemViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """CRUD operations for a OrderItem object

    POST method:
    creates an order item object. Read more in
    docs of the method

    GET method:
    Input an id (integer) in the store/order-item/{id} to get
    a particular order item data

    UPDATE method - Forbidden

    PATCH method:
    Partially change an order item. Read more in
    docs of the method

    DESTROY method:
    Input an id (integer) in the store/order-item/{id} to
    destroy an order item
    """

    queryset = OrderItem.objects.all().select_related(
        'product'
    ).order_by('-time_added')
    serializer_class = OrderItemCRUDSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        """Method to create a new OrderItem instance

        <ul>Parameters
        <li>quantity - a count of particular products in one
        OrderItem instance</li>
        <li>product_id - (int) of product id

        This POST method creates an order item with product and
        quantity of product items
        """
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        if not any((product_id, quantity)):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data={
            'product_id': product_id,
            'quantity': quantity
        })
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Products.DoesNotExist:
            return Response(
                {'error': 'Products object doesn\'t exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """This method is forbidden"""
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):

        """This method patches only a quantity of products

        So, insert JSON like:
        {
            "quantity": 10
        }
        To change quantity in a current order item
        """

        instance = self.get_queryset().get(id=kwargs.get('pk'))
        serializer = self.serializer_class(
            instance, data=request.data, partial=True
        )
        serializer.is_valid()
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_202_ACCEPTED
        )


class OrderItemCartRelViewset(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    rel_manager = OrderItemCartRelations.objects
    pref_order_item = rel_manager.prefetch_related('order_item')
    pref_order_item_sel_cart = pref_order_item.select_related('cart')

    queryset = pref_order_item_sel_cart.all()
    serializer_class = OrderItemCartRelSerializer
    permission_classes = (AllowAny, )

    def update(self, request, *args, **kwargs):
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
        cart_id = get_valid_cart_id_or_400(request)
        order_item_pk = get_valid_order_item_pk_or_400(kwargs)
        try:
            OrderItemCartRelations.objects.get(
                order_item_id=order_item_pk, cart_id=cart_id
            ).delete()
        except OrderItemCartRelations.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)
