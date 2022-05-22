from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Types(models.Model):
    type_name = models.CharField(max_length=50)

    class Meta:
        ordering = ('type_name',)
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.type_name

    def get_absolute_url(self):
        return reverse('type', kwargs={'type_id': self.pk})


class Colors(models.Model):
    color_name = models.CharField(max_length=50)

    class Meta:
        ordering = ('color_name',)
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return self.color_name

    def get_absolute_url(self):
        return reverse('color', kwargs={'color_id': self.pk})


class Gender(models.Model):
    gender_name = models.CharField(max_length=100, db_index=True)

    class Meta:
        ordering = ('gender_name',)
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'

    def __str__(self):
        return self.gender_name

    def get_absolute_url(self):
        return reverse('gender', kwargs={'gender_id': self.pk})


class Category(models.Model):
    category_name = models.CharField(max_length=100, db_index=True)

    class Meta:
        ordering = ('category_name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})


class Products(models.Model):
    product_name = models.CharField(max_length=50, null=True)
    slug = models.SlugField(null=False, unique=False)
    product_photo = models.ImageField(null=True, blank=True, upload_to='photos/%Y/%m/%d/')
    product_description = models.CharField(max_length=1024, null=True)
    product_size = models.CharField(max_length=50)
    product_price = models.IntegerField(null=True)
    product_available = models.DecimalField(max_digits=10, decimal_places=3)
    product_type = models.ForeignKey(Types, related_name="products", on_delete=models.CASCADE, null=True)
    product_color = models.ForeignKey(Colors, related_name="products", on_delete=models.CASCADE, null=True)
    product_gender = models.ForeignKey(Gender, related_name="products", on_delete=models.CASCADE, null=True)
    product_category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE, null=True)
    digital = models.BooleanField(default=False, null=True, blank=False)

    class Meta:
        ordering = ('product_name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def get_absolute_url(self):
        return reverse('view', kwargs={'product_id': self.pk})

    def get_absolute_url2(self):
        return reverse('delete_item', kwargs={'product_id': self.pk})

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.pk)

    @property
    def shipping(self):
        shippiing = False
        orderitem = self.orderitem_set.all()
        for i in orderitem:
            if i.product.digital == False:
                shippiing = True
        return shippiing

    @property
    def get_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitem])
        return total

    @property
    def get_cart_items(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])
        return total

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.quantity * self.product.product_price
        return total

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zip_code = models.CharField(max_length=50, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Адрес достаки'
        verbose_name_plural = 'Адреса доставки'
