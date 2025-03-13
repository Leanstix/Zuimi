from django.urls import path
from .views import GenerateAccessToken

urlpatterns = [
    path('generate-access-token/', GenerateAccessToken.as_view(), name='generate-access-token'),
]