import unittest

from products.models import Category, Products, ProductTypes


def get_product(
        title: str, category: Category, description: str, price: int,
        comp: str, product_type: ProductTypes
):
    product_obj = Products.objects.create(
        title=title, category=category, description=description,
        price=price, composition=comp
    )
    product_obj.product_type.add(product_type)
    return product_obj


def get_category(name: str):
    return Category.objects.create(name=name)


def get_package_item(item: Products, count: int):
    item_price = item.price
    return Package.objects.create(
        item=item, count=count
    )


class PackageTests(unittest.TestCase):

    def setUp(self):
        self.product_name1 = 'Product1'
        self.product_name2 = 'Product2'

        self.category_name_1 = 'Category1212131'
        self.category_name_2 = 'Category212333'

        self.desc1 = 'desk1'
        self.desc2 = 'desk2'

        self.composition1 = 'comp1'
        self.composition2 = 'comp2'

        self.product_type_title1 = 'Pt1123123'
        self.product_type_title2 = 'Pt212312321'

        self.category1 = get_category(name=self.category_name_1)
        self.category2 = get_category(name=self.category_name_2)

        self.product_type1 = ProductTypes.objects.create(
            title=self.product_type_title1
        )
        self.product_type2 = ProductTypes.objects.create(
            title=self.product_type_title2
        )

        self.product1 = get_product(
            title=self.product_name1, category=self.category1,
            description=self.desc1, price=500, comp=self.composition1,
            product_type=self.product_type1
        )
        self.product2 = get_product(
            title=self.product_name2, category=self.category2,
            description=self.desc2, price=1000, comp=self.composition2,
            product_type=self.product_type2
        )

        self.product_count1 = 5
        self.product_count2 = 10

        self.package_1 = get_package_item(
            item=self.product1, count=self.product_count1)
        self.package_2 = get_package_item(
            item=self.product2, count=self.product_count2
        )

    def test_package_with_created_item(self):
        self.assertEqual(self.package_1.item, self.product1)
        self.assertEqual(self.package_2.item, self.product2)

    def test_package_with_count(self):
        self.assertEqual(self.package_1.count, self.product_count1)
        self.assertEqual(self.package_2.count, self.product_count2)

    def test_total_package_cost(self):
        total1 = self.product_count1 * self.product1.price
        total2 = self.product_count2 * self.product2.price
        self.assertTrue(isinstance(total1, int))
        self.assertTrue(isinstance(total2, int))
        self.assertEqual(self.package_1.package_price, total1)
        self.assertEqual(self.package_2.package_price, total2)

    def tearDown(self):
        self.product1.delete()
        self.product2.delete()
        self.category1.delete()
        self.category2.delete()
        self.product_type1.delete()
        self.product_type2.delete()


class OrderTests(unittest.TestCase):

    def setUp(self) -> None:
        self.consumer_phone = '123456789'




if __name__ == '__main__':
    unittest.main()