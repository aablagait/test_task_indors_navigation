"""URL пути."""

from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet


app_name = 'users'


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
