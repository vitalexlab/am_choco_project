import unittest

from django.db.utils import DataError

from products.models import Category


class ModelsTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.category_1 = Category.objects.create(
            name='Category 22',
        )
        self.impossible_name = '123456789012345678901234567890123456789012345678901'

    def test_category_slug_equals_name(self):
        self.assertEquals(self.category_1.slug, f'category-22')

    def test_possibility_to_change_name(self):
        self.category_1.name = 'Category 33'
        self.assertEquals(self.category_1.name, 'Category 33')
        # self.assertEquals(self.category_1.slug, 'category-33') #TODO upgrade making slugs

    def test_possibility_to_change_name_to_cyrriltic(self):
        self.category_1.name = 'Печенье'
        self.assertEquals(self.category_1.name, "Печенье")

    def test_impossible_to_create_with_impossible_name(self):
        try:
            Category.objects.create(
                name=self.impossible_name
            )
            is_it_possible = True
        except DataError:
            is_it_possible = False
        self.assertEqual(is_it_possible, False)

    def tearDown(self):
        self.category_1.delete()


if __name__ == '__main__':
    unittest.main()
