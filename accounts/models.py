from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserType(models.TextChoices):
    GUEST = "guest", "Guest"
    REGULAR = "regular", "Regular"
    ADMIN = "admin", "Admin"


class CustomUserManager(BaseUserManager):
    """Define a model manager for CustomUser model with no username field."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("user_type", UserType.ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        print(f"extra_fields: {extra_fields}")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email as the unique identifier."""

    user_type = models.CharField(
        max_length=20, choices=UserType.choices, default=UserType.REGULAR
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=False)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        # Set the admin status according to the user type
        if self.user_type == UserType.ADMIN:
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(email={self.email!r}, username={self.username!r}, user_type={self.user_type!r})"

    def __str__(self):
        return self.email
