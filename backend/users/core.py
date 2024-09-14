"""Общие методы для всего приложения."""


def is_subscribed(request, model, obj):
    """Получение информации о наличии подписки на указанного пользователя."""
    if request and request.user.is_authenticated:
        return model.objects.filter(
            follower=request.user,
            following=obj
        ).exists()
    return False
