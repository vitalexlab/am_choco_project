import unittest

from django.core.exceptions import ValidationError

from products.models import Category, Products, ProductTypes
from store.models import OrderItem, Order


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


def get_order_item(
        item: Products, count: int, data: Order):
    return OrderItem.objects.create(
        product=item, quantity=count, order=data
    )


def get_order(phone: str):
    return Order.objects.create(consumer_phone=phone)

#
# class OrderItemTests(unittest.TestCase):
#
#     def setUp(self):
#         self.product_name1 = 'Product1'
#         self.product_name2 = 'Product2'
#
#         self.category_name_1 = 'Category1212131'
#         self.category_name_2 = 'Category212333'
#
#         self.desc1 = 'desk1'
#         self.desc2 = 'desk2'
#
#         self.composition1 = 'comp1'
#         self.composition2 = 'comp2'
#
#         self.product_type_title1 = 'Pt1123123'
#         self.product_type_title2 = 'Pt212312321'
#
#         self.category1 = get_category(name=self.category_name_1)
#         self.category2 = get_category(name=self.category_name_2)
#
#         self.product_type1 = ProductTypes.objects.create(
#             title=self.product_type_title1
#         )
#         self.product_type2 = ProductTypes.objects.create(
#             title=self.product_type_title2
#         )
#
#         self.phone1 = '+375296217433'
#         self.phone2 = '+375447192042'
#
#         self.product1 = get_product(
#             title=self.product_name1, category=self.category1,
#             description=self.desc1, price=500, comp=self.composition1,
#             product_type=self.product_type1
#         )
#         self.product2 = get_product(
#             title=self.product_name2, category=self.category2,
#             description=self.desc2, price=1000, comp=self.composition2,
#             product_type=self.product_type2
#         )
#
#         self.product_count1 = 5
#         self.product_count2 = 10
#
#         self.sale1 = 0
#         self.sale2 = 50
#         self.sale3 = 110
#         self.sale4 = -10
#
#         self.order1 = get_order('+375296217433')
#         self.order2 = get_order('+375447192042')
#
#         self.order_item1 = get_order_item(
#             item=self.product1, count=self.product_count1, data=self.order1,
#
#         )
#         self.order_item2 = get_order_item(
#             item=self.product2, count=self.product_count2, data=self.order2,
#         )
#
#     def test_orderitem_with_created_item(self):
#         self.assertEqual(self.order_item1.product.title, self.product1.title)
#         self.assertEqual(self.order_item2.product.title, self.product2.title)
#
#     def test_orderitem_with_count(self):
#         self.assertEqual(self.order_item1.quantity, self.product_count1)
#         self.assertEqual(self.order_item2.quantity, self.product_count2)
#
#     def test_orderitem_order_data(self):
#         pass
#
#     def test_orderitem_sale(self):
#         pass
#
#     def test_orderitem_cost(self):
#         total1 = self.product_count1 * self.product1.price
#         self.assertTrue(isinstance(total1, int))
#         total2 = self.product_count2 * self.product2.price
#         self.assertTrue(isinstance(total2, int))
#         self.assertEqual(self.order_item1.get_cost, total1)
#         self.assertEqual(self.order_item2.get_cost, total2)
#
#     def tearDown(self):
#         self.product1.delete()
#         self.product2.delete()
#         self.category1.delete()
#         self.category2.delete()
#         self.product_type1.delete()
#         self.product_type2.delete()


class OrderTests(unittest.TestCase):

    def setUp(self) -> None:
        self.phone1 = '+375296217433'
        self.phone2 = '+375446217433'

    def test_order_creation_positive(self):
        """Positive order creation test

        We test that phone has allowed form
        """

        self.assertEqual(
            Order.objects.create(consumer_phone=self.phone1).consumer_phone,
            self.phone1
        )
        self.assertEqual(
            Order.objects.create(consumer_phone=self.phone2).consumer_phone,
            self.phone2
        )

    def test_order_creation_negative(self):
        """Negative order creation test

        We test that phone won't be created with an invalid number
        """
        self.assertRaises(ValidationError, Order.objects.create(consumer_phone='12345'))


if __name__ == '__main__':
    unittest.main()
