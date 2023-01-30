from rest_framework import status
from rest_framework.response import Response


def get_valid_cart_id_or_400(request) -> [int, Response]:
    """Returns either cart_id or 400 BAD REQUEST"""

    cart_id = request.session.get('cart_id', False)
    if not isinstance(cart_id, int):
        return Response(
            {
                'error': 'An incorrect cart_id type: must be int'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    return cart_id


def get_valid_order_item_pk_or_400(kwargs: dict) -> [int, Response]:
    """Returns either order_item_pk or 400 BAD REQUEST"""

    try:
        order_item_pk = int(kwargs.get('pk'))
    except ValueError:
        return Response(
            {'error': 'order_item_pk must be an integer'},
            status=status.HTTP_400_BAD_REQUEST
        )
    return order_item_pk
