# Generated by Django 4.1.5 on 2023-01-28 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_cart_is_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='session_id',
            field=models.CharField(default=1, max_length=100, verbose_name='ID cессии'),
            preserve_default=False,
        ),
    ]
