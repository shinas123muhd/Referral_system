from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User, Referral
from users.serializers import UserSerializer, ReferralSerializer
from users.views import RegisterUser, UserDetails, ViewReferrals
from django.contrib.auth.models import User as DjangoUser

# Create your tests here.
class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {'name': 'TestUser', 'email': 'test@example.com', 'password': 'test123'}
        self.referring_user = User.objects.create(name='Referring User', email='referrer@example.com', password='ref123', referral_code='referral_code_here')
        

    def test_register_user_without_referral(self):
        response = self.client.post(reverse('registeruser'), self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_with_referral(self):
        referral_code_data = {**self.user_data, 'referred_by': self.referring_user.referral_code}
        
        response = self.client.post(reverse('registeruser'), referral_code_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserDetailsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(name='TestUser', email='test@example.com', password='test123')

    def test_get_user_details(self):
        response = self.client.get(reverse('userdetails', args=[self.user.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first_user = response.data[0]  
        self.assertEqual(first_user['name'], self.user.name)

    
    def test_view_referrals(self):
        response = self.client.get(reverse('viewreferrals', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
