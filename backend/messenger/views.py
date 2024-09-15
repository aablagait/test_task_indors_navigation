from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from .models import Message
from .serializers import MessegeSerializer


class MessengerViewSet(viewsets.ModelViewSet):
    """Представления сообщений."""

    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = MessegeSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """Отображение всех сообщений текущего пользователя."""
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).order_by('-timestamp')

    def perform_create(self, serializer):
        """Автоматическое определение
        отправителя при отправке сообщения."""
        serializer.save(sender=self.request.user)

    @action(detail=False, methods=['get'], url_path='chats')
    def list_chats(self, request):
        """Отображение списка пользователей, с которыми есть переписка."""
        user = request.user
        # Находим пользователей, с которыми есть переписка
        sent_messages = Message.objects.filter(sender=user).values_list('recipient', flat=True)
        received_messages = Message.objects.filter(recipient=user).values_list('sender', flat=True)
        chat_users_ids = set(sent_messages).union(set(received_messages))

        chat_users = User.objects.filter(id__in=chat_users_ids)

        return Response([{'id': u.id, 'username': u.username} for u in chat_users])

    @action(detail=True, methods=['get'], url_path='messages')
    def list_messages(self, request, pk=None):
        """Отображение всех сообщений с конкретным пользователем."""
        user = request.user
        recipient = User.objects.get(id=pk)
        messages = Message.objects.filter(
            Q(sender=user, recipient=recipient) | Q(sender=recipient, recipient=user)
        ).order_by('timestamp')
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
