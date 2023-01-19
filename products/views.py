from django.shortcuts import render
from rest_framework import views, response

from products.models import Products, Category, ProductTypes

from .serializers import (CategorySerializer, ProductTypesSerializer)


class CategoryAPIView(views.APIView):
    "To show all categories on main page"

    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return response.Response(serializer.data)


class ProductTypesAPIView(views.APIView):
    """To show all product types"""

    def get(self, request):
        queryset = ProductTypes.objects.all()
        serializer = ProductTypesSerializer(queryset, many=True)
        return response.Response(serializer.data)
