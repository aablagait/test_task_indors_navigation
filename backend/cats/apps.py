"""Настройка админки для Котиков."""

from django.apps import AppConfig


class CatsConfig(AppConfig):
    """Настройка админки для Котиков."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cats'
