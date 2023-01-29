from rest_framework import routers

from store.views import CartViewSet, OrderItemViewset
    # AddOrDeleteOrderItemFromCart

router = routers.DefaultRouter()
router.register('cart', CartViewSet, basename='cart')
router.register('order-item', OrderItemViewset, basename='order-item')

urlpatterns: list = [] + router.urls
