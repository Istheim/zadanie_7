from rest_framework import serializers

from lesson.models import Lesson, Subscrib
from lesson.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            UrlValidator(fields=['title', 'description', 'video_url']),
            serializers.UniqueTogetherValidator(fields=['title', 'description', 'video_url'],
                                                queryset=Lesson.objects.all())
        ]


class SubscribSerializer(serializers.ModelSerializer):
    """ Сериализотор подписок(подписан или нет) """

    class Meta:
        model = Subscrib
        fields = '__all__'