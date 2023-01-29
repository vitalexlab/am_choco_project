import json

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
        # Common variables
        self.endpoint = 'http://127.0.0.1:8000/store/cart/'
        self.pathname = 'cart-detail'
        # Cart variables
        self.cust_phone = '+375447192042'
        self.wishes = 'some wishes'
        self.cart_sale = 0
        self.session_id = hash(timezone.now())
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

    def get_response(self, cart_id: str):
        url = self.endpoint + cart_id + '/'
        return self.client.get(url)

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

    def create_cart_obj(self):
        test_cart = Cart.objects.create(
            customer_phone=self.cust_phone, customer_wishes=self.wishes,
            cart_sale=0, is_completed=False, session_id=self.session_id
        )
        return test_cart

    def test_get_detail_cart(self):
        """Ensure that we can show a cart"""
        cart = self.create_cart_obj()
        response = self.get_response(str(cart.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cart.cart_sale, 0)
        self.assertNotEqual(cart.is_completed, True)
        self.assertEqual(cart.customer_phone, self.cust_phone)

    def test_create_detail_cart(self):
        post_data = {
            "order": {
                "customer_phone": "+375296217431"
            },
            "order_item": [],
        }
        json_post_data = json.dumps(post_data)
        response = self.client.post(
            path=self.endpoint, data=json_post_data, content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
