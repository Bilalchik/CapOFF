from django.db import models
from django.conf import settings

from .choices import BannerLocationEnum


class Category(models.Model):
    title = models.CharField(max_length=123)

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=123)
    logo = models.ImageField(upload_to='media/brand_logos')

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=123)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brands = models.ManyToManyField(Brand)
    description = models.TextField(blank=True, null=True)
    cover = models.ImageField(upload_to='media/product_covers')
    old_price = models.DecimalField(decimal_places=2, max_digits=12)
    new_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Banner(models.Model):
    title = models.CharField(max_length=123)
    description = models.TextField(blank=True, null=True)
    cover = models.ImageField(upload_to='media/banner_covers')
    location = models.CharField(max_length=15, choices=BannerLocationEnum.choices)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=123)

    def __str__(self):
        return self.title


class Storage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='storages')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.product} -->{self.size}({self.quantity}))'


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(decimal_places=2, max_digits=12, default=0)

    def __str__(self):
        return f"{self.user}"


class BasketItems(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.basket.user}"
