from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as BaseGroup
from django.db import models


class User(AbstractUser):
    api_last_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='Последний ip при обращении по API'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Group(BaseGroup):
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
