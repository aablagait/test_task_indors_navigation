from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.files.base import ContentFile

from .models import Message


User = get_user_model()


class MessegeSerializer(serializers.ModelSerializer):
    """Сериализатор для отправки сообщений."""

    class Meta:
        model = Message
        fields = ('recipient', 'content', 'timestamp', )
        read_only_fields = ('timestamp', )
