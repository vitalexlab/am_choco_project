from rest_framework.serializers import ModelSerializer

from products.models import Products, Category, ProductTypes


class CategorySerializer(ModelSerializer):

    """Serializer to show all available categories with their images"""

    class Meta:
        model = Category
        fields = ['name', 'image']


class ProductTypesSerializer(ModelSerializer):

    class Meta:
        model = ProductTypes
        fields = ['id', 'title']
