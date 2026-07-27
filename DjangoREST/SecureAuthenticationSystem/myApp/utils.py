from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from twilio.rest import Client

def send_otp_sms(user, otp):
    """
    Sends the OTP + a verification link via SMS.

    NOTE: Plug in your real SMS gateway here (Twilio, MSG91, TextLocal, etc).
    For local development we just print to the console so you can see it
    working end-to-end without paying for SMS credits.
    """
    verify_link = f"{settings.FRONTEND_BASE_URL}/verify-otp?mobile={user.mobile}&otp={otp.code}"
    message = (
        f"Your verification OTP is {otp.code}. It is valid for "
        f"{otp.OTP_VALID_MINUTES} minutes. Verify here: {verify_link}"
    )

    # ---- Real gateway integration point ----
    client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(body=message, from_=settings.TWILIO_FROM_NUMBER, to=user.mobile)
    # -----------------------------------------

    print(f"[SMS -> {user.mobile}] {message}")  # dev-mode stand-in
    return message

class SetPasswordTokenGenerator(PasswordResetTokenGenerator):
    """
    Same idea as Django's built-in password-reset token, but we make it
    invalidate itself once is_mobile_verified flips (so a token generated
    before verification can't be reused oddly). We reuse it for the
    "set your password" email link too.
    """

    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_mobile_verified}{user.password}"


set_password_token_generator = SetPasswordTokenGenerator()

def send_set_password_email(user):
    """
    Sends the "set your password" link to the user's email after OTP
    verification succeeds. Uses Django's email backend, so in dev it
    prints to console (see EMAIL_BACKEND in settings.py); switch to real
    SMTP credentials in production.
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = set_password_token_generator.make_token(user)
    set_password_link = f"{settings.FRONTEND_BASE_URL}/set-password/{uidb64}/{token}/"

    send_mail(
        subject="Set your password",
        message=(
            f"Hi {user.first_name},\n\n"
            f"Your mobile number is verified. Click the link below to set your "
            f"password and activate your account:\n\n{set_password_link}\n\n"
            f"This link is valid for a limited time and can only be used once."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    return set_password_link