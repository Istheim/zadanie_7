from rest_framework import serializers

from course.models import Course, Subscrip
from course.validators import UrlValidator
from lesson.serliazers import LessonSerializer
from user.serliazers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    lesson = LessonSerializer(many=True, read_only=True)

    def get_num_lessons(self, obj):
        return obj.lesson_set.all().count()  # Возвращает количество уроков

    class Meta:
        model = Course
        fields = '__all__'
        validators = [
            UrlValidator(fields=['title', 'description']),
            serializers.UniqueTogetherValidator(fields=['title', 'description'],
                                                queryset=Course.objects.all())
        ]


class SubscripSerializer(serializers.ModelSerializer):
    """ Сериализотор подписок(подписан или нет) """

    class Meta:
        model = Subscrip
        fields = '__all__'