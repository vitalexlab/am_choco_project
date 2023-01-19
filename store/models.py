from django.db import models

from products.models import Products


class Package(models.Model):

    item = models.ForeignKey(
        Products, on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    count = models.PositiveIntegerField(
        verbose_name='Количество, шт.'
    )
    package_price = models.PositiveIntegerField(
        verbose_name='Стоимость заказа, коп.'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.item} - {self.count} шт.'


class Order(models.Model):

    consumer_phone = models.CharField(
        max_length=13, verbose_name='Телефон покупателя'
    )
    packages = models.ManyToManyField(
        Package, related_name='package',
        verbose_name='Товары в корзину'
    )
    total_order_cost = models.PositiveIntegerField(
        verbose_name="Общая стоимость корзины, коп."
    )

    class Meta:
        verbose_name = 'Корзина заказов'
        verbose_name_plural = 'Корзины заказов'

    def __str__(self):
        return f'Заказ №{self.id}/ Покупатель {self.consumer_phone}'
