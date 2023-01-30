# Generated by Django 4.1.5 on 2023-01-30 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitemcartrelations',
            options={'verbose_name': 'Добавление/ удаление товаров из корзины', 'verbose_name_plural': 'Добавление/ удаление товаров из корзины'},
        ),
        migrations.AlterField(
            model_name='orderitemcartrelations',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.cart', verbose_name='Корзина'),
        ),
        migrations.AlterField(
            model_name='orderitemcartrelations',
            name='order_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.orderitem', verbose_name='Заказываемые товары'),
        ),
        migrations.AlterUniqueTogether(
            name='orderitemcartrelations',
            unique_together={('order_item', 'cart')},
        ),
    ]