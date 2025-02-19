'''Zuimi URL Configuration'''
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.http import JsonResponse
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version="v1",
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="leanstixx@gmail.com"),
        License=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', lambda request: JsonResponse({'message': 'Welcome to the API of Zuimi!'})),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)