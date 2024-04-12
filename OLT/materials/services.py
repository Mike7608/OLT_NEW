import json
from datetime import datetime, timedelta

from django_celery_beat.models import PeriodicTask, IntervalSchedule


def set_schedule(*args, **kwargs):
    """
    Периодическая задача для проверки пользователей на активность
    """
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=24,
        period=IntervalSchedule.HOURS,
    )
    PeriodicTask.objects.create(
        interval=schedule,
        name='Block inactive users',
        task='OLT.tasks.block_inactive_users',
        args=json.dumps(['arg1', 'arg2']),
        kwargs=json.dumps({
            'be_careful': True,
        }),
        expires=datetime.utcnow() + timedelta(seconds=30)
    )
