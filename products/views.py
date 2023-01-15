from django.shortcuts import render
from rest_framework import views, response

from products.models import Products, Category

from .serializers import ProductsSerializer, CategorySerializer


class CategoryAPIView(views.APIView):
    "To show all categories on main page"

    def get(self, request):
        queryset = Category.objects.all()
        serilalizer = CategorySerializer(queryset, many=True)
        return response.Response(serilalizer.data)


class ProductsAPIView(views.APIView):

    """List all products"""
    def get(self, request, format=None):
        queryset = Products.objects.all()
        serializer = ProductsSerializer(queryset, many=True)
        return response.Response(serializer.data)
