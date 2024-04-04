from django.db import models

from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    pict = models.ImageField(upload_to='course/', verbose_name='превью', null=True, blank=True)
    description = models.CharField(max_length=250, verbose_name='описание', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None, verbose_name='user_id')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена курса')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание', null=True, blank=True)
    pict = models.ImageField(upload_to='lesson/', verbose_name='превью', null=True, blank=True)
    url_video = models.URLField(verbose_name='видео ссылка', blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None, verbose_name='user_id')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена урока')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    # подписчик
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # на какой курс подписка
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.course}'

    class Meta:
        verbose_name = "Подписка на курс"
