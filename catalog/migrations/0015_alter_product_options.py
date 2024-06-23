# Generated by Django 5.0.6 on 2024-06-21 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name', 'category', 'purchase_price'], 'permissions': [('unpublish_a_product', 'Unpublish a product'), ('change_description_product,', 'Change description product'), ('change_category_product', 'Change category product')], 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
    ]
