from builtins import *

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from course.models import Course, Subscrip
from user.models import User


class SubscripTestCase(APITestCase):

    def setUp(self):
        self.course = Course.objects.create(
            title='TestCourse',
            description='Test',
            #user=self.user
        )

        self.user = User.objects.create(
            email='admin@mail.ru',
            password='admin',
            is_superuser=True
        )

        self.data = {
            'user': self.user,
            'course': self.course,
        }
        self.subscription = Subscrip.objects.create(**self.data)

        self.client.force_authenticate(user=self.user)

    def test_create_subscription(self):
        """ Тестирование подписки на курс """

        data = {
            'user': self.user.pk,
            'course': self.course.pk,
            'subscribed': True
        }

        response = self.client.post(
            reverse('course:subscrip-list'),
            data=data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Subscrip.objects.all().count(),
            2
        )

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "subscribed": True,
                "user": self.user.pk,
                "course": self.course.pk
            }
        )

    def test_unsubscribe(self):
        """ Тестирование отписки на курс """

        data = {
            'user': self.user.pk,
            'course': self.course.pk,
            'subscribed': False
        }

        response = self.client.patch(
            reverse('course:subscrip-detail', kwargs={'id': self.subscription.pk}),
            data=data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            Subscrip.objects.all().count(),
            1
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.subscription.pk,
                "subscribed": False,
                "user": self.user.pk,
                "course": self.course.pk
            }
        )

    def test_list_subscription(self):
        """ Тестирование списка подписок """

        response = self.client.get(
            reverse('course:subscrip-list'),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            Subscrip.objects.all().count(),
            1
        )

    def test_subscription_retrieve(self):
        """ Тестирование вывода одной подписки """

        response = self.client.get(
            reverse('course:subscrip-detail', kwargs={'id': self.subscription.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.subscription.pk,
                "subscribed": False,
                "user": self.user.pk,
                "course": self.course.pk
            }
        )

    def test_subscription_destroy(self):
        """ Тестирование удаления подписки """

        response = self.client.delete(
            reverse('course:subscrip-detail', kwargs={'id': self.subscription.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            list(Subscrip.objects.all()),
            []
        )

    def tearDown(self):
        self.user.delete()
        self.course.delete()
        self.subscription.delete()
