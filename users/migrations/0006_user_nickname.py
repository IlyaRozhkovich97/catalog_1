# Generated by Django 5.0.6 on 2024-06-24 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='никнейм'),
        ),
    ]
