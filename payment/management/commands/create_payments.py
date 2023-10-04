from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.utils import timezone
from payment.models import Payment
from user.models import User
from lesson.models import Lesson
from course.models import Course
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Create random payments'

    def handle(self, *args, **kwargs):
        # Получаем всех пользователей
        users = User.objects.all()

        # Получаем все курсы и уроки
        courses = Course.objects.all()
        lessons = Lesson.objects.all()

        # Создаем случайные платежи для каждого пользователя
        for user in users:
            payment = Payment(
                user=user,
                data_pay=timezone.now(),
                pay_course=random.choice(courses) if courses else None,
                pay_lesson=random.choice(lessons) if lessons else None,
                amount=Decimal(random.uniform(10, 2000)),
                payment_method=random.choice([Payment.CASH, Payment.BANK_TRANSFER])
            )
            payment.save()


