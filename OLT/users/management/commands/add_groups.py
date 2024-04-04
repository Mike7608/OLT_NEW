from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):

    def handle(self, *args, **options):
        Group.objects.all().delete()

        # Создаем новую группу
        group_moderator_materials = Group.objects.create(name='moderator_materials')

        # Добавляем разрешения группе
        group_moderator_materials.permissions.add(
            Permission.objects.get(codename='change_course'),
            Permission.objects.get(codename='view_course'),
            Permission.objects.get(codename='change_lesson'),
            Permission.objects.get(codename='view_lesson'),
        )
