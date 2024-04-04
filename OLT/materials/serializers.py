from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import VideoValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoValidator(field='url_video')]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    count_lessons = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'title', 'pict', 'description', 'lessons', 'count_lessons', 'is_subscribed')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['lessons'] = LessonSerializer(instance.lesson_set.all(), many=True).data
        return data

    def get_count_lessons(self, instance):
        return instance.lesson_set.count()

    def get_is_subscribed(self, course):
        user = self.context['request'].user
        is_subscribed = Subscription.objects.filter(user=user, course=course).exists()
        return is_subscribed
