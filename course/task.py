from celery import shared_task
from django.core.mail import send_mail
from .models import Subscrip, Course


@shared_task
def send_subscription_notification(course_id):
    try:
        course = Course.objects.get(id=course_id)
        subscribers = Subscrip.objects.filter(course=course, subscribed=True)

        for subscriber in subscribers:
            send_mail(
                'Уведомление об обновлении курса',
                f'Курс {course.title} был обновлен.',
                'your_email@example.com',
                [subscriber.user.email],
                fail_silently=False,
            )

    except Course.DoesNotExist:
        pass  # Обработка отсутствия курса с данным ID
