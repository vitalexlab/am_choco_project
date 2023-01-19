import unittest
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import DataError

from products.models import Category, ProductTypes, Products


class CategoryTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.category_1 = Category.objects.create(
            name='Category 22',
        )
        self.impossible_name1 = '123456789012345678901234567890123456789012345678901'

    def test_category_title_is_predictable(self):
        self.assertEquals(self.category_1.name, 'Category 22')

    def test_category_slug_equals_name(self):
        self.assertEquals(self.category_1.slug, 'category-22')

    def test_possibility_to_change_category_name(self):
        self.category_1.name = 'Category 33'
        self.assertEquals(self.category_1.name, 'Category 33')
        # self.assertEquals(self.category_1.slug, 'category-33') #TODO upgrade making slugs

    def test_possibility_to_change_category_name_to_cyrriltic(self):
        self.category_1.name = 'Печенье'
        self.assertEquals(self.category_1.name, "Печенье")

    def test_impossible_to_create_with_impossible_category_name(self):
        try:
            Category.objects.create(
                name=self.impossible_name1
            )
            is_it_possible = True
        except DataError:
            is_it_possible = False
        self.assertEqual(is_it_possible, False)

    def tearDown(self):
        self.category_1.delete()


class ProductTypesTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.product_type = ProductTypes.objects.create(
            title='Product type title'
        )
        self.impossible_name2 = '1333456789012345678901234567890123456789012345678901'

    def test_product_type_title_is_predictable(self):
        self.assertEquals(self.product_type.title, 'Product type title')

    def test_possibility_to_change_product_type_name(self):
        self.product_type.title = 'New product type title'
        self.assertEquals(self.product_type.title, 'New product type title')

    def test_possibility_to_change_product_type_name_to_cyrriltic(self):
        self.product_type.title = 'Что-то'
        self.assertEquals(self.product_type.title, 'Что-то')

    def test_impossible_to_create_with_impossible_product_type_name(self):
        try:
            ProductTypes.objects.create(
                title=self.impossible_name2
            )
            is_it_possible = True
        except DataError:
            is_it_possible = False
        self.assertEqual(is_it_possible, False)

    def tearDown(self):
        self.product_type.delete()


class ProductsTestCase(unittest.TestCase):

    def setUp(self) -> None:

        # image_jpg = SimpleUploadedFile(
        #     name='test_image.jpg',
        #     content=open('products/tests/test_image.jpg', 'rb').read(),
        #     content_type='image/jpeg'
        # )
        self.category = Category.objects.create(
            name='Some category', slug='somecategory'
        )
        self.product_type = ProductTypes.objects.create(
            title='Product type title', slug='productslugtype'
        )
        self.product_1 = Products.objects.create(
            title='Product title', category=self.category,
            description='some desc', composition='Some composition',
            price=100
        )
        self.product_1.product_type.add(self.product_type)

        self.impossible_title = ''.join([str(y) for y in range(155)])



    def test_length_product_title(self):
        self.assertLess(len(self.product_1.title), 150)
        self.product_1.title = 's' * 151
        self.assertRaises(DataError, self.product_1.save)

    def test_product_title_is_predictable(self):
        self.assertEquals(self.product_1.title, 'Product title')

    def test_product_category_is_predictable(self):
        self.assertEquals(self.product_1.category, self.category)

    def test_product_type_is_predictable(self):
        self.assertEquals(
            self.product_1.product_type.first().title, self.product_type.title
        )

    def test_product_desc_is_predictable(self):
        self.assertEquals(self.product_1.description, 'some desc')

    def test_product_comp_is_predictable(self):
        self.assertEquals(self.product_1.composition, 'Some composition')

    def test_possibility_to_change_product_name(self):
        self.product_1.title = 'New product type title'
        self.assertEquals(self.product_1.title, 'New product type title')

    def test_possibility_to_change_product__name_to_cyrriltic(self):
        self.product_type.title = 'Что-то'
        self.assertEquals(self.product_type.title, 'Что-то')

    def test_impossible_to_create_with_impossible_product_name(self):
        try:
            ProductTypes.objects.create(
                title=self.impossible_title
            )
            is_it_possible = True
        except DataError:
            is_it_possible = False
        self.assertEqual(is_it_possible, False)

    def tearDown(self):
        self.product_1.delete()
        self.category.delete()
        self.product_type.delete()


if __name__ == '__main__':
    unittest.main()
