from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from products.models import Products


class Order(models.Model):

    class Meta:
        verbose_name = 'Детали заказа'
        verbose_name_plural = 'Детали заказа'

    consumer_phone = models.CharField(
        max_length=13, verbose_name='Телефон покупателя'
    )
    date_time_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заказ №{self.id}/ Покупатель {self.consumer_phone}'


class OrderItem(models.Model):

    class Meta:
        verbose_name = 'Заказываемые товары'
        verbose_name_plural = 'Заказываемые товары'

    product = models.ForeignKey(
        Products, on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name='Товар',
    )
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name='Детали заказа'
    )
    quantity = models.IntegerField(default=0, null=True, blank=True,
                                   verbose_name='Количество, шт.')
    time_added = models.DateTimeField(auto_now_add=True)
    sale = models.PositiveIntegerField(
        verbose_name='Cкидка',
        default=0, validators=[MaxValueValidator(100), MinValueValidator(0)]
    )

    @property
    def get_cost(self):
        cost = self.product.price * self.quantity * (100 - self.sale) / 100
        return cost

    def __str__(self):
        return f'{self.product} - {self.quantity} шт. ({int(self.get_cost// 100)}.{int(self.get_cost % 100)} руб.)'


class Cart(models.Model):

    class Meta:
        verbose_name = 'Корзина заказов'
        verbose_name_plural = 'Корзины заказов'

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name='Данные заказа',
        blank=False, null=False
    )
    order_item = models.ManyToManyField(
        OrderItem, related_name='orderitem',verbose_name='Заказ товара'
    )
    cart_sale = models.PositiveIntegerField(
        default=0, verbose_name='Скидка на корзину, %', validators=[
            MaxValueValidator(100), MinValueValidator(0)
        ]
    )
    total_cost = models.PositiveIntegerField(
        default=0, verbose_name='Стоимость корзины, коп.', validators=[
            MinValueValidator(1)
        ]
    )
    is_completed = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return f'{self.order}/{self.order_item} ({self.total_cost} коп.)'
