from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager for User model."""

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault("role", "ADMIN")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """Custom user model with email as the unique identifier."""

    username = None
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("REVIEWER", "Reviewer"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="REVIEWER")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
