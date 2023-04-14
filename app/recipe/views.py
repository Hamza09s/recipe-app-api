"""
Views for the recipe APIs
"""
from rest_framework import (
    viewsets,
    mixins,
    status,
)

# mixin is additional things you can mix in the
# view to add in functionality

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""

    serializer_class = serializers.RecipeDetailSerializer
    # added detail the reason being beside for list we want to use this
    queryset = Recipe.objects.all()
    # objects that are available to the model ;Model.objects.all(), which
    #  returns a QuerySet containing all the objects in the database
    # for a particular model.
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        queryset = self.queryset
        return queryset.filter(user=self.request.user).order_by("-id")
        # we get user by request from the authentication system
        # as we know user is authenticated
        # so we can filter recipe for the user that is authenticated

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == "list":
            return serializers.RecipeSerializer
        # return reference to a class not instance
        elif self.action == "upload_image":
            return serializers.RecipeImageSerializer
        # we are gonna define our custom action
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        # serializer is validated
        serializer.save(user=self.request.user)

        # the reason why we have a listview and detailview is because
        # we don't want to use unnecessary resources to show details
        # every time so we default to listview

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# mixins are things you can mix in a view to add additional
# functionality


class BaseRecipeAttrViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-name")


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""

    # Put Generic in last since it can override some behaviour
    # mixin Update provides update functionality
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     """Filter queryset to authenticated user."""
    #     return self.queryset.filter(user=self.request.user).order_by("-name").distinct()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""

    # Put Generic in last since it can override some behaviour
    # mixin Update provides update functionality
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    # tells drf what models we want manageable through
    # ingredient viewset

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     """Filter queryset to authenticated user."""
    #     return self.queryset.filter(user=self.request.user).order_by("-name").distinct()
