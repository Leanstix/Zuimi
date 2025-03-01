from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EmailRegistrationSerializer, ChangePasswordSerializer, UserActivationSerializer, ProfileUpdateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Please check the terminal for your activation link."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserActivationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserActivationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UpdateUserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        serializer = UpdateUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.GET.get('token')
        try:
            user = User.objects.get(activation_token=token)
            if user.activate(token):
                return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)
            return Response({"message": "Invalid activation token."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "Invalid or expired activation token."}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
