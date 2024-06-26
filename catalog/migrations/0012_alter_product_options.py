# Generated by Django 5.0.6 on 2024-06-19 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_alter_product_is_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name', 'category', 'purchase_price'], 'permissions': [('can_unpublish_product', 'Can unpublish product'), ('can_change_product_description', 'Can change product description'), ('can_change_product_category', 'Can change product category')], 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
    ]
