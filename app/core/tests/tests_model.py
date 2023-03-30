"""
Tests for models.
"""


from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

        # according chatgpt

        # Email address normalization is the process of converting
        #  an email address to a
        # standard format, typically all lowercase letters,
        # to ensure consistency and avoid
        #  confusion caused by different capitalization of the
        # same email address. For
        # example, the email address 'JohnDoe@example.com' would be
        #  normalized to 'johndoe@example.com'.
        # In the test_new_user_email_normalized method,
        # the sample_emails list contains
        # pairs of email addresses and their expected normalized
        # versions. The method
        # iterates over each pair and creates a new user with the
        # provided email address
        # using the create_user method. It then checks
        # whether the created user's email
        # address matches the expected normalized version.
        # The different capitalization in the sample_emails list is
        # intentional, as email
        # addresses are case-insensitive. Different email providers
        # may handle
        # capitalization differently, but they all treat the same email
        # address with different capitalization as equivalent.
        #  Therefore, to ensure consistency and avoid confusion,
        # the email address should be normalized to a standard format,
        #  such as all lowercase letters.
    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )
        self.assertTrue(user.is_superuser)
        # superuser and staff will allow you to have
        self.assertTrue(user.is_staff)
        # access to everything in django admin,staff used to login to django admin
