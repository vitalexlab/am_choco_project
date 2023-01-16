from django.urls import path

from products.views import ProductsAPIView, CategoryAPIView


urlpatterns = [
    # path('items/', ProductsAPIView.as_view()),
    path('categories/', CategoryAPIView.as_view(), name='categories')
]
