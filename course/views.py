from builtins import *

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from course.models import Course, Subscrip
from course.paginators import CoursePaginator
from course.serliazers import CourseSerializer, SubscripSerializer
from user.models import UserRoles


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CoursePaginator

    @action(detail=False, methods=['post'])
    def custom_create(self, request, *args, **kwargs):
        if request.user.role == UserRoles.MODERATOR:
            return Response({"detail": "Модераторы не могут создавать курсы."})
        return super().create(request, *args, **kwargs)

    def custom_destroy(self, request, *args, **kwargs):
        if request.user.role == UserRoles.MODERATOR:
            return Response({"detail": "Модераторы не могут удалять курсы."})
        return super().destroy(request, *args, **kwargs)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """ ViewSet для подписок """

    serializer_class = SubscripSerializer
    queryset = Subscrip.objects.all()
    lookup_field = 'id'

    def perform_create(self, serializer):
        """ Сохранение подписки True или False для определенного пользователя"""

        new_subscription = serializer.save(user=self.request.user)  # Привязка
        new_subscription.save()  # Сохраняем
