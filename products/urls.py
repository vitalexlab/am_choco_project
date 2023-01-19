from django.urls import path

from products.views import CategoryAPIView, ProductTypesAPIView


urlpatterns = [
    # path('items/', ProductsAPIView.as_view()),
    path('categories/', CategoryAPIView.as_view(), name='categories'),
    path('types/', ProductTypesAPIView.as_view(), name='types')
]
