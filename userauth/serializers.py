from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from dotenv import load_dotenv
import os

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'university_id', 'password']

    def create(self, validated_data):
        # Pop password from validated_data
        password = validated_data.pop('password')

        # Create user instance
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Email = os.environ.get('EMAIL_HOST_USER')

       #sending an email to the user to receive their activation link
        activation_url = f"https://flow-aleshinloye-olamilekan-s-projects.vercel.app/activate?token={user.activation_token}"
        send_mail(
            "Zuimi User Activation",#subject
            f"click on the link to activate your account {activation_url}",#message
            Email, #from email
            [user.email], #toemail
            fail_silently=False
        )
        print(f"Activation link (copy and paste in browser to activate): {activation_url}")

        return user

class UserActivationSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        try:
            user = User.objects.get(activation_token=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired activation token.")
        return value
    
    def save(self):
        token = self.validated_data['token']
        user = User.objects.get(activation_token=token)
        user.activate_account()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("incorrect Current Password!!!")
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user