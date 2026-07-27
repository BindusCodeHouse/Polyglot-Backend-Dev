from datetime import date
from rest_framework import serializers
from .models import User,OTP
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from datetime import date
from django.contrib.auth import authenticate
from .utils import set_password_token_generator
from .validators import validate_strong_password

class RegisterSerializer(serializers.ModelSerializer):
    """
    Step 1: Collect profile details. No password here yet -
    that happens later, after OTP verification (set-password step).
    """
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "full_name", "age",
            "dob", "email", "mobile", "hobby", "gender",
        ]

    def validate_mobile(self, value):
        if not value.startswith("+"):
            raise serializers.ValidationError(
                "Mobile number must start with country code, e.g. +91."
            )

        digits = value[1:]

        if not digits.isdigit():
            raise serializers.ValidationError(
                "Mobile number must contain only digits after the + sign."
            )

        if not (10 <= len(digits) <= 15):
            raise serializers.ValidationError(
                "Enter a valid mobile number (10-15 digits)."
            )

        return value

    def validate_dob(self, value):
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def create(self, validated_data):
        # create_user() sets an unusable password until the set-password step
        return User.objects.create_user(**validated_data)

class VerifyOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    otp = serializers.CharField(
        max_length=6,
        min_length=6
    )

    def validate(self, attrs):
        try:
            user = User.objects.get(
                mobile=attrs["mobile"]
            )
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "mobile": "No user found with this mobile number."
            })

        try:
            otp_obj = user.otp
        except OTP.DoesNotExist:
            raise serializers.ValidationError({
                "otp": "No OTP found for this user."
            })

        attrs["user"] = user
        attrs["otp_obj"] = otp_obj

        return attrs

class SetPasswordSerializer(serializers.Serializer):
    """
    Step 3: Called from the link sent in the email.
    uid + token identify & authorize the user (like Django's password reset).
    """

    uidb64 = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    accepted_terms_and_conditions = serializers.BooleanField()
    accepted_privacy_policy = serializers.BooleanField()

    def validate(self, attrs):
        # Decode uid -> user
        try:
            uid = force_str(urlsafe_base64_decode(attrs["uidb64"]))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError({"uidb64": "Invalid link."})

        if not user.is_mobile_verified:
            raise serializers.ValidationError("Mobile number must be verified before setting a password.")

        if not set_password_token_generator.check_token(user, attrs["token"]):
            raise serializers.ValidationError({"token": "Invalid or expired link."})

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        # Run both our custom strength rules and Django's built-in validators
        try:
            validate_strong_password(attrs["password"])
            validate_password(attrs["password"], user=user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        if not attrs["accepted_terms_and_conditions"]:
            raise serializers.ValidationError({"accepted_terms_and_conditions": "You must accept the Terms & Conditions."})
        if not attrs["accepted_privacy_policy"]:
            raise serializers.ValidationError({"accepted_privacy_policy": "You must accept the Privacy Policy."})

        attrs["user"] = user
        return attrs

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs["email"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("Account is not active. Please complete registration first.")
        attrs["user"] = user
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "first_name", "last_name", "age", "dob", "email",
            "mobile", "hobby", "gender", "is_mobile_verified", "is_active",
        ]
        read_only_fields = fields