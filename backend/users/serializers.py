"""Сериализаторы для Юзеров."""

import base64

from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.files.base import ContentFile

from .models import Subscriber
from .core import is_subscribed
from .constants import BLACK_LIST_OF_USERNAMES


User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Перевод изображения в строку."""

    def to_internal_value(self, data):
        """Перевод изображения."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class AvatarSerializer(serializers.Serializer):
    """Сериализатор изменения аватара."""

    avatar = Base64ImageField(required=False, allow_null=True, use_url=True)

    def validate(self, attrs):
        """Проверка наличия поля avatar в запросе."""
        if attrs.get('avatar'):
            return attrs
        raise serializers.ValidationError('Поле "avatar" - обязательное')

    def update(self, instance, validated_data):
        """Обновлние поля avatar."""
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance

    def to_representation(self, obj):
        """Возвращаем представление с абсолютной ссылкой на аватар."""
        ret = super().to_representation(obj)
        request = self.context.get('request')
        if obj.avatar and request:
            avatar_url = obj.avatar.url
            ret = request.build_absolute_uri(avatar_url)
        return ret


class UserSerializer(serializers.ModelSerializer):
    """"Сериализатор пользователя."""

    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField(read_only=True,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.fields.pop('is_subscribed', None)
            self.fields.pop('avatar', None)

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'password',
                  'is_subscribed',
                  'avatar',)
        read_only_fields = ('id',
                            'is_subscribed',
                            'avatar',)
        write_only_fields = ('password',)

    def validate_username(self, username):
        """Валидация данных """
        if username in BLACK_LIST_OF_USERNAMES:
            raise serializers.ValidationError(
                f"Нельзя создать пользователя с username {username}"
            )
        return username

    def create(self, validated_data):
        """Создание пользователя."""
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_avatar(self, obj):
        """Получение абсолютной ссылки на изображение."""
        request = self.context.get('request')
        if obj.avatar and request:
            avatar_url = obj.avatar.url
            return request.build_absolute_uri(avatar_url)
        return None

    def get_is_subscribed(self, obj):
        """Определение подписан ли автор запроса на этого пользователя."""
        request = self.context.get('request')
        return is_subscribed(request=request,
                             model=Subscriber,
                             obj=obj)


class SubscribeCreateSerialize(serializers.ModelSerializer):
    """Сериализатор для подписки на пользователя."""

    class Meta:
        model = Subscriber
        fields = ('follower', 'following',)

    def validate(self, data):
        """Запрещаем подписку на самого себя.
        и подписку дважды на одного пользователя"""

        if data['follower'] == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя.'
            )
        if Subscriber.objects.filter(**data).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя.'
            )
        return data


class SubscribePresentSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения информации
    о пользователе на которого подписан.
    Вывод информацию о рецептах, их количсетве."""

    avatar = serializers.SerializerMethodField(
        read_only=True
    )
    is_subscribed = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')


    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'avatar',)

    def get_avatar(self, obj):
        """Получение абсолютной ссылки на изображение."""
        request = self.context.get('request')
        if obj.avatar and request:
            avatar_url = obj.avatar.url
            return request.build_absolute_uri(avatar_url)
        return None

    def get_is_subscribed(self, obj):
        """Определение подписан ли автор запроса на этого пользователя."""
        request = self.context.get('request')
        return is_subscribed(request=request,
                             model=Subscriber,
                             obj=obj)
