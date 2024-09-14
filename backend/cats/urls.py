"""URL пути."""

from django.urls import path, include
from rest_framework import routers

from .views import CatViewSet


app_name = 'cats'


router = routers.DefaultRouter()
router.register(r'cats', CatViewSet, basename='cat')

urlpatterns = [
    path('', include(router.urls)),
]
