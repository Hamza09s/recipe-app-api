"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
# restframework allows generic ways to handle apis which can be
# configured/overrided

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer
    # CreateApiView create user
    # set serializer so django knows what serializer to use
    # so it will know which model it wants to use since
    # it was defined


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    # we are customizing to use email and password


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    # using token authentication for our case
    permission_classes = [permissions.IsAuthenticated]
    # what permission this user has or allowed to do
    # no other restriction besides being authenticated

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
