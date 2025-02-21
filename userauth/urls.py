from django.urls import path
from django.conf.urls.static import static
from django.conf import settings 
from .views import ActivateAccountView, UserRegistrationView, UserActivationView, ChangePasswordView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('activate/', UserActivationView.as_view(), name='activate'),
    path('activate-account/', ActivateAccountView.as_view(), name='activate-account'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)