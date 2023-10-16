from builtins import *

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from course.models import Course
from lesson.models import Lesson
from user.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.course = Course.objects.create(
            title='TestCourse',
            description='Test'
        )

        self.user = User.objects.create(
            email='admin@mail.ru',
            password='admin',
            is_superuser=True
        )

        self.lesson = Lesson.objects.create(
            course_title=self.course,
            title='TestLesson',
            description='TestLessonDescription',
            video_url='https://youtube.com',
            user=self.user
        )

        self.client.force_authenticate(user=self.user)

    def test_create_Lesson(self):
        """ Создание урока"""
        data = {
            "course_title": self.course.pk,
            "title": "TEST1",
            "description": "TEST1",
            "video_url": "https://youtube.com",
            "user": self.user.pk
        }

        response = self.client.post(
            reverse('lesson:lesson-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': 2, 'title': 'TEST1', 'description': 'TEST1', 'preview': None, 'video_url': 'https://youtube.com',
             'course_title': self.course.pk, 'user': self.user.pk}

        )

        self.assertTrue(
            Lesson.objects.all().count(), 2
        )

    def test_get_list(self):
        response = self.client.get(
            reverse('lesson:lesson-list')
        )
        print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_retrieve(self):
        response = self.client.get(
            reverse('lesson:lesson-get', kwargs={'pk': self.lesson.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': 5, 'title': 'TestLesson', 'description': 'TestLessonDescription', 'preview': None,
             'video_url': 'https://youtube.com', 'course_title': self.course.pk, 'user': self.user.pk}

        )

    def test_lesson_update(self):
        data = {
            "course_title": self.course.pk,
            "title": "LessonTestTitle",
            "description": "TEST2",
            "video_url": "https://youtube.com/test2/",
            "user": self.user.pk
        }

        response = self.client.patch(
            reverse('lesson:lesson-update', kwargs={'pk': self.lesson.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': 6, 'title': 'LessonTestTitle', 'description': 'TEST2', 'preview': None,
             'video_url': 'https://youtube.com/test2/', 'course_title': self.course.pk, 'user': self.user.pk}

        )

    def test_lesson_destroy(self):
        response = self.client.delete(
            reverse('lesson:lesson-delete', kwargs={'pk': self.lesson.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            list(Lesson.objects.all()),
            []
        )

    def tearDown(self):
        self.user.delete()
        self.course.delete()
        self.lesson.delete()


