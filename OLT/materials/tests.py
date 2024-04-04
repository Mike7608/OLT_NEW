from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from .models import Lesson, Course


class LessonAPITestCase(APITestCase):
    def setUp(self):
        """ Заполнение данными """
        self.client = APIClient()

        self.user = User.objects.create(
            email='admin@my.com',
            is_superuser=True,
            is_staff=True,
            is_active=True)
        self.user.set_password('12345-')
        self.user.save()

        self.course = Course.objects.create(
            title="Test Course",
            description='Test Description Course',
            user=self.user)

        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Description Lesson',
            user=self.user,
            course=self.course)

        access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_create_lesson(self):
        """ Тест на создание урока """

        data = {'title': 'Новый урок', 'description': 'Новое описание урока', "course": 1}
        response = self.client.post('/lesson/create/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_lessons(self):
        response = self.client.get('/lesson/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

    def test_retrieve_lesson(self):
        response = self.client.get(f'/lesson/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        data = {'title': 'Updated Lesson', 'description': 'Updated Description'}
        response = self.client.patch(f'/lesson/update/{self.lesson.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        response = self.client.delete(f'/lesson/delete/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_subscription(self):
        # Создание подписки на курс
        response = self.client.post('/subscription/', {'course_id': self.course.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')

        # Удаление подписки на курс
        response = self.client.post('/subscription/', {'course_id': self.course.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')
