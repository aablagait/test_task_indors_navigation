import pytest

from django.urls import reverse
from users.models import Subscriber
from http import HTTPStatus


@pytest.mark.django_db
def test_get_subscribe(authenticated_client, other_user, user, subscribe_form):
    """Тест на добавление пользователя в подписки."""
    url = reverse('users:user-subscribe', args=[other_user.pk])
    count_subscribe = Subscriber.objects.count()
    response = authenticated_client.post(url, data=subscribe_form)
    assert response.status_code == HTTPStatus.CREATED
    assert Subscriber.objects.count() == count_subscribe + 1


@pytest.mark.django_db
def test_available_subscribe(authenticated_client):
    """Тест на доступность страницы подписок."""
    url = reverse('users:user-subscriptions')
    response = authenticated_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_delete_subscribe(
        authenticated_client, other_user, user, subscribe_form
):
    """Тест на удаление пользователя из подписок."""
    url = reverse('users:user-subscribe', args=[other_user.pk])
    authenticated_client.post(url, data=subscribe_form)
    response = authenticated_client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not Subscriber.objects.filter(
        follower=user, following=other_user
    ).exists()
