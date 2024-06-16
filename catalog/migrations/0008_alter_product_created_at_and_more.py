# Generated by Django 5.0.6 on 2024-06-07 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_alter_version_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания'),
        ),
        migrations.AlterField(
            model_name='product',
            name='purchase_price',
            field=models.IntegerField(verbose_name='цена продажи'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='дата и время последнего изменения'),
        ),
        migrations.AlterField(
            model_name='version',
            name='is_current',
            field=models.BooleanField(default=False, verbose_name='текущая версия'),
        ),
        migrations.AlterField(
            model_name='version',
            name='version_name',
            field=models.CharField(max_length=100, verbose_name='название версии'),
        ),
        migrations.AlterField(
            model_name='version',
            name='version_number',
            field=models.CharField(max_length=100, verbose_name='номер версии'),
        ),
    ]