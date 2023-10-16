from rest_framework import serializers

from lesson.models import Lesson
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