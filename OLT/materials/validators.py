import re
from rest_framework import serializers


class VideoValidator:

    def __init__(self, field, message='Недопустимая ссылка'):
        self.field = field
        self.message = message

    def __call__(self, value):

        link = value.get(self.field)

        if not link:
            return

        pattern = re.compile(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$')

        if not pattern.match(link):
            raise serializers.ValidationError({self.field: [self.message]})

