from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from lesson.models import Lesson


class LessonAPITestCase(APITestCase):
    def setUp(self):
        self.lesson_data = {
            'title': 'Lesson Title',
            'description': 'Lesson Description',
            'video_url' : 'https://youtube.com',
            # Add other fields as needed
        }
        self.lesson = Lesson.objects.create(**self.lesson_data)

    def test_create_lesson(self):
        url = reverse('lesson-list')
        response = self.client.post(url, self.lesson_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)  # Assuming there's an initial lesson created

    def test_retrieve_lesson(self):
        url = reverse('lesson-detail', kwargs={'pk': self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson_data['title'])

    def test_update_lesson(self):
        updated_data = {'description': 'Updated Description'}
        url = reverse('lesson-detail', kwargs={'pk': self.lesson.pk})
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.description, updated_data['description'])

    def test_delete_lesson(self):
        url = reverse('lesson-detail', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(pk=self.lesson.pk).exists())



