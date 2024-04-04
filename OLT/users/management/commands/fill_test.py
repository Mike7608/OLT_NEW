from django.core.management import BaseCommand
from django.db.models.functions import datetime
from django.contrib.auth.models import Group, Permission
from materials.models import Course, Lesson
from users.models import User, Payments


class Command(BaseCommand):

    def handle(self, *args, **options):
        Payments.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        User.objects.all().delete()

        # создаем тестового пользователя
        user_test = User.objects.create(
            email='admin@my.com',
            first_name='admin',
            last_name='admin',
            is_staff=True,
            is_superuser=True
        )

        user_test.set_password('12345-')
        user_test.save()

        # создаем тестового администратора на курсы и уроки
        moder_test = User.objects.create(
            email='mod@my.com',
            first_name='mod',
            last_name='mod',
        )

        moder_test.set_password('12345+')
        moder_test.save()

        # создаем тестовый курс
        course_test: Course = Course.objects.create(
            title="Python",
            description='Глубокое изучения языка Python',
            user=user_test,
        )
        course_test.save()

        # создаем второй тестовый курс
        course_test2: Course = Course.objects.create(
            title="Django 4",
            description='Глубокое изучения фреймворка Django 4',
            user=moder_test,
        )
        course_test.save()

        # создаем тестовые уроки для курса
        lesson_test1 = Lesson.objects.create(
            title='Основы Python. Введение.',
            description='Основы языка Python. Введение.',
            url_video='https://youtu.be/VXYyJX5qMiQ?list=PLlWXhlUMyooaeSj8L8tVVbtUo0WCO4ORR',
            course=course_test,
            user=user_test
        )
        lesson_test1.save()
        lesson_test2 = Lesson.objects.create(
            title='Основы Python. Типы данных',
            description='Типы данных, объекты, литералы',
            course=course_test,
            user=user_test
        )
        lesson_test2.save()

        # создаем тестовую оплату курса и уроков
        pay_test_course = Payments.objects.create(
            user=user_test,
            date_pay=datetime.Now(),
            pay_course=course_test,
            pay_summ=1000.50,
            pay_method=Payments.Transfer,
        )
        pay_test_course.save()

        pay_test_lesson = Payments.objects.create(
            user=user_test,
            date_pay=datetime.Now(),
            pay_lesson=lesson_test2,
            pay_summ=500,
            pay_method=Payments.Cash,
        )
        pay_test_lesson.save()
