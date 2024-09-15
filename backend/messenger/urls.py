"""URL пути."""

from django.urls import path, include
from rest_framework import routers

from .views import MessengerViewSet


app_name = 'messenger'


router = routers.DefaultRouter()
router.register(r'messenge', MessengerViewSet, basename='messenge')

urlpatterns = [
    path('', include(router.urls)),
]
