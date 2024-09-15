"""Сериалайзер для Котиков."""

import base64
import datetime as dt

import webcolors
from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Cat


class Base64ImageField(serializers.ImageField):
    """Перевод изображения в строку."""

    def to_internal_value(self, data):
        """Перевод изображения."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class CatSerializer(serializers.ModelSerializer):
    """Сериализатор Котиков."""

    age = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)
    image_url = serializers.SerializerMethodField(
        'get_image_url',
        read_only=True,
    )

    class Meta:
        """Выбор необходимых полей."""

        model = Cat
        fields = (
            'id', 'name', 'color', 'birth_year',
            'owner', 'age', 'image', 'image_url'
        )
        read_only_fields = ('owner',)

    def get_image_url(self, obj):
        """Получение изображения."""
        if obj.image:
            return obj.image.url
        return None

    def get_age(self, obj):
        """Получение возраста."""
        return dt.datetime.now().year - obj.birth_year
