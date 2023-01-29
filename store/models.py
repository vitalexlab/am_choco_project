from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from products.models import Products
from store.utils import ValidatePhone


class OrderItem(models.Model):

    class Meta:
        verbose_name = 'Заказываемые товары'
        verbose_name_plural = 'Заказываемые товары'

    product = models.ForeignKey(
        Products, on_delete=models.PROTECT,
        verbose_name='Товар',
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
        if self.product:
            cost = self.product.price * self.quantity * (100 - self.sale) / 100
        else:
            cost = 0
        return cost

    def __str__(self):
        return f'{self.product} - {self.quantity} шт. ({int(self.get_cost// 100)}.{int(self.get_cost % 100)} руб.)'


class Cart(models.Model):

    class Meta:
        verbose_name = 'Корзина заказов'
        verbose_name_plural = 'Корзины заказов'

    customer_phone = models.CharField(
        max_length=13, verbose_name='Телефон покупателя',
        null=False, blank=False
    )
    customer_wishes = models.TextField(
        verbose_name='Пожелания покупателя', null=True, blank=True
    )
    order_item = models.ManyToManyField(
        OrderItem, related_name='orderitem',verbose_name='Заказ товара'
    )
    cart_sale = models.PositiveIntegerField(
        default=0, verbose_name='Скидка на корзину, %', validators=[
            MaxValueValidator(100), MinValueValidator(0)
        ]
    )
    is_confirmed = models.BooleanField(
        verbose_name='Подтвержден',
        default=False, null=False, blank=False
    )
    is_completed = models.BooleanField(
        verbose_name='Выполнен',
        default=False, null=False, blank=False
    )
    time_created = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        total_cost = sum(
            [order_item.get_cost for order_item in self.order_item.all()]
        )
        return total_cost

    total_cost.fget.short_description = 'Сумма корзины, коп.'

    def __str__(self):
        return f'{self.customer_phone}/ на сумму ({self.total_cost // 100} руб. {int(self.total_cost % 100)} коп.)'

    def clean(self):
        phone = ValidatePhone(str(self.customer_phone))
        if not phone.validate():
            raise ValidationError({'consumer_phone': self.customer_phone})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Cart, self).save(*args,**kwargs)
