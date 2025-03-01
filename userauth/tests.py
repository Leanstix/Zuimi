from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAuthTests(APITestCase):

    def test_user_registration(self):
        url = reverse('register')
        data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'user_name': 'testuser',
            'phone_number': '+1234567890',
            'password': 'TestPassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Account created successfully! Please check your email to activate your account.")

    def test_user_activation(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            user_name='testuser',
            phone_number='+1234567890',
            password='TestPassword123'
        )
        url = reverse('activate')
        data = {'token': user.activation_token}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Account activated successfully!")

    def test_user_profile_update(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            user_name='testuser',
            phone_number='+1234567890',
            password='TestPassword123',
            is_active=True
        )
        self.client.force_authenticate(user=user)
        url = reverse('profile-update')
        data = {
            'first_name': 'UpdatedTest',
            'last_name': 'UpdatedUser',
            'user_name': 'updatedtestuser',
            'phone_number': '+0987654321'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'UpdatedTest')
        self.assertEqual(response.data['last_name'], 'UpdatedUser')
        self.assertEqual(response.data['user_name'], 'updatedtestuser')
        self.assertEqual(response.data['phone_number'], '+0987654321')

    def test_change_password(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            user_name='testuser',
            phone_number='+1234567890',
            password='TestPassword123',
            is_active=True
        )
        self.client.force_authenticate(user=user)
        url = reverse('change-password')
        data = {
            'current_password': 'TestPassword123',
            'new_password': 'NewTestPassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Password changed successfully!")