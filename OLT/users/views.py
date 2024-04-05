import stripe
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from OLT import settings
from materials.models import Course, Lesson
from users.models import User, Payments
from users.pay_services import create_product, create_price, create_session
from users.permissions import IsOwner
from users.serializers import UserSerializer, PaymentsSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['pay_course', 'pay_lesson', 'pay_method']
    ordering_fields = ['date_pay']
    permission_classes = [IsAuthenticated]


class PaymentsCreateAPIView(APIView):

    def post(self, request):
        # Берем данные для платежа из запроса
        user = request.user
        pay_method = 2  # Безналичный

        record_id = request.data.get('id')

        lesson_id = course_id = None

        if request.data.get('course'):
            # если имеется поле COURSE - значит выбрана оплата урока
            pay_obj = Lesson.objects.get(pk=record_id)
            lesson_id = pay_obj.pk
        else:
            # иначе выбрана оплата курса
            pay_obj = Course.objects.get(pk=record_id)
            course_id = pay_obj.pk

        # Создаем продукт в Stripe
        product_stripe = create_product(pay_obj.title,  pay_obj.description)

        # Создаем цену в Stripe
        price_stripe = create_price(product_stripe, pay_obj.price, 'BYN')

        # Получем текущее время для поля pay_date
        pay_date = timezone.now()

        # Создаем сессию для платежа в Stripe
        success_url = "http://example.com/success"  # Замените на ваш URL успешного платежа
        cancel_url = "http://example.com/cancel"  # Замените на ваш URL отмены платежа
        session_id, session_url = create_session(price_stripe, success_url, cancel_url)

        # Создаем запись о платеже в нашей БД
        Payments.objects.create(user=user, pay_summ=pay_obj.price, pay_method=pay_method,
                                session_id=session_id,
                                payment_link=session_url, date_pay=pay_date, pay_lesson_id=lesson_id,
                                pay_course_id=course_id)

        if session_url:
            # Если сессия создана успешно, возвращаем URL для оплаты
            return Response({'session_url': session_url}, status=status.HTTP_201_CREATED)
        else:
            # Если возникла ошибка при создании сессии, возвращаем соответствующий ответ
            return Response({'Ошибка': 'Не удалось создать сеанс оформления заказа.'}, status=status.HTTP_400_BAD_REQUEST)

