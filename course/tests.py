from builtins import list

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from course.models import Course, Subscrip
from user.models import User


class SubscripTestCase(APITestCase):
    """ Тестирование подписки на курс """

    def setUp(self):
        """ Тестовые настройки создание экземпляров моделей """

        self.user = User.objects.create(email='admin@mail.ru', password='admin', is_superuser=True)
        self.token = f'Bearer {AccessToken.for_user(self.user)}'
        self.course = Course.objects.create(name_courses="TEST", description_courses="TEST", owner=self.user)

        self.data = {
            'user': self.user,
            'course': self.course,
        }

        self.subscription = Subscrip.objects.create(**self.data)

    def test_create_subscription(self):
        """ Тестирование подписки на курс """

        expected_data = {
            'user': self.user.pk,
            'course': self.course.pk,
            'subscribed': True
        }

        response = self.client.post(
            reverse('course:subscrip-list'),
            data=expected_data,
            HTTP_AUTHORIZATION=self.token
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

        expected_data = {
            'user': self.user.pk,
            'course': self.course.pk,
            'subscribed': False
        }

        response = self.client.patch(
            reverse('course:subscrip-detail', kwargs={'id': self.subscription.pk}),
            data=expected_data,
            HTTP_AUTHORIZATION=self.token
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
            HTTP_AUTHORIZATION=self.token
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
            reverse('course:subscrip-detail', kwargs={'id': self.subscription.pk}),
            HTTP_AUTHORIZATION=self.token
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
            reverse('course:subscrip-detail', kwargs={'id': self.subscription.pk}),
            HTTP_AUTHORIZATION=self.token
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
