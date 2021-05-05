from authentication.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Create your tests here.
class RegistrationTestCase(APITestCase):

    def test_registration(self):

        data = {
            "email": "bobwhite@gmail.com",
            "username": "bobwhite",
            "password": "Abc123..",
            "first_name": "Bob",
            "last_name": "White",
            "phone": "+50578251453"
        }

        response = self.client.post('/auth/users/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginTestCase(APITestCase):

    email = 'bobwhite@gmail.com'
    password = 'Abc123..'

    def setUp(self):
        self.user = User.objects.create_user(
            email = self.email,
            username = "bobwhite",
            password =  self.password,
            first_name = "Bob",
            last_name = "White",
            phone = "+50578251453"
        )

    def test_login(self):

        data = {
            "email": self.email,
            "password": self.password
        }

        response = self.client.post('/auth/token/login/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_fail(self):

        data = {
            "email": self.email,
            "password": self.password + "123"
        }

        response = self.client.post('/auth/token/login/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email = "bobwhite@gmail.com",
            username = "bobwhite",
            password = "Abc123..",
            first_name = "Bob",
            last_name = "White",
            phone = "+50578251453"
        )

        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_logout(self):

        response = self.client.post('/auth/token/logout/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)