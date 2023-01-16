from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Category


class CategoryTest(APITestCase):

    def setUp(self) -> None:
        Category.objects.create(name='Category1')
        self.pathname = 'categories'

    def get_response_category(self):
        url = reverse(self.pathname)
        response = self.client.get(url)
        return response

    def test_list_categories_url(self):
        """Ensure that we can show a category list"""
        response = self.get_response_category()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_categories_count(self):
        """Ensure that all the categories are shown"""
        response = self.get_response_category()
        self.assertEqual(len(response.data), 1)
        Category.objects.create(name='Category2')
        response2 = self.get_response_category()
        self.assertEqual(len(response2.data), 2)

    def test_category_name(self):
        """Ensure that a name in a view is equal with a name from db"""
        name_from_db = Category.objects.get().name
        response = self.get_response_category()
        name_from_view = response.data[0].get('name')
        self.assertEqual(name_from_db, name_from_view)

    def test_category_slug(self):
        """Ensure that in a view we are not can get a slug"""
        slug1 = 'slug1'
        new_cat = Category.objects.create(name='cat3', slug=slug1)
        slug1_from_db = new_cat.slug
        response = self.get_response_category()
        slug1_from_view = response.data[1].get('slug')
        self.assertNotEqual(slug1_from_db, slug1_from_view)
