from django.conf import settings
from django.db import models

from course.models import Course
from user.models import User

NULLABLE = {'blank': True, 'null': True}


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='static/lesson', verbose_name='Превью', **NULLABLE)
    video_url = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)
    course_title = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Название курса', null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Subscrib(models.Model):
    """ Класс для модели подписок"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name="Пользователь", )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    subscribed = models.BooleanField(default=False, verbose_name='Статус подписки')

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'