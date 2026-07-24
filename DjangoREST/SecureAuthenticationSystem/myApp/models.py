import random
import uuid
from datetime import timedelta
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Custom manager because we use email as the username field
    instead of Django's default 'username' field.
    """

    def create_user(self, email, mobile, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not mobile:
            raise ValueError("Mobile number is required")

        email = self.normalize_email(email)
        user = self.model(email=email, mobile=mobile, **extra_fields)

        if password:
            user.set_password(password)  # this hashes the password
        else:
            user.set_unusable_password()  # user hasn't set a password yet (OTP stage)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_mobile_verified", True)
        return self.create_user(email, mobile, password, **extra_fields)


class GenderChoices(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    - is_active: True only after the user has successfully set a password.
    - is_mobile_verified: True only after OTP verification.
    Until both steps are done, the user cannot log in.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(
        max_length=201,
        editable=False
    )

    age = models.PositiveIntegerField(default=0)
    dob = models.DateField(verbose_name="Date of Birth")
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    hobby = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)

    accepted_terms_and_conditions = models.BooleanField(default=False)
    accepted_privacy_policy = models.BooleanField(default=False)

    is_mobile_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)  # becomes True after password is set
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"          # login identifier used internally
    REQUIRED_FIELDS = ["mobile", "first_name", "last_name", "dob"]

    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class OTP(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="otp"
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    otp_attempts = models.PositiveIntegerField(default=0)

    OTP_VALID_MINUTES = 5

    @classmethod
    def generate_for_user(cls, user):
        """Create or update OTP for a user."""

        code = f"{random.randint(100000, 999999)}"

        otp, created = cls.objects.get_or_create(
            user=user,
            defaults={
                "code": code,
                "expires_at": timezone.now() + timedelta(
                    minutes=cls.OTP_VALID_MINUTES
                ),
                "is_used": False,
                "otp_attempts": 1,
            },
        )

        if not created:
            otp.code = code
            otp.created_at = timezone.now()
            otp.expires_at = timezone.now() + timedelta(
                minutes=cls.OTP_VALID_MINUTES
            )
            otp.is_used = False
            otp.otp_attempts += 1

            otp.save(
                update_fields=[
                    "code",
                    "created_at",
                    "expires_at",
                    "is_used",
                    "otp_attempts",
                ]
            )

        return otp

    def is_valid(self):
        return (not self.is_used) and timezone.now() <= self.expires_at

    def __str__(self):
        return f"OTP {self.code} for {self.user.email}"
