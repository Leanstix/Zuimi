from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.core.validators import RegexValidator, EmailValidator
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
import logging
import os

logger = logging.getLogger(__name__)

class CustomUserManager(BaseUserManager):
    try:
        def create_user(self, email, password=None, **extra_fields):
            if not email:
                raise ValueError("Email field is required")
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            if password:
                user.set_password(password)
            user.save(using=self._db)

            # Send activation email
            activation_link = f"{settings.FRONTEND_URL}/activate/{user.activation_token}"
            subject = "Account Activation"
            message = f"Hi {email},\n\nPlease activate your account using the link below:\n{activation_link}\n\nThank you!"

            email_from = os.environ.get('EMAIL_HOST_USER', 'noreply@example.com')
            send_mail(subject, message, email_from, [email], fail_silently=False)

            logger.info(f"User {email} created successfully and activation email sent.")

            return user
        
    except Exception as e:
        logger.error(f"Error during user registration: {e}")
        raise ValidationError("Error during user registration")
        

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    email = models.EmailField(unique=True, validators=[EmailValidator()])
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=100, default=get_random_string)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_name']

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.user_name and not self.activation_token and not self.email_verified:
            self.user_name = self.email
        super().save(*args, **kwargs)

    def activate(self, token):
        if token == self.activation_token:
            self.is_active = True
            self.email_verified = True
            self.activation_token = None
            self.save(update_fields=['is_active', 'email_verified', 'activation_token'])
            return True
        return False
    def activate(self, token):
        if token == self.activation_token:
            self.is_active = True
            self.email_verified = True
            self.activation_token = None
            self.save(update_fields=['is_active', 'email_verified', 'activation_token'])
            return True
        return False
        