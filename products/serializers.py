from rest_framework.serializers import ModelSerializer

from products.models import Products, Category


class CategorySerializer(ModelSerializer):

    """Serializer to show all available categories with their images"""

    class Meta:
        model = Category
        fields = ['name', 'image']


class ProductsSerializer(ModelSerializer):
    """Serializer to show the data for a list of all products"""
    class Meta:
        model = Products
        fields = ['id', 'title', 'category', 'product_type', 'image', 'description', 'price']
