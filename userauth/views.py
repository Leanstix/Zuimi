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
            try:
                user = serializer.save()
                return Response(
                    {"message": f"Account created successfully! Check {user.email} for activation instructions."}, 
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({"error": "Something went wrong. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserActivationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileUpdateSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
