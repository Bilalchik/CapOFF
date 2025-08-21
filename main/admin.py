from django.contrib import admin
from .models import Brand, Category, Product, Banner, Size, Storage, Basket, BasketItems


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Banner)
admin.site.register(Size)
admin.site.register(Storage)
admin.site.register(Basket)
admin.site.register(BasketItems)
