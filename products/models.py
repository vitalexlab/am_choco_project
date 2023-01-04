from django.db import models
from django.template.defaultfilters import slugify # new


class Category(models.Model):
    """Categories

    The category is used to sort products
    """
    name = models.CharField(
        max_length=50,
        verbose_name='Название категории',
        db_index=True
    )
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"


class ProductTypes(models.Model):
    title = models.CharField(max_length=50, verbose_name='Тип товара')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип товара'
        verbose_name_plural = 'Типы товаров'


class Products(models.Model):
    title = models.CharField(
        max_length=150, verbose_name='Название товара', db_index=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT
    )
    product_type = models.ManyToManyField(
        ProductTypes, related_name='product_type',
        verbose_name='Тип товара'
    )
    image = models.ImageField(verbose_name='Изоображениe товара')
    description = models.TextField(verbose_name='Описание товара')
    composition = models.TextField(verbose_name='Cостав')

    def __str__(self):
        return f'{self.title} - {self.category}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
