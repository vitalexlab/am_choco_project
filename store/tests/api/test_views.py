from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Category, ProductTypes, Products
from store.models import OrderItem, Cart


def get_cart_url(pathname: str):
    url = reverse(pathname)
    return url


class CartTest(APITestCase):

    def setUp(self) -> None:
        self.pathname = 'cart-detail'
        self.cust_phone = '+375447192042'
        self.wishes = 'some wishes'
        self.cart_sale = 0
        self.host = 'http://127.0.0.1:8000'
        # For a OrderItem instance creation
        self.prod_quantity5 = 5
        self.product_sale = 0
        # For a Products instance creation
        self.product_title = 'Product'
        self.desc = 'Description'
        self.comp = 'Composition'
        self.price = 5000
        # For a Category instance creation
        self.category_name = 'Category'
        # For a Product_type instance creation
        self.pt_name = 'Type'

    def create_category(self):
        return Category.objects.create(name=self.category_name)

    def create_product_type(self):
        product_type = ProductTypes.objects.create(
            title=self.pt_name
        )
        return product_type

    def create_product(self):
        product = Products.objects.create(
            title=self.product_title, category=self.create_category(),
            description=self.desc, composition=self.comp, price=self.price
        )
        product.product_type.add(self.create_product_type(), )
        return product

    def create_order_item(self):
        order_item = OrderItem.objects.create(
            product=self.create_product(), quantity=self.prod_quantity5,
            sale=self.product_sale
        )
        return order_item

    def create_cart_obj(self, session_id):
        order_item = self.create_order_item()
        test_cart = Cart.objects.create(
            customer_phone=self.cust_phone, customer_wishes=self.wishes,
            cart_sale=0, is_completed=False, session_id=session_id
        )
        test_cart.order_item.add(order_item)
        return test_cart

    def test_get_detail_cart(self):
        """Ensure that we can show a cart"""
        cart = self.create_cart_obj(session_id=hash(timezone.now()))
        url = self.host + '/store/cart/' + str(cart.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cart.cart_sale, 0)
        self.assertNotEqual(cart.is_completed, True)
        self.assertEqual(cart.customer_phone, self.cust_phone)
