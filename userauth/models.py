from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator, EmailValidator
from django.utils.crypto import get_random_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, **extra_fields):
        if not email:
            raise ValueError("Email field is required")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_unusable_password()  # No password at initial creation
        user.generate_activation_token()
        user.save()
        
        activation_link = f"{settings.FRONTEND_URL}/activate/{user.activation_token}"
        print(f"Activation link: {activation_link}")
        logger.info(f"User {email} created successfully. Activation link: {activation_link}")

        return user

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    email = models.EmailField(unique=True, validators=[EmailValidator()])
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    user_name = models.CharField(max_length=100, blank=True, unique=True)
    phone_number = models.CharField(
        max_length=15, blank=True, validators=[RegexValidator(r'^\+?1?\d{9,15}$')]
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    profile_picture = models.URLField(blank=True, null=True)
    activation_token = models.CharField(max_length=100, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def generate_activation_token(self):
        """Generate a new activation token and save it."""
        self.activation_token = get_random_string(length=32)
        self.save(update_fields=['activation_token'])

    def activate(self, token):
        """Activate the user if the token matches."""
        if self.activation_token and token == self.activation_token:
            self.is_active = True
            self.email_verified = True
            self.activation_token = None  # Reset after activation
            self.save(update_fields=['is_active', 'email_verified', 'activation_token'])
            return True
        return False
