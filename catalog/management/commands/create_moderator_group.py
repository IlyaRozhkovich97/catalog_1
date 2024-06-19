# users/management/commands/create_moderator_group.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Create moderator group with specific permissions'

    def handle(self, *args, **kwargs):
        moderator_group, created = Group.objects.get_or_create(name='Moderators')

        # Получаем разрешения по названию
        permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Product),
            codename__in=[
                'can_unpublish_product',
                'can_edit_product_description',
                'can_edit_product_category'
            ]
        )

        # Назначаем разрешения группе
        for permission in permissions:
            moderator_group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Successfully created or updated Moderators group'))
