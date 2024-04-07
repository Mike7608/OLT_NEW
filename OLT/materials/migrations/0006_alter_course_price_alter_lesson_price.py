# Generated by Django 5.0.4 on 2024-04-05 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0005_lesson_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена курса'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена урока'),
        ),
    ]
