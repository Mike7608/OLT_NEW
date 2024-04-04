from django.contrib.auth.models import AbstractUser
from django.db import models

from users.pay_services import create_session


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', null=True, blank=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', null=True, blank=True)
    city = models.CharField(max_length=30, verbose_name='город')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Payments(models.Model):
    from materials.models import Course, Lesson

    Cash = 1
    Transfer = 2

    METHOD = [
        (Cash, "Наличные"),
        (Transfer, "Перевод на счет")
    ]

    user = models.ForeignKey(
                            User,
                            on_delete=models.CASCADE
                            )
    date_pay = models.DateTimeField(
                                    verbose_name='дата оплаты'
                                    )
    pay_course = models.ForeignKey(
                                    Course,
                                    on_delete=models.DO_NOTHING,
                                    null=True,
                                    blank=True
                                    )
    pay_lesson = models.ForeignKey(Lesson,
                                   on_delete=models.DO_NOTHING,
                                   null=True,
                                   blank=True
                                   )
    pay_summ = models.DecimalField(decimal_places=2,
                                   max_digits=10,
                                   verbose_name='Сумма оплаты'
                                   )
    pay_method = models.PositiveSmallIntegerField(default=1,
                                                  choices=METHOD,
                                                  verbose_name='Способ оплаты'
                                                  )
    session_id = models.CharField(max_length=50,
                                  verbose_name="Идентификатор сессии",
                                  null=True,
                                  blank=True
                                  )
    payment_link = models.CharField(max_length=50,
                                    verbose_name="Ссылка на платеж",
                                    null=True,
                                    blank=True
                                    )

    def create_session(self, success_url, cancel_url):
        """Создать сессию для платежа."""
        if not self.session_id or not self.payment_link:
            return None
        return create_session(self.payment_link, success_url, cancel_url)

    def __str__(self):
        # pylint: disable=no-member
        return f"Оплата от {self.user.email} за {self.pay_course or self.pay_lesson} проведена {self.date_pay}"

    class Meta:
        verbose_name = "Платежи"
