from django.db import models

from course.models import Course
from lesson.models import Lesson
from user.models import User

NULLABLE = {'blank': True, 'null': True}


class Payment(models.Model):
    CASH = 'CASH'
    BANK_TRANSFER = 'BANK_TRANSFER'

    PAYMENT_METHOD_CHOICES = [
        (CASH, 'Наличные'),
        (BANK_TRANSFER, 'Перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    data_pay = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    pay_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплата курса', **NULLABLE)
    pay_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплата урока', **NULLABLE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.user}, {self.amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


