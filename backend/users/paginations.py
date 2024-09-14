"""Настройки пагинации для приложения Users."""

from rest_framework.pagination import PageNumberPagination


class CustomUserPagination(PageNumberPagination):
    """В параметрах запроса можно указать параметр
    limit, который ограничит количество выводимых пользователей."""

    page_size_query_param = 'limit'
