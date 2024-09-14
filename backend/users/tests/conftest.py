"""Фикстуры для тестов"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


User = get_user_model()

image = ('data:image/png;base64,'
         'iVBORw0KGgoAAAANSUhEUgA'
         'AAAEAAAABAgMAAABieywaAA'
         'AACVBMVEUAAAD///9fX1/S0'
         'ecCAAAACXBIWXMAAA7EAAAO'
         'xAGVKw4bAAAACklEQVQImWN'
         'oAAAAggCByxOyYQAAAABJRU'
         '5ErkJggg=='),


@pytest.fixture
def user_form():
    """Форма для создания юзера."""
    return {
        'email': 'vpupkin@yandex.ru',
        'username': 'vasya.pupkin',
        'first_name': 'Вася',
        'last_name': 'Иванов',
        'password': 'Qwerty123nano'
    }


@pytest.fixture
def other_user_form():
    """Форма для создания юзера."""
    return {
        'email': 'alex@yandex.ru',
        'username': 'alex.pupkin',
        'first_name': 'Вася',
        'last_name': 'Иванов',
        'password': 'qwertypassword'
    }


@pytest.fixture
def avatar_form():
    """Форма для создания аватара."""
    return {
        'avatar': image
    }


@pytest.fixture
def password_form():
    """Форма для обновления пароля."""
    return {
        'new_password': 'Qwerty123nanoNew',
        'current_password': 'Qwerty123nano'
    }


@pytest.fixture
def token_form(user_client):
    """Форма для создания токена."""
    return {
        'password': 'Qwerty123nano',
        'email': 'vpupkin@yandex.ru'
    }


@pytest.fixture
def user(django_user_model, user_form):
    """Модель юзера."""
    return django_user_model.objects.create_user(**user_form)


@pytest.fixture
def user_id(user):
    return (user.id,)


@pytest.fixture
def other_user(django_user_model, other_user_form):
    """Модель юзера."""
    return django_user_model.objects.create_user(**other_user_form)


@pytest.fixture
def user_client(client, user):
    """Клиент юзера."""
    client.force_login(user)
    return client


@pytest.fixture
def api_client():
    """Клиент для тестов через API."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    """Аутентифицированный клиент для тестов через API."""
    token, created = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client


@pytest.fixture
def subscribe_form(user, other_user):
    """Форма для отправки подписки."""
    return {
        'follower': user.id,
        'following': other_user.id
    }
