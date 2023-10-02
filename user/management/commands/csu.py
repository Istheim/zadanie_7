from django.core.management import BaseCommand

from user.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.object.create(
            email='admin@mail.ru',
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )
        user.set_password('asdasda12')
        user.save()