import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserActivationSerializer, UserProfileUpdateSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView, AllowAny
from django.contrib.auth import get_user_model
from .models import User
import logging