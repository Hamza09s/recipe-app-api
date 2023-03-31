# """
# Tests for the user API
# """
# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.urls import reverse

# from rest_framework.test import APIClient
# from rest_framework import status

# CREATE_USER_URL = reverse('user:create')
# # user as app and create as endpoint
# # gives flexibility to pass dictionary into params
# # into function call which we can pass to the user


# def create_users(**params):
#     """Create and return a new user."""
#     return get_user_model().objects.create_user(**params)


# class PublicUserApiTests(TestCase):
#     """Test the public features of the user API."""

#     def setUp(self):
#         self.client = APIClient()

#     def test_create_user_success(self):
#         """Test creating a user is successful."""
#         payload = {
#             'email': 'test@example.com',
#             'password': 'testpass123',
#             'name': 'Test Name',
#         }
