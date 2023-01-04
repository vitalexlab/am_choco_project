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
