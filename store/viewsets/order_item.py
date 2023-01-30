from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from products.models import Products
from store.models import OrderItem
from store.serializers.order_item import OrderItemCRUDSerializer


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
