from django.urls import path
from rest_framework import routers

from store.views import CartViewSet

router = routers.DefaultRouter()
router.register('cart', CartViewSet, basename='cart')

urlpatterns = [
    # path('cart/<str:phone>/', CartAPIView.as_view(), name='cart'),
]

urlpatterns += router.urls
