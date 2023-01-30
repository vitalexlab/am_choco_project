from rest_framework import routers

from store.viewsets.cart import CartViewSet
from store.viewsets.order_item import OrderItemViewSet
from store.viewsets.orderitem_cart import OrderItemCartRelViewset

router = routers.DefaultRouter()
router.register('cart', CartViewSet, basename='cart')
router.register('order-item', OrderItemViewSet, basename='order-item')
router.register(
    'add-order-item', OrderItemCartRelViewset, basename='add-order-item'
)

urlpatterns: list = [] + router.urls
