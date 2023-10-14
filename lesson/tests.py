from builtins import list

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from lesson.models import Lesson, Subscrib
from user.models import User
from course.models import Course


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='admin@mail.com', password='admin', is_superuser=True)
        self.token = f'Bearer {AccessToken.for_user(self.user)}'
        self.course = Course.objects.create(title="TestCourse", description="TestCourseDescription")
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='TestLesson',
            description='TestLessonDescription',
            video_url='https://youtube.com',
        )

    def test_lesson_create(self):
        expected_data = {
            "course": self.course.pk,
            "title": "TEST1",
            "description": "TEST1",
            "video_url": "https://youtube.com",
        }
        response = self.client.post(
            reverse('lesson-create'),
            data=expected_data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "course": self.course.pk,
                "title": "TEST1",
                "description": "TEST1",
                "video_url": self.lesson.video_url,
            }
        )

    def test_lesson_list(self):
        response = self.client.get(
            reverse('lesson-list'),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.pk,
                        "course": self.course.pk,
                        "title": self.lesson.title,
                        "description": self.lesson.description,
                        "video_url": self.lesson.video_url,
                    }
                ]
            }
        )

    def test_lesson_retrieve(self):
        response = self.client.get(
            reverse('lesson-get', kwargs={'pk': self.lesson.pk}),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.pk,
                "course": self.course.pk,
                "title": self.lesson.title,
                "description": self.lesson.description,
                "video_url": self.lesson.video_url,
            }
        )

    def test_lesson_update(self):
        expected_data = {
            "course": self.course.pk,
            "title": "TEST2",
            "description": "TEST2",
            "video_url": "https://youtube.com/test2/",
        }
        response = self.client.patch(
            reverse('lesson-update', kwargs={'pk': self.lesson.pk}),
            data=expected_data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.pk,
                "course": self.course.pk,
                "title": "TEST2",
                "description": "TEST2",
                "video_url": "https://youtube.com/test2/",
            }
        )

    def test_lesson_destroy(self):
        response = self.client.delete(
            reverse('lesson-delete', kwargs={'pk': self.lesson.pk}),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(list(Lesson.objects.all()), [])

    def tearDown(self):
        self.user.delete()
        self.course.delete()
        self.lesson.delete()


class SubscribTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='admin@mail.com', password='admin', is_superuser=True)
        self.token = f'Bearer {AccessToken.for_user(self.user)}'
        self.course = Course.objects.create(title="TestCourse", description="TestCourseDescription")
        self.subscrib = Subscrib.objects.create(
            user=self.user,
            course=self.course,
            subscribed=False
        )

    def test_create_subscription(self):
        expected_data = {
            'user': self.user.pk,
            'course': self.course.pk,
            'subscribed': True
        }
        response = self.client.post(
            reverse('subscrib-list'),
            data=expected_data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscrib.objects.all().count(), 2)
        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "user": self.user.pk,
                "course": self.course.pk,
                "subscribed": True,
            }
        )

    def test_list_subscription(self):
        response = self.client.get(
            reverse('subscrib-list'),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.subscrib.pk,
                        "user": self.user.pk,
                        "course": self.course.pk,
                        "subscribed": False,
                    }
                ]
            }
        )

    def test_subscription_retrieve(self):
        response = self.client.get(
            reverse('subscrib-detail', kwargs={'pk': self.subscrib.pk}),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.subscrib.pk,
                "user": self.user.pk,
                "course": self.course.pk,
                "subscribed": False,
            }
        )

    def test_subscription_destroy(self):
        response = self.client.delete(
            reverse('subscrib-detail', kwargs={'pk': self.subscrib.pk}),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(list(Subscrib.objects.all()), [])

    def tearDown(self):
        self.user.delete()
        self.course.delete()
        self.subscrib.delete()
