from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import CoursePagination, LessonPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwner, IsModeratorMaterials


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        match self.action:
            case 'list':
                permission_classes = [IsAuthenticated]
            case 'create':
                permission_classes = [IsAuthenticated, ~IsModeratorMaterials]
            case 'retrieve':
                permission_classes = [IsAuthenticated, IsModeratorMaterials | IsOwner]
            case 'update':
                permission_classes = [IsAuthenticated, IsModeratorMaterials | IsOwner]
            case 'destroy':
                permission_classes = [IsAuthenticated, IsOwner]
            case _:
                permission_classes = None

        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user = request.user

        data = []
        # Добавляем признак подписки пользователя на каждый курс
        for course in queryset:
            is_subscribed = Subscription.objects.filter(user=user, course=course).exists()
            serializer = self.get_serializer(course)
            course_data = serializer.data
            course_data['is_subscribed'] = is_subscribed
            data.append(course_data)

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        queryset = Course.objects.all()
        user = request.user
        course = get_object_or_404(queryset, pk=kwargs['pk'])

        # Проверяем подписку пользователя на курс
        is_subscribed = Subscription.objects.filter(user=user, course=course).exists()

        # Сериализуем данные курса с признаком подписки пользователя
        serializer = self.get_serializer(course)
        data = serializer.data
        data['is_subscribed'] = is_subscribed

        return Response(data)


class LessonCreateAPIView(generics.CreateAPIView):
    # create
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModeratorMaterials]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    #  list
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    # detail
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModeratorMaterials | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    # update
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModeratorMaterials | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    # delete
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
            # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'
            # Возвращаем ответ в API
        return Response({"message": message})
