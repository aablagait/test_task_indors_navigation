"""Основной файл URL путей."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('cats.urls')),
    path('api/', include('users.urls')),
    path('api/', include('messenger.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

schema_view = get_schema_view(
   openapi.Info(
      title="Task API",
      default_version='v1',
      description="Документация для тестового задания в компанию Индорс Навигейшн",
      contact=openapi.Contact(email="aleksej.bocharov9@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
       name='schema-redoc'),
]
