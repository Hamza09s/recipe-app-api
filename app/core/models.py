"""
Database models.
"""
import uuid
import os


from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    # extract the extension of the filename
    filename = f"{uuid.uuid4()}{ext}"
    # we are creating our own filename through uuid
    # this way the upload png we keep the png extension, jpeg for
    # jpeg

    return os.path.join("uploads", "recipe", filename)
    # this way instead of string ourselves because
    # ensures string is created in appropriate format
    # for the OS we are running the code on
    # so best to use os.path.join to create paths
    # since windows,linux can have different paths


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        # spelling is important otherwise django cli won't pick it
        # check these lines when issue with django admin login
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Recipe(models.Model):
    """Recipe object."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    # user to whom the recipe belongs to
    # we are using foreign key because this allows us to
    # set up a relationship with another model
    # settings.auth if we ever change it don't have to change it
    # through the code base

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # text can hold more content
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField("Tag")
    ingredients = models.ManyToManyField("Ingredient")
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)
    # path tp where you want to upload the path to

    def __str__(self):
        return self.title

    # returns string representation of the object
    # if you don't specify this the django admin wil show id


# test_db wasn't destroyed last time as migrations weren't applied


class Tag(models.Model):
    """Tag for filtering recipes."""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredients for recipes"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
