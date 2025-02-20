from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.core.validators import RegexValidator, EmailValidator
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from .drive_utils import upload_file_to_drive
import logging
import requests
from io import BytesIO
import json
import os

class CustomUserManager(BaseUserManager):
    def create(self, validated_data):
        try:
            # Extracting necessary fields
            email = validated_data['email']
            password = validated_data['password']

            # Create the user
            user = User.objects.create_user(
                email=email,
                password=password,
                **{k: v for k, v in validated_data.items() if k not in ['email', 'password']}
            )

            # Log user creation success
            logger.info(f"User created successfully: {email}")

            # Send activation email
            activation_link = f"{settings.FRONTEND_URL}/activate/{user.activation_token}"
            subject = "Account Activation"
            message = f"Hi {email},\n\nPlease activate your zuimi account using the link below:\n{activation_link}\n\nThank you!"

            # Log email attempt
            logger.info(f"Sending activation email to {email}")

            email_from = os.environ.get('EMAIL_HOST_USER')
            if not email_from:
                raise ValueError("EMAIL_HOST_USER environment variable is not set.")
            
            send_mail(
                subject=subject,
                message=message,
                from_email=email_from,
                recipient_list=[email],
                fail_silently=False,
            )

            # Log email success
            logger.info(f"Activation email sent successfully to {email}")

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
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=100, default=get_random_string)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    
    objects = CustomUserManager()

    def __str__(self):
        return super().__str__()
    
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
        