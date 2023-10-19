from celery import shared_task
from django.contrib.auth.models import User
from django.utils import timezone


@shared_task
def block_inactive_users():
    # Получаем всех пользователей, которые не заходили более месяца
    threshold = timezone.now() - timezone.timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=threshold, is_active=True)

    # Блокируем каждого пользователя
    for user in inactive_users:
        user.is_active = False
        user.save()
