"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client;also camelcase because thats 
        how lib names its methods"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_users_lists(self):
        """Test that users are listed on page."""
        url = reverse(
            'admin:core_user_changelist')  # determines which
        # url we will pull from
        # django admin,shows lists of users in page
        # http get request,because of force login it will
        res = self.client.get(url)
        # be user we forced login of;the admin.
        # res will contain response

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
        # it will check if it has user name and email
        # because these are the 2 list
        # fields we want displayed on the page

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:core_user_change', args=[
                      self.user.id])  # will return user id fro url
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
