from django.urls import reverse

from products.models import Category, ProductTypes, Products
from store.models import OrderItem, Cart


def get_url_from_namespace(pathname: str):
    url = reverse(pathname)
    return url


def get_cart(
    customer_phone: str, customer_wishes: str,
    cart_sale: int
):
    test_cart = Cart.objects.create(
        customer_phone=customer_phone, customer_wishes=customer_wishes,
        cart_sale=cart_sale
    )
    return test_cart


def get_orderitem(
        product: Products, quantity: int, sale: int
):
    return OrderItem.objects.create(
        product=product, quantity=quantity, sale=sale
    )


def get_product_type(title:str) -> ProductTypes:
    return ProductTypes.objects.create(title=title)


def get_product(
        title: str, category: Category, product_type: ProductTypes,
        description: str, composition: str, price: int
) -> Products:
    obj = Products.objects.create(
        title=title, category=category, description=description,
        composition=composition, price=price
    )
    obj.product_type.add(product_type)
    return obj


def get_category(name: str) -> Category:
    return Category.objects.create(name=name)
