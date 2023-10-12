from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from lesson.models import Lesson, Subscrib
from lesson.paginators import LessonPaginator
from lesson.permissions import IsOwner, IsModerator, IsMember
from lesson.serliazers import LessonSerializer, SubscribSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsMember]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsMember]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class SubscribViewSet(viewsets.ModelViewSet):
    """ ViewSet для подписок """

    serializer_class = SubscribSerializer
    queryset = Subscrib.objects.all()
    lookup_field = 'id'

    def perform_create(self, serializer):
        """ Сохранение подписки True или False для определенного пользователя"""

        new_subscription = serializer.save(user=self.request.user)  # Привязка
        new_subscription.save()  # Сохраняем