# Generated by Django 5.0.2 on 2024-03-10 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_course_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='Цена урока'),
        ),
    ]