from rest_framework import views, response, status

from products.models import Products, Category, ProductTypes

from .serializers import (
    CategorySerializer, ProductTypesSerializer, ProductSerializer
)


class CategoryAPIView(views.APIView):
    "To show all categories on main page"

    def get(self, request):
        queryset = Category.objects.all()
        if queryset:
            serializer = CategorySerializer(queryset, many=True)
            return response.Response(serializer.data)
        else:
            return response.Response(status=status.HTTP_404_NOT_FOUND)


class ProductTypesAPIView(views.APIView):
    """To show all product types"""

    def get(self, request):
        queryset = ProductTypes.objects.all()
        if queryset:
            serializer = ProductTypesSerializer(queryset, many=True)
            return response.Response(serializer.data)
        else:
            return response.Response(status=status.HTTP_404_NOT_FOUND)


class ProductsAPIView(views.APIView):
    """Shows all the products from db"""

    def get(self, request):
        queryset = Products.objects.all()
        if queryset:
            serializer = ProductSerializer(queryset, many=True)
            return response.Response(serializer.data)
        else:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
