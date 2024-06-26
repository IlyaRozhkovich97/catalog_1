# Generated by Django 5.0.6 on 2024-06-23 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_alter_product_is_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name', 'category', 'purchase_price'], 'permissions': [('can_unpublish_product', 'Can unpublish product'), ('change_description_product', 'Can change product description'), ('change_category_product', 'Can change product category')], 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
    ]
