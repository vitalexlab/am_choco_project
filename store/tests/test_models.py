import unittest

from products.models import Category, Products, ProductTypes
from store.models import OrderItem, Cart


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
        item: Products, count: int, sale: int
):
    return OrderItem.objects.create(
        product=item, quantity=count, sale=sale
    )


def get_product_type(title: str):
    return ProductTypes.objects.create(title=title)


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
        self.order_item1 = get_order_item(
            item=self.product1, count=self.product_count5, sale=0
        )
        self.assertEqual(self.order_item1.product, self.product1)
        self.assertEqual(self.order_item1.quantity, 5)

    def test_orderitem_quantity(self):
        product1 = Products.objects.get(title=self.product_name)
        self.order_item1 = get_order_item(
            item=product1, count=self.product_count5, sale=0
        )
        self.assertEqual(self.order_item1.quantity, self.product_count5)
        self.order_item2 = get_order_item(
            item=product1, count=self.product_count10, sale=0
        )
        self.assertEqual(self.order_item1.quantity, self.product_count5)
        self.assertEqual(self.order_item2.quantity, self.product_count10)


    def test_orderitem_sale(self):
        order_item = OrderItem.objects.first()
        self.assertEqual(order_item.sale, 0)
        order_item.sale = 10
        self.assertEqual(order_item.sale, 10)

    def test_orderitem_cost(self):
        product = Products.objects.first()
        order_item = OrderItem.objects.get(product=product)
        total1 = order_item.quantity * product.price * (
                (100 - order_item.sale) / 100
        )
        self.assertTrue(isinstance(total1, float))
        self.assertEqual(order_item.get_cost, total1)

    def test_cost_orderitem_changes_due_to_sale(self):
        product = Products.objects.first()
        order_item = OrderItem.objects.get(product=product)
        order_item.sale = 10
        total2 = order_item.quantity * product.price * (
                (100 - order_item.sale) / 100
        )
        self.assertTrue(isinstance(total2, float))
        self.assertEqual(order_item.get_cost, total2)


class CartTests(unittest.TestCase):

    def setUp(self) -> None:
        self.phone = '+375446875243'
        self.cart_sale = 10
        self.total_cost = 10
        self.status = True
        self.count = 2
        self.category_title = 'title'
        self.desc = 'some desc'
        self.prod_price = 100
        self.comp = 'some composition'
        self.pt_title = 'title2'

    def test_cart_creation_positive(self):
        category = get_category(
            name='category'
        )
        product_type = get_product_type(title=self.pt_title)
        product = get_product(
            title=self.category_title, category=category,
            description=self.desc, price=self.prod_price,
            comp=self.comp, product_type=product_type
        )
        order_item = get_order_item(
            item=product, count=self.count, sale=0,
        )
        cart = Cart.objects.create(
            customer_phone='+375296217433', is_completed=self.status
        )
        cart.order_item.add(order_item)
        self.assertEqual(cart.customer_phone, '+375296217433')

    def test_cart_is_completed(self):
        cart = Cart.objects.get(customer_phone='+375296217433')
        self.assertEqual(cart.is_completed, True)

    def test_cart_totalcost(self):
        cart = Cart.objects.get(customer_phone='+375296217433')
        item_cost = 0
        for item in cart.order_item.all():
            product_quantity = item.quantity
            product_price = item.product.price
            item_sale = item.sale
            item_cost += product_quantity * product_price * (100 - item_sale) / 100
        self.assertEqual(cart.total_cost, item_cost)


if __name__ == '__main__':
    unittest.main()
