from rest_framework import serializers
from django.contrib.auth import get_user_model 
from django.conf import settings
import os
from dotenv import load_dotenv
import string
import random
#from django.core.mail import send_mail

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.create(email=email, **validated_data)
        user.save()
        Email = os.environ.get('EMAIL_HOST_USER')
        activation_url = f"http://localhost:3000/activate?token={user.activation_token}"

        '''send_mail(
            "Zuimi User Activation",
            f"Click the link to activate your account: {activation_url}",
            Email,
            [user.email],
            fail_silently=False,
        )'''

        print(f"Activation link (copy and paste in browser to activate): {activation_url}")
        return user

class ProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'user_name', 'phone_number', 'password']
        read_only_fields = ['email']

    def validate(self, attrs):
        if not self.instance.is_active:
            raise serializers.ValidationError("Account is not active. Complete activation first.")
        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password:
            instance.set_password(password)

        instance.save()
        return User

class UserActivationSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        try:
            user = User.objects.get(activation_token=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired activation token.")
        return value
    
    def generate_password(self, length=13):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(length))
        return password

    def save(self):
        user = User.objects.get(activation_token=self.validated_data['token'])
        user.activate(self.validated_data['token'])
        new_password = self.generate_password()
        user.set_password(new_password)
        user.save()
        print(f"New password for user {user.email}: {new_password}")
        return user

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect current password.")
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
