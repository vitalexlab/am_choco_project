from django.db.utils import DataError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Category, ProductTypes, Products


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


class ProductTypesTests(APITestCase):
    def setUp(self) -> None:
        pt1 = ProductTypes.objects.create(
            title='Name1', slug='Slug1'
        )
        pt2 = ProductTypes.objects.create(
            title='Name2'
        )
        self.name = 'types'

    def get_response(self):
        url = reverse(self.name)
        response = self.client.get(url)
        return response

    def test_get_product_types_list(self):
        response = self.get_response()
        self.assertEqual(len(response.data), 2)

    def test_count_product_types(self):
        count = ProductTypes.objects.count()
        response_data = self.get_response().data
        self.assertEqual(count, len(response_data))

    def test_product_type_title(self):
        new_product_type = ProductTypes.objects.create(title='New')
        product_from_response = self.get_response().data
        self.assertEqual(product_from_response[0].get('title'), 'Name1')
        self.assertEqual(product_from_response[1].get('title'), 'Name2')
        self.assertEqual(product_from_response[2].get('title'), new_product_type.title)

    def test_product_type_slug_from_db(self):
        product_type_1 = ProductTypes.objects.get(title='Name1')
        self.assertEqual(product_type_1.slug, 'Slug1')

    def test_product_type_slug_not_in_view(self):
        response = self.get_response().data
        for item in response:
            self.assertEqual(item.get('slug'), None)


class ProductTests(APITestCase):

    def setUp(self) -> None:
        self.category_name1 = 'Cat1'
        self.category_name2 = 'Cat2'
        self.category_obj1 = Category.objects.create(name=self.category_name1)
        self.category_obj2 = Category.objects.create(name=self.category_name2)

        self.pr_title1 = 'pt_title1'
        self.pr_title2 = 'pt_title2'
        pr_type1 = ProductTypes.objects.create(title=self.pr_title1)
        pr_type2 = ProductTypes.objects.create(title=self.pr_title2)

        self.title1 = 'Title1'
        self.title2 = 'Title2'

        self.desc1 = 'desc1'
        self.desc2 = 'desc2'

        self.compos1 = 'comp1'
        self.compos2 = 'comp2'

        self.price1 = 500
        self.price2 = 1000

        self.product_1 = Products.objects.create(
            title=self.title1, category=self.category_obj1, description=self.desc1,
            composition=self.compos1, price=self.price1
        )
        self.product_1.product_type.add(pr_type1)

        self.product_2 = Products.objects.create(
            title=self.title2, category=self.category_obj2, description=self.desc2,
            composition=self.compos2, price=self.price2
        )
        self.product_2.product_type.add(pr_type2)
        self.product_3 = Products.objects.create(
            title=self.title2, category=self.category_obj2, price=self.price2
        )
        self.response = self.get_response_data()

    def get_response_data(self):
        url = reverse('products')
        response = self.client.get(url)
        return response.data

    def test_product_title_equals_db_ones(self):
        self.assertEqual(self.response[0].get('title'), self.product_1.title)
        self.assertEqual(self.response[1].get('title'), self.product_2.title)
        self.assertEqual(self.response[2].get('title'), self.product_3.title)

    def test_product_types_of_product(self):
        self.assertEqual(
            self.response[0].get('product_type')[0].get('title'),
            self.pr_title1
        )
        self.assertEqual(
            self.response[1].get('product_type')[0].get('title'),
            self.pr_title2
        )
        self.assertTrue(
            self.response[2].get('product_type') == []
        )

    def test_product_types_serialized_data_count(self):
        self.assertEqual(len(self.response[0].get('product_type')[0]), 2)
        self.assertEqual(len(self.response[1].get('product_type')[0]), 2)
        self.assertEqual(self.response[2].get('product_type'), [])
        # self.assertRaises(IndexError, self.response[2].get('product_type')[0])

    def test_category_of_products(self):
        self.assertEqual(
            self.product_1.category,
            self.category_obj1
        )
        self.assertEqual(
            self.product_2.category,
            self.category_obj2
        )
        self.assertEqual(
            self.product_3.category,
            self.category_obj2
        )
        product_4 = Products.objects.create(
            title='title', category=self.category_obj1, price=1
        )
        new_resp = self.get_response_data()
        self.assertEqual(
            product_4.category.id, new_resp[3].get('category'),
        )

    def test_descriptions_products(self):
        for item in self.response:
            self.assertTrue(isinstance(item.get('description'), str))

    def test_product_composition(self):
        for item in self.response:
            self.assertTrue(isinstance(item.get('description'), str))

    def test_product_price(self):
        for item in self.response:
            self.assertTrue(item.get('price'), int)
