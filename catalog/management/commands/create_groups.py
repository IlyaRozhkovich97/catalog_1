from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create moderator group with specific permissions'

    def handle(self, *args, **kwargs):
        # Создаем группу модераторов
        moderator_group, created = Group.objects.get_or_create(name='Moderator')

        # Определяем необходимые права
        permissions = [
            Permission.objects.get(codename='can_unpublish_product'),
            Permission.objects.get(codename='change_description_product'),
            Permission.objects.get(codename='change_category_product'),
        ]

        # Назначаем права группе
        for permission in permissions:
            moderator_group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Successfully created Moderator group with specific permissions'))
