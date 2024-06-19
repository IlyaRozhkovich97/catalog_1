from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create moderator group with specific permissions'

    def handle(self, *args, **kwargs):
        # Создаем или получаем группу "Модераторы"
        group, created = Group.objects.get_or_create(name='Модераторы')

        # Получаем необходимые разрешения
        permissions = [
            Permission.objects.get(codename='can_unpublish_product'),
            Permission.objects.get(codename='can_change_description'),
            Permission.objects.get(codename='can_change_category'),
        ]

        # Назначаем разрешения группе
        for permission in permissions:
            group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Successfully created/updated moderator group'))
