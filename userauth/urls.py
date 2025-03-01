from django.urls import path
from django.conf.urls.static import static
from django.conf import settings 
from .views import ActivateAccountView, UserActivationView, ChangePasswordView, EmailRegistrationView, ProfileUpdateView

urlpatterns = [
    path('register/', EmailRegistrationView.as_view(), name='register'),
    path('activate/', UserActivationView.as_view(), name='activate'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    #path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)