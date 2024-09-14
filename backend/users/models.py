"""Модель пользователя."""

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import UserManager
from django.db.models import Q, F

from .constants import (
    MAX_LENGTH_USERNAME,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_FIRSTNAME,
    MAX_LENGTH_LASTNAME,
)


class CustomUserManager(UserManager):
    """Указание полей для аутентификации."""

    def get_by_natural_key(self, username):
        return self.get(
            Q(**{self.model.USERNAME_FIELD: username})
            | Q(**{self.model.EMAIL_FIELD: username})
        )


class User(AbstractUser):
    """
    Измененная модель пользователя с
    новыми полями avatar и is_subscribed.
    """

    username = models.CharField(
        error_messages={'unique': 'A user with that username already exists.'},
        help_text=f'Required. {MAX_LENGTH_USERNAME} '
                  f'characters or fewer. Letters, '
                  f'digits and @/./+/-/_ only.',
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Неверный символ в логине'),
            UnicodeUsernameValidator()
        ],
        verbose_name='username'
    )
    first_name = models.CharField(blank=False, max_length=MAX_LENGTH_FIRSTNAME)
    last_name = models.CharField(blank=False, max_length=MAX_LENGTH_LASTNAME)
    is_subscribed = models.BooleanField(
        default=False,
    )
    avatar = models.ImageField(
        'Аватар',
        blank=True,
        upload_to='users/',
        null=True,
        default=None,
    )
    email = models.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        verbose_name='email address',
        unique=True
    )
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()
    # groups = models.ManyToManyField(
    #     Group,
    #     related_name='custom_user_set',  # Уникальное имя для обратной связи
    #     blank=True,
    #     help_text='The groups this user belongs to.',
    #     verbose_name='groups',
    # )
    #
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name='custom_user_permissions_set',  # Уникальное имя для обратной связи
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     verbose_name='user permissions',
    # )

    def __str__(self):
        """Отображение username."""
        return self.username


class Subscriber(models.Model):
    """Модель подписок на пользователя."""
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings',
        verbose_name='автор',
    )

    class Meta:
        """Ограничение на подписку на одного пользователя дважды."""

        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'],
                                    name='unique_follower_following'),
            models.CheckConstraint(check=~Q(follower=F('following')),
                                   name='no_self_subscription'),
        ]

    def __str__(self):
        return self.follower.username
