from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth import get_user_model

from OLT import settings
from materials.models import Course, Subscription


@shared_task
def send_email_update_object(obj_id):
    course = Course.objects.get(id=obj_id)

    # выбираем всех кто подписан на заданный курс
    list_subs = Subscription.objects.filter(course=obj_id)

    # Если прошло более 4 часов с момента последнего обновления
    if timezone.now() - course.stamp_update > timedelta(hours=4):
        # Тогда отправляем сообщение
        send_mail(
            'Уведомление об обновлении курса',
            'Курс, на который вы подписались, обновлен.',
            settings.EMAIL_HOST_USER,
            [subs.user.email for subs in list_subs],
            fail_silently=False,
        )

    # Сохраняем в БД время последнего уведомления
    course.stamp_update = timezone.now()
    course.save()


@shared_task
def block_inactive_users():
    # Берем модель пользователя
    user = get_user_model()

    # Берем период 30 дней
    period = timezone.now() - timedelta(days=30)

    # Выбираем пользователей, которые не заходили в систему более указанного периода
    users = user.objects.filter(last_login__lte=period)

    # Блокируем неактивных пользователей
    users.update(is_active=False)
