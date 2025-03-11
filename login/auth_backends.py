from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in with either 
    email or phone number.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        # Check if the username is an email or phone number
        try:
            user = User.objects.get(email=username)  # Try email first
        except User.DoesNotExist:
            try:
                user = User.objects.get(phone_number=username)  # Try phone number
            except User.DoesNotExist:
                return None  # No user found

        # Check if the password is correct
        if user.check_password(password):
            return user
        return None

