# Generated by Django 4.0.4 on 2022-05-22 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Элемент заказа', 'verbose_name_plural': 'Элементы заказа'},
        ),
        migrations.AlterModelOptions(
            name='products',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AlterModelOptions(
            name='shippingaddress',
            options={'verbose_name': 'Адрес достаки', 'verbose_name_plural': 'Адреса доставки'},
        ),
    ]
