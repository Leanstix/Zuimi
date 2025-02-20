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
            "Flow User Activation",#subject
            f"click on the link to activate your account {activation_url}",#message
            Email, #from email
            [user.email], #toemail
            fail_silently=False
        )
        print(f"Activation link (copy and paste in browser to activate): {activation_url}")

        return user