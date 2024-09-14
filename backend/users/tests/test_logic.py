"""Тесты на корректную работу логики приложения."""

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus


User = get_user_model()


@pytest.mark.django_db
def test_create_user(client, user_form):
    """
    Тест проверяет создание пользователя
    """
    url = reverse('users:user-list')
    count_users_before = User.objects.count()
    response = client.post(url, data=user_form)
    assert response.status_code == HTTPStatus.CREATED
    assert User.objects.count() == count_users_before + 1


@pytest.mark.django_db
def test_recreate_exist_user(client, user_form):
    """
    Тест проверяет ошибку при создании второго пользователя
    с таким же username.
    """
    url = reverse('users:user-list')
    count_users_before = User.objects.count()
    client.post(url, data=user_form)
    response = client.post(url, data=user_form)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert User.objects.count() == count_users_before + 1


def test_pagination_user(authenticated_client):
    """Тест на наличие пагинации
    'count' должен содержаться.
    """
    url = reverse('users:user-list')
    response = authenticated_client.get(url)
    response_data = response.json()
    assert 'count' in response_data
    assert response_data['count'] == User.objects.count()
