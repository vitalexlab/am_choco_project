import unittest

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

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


class OrderItemTests(unittest.TestCase):

    def setUp(self):
        self.product_name = 'Product2'
        self.category_name = 'Category212333'
        self.desc = 'desk1'
        self.composition1 = 'comp1'
        self.product_type_title = 'Pt212312321'
        self.phone = '+375296217433'
        self.product_count5 = 5
        self.product_count10 = 10
        self.sale0 = 0

    def test_order_item_creation(self):
        self.category1 = get_category(name=self.category_name)
        self.assertEqual(self.category1.name, 'Category212333')
        self.product_type1 = ProductTypes.objects.create(
            title=self.product_type_title
        )
        self.assertEqual(self.product_type1.title, 'Pt212312321')
        self.product1 = get_product(
            title=self.product_name, category=self.category1,
            description=self.desc, price=500, comp=self.composition1,
            product_type=self.product_type1
        )
        self.assertEqual(self.product1.title, 'Product2')
        self.order1 = get_order(self.phone)
        self.assertEqual(self.order1.consumer_phone, '+375296217433')
        self.order_item1 = get_order_item(
            item=self.product1, count=self.product_count5, data=self.order1,
        )
        self.assertEqual(self.order_item1.product, self.product1)
        self.assertEqual(self.order_item1.quantity, 5)
        self.assertEqual(self.order_item1.order.consumer_phone, '+375296217433')

    def test_orderitem_quantity(self):
        product1 = Products.objects.get(title=self.product_name)
        order1 = Order.objects.get(consumer_phone=self.phone)
        self.order_item1 = get_order_item(
            item=product1, count=self.product_count5, data=order1,
        )
        self.assertEqual(self.order_item1.quantity, self.product_count5)
        self.order_item2 = get_order_item(
            item=product1, count=self.product_count10, data=order1
        )
        self.assertEqual(self.order_item1.quantity, self.product_count5)
        self.assertEqual(self.order_item2.quantity, self.product_count10)

    def test_orderitem_order_data(self):
        order_item_1 = OrderItem.objects.first()
        order_1 = Order.objects.get(consumer_phone=self.phone)
        self.assertEqual(order_item_1.order, order_1)
        self.assertEqual(order_item_1.order.consumer_phone, self.phone)

    def test_orderitem_sale(self):
        order_item = OrderItem.objects.first()
        self.assertEqual(order_item.sale, 0)
        order_item.sale = 10
        self.assertEqual(order_item.sale, 10)

    def test_orderitem_cost(self):
        product = Products.objects.first()
        order_item = OrderItem.objects.first()
        total1 = self.product_count5 * product.price * (
                (100 - order_item.sale) / 100
        )
        self.assertTrue(isinstance(total1, float))
        self.assertEqual(order_item.get_cost, total1)

    def test_cost_orderitem_changes_due_to_sale(self):
        product = Products.objects.first()
        order_item = OrderItem.objects.first()
        order_item.sale = 10
        total2 = self.product_count5 * product.price * (
                (100 - order_item.sale) / 100
        )
        self.assertTrue(isinstance(total2, float))
        self.assertEqual(order_item.get_cost, total2)



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

    # def test_order_creation_negative(self):
    #     """Negative order creation test
    #
    #     We test that phone won't be created with an invalid number
    #     """
    #     self.assertRaises(ValidationError, Order.objects.create(consumer_phone='12345'))


if __name__ == '__main__':
    unittest.main()
