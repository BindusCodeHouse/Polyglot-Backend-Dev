from django.contrib import admin
from .models import User, OTP


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "full_name",
        "age",
        "dob",
        "email",
        "mobile",
        "hobby",
        "gender",
        "accepted_terms_and_conditions",
        "accepted_privacy_policy",
        "is_mobile_verified",
        "is_active",
        "is_staff",
        "created_at",
        "updated_at",
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "code",
        "created_at",
        "expires_at",
        "is_used",
        "otp_attempts",
    )