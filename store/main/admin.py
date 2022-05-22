from django.contrib import admin
from .models import Products, Types, Colors, Category, Gender, ShippingAddress, Order, OrderItem


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_description', 'product_available', 'product_photo', 'product_price')
    list_editable = ('product_description', 'product_price', )
    prepopulated_fields = {"slug": ("product_description",)}


admin.site.register(Products, ProductsAdmin)
admin.site.register(Types)
admin.site.register(Colors)
admin.site.register(Category)
admin.site.register(Gender)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)


admin.site.site_header='Qazaq Republic'
