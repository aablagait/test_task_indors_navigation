"""Фикстуры для теста рецептов"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from cats.models import Cat


User = get_user_model()


image = str('data:image/png;base64,'
            'iVBORw0KGgoAAAANSUhEUgA'
            'AAAEAAAABAgMAAABieywaAA'
            'AACVBMVEUAAAD///9fX1/S0'
            'ecCAAAACXBIWXMAAA7EAAAO'
            'xAGVKw4bAAAACklEQVQImWN'
            'oAAAAggCByxOyYQAAAABJRU'
            '5ErkJggg==')


@pytest.fixture
def user_form():
    """Форма для создания юзера."""
    return {
        'email': 'vpupkin@yandex.ru',
        'username': 'vasya.pupkin',
        'first_name': 'Вася',
        'last_name': 'Иванов',
        'password': 'Qwerty123'
    }


@pytest.fixture
def user(django_user_model, user_form):
    """Модель юзера."""
    return django_user_model.objects.create_user(**user_form)


@pytest.fixture
def user_client(client, user):
    """Клиент юзера."""
    client.force_login(user)
    return client


@pytest.fixture
def api_client():
    """Клиент API."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    """Аутентифицированный клиент."""
    token, created = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client


@pytest.fixture
def cat_form(user):
    """Форма для создания котика."""
    return {
        'name': 'pushok',
        'color': 'black',
        'birth_year': 2019,
        'image': image,
    }


@pytest.fixture
def cat_other_form(user):
    """Форма для создания котика."""
    return {
        'name': 'finik',
        'color': 'white',
        'birth_year': 2020,
        'image': image,
    }


@pytest.fixture
def cat(user):
    """Модель котика."""

    cat = Cat.objects.create(
        owner=user,
        image=image,
        name='pushok',
        color='black',
        birth_year=2020
    )
    return cat
