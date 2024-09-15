"""Тесты на страницы приложения."""

import pytest
from django.urls import reverse
from http import HTTPStatus

from cats.models import Cat


@pytest.mark.django_db
def test_cat(client):
    """Тест на доступность страницы котика."""
    url = reverse('cats:cat-list')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_cat_create(authenticated_client, cat_form):
    """Тест на создание котика."""
    url = reverse('cats:cat-list')
    count_recipe = Cat.objects.count()
    response = authenticated_client.post(url, data=cat_form, format='json')
    assert response.status_code == HTTPStatus.CREATED
    assert count_recipe + 1 == Cat.objects.count()


@pytest.mark.django_db
def test_cat_detail(authenticated_client, cat):
    """Тест на получение информации определенного котика."""
    url = reverse('cats:cat-detail', args=[cat.pk])
    response = authenticated_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_cat_patch(authenticated_client, cat, cat_other_form):
    """Тест на изменение котика."""
    url = reverse('cats:cat-detail', args=[cat.pk])
    response = authenticated_client.patch(
        url, data=cat_other_form, format='json'
    )
    assert response.status_code == HTTPStatus.OK
    cat.refresh_from_db()
    assert cat.name == cat_other_form['name']


@pytest.mark.django_db
def test_cat_delete(authenticated_client, cat):
    """Тест на удаление котика."""
    url = reverse('cats:cat-detail', args=[cat.pk])
    start_count = Cat.objects.count()
    response = authenticated_client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert Cat.objects.count() == start_count - 1
