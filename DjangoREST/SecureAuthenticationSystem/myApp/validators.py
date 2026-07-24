import re

from django.core.exceptions import ValidationError


def validate_strong_password(password):
    """
    Enforces a strong password:
    - at least 8 characters
    - at least 1 uppercase letter
    - at least 1 lowercase letter
    - at least 1 digit
    - at least 1 special character
    Raises ValidationError (DRF turns this into a 400 response) if it fails.
    """
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter.")
    if not re.search(r"[0-9]", password):
        errors.append("Password must contain at least one digit.")
    if not re.search(r"[!@#$%^&*()\-_=+{};:,<.>?/\\|~`]", password):
        errors.append("Password must contain at least one special character.")

    if errors:
        raise ValidationError(errors)
