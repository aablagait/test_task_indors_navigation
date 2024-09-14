"""Модуль для работы с Котиками."""

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Cat(models.Model):
    """Модель котика."""

    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16)
    birth_year = models.IntegerField()
    owner = models.ForeignKey(
        User, related_name='cats',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='cats/images/',
        null=True,
        default=None
    )

    def __str__(self):
        """Возвращаем имя в админку."""
        return self.name
