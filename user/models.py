from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=30, verbose_name='почта', unique=True)
    phone = models.CharField(max_length=10, verbose_name='телефон')
    city = models.CharField(max_length=20, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(upload_to='user', verbose_name='аватарка', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}, {self.phone}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
