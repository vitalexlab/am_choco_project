import json

from rest_framework import status
from rest_framework.test import APITestCase

from store.models import OrderItem
from store.tests.utils import (
    get_product, get_category, get_product_type, get_orderitem
)


class OrderItemTest(APITestCase):

    def setUp(self) -> None:
        # Common data
        self.endpoint = 'http://127.0.0.1:8000/store/order-item/'
        # Product data
        self.prod_name = 'Product'
        self.prod_desc = 'Description'
        self.prod_comp = 'Composition'
        self.prod_price = 500
        # Category data
        self.cat_name = 'Category'
        # ProductType data
        self.pt_title = 'Product Type'
        # OrderItem
        self.count = 10
        self.order_sale = 0

    def test_create_orderitem(self):
        category_obj = get_category(name=self.cat_name)
        product_type = get_product_type(
            title=self.pt_title
        )
        product = get_product(
            title=self.prod_name, category=category_obj,
            product_type=product_type, description=self.prod_desc,
            composition=self.prod_comp, price=self.prod_price
        )

        post_data = {
            'product_id': product.id,
            'quantity': self.count
        }
        post_data = json.dumps(post_data)
        response = self.client.post(
            path=self.endpoint, data=post_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        count_from_response = response.data.get('quantity')
        self.assertEqual(count_from_response, self.count)
        obj_name_from_response = response.data.get('product').get('title')
        self.assertEqual(obj_name_from_response, product.title)
        sale_from_response = response.data.get('sale')
        self.assertEqual(sale_from_response, 0)

    def test_get_order_item(self):
        category_obj = get_category(name=self.cat_name)
        product_type = get_product_type(
            title=self.pt_title
        )
        product = get_product(
            title=self.prod_name, category=category_obj,
            product_type=product_type, description=self.prod_desc,
            composition=self.prod_comp, price=self.prod_price
        )

        order_item = get_orderitem(
            product=product, quantity=self.count, sale=self.order_sale
        )
        url = self.endpoint + str(order_item.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        quantity_response = response.data.get('quantity')
        self.assertEqual(quantity_response, self.count)
        product_response = response.data.get('product')
        product_title_response = product_response.get('title')
        self.assertEqual(product_title_response, product.title)
        product_id_response = product_response.get('id')
        self.assertEqual(product_id_response, product.id)
        price_response = product_response.get('price')
        self.assertEqual(price_response, product.price)
        self.assertEqual(response.data.get('sale'), 0)

    def test_update_order_item_is_forbidden(self):
        category_obj = get_category(name=self.cat_name)
        product_type = get_product_type(
            title=self.pt_title
        )
        product = get_product(
            title=self.prod_name, category=category_obj,
            product_type=product_type, description=self.prod_desc,
            composition=self.prod_comp, price=self.prod_price
        )

        post_data = {
            'product_id': product.id,
            'quantity': self.count
        }
        post_data = json.dumps(post_data)
        response_post = self.client.post(
            path=self.endpoint, data=post_data,
            content_type='application/json'
        )
        order_item_id = response_post.data.get('id')
        put_data = {
            'product_id': product.id,
            "quantity": 17
        }
        put_data = json.dumps(put_data)
        url = self.endpoint + str(order_item_id) + '/'
        response = self.client.put(
            path=url, data=put_data, content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def patch_order_item(self):
        category_obj = get_category(name=self.cat_name)
        product_type = get_product_type(
            title=self.pt_title
        )
        product = get_product(
            title=self.prod_name, category=category_obj,
            product_type=product_type, description=self.prod_desc,
            composition=self.prod_comp, price=self.prod_price
        )

        post_data = {
            'product_id': product.id,
            'quantity': self.count
        }
        post_data = json.dumps(post_data)
        response_post = self.client.post(
            path=self.endpoint, data=post_data,
            content_type='application/json'
        )
        order_item_id = response_post.data.get('id')
        patch_data = {
            "quantity": 17
        }
        patch_data = json.dumps(patch_data)
        url = self.endpoint + str(order_item_id) + '/'
        response = self.client.patch(
            path=url, data=patch_data, content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        product_id_test = 3
        patch_data2 = {
            'product_id': product_id_test,
            "quantity": 13
        }
        url = self.endpoint + str(order_item_id) + '/'
        response = self.client.patch(
            path=url, data=patch_data2, content_type='application/json'
        )

        self.assertNotEqual(
            response.data.get('product'), product_id_test
        )
        self.assertEqual(
            response.data.get('product_id'), product.id
        )
        product_id_test = 'qw'
        patch_data2 = {
            'product_id': product_id_test,
            "quantity": 13
        }
        url = self.endpoint + str(order_item_id) + '/'
        response = self.client.patch(
            path=url, data=patch_data2, content_type='application/json'
        )
        self.assertTrue(
            isinstance(
                response.data.get('product_id'), int
            )
        )

    def test_destroy_orderitem(self):
        category_obj = get_category(name=self.cat_name)
        product_type = get_product_type(
            title=self.pt_title
        )
        product = get_product(
            title=self.prod_name, category=category_obj,
            product_type=product_type, description=self.prod_desc,
            composition=self.prod_comp, price=self.prod_price
        )

        post_data = {
            'product_id': product.id,
            'quantity': self.count
        }
        post_data = json.dumps(post_data)
        response_post = self.client.post(
            path=self.endpoint, data=post_data,
            content_type='application/json'
        )
        order_item_id = response_post.data.get('id')
        url = self.endpoint + str(order_item_id) + '/'
        response_delete = self.client.delete(
            path=url
        )
        self.assertEqual(
            response_delete.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(response_delete.data, None)
