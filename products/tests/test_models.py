import unittest

from django.db.utils import DataError

from products.models import Category, ProductTypes


class ModelsTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.category_1 = Category.objects.create(
            name='Category 22',
        )
        self.product_type = ProductTypes.objects.create(
            title='Product type title'
        )
        self.impossible_name = '123456789012345678901234567890123456789012345678901'

    def test_category_title_is_predictable(self):
        self.assertEquals(self.category_1.name, 'Category 22')

    def test_product_type_title_is_predictable(self):
        self.assertEquals(self.product_type.title, 'Product type title')

    def test_category_slug_equals_name(self):
        self.assertEquals(self.category_1.slug, f'category-22')

    def test_possibility_to_change_category_name(self):
        self.category_1.name = 'Category 33'
        self.assertEquals(self.category_1.name, 'Category 33')
        # self.assertEquals(self.category_1.slug, 'category-33') #TODO upgrade making slugs

    def test_possibility_to_change_product_type_name(self):
        self.product_type.title = 'New product type title'
        self.assertEquals(self.product_type.title, 'New product type title')

    def test_possibility_to_change_category_name_to_cyrriltic(self):
        self.category_1.name = 'Печенье'
        self.assertEquals(self.category_1.name, "Печенье")

    def test_impossible_to_create_with_impossible_category_name(self):
        try:
            Category.objects.create(
                name=self.impossible_name
            )
            is_it_possible = True
        except DataError:
            is_it_possible = False
        self.assertEqual(is_it_possible, False)

    def test_possibility_to_change_product_type_name_to_cyrriltic(self):
        self.product_type.title = 'Что-то'
        self.assertEquals(self.product_type.title, 'Что-то')

    def test_impossible_to_create_with_impossible_product_type_name(self):
        try:
            ProductTypes.objects.create(
                title=self.impossible_name
            )
            is_it_possible = True
        except DataError:
            is_it_possible = False
        self.assertEqual(is_it_possible, False)

    def tearDown(self):
        self.category_1.delete()
        self.product_type.delete()


if __name__ == '__main__':
    unittest.main()
