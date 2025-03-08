from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EmailRegistrationSerializer, ChangePasswordSerializer, UserActivationSerializer, ProfileUpdateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.utils.timezone import now

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
            user = serializer.save()
            
            if user.is_active:
                return Response({"message": "Your account is already activated."}, status=status.HTTP_200_OK)
            
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
        
        if not token:
            return Response({"error": "Activation token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(activation_token=token)

            # Check if already activated
            if user.is_active:
                return Response({"message": "Account is already activated."}, status=status.HTTP_200_OK)

            # Example: Ensure token hasn't expired (assuming you store token creation time)
            if user.activation_token_expires and user.activation_token_expires < now():
                return Response({"error": "Activation token has expired."}, status=status.HTTP_400_BAD_REQUEST)

            # Activate user
            user.is_active = True
            user.activation_token = None  # Clear the token
            user.save()

            return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Invalid or expired activation token."}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = request.user

            # Validate old password (if needed)
            old_password = serializer.validated_data.get("old_password")
            if not user.check_password(old_password):
                return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            # Save the new password
            user.set_password(serializer.validated_data.get("new_password"))
            user.save()

            return Response({"message": "Password changed successfully!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)