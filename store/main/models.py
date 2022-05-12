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
    product_price = models.CharField(max_length=50, null=True)
    product_available = models.DecimalField(max_digits=10, decimal_places=3)
    product_type = models.ForeignKey(Types, related_name="products", on_delete=models.CASCADE, null=True)
    product_color = models.ForeignKey(Colors, related_name="products", on_delete=models.CASCADE, null=True)
    product_gender = models.ForeignKey(Gender, related_name="products", on_delete=models.CASCADE, null=True)
    product_category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('product_name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.pk})

    def __str__(self):
        return self.product_name
