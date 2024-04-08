import os
from celery import Celery
from django.utils import timezone

# Установить настройки по умолчанию из Django-проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OLT.settings')

app = Celery('config')

# Использование здесь строки означает, что рабочему процессу не нужно сериализовать
# объект конфигурации дочерним процессам.
# - namespace='CELERY' означает, что все ключи конфигурации, связанные с Celery,
# должны иметь префикс `CELERY_`.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически загружать задачи из всех зарегистрированных приложений Django
app.autodiscover_tasks()

# Настройка для celery beat
app.conf.beat_schedule = {
    'block_inactive_users': {
        'task': 'OLT.tasks.block_inactive_users',
        'schedule': timezone.timedelta(days=1),
    }
}

# Пример использования
# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
