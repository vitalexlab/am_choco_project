import json

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Cart
from store.tests.utils import get_cart


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

    def test_get_detail_cart(self):
        """Ensure that we can show a cart"""
        cart = get_cart(
            self.cust_phone, self.wishes, cart_sale=self.cart_sale
        )
        response = self.get_response(str(cart.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cart.cart_sale, 0)
        self.assertNotEqual(cart.is_completed, True)
        self.assertEqual(cart.customer_phone, self.cust_phone)

    def test_create_detail_cart_without_wishes(self):
        post_data = {
            "order": {
                "customer_phone": "+375296217431"
            },
        }
        json_post_data = json.dumps(post_data)
        response = self.client.post(
            path=self.endpoint, data=json_post_data, content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        response_data = response.data
        cust_wishes = response_data.get('customer_wishes')
        self.assertEqual(cust_wishes, None)
        order_item = response_data.get('order_item')
        self.assertEqual(order_item, [])
        total_cost = response_data.get('total_cost')
        self.assertEqual(total_cost, 0)
        self.assertTrue(isinstance(total_cost, int))

    def test_create_detail_cart_with_wishes(self):
        post_data = {
            "order": {
                "customer_phone": "+375296217431",
                "customer_wishes": "some data"
            },
        }
        json_post_data = json.dumps(post_data)
        response = self.client.post(
            path=self.endpoint, data=json_post_data, content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        response_data = response.data
        cust_wishes = response_data.get('customer_wishes')
        self.assertEqual(cust_wishes, 'some data')
        order_item = response_data.get('order_item')
        self.assertEqual(order_item, [])
        total_cost = response_data.get('total_cost')
        self.assertEqual(total_cost, 0)
        self.assertTrue(isinstance(total_cost, int))

    def test_create_detail_cart_with_order_items(self):
        post_data = {
            "order": {
                "customer_phone": "+375296217431",
                "customer_wishes": "some data"
            },
            "order_items": [
                {
                    "id": 1
                }
            ]
        }
        json_post_data = json.dumps(post_data)
        response = self.client.post(
            path=self.endpoint, data=json_post_data, content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        response_data = response.data
        cust_wishes = response_data.get('customer_wishes')
        self.assertEqual(cust_wishes, 'some data')
        order_item = response_data.get('order_item')
        self.assertEqual(order_item, [])
        total_cost = response_data.get('total_cost')
        self.assertEqual(total_cost, 0)
        self.assertTrue(isinstance(total_cost, int))

    def test_create_detail_cart_with_order_items_total_cost(self):
        post_data = {
            "order": {
                "customer_phone": "+375296217431",
                "customer_wishes": "some data"
            },
            "order_items": [
                {
                    "id": 1
                },
            ],
            "total_cost": 10
        }
        json_post_data = json.dumps(post_data)
        response = self.client.post(
            path=self.endpoint, data=json_post_data, content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        response_data = response.data
        cust_wishes = response_data.get('customer_wishes')
        self.assertEqual(cust_wishes, 'some data')
        order_item = response_data.get('order_item')
        self.assertEqual(order_item, [])
        total_cost = response_data.get('total_cost')
        self.assertEqual(total_cost, 0)
        self.assertTrue(isinstance(total_cost, int))

    def test_destroy_cart(self):
        cart = get_cart(self.cust_phone, self.wishes, self.cart_sale)
        url = self.endpoint + str(cart.id) + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cart.objects.filter(id=cart.id).count(), 0)
