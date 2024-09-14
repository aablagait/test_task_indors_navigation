"""Тесты на страницы приложения."""

import pytest
from django.urls import reverse
from http import HTTPStatus


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args, status',
    (
        ('users:user-list', None, HTTPStatus.OK),
        ('users:user-detail', pytest.lazy_fixture('user_id'),
         HTTPStatus.OK),
        ('users:user-me', None, HTTPStatus.UNAUTHORIZED),
    )
)
def test_availabilyty_for_anon(client, name, args, status, user):
    """Тест доступности страниц для анонима."""
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args, status, params',
    (
        ('users:user-list', None, HTTPStatus.OK, None),
        ('users:user-list', None, HTTPStatus.OK, {'limit': 2}),
        ('users:user-list', None, HTTPStatus.OK, {'limit': 2, 'page': 2}),
        ('users:user-detail', pytest.lazy_fixture('user_id'),
         HTTPStatus.OK, None),
        ('users:user-me', None, HTTPStatus.OK, None),
    )
)
def test_availabilyty_for_user(
        authenticated_client, name, args, status, params):
    """Тест доступности страниц для пользователя."""
    url = reverse(name, args=args)
    response = authenticated_client.get(url, params=params)
    assert response.status_code == status


@pytest.mark.django_db
def test_availabilyty_page_for_registration(client, user_form):
    """Тест страницы регистрации."""
    url = reverse('users:user-list')
    response = client.post(url, data=user_form)
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.django_db
def test_availabilyty_page_for_reset_avatar(authenticated_client, avatar_form):
    """Тест страницы сменя аватара."""
    url = reverse('users:user-avatar')
    response = authenticated_client.put(url, data=avatar_form)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_availabilyty_page_for_reset_avatar_without_avatar_field(
        authenticated_client, avatar_form):
    """Тест страницы сменя аватара без поля
    avatar в запросе"""
    url = reverse('users:user-avatar')
    response = authenticated_client.put(url, )
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_availabilyty_page_for_delete_avatar(
        authenticated_client, avatar_form):
    """Тест страницы удаления аватара."""
    url = reverse('users:user-avatar')
    response = authenticated_client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.django_db
def test_availabilyty_page_for_reset_password(
        authenticated_client, password_form):
    """Тест страницы смены пароля."""
    url = reverse('users:user-set-password')
    response = authenticated_client.post(url, data=password_form)
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.django_db
def test_availabilyty_page_for_get_token(
        user_client, token_form):
    """Тест странцы получения и удаления токена."""
    url = reverse('users:login')
    response = user_client.post(url, data=token_form)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_availabilyty_page_for_delete_token(
        user_client, token_form, authenticated_client):
    """Тест странцы удаления токена."""
    url = reverse('users:logout')
    response = authenticated_client.post(url)
    assert response.status_code == HTTPStatus.NO_CONTENT
