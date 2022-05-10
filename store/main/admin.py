from django.contrib import admin
from .models import Products, Types, Colors, Category, Gender


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_available', 'product_photo', 'product_price')
    prepopulated_fields = {"slug": ("product_name",)}


admin.site.register(Products, ProductsAdmin)
admin.site.register(Types)
admin.site.register(Colors)
admin.site.register(Category)
admin.site.register(Gender)
