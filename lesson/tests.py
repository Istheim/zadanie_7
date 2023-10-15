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
            course_title=self.course,
            title='TestLesson',
            description='TestLessonDescription',
            video_url='https://youtube.com',
            user=self.user
        )

    def test_lesson_create(self):
        expected_data = {
            "course_title": self.course.pk,
            "title": "TEST1",
            "description": "TEST1",
            "video_url": "https://youtube.com",
            "user": self.user.pk
        }
        response = self.client.post(
            reverse('lesson:lesson-create'),
            data=expected_data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "course_title": self.course.pk,
                "title": "TEST1",
                "description": "TEST1",
                "video_url": self.lesson.video_url,
                "preview": None,
                "user": self.user.pk
            }
        )

    def test_lesson_list(self):
        response = self.client.get(
            reverse('lesson:lesson-list'),
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
                        "course_title": self.course.pk,
                        "title": self.lesson.title,
                        "description": self.lesson.description,
                        "video_url": self.lesson.video_url,
                        "preview": None,
                        "user": self.user.pk
                    }
                ]
            }
        )

    def test_lesson_retrieve(self):
        response = self.client.get(
            reverse('lesson:lesson-get', kwargs={'pk': self.lesson.pk}),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.pk,
                "course_title": self.course.pk,
                "title": self.lesson.title,
                "description": self.lesson.description,
                "video_url": self.lesson.video_url,
                "preview": None,
                "user": self.user.pk
            }
        )

    def test_lesson_update(self):
        expected_data = {
            "course_title": self.course.pk,
            "title": "TEST2",
            "description": "TEST2",
            "video_url": "https://youtube.com/test2/",
            "preview": None,
            "user": self.user.pk
        }
        response = self.client.patch(
            reverse('lesson:lesson-update', kwargs={'pk': self.lesson.pk}),
            data=expected_data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.pk,
                "course_title": self.course.pk,
                "title": "TEST2",
                "description": "TEST2",
                "video_url": "https://youtube.com/test2/",
                "preview": None,
                "user": self.user.pk
            }
        )

    def test_lesson_destroy(self):
        response = self.client.delete(
            reverse('lesson:lesson-delete', kwargs={'pk': self.lesson.pk}),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(list(Lesson.objects.all()), [])

    def tearDown(self):
        self.user.delete()
        self.course.delete()
        self.lesson.delete()
