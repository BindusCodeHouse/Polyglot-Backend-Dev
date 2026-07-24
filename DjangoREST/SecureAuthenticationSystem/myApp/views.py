from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OTP, User
from .serializers import (
    RegisterSerializer, SetPasswordSerializer, VerifyOTPSerializer, LoginSerializer, UserProfileSerializer
)
from .utils import send_otp_sms,send_set_password_email
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    """
    STEP 1 — Register.
    No authentication required. Collects profile info, creates an
    inactive/unverified user, and sends an OTP to their mobile number.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        otp = OTP.generate_for_user(user)
        send_otp_sms(user, otp)

        return Response(
            {
                "data": serializer.data,
                "message": "Registration successful. An OTP has been sent to your mobile number.",
                "mobile": user.mobile,
                "next_step": "/myApp/verify-otp/",
            },
            status=status.HTTP_201_CREATED,
        )

class VerifyOTPView(APIView):

    permission_classes = [AllowAny]

    MAX_OTP_ATTEMPTS = 3

    def post(self, request):

        serializer = VerifyOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data["user"]
        otp_obj = serializer.validated_data["otp_obj"]
        entered_otp = serializer.validated_data["otp"]

        # --------------------------------
        # OTP is incorrect
        # --------------------------------

        if otp_obj.code != entered_otp:

            otp_obj.otp_attempts += 1

            # 3 wrong attempts
            if otp_obj.otp_attempts >= self.MAX_OTP_ATTEMPTS:

                user.delete()

                return Response(
                    {
                        "message": (
                            "You have entered the wrong OTP "
                            "3 times. Your registration has been "
                            "cancelled. Please register again."
                        ),
                        "next_step": "/myApp/register/"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Save attempt
            otp_obj.save(
                update_fields=["otp_attempts"]
            )

            attempts_remaining = (
                self.MAX_OTP_ATTEMPTS
                - otp_obj.otp_attempts
            )

            return Response(
                {
                    "message": (
                        "Invalid OTP. "
                        "Please enter the correct OTP."
                    ),
                    "attempts_remaining": attempts_remaining,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # --------------------------------
        # OTP is correct
        # --------------------------------

        otp_obj.is_used = True

        otp_obj.save(
            update_fields=["is_used"]
        )

        user.is_mobile_verified = True

        user.save(
            update_fields=["is_mobile_verified"]
        )

        send_set_password_email(user)

        return Response(
            {
                "message": (
                    "Mobile number verified successfully. "
                    "A link to set your password has been "
                    "sent to your email."
                )
            },
            status=status.HTTP_200_OK
        )

class SetPasswordView(APIView):
    """
    STEP 3 — Set Password (via the link emailed in Step 2).
    No JWT auth required — the uid + token in the payload IS the authorization.
    On success: hashes & saves the password, activates the account.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        user.set_password(serializer.validated_data["password"])  # hashes automatically (PBKDF2 by default)
        user.accepted_terms_and_conditions = serializer.validated_data["accepted_terms_and_conditions"]
        user.accepted_privacy_policy = serializer.validated_data["accepted_privacy_policy"]
        user.is_active = True
        user.save()

        return Response(
            {
                "message": "Password set successfully. Your account is now active.",
                "login_api": "/myApp/login/",
            },
            status=status.HTTP_200_OK,
        )

def get_tokens_for_user(user):
    """Issues a fresh access + refresh JWT pair for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

class LoginView(APIView):
    """
    STEP 4 — Login.
    No authentication required (this is what ISSUES the token).
    Returns access token (5 min) + refresh token (1 day) on success.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        tokens = get_tokens_for_user(user)

        return Response(
            {
                "message": "Login successful.",
                "tokens": tokens,
                "user": UserProfileSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )

class ProfileView(APIView):
    """
    Example of a PROTECTED endpoint — every request must carry:
    Authorization: Bearer <access_token>
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserProfileSerializer(request.user).data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    Blacklists the refresh token so it can no longer be used to get new
    access tokens. Requires the token_blacklist app (already wired up in
    settings.py / INSTALLED_APPS).
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except KeyError:
            return Response({"refresh": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"detail": "Invalid or already-used refresh token."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
