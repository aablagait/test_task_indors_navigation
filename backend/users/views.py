"""Представления."""

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet

from .serializers import (AvatarSerializer,
                          SubscribeCreateSerialize,
                          SubscribePresentSerializer,
                          )
from .models import Subscriber
from .paginations import CustomUserPagination


User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """Вьюсет для регистрации пользователя,
    смены пароля,
    смены аватара,
    получения списка пользователей,
    нформации о конкретном пользователе,
    подписки на другого юзера,
    получении списка подписок."""

    pagination_class = CustomUserPagination

    def get_queryset(self):
        """Возвращаем всех пользователей."""
        return User.objects.all().order_by('id')

    def get_permissions(self):
        """Получение ограничений для различных пользователей."""
        if self.action in ('list', 'retrieve'):
            return (permissions.AllowAny(),)
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        """Ограничение на методы запроса."""
        if request.method == 'GET':
            return super().retrieve(request, *args, **kwargs)
        raise Response(
            {'detail': f'Метод {request.method} не разрешен.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=False,
            methods=['PUT', 'DELETE'],
            permission_classes=[permissions.IsAuthenticated],
            url_path='me/avatar',)
    def avatar(self, request):
        """Добавление и удаление аватара."""
        if request.method == 'PUT':
            user = get_object_or_404(User, username=request.user.username)
            serializer = AvatarSerializer(user, data=request.data,
                                          partial=True,)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        request.user.avatar.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=[permissions.IsAuthenticated],
            )
    def subscribe(self, request, id=None):
        """Подписка на пользователя, указанного в запросе."""
        following = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            data = {
                'follower': request.user.id,
                'following': following.id,
            }
            serializer = SubscribeCreateSerialize(data=data,
                                                  context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(SubscribePresentSerializer(
                following,
                context={'request': request}
            ).data, status=status.HTTP_201_CREATED)
        subscription = Subscriber.objects.filter(
            follower=request.user,
            following=id
        )
        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'detail': 'У вас нет такой подписки.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False,
            methods=['GET'],
            permission_classes=[permissions.IsAuthenticated],
            url_path='subscriptions',
            )
    def subscriptions(self, request):
        """Список моих подписок."""
        followings = User.objects.filter(
            followings__follower=request.user
        ).order_by('first_name')
        paginator = CustomUserPagination()
        page = paginator.paginate_queryset(followings, request)
        if page:
            serializer = SubscribePresentSerializer(
                page,
                many=True,
                context={'request': request}
            )
            return paginator.get_paginated_response(serializer.data)
        serializer = SubscribePresentSerializer(
            followings,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
