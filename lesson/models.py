from django.db import models

from course.models import Course

NULLABLE = {'blank': True, 'null': True}


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='static/lesson', verbose_name='Превью')
    video_url = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)
    course_title = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Название курса', null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
