# Generated by Django 5.0.6 on 2024-06-04 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_version'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='version',
            options={'verbose_name': 'Версия', 'verbose_name_plural': 'Версии'},
        ),
    ]
