from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        print(data)
        phone_number = data.get('phone_number')
        email = data.get('email')
        password = data.get('password')

        if not (email or phone_number):
            raise serializers.ValidationError("Must include either 'email' or 'phone_number' along with 'password'.")

        user = authenticate(
            request=self.context.get('request'),
            username=email or phone_number,
            password=password
        )
        if user is None:
            raise AuthenticationFailed("Invalid credentials.")

        if not user.is_active:
            raise AuthenticationFailed("This account is inactive.")

        return {'user': user}
