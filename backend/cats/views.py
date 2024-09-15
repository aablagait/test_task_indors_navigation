"""Представления для Котиков."""

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Cat
from .serializers import CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    """Представление для котиков."""

    queryset = Cat.objects.all().order_by('id')
    serializer_class = CatSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        """Создание котика."""
        serializer.save(owner=self.request.user)
