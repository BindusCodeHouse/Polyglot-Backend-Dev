# Strong Authentication System

A secure and scalable **Django REST Framework (DRF) authentication system** that implements a multi-step user registration and authentication workflow.

The system uses:

* Django
* Django REST Framework
* PostgreSQL
* JWT Authentication
* Mobile OTP Verification
* Email-based Password Setup
* Django Password Validation
* Refresh Token Blacklisting
* Swagger/OpenAPI Documentation

The application is designed as a **REST API backend only**. It does not include a frontend UI.

---

## Features

### User Registration

Users can register by providing:

* First Name
* Last Name
* Full Name
* Age
* Date of Birth
* Email
* Mobile Number
* Hobby
* Gender

During registration:

1. User submits registration details.
2. The user account is created.
3. The account remains inactive until the registration process is completed.
4. An OTP is generated for mobile verification.
5. OTP is sent to the user's mobile number.

---

### Mobile OTP Verification

The user verifies their mobile number using the OTP received through SMS.

Security features:

* OTP is linked to the user.
* OTP has an expiration time.
* OTP can only be used once.
* User gets a maximum of 3 incorrect OTP attempts.
* After 3 incorrect attempts, the user account is permanently deleted.
* The user must register again after exceeding the maximum attempts.

After successful OTP verification:

1. The mobile number is marked as verified.
2. The OTP is marked as used.
3. A password setup link is sent to the user's email.

---

### Password Setup

After successful mobile verification, the user receives a password setup link through email.

The password setup request contains:

* `uidb64`
* `token`
* `password`
* `confirm_password`
* `accepted_terms_and_conditions`
* `accepted_privacy_policy`

Security validations include:

* User must exist.
* UID must be valid.
* Mobile number must already be verified.
* Password reset token must be valid and not expired.
* Password and confirm password must match.
* Custom password strength validation.
* Django's built-in password validators.
* Terms & Conditions must be accepted.
* Privacy Policy must be accepted.

After successful password setup:

* Password is securely hashed using Django's password hashing system.
* User accepts Terms & Conditions.
* User accepts Privacy Policy.
* User account is activated.

---

### JWT Login

After completing registration and password setup, the user can log in using:

* Email
* Password

After successful authentication, the API returns:

* Access Token
* Refresh Token
* User Profile

The access token is used to access protected APIs.

The refresh token is used to obtain a new access token after the access token expires.

---

### Protected Profile API

The profile API requires JWT authentication.

The client must send:

```text
Authorization: Bearer <access_token>
```

Only authenticated users can access their profile.

---

### Secure Logout

The logout API requires authentication and a refresh token.

When the user logs out:

1. The refresh token is received by the API.
2. The refresh token is blacklisted.
3. The blacklisted refresh token can no longer be used to generate new access tokens.

This provides server-side refresh token invalidation.

---

# Authentication Flow

The complete authentication flow is:

```text
                             Enter OTP
                                  │
                                  ▼
                             OTP Correct?
                              /        \
                            YES         NO
                             │           │
                             ▼           ▼
                      Verify Mobile   Increase Attempts
                             │           │
                             │           ▼
                             │      Attempts >= 3?
                             │        /       \
                             │      YES        NO
                             │       │          │
                             │       ▼          ▼
                             │   Delete User  Try OTP Again
                             │       │
                             │       ▼
                             │  Register Again
                             │
                             ▼
                      Send Password
                       Setup Email
                             │
                             ▼
                       Set Password
                             │
                             ▼
                      Activate Account
                             │
                             ▼
                           Login
                             │
                             ▼
                      Generate JWT
                             │
                             ▼
                    Access Protected APIs
                             │
                             ▼
                          Logout
                             │
                             ▼
                   Blacklist Refresh Token
```

---

# Project Structure

A recommended project structure is:

```text
StrongAuthenticationSystem/
│
├── manage.py
│
├── myProject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── myApp/
│   ├── migrations/
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── utils.py
│   └── tests.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# API Endpoints

Assuming the application is mounted using:

```python
path("myApp/", include("myApp.urls"))
```

The available endpoints are:

| Method | Endpoint               | Authentication | Description                       |
| ------ | ---------------------- | -------------- | --------------------------------- |
| POST   | `/myApp/register/`     | No             | Register a new user               |
| POST   | `/myApp/verify-otp/`   | No             | Verify mobile OTP                 |
| POST   | `/myApp/set-password/` | No             | Set password and activate account |
| POST   | `/myApp/login/`        | No             | Login and receive JWT tokens      |
| GET    | `/myApp/profile/`      | JWT Required   | Get authenticated user's profile  |
| POST   | `/myApp/logout/`       | JWT Required   | Blacklist refresh token           |

---

# API Flow

## Step 1 — Register

### Endpoint

```text
POST /myApp/register/
```

### Request

```json
{
    "first_name": "Bindu",
    "last_name": "Bhatia",
    "age": 25,
    "dob": "2001-01-01",
    "email": "bindu@example.com",
    "mobile": "+919876543210",
    "hobby": "Reading",
    "gender": "Female"
}
```

### Successful Response

```json
{
    "data": {
        "first_name": "Bindu",
        "last_name": "Bhatia",
        "full_name": "Bindu Bhatia",
        "age": 25,
        "dob": "2001-01-01",
        "email": "bindu@example.com",
        "mobile": "+919876543210",
        "hobby": "Reading",
        "gender": "Female"
    },
    "message": "Registration successful. An OTP has been sent to your mobile number.",
    "mobile": "+919876543210",
    "next_step": "/myApp/verify-otp/"
}
```

---

## Step 2 — Verify OTP

### Endpoint

```text
POST /myApp/verify-otp/
```

### Request

```json
{
    "mobile": "+919876543210",
    "otp": "123456"
}
```

### Successful Response

```json
{
    "message": "Mobile number verified successfully. A link to set your password has been sent to your email."
}
```

After successful verification:

```text
is_mobile_verified = True
otp.is_used = True
```

The user receives an email containing a password setup link.

---

## Incorrect OTP

If the OTP is incorrect:

```json
{
    "message": "Invalid OTP. Please enter the correct OTP.",
    "attempts_remaining": 2
}
```

The maximum number of incorrect attempts is:

```text
3
```

After the third incorrect attempt:

```json
{
    "message": "You have entered the wrong OTP 3 times. Your registration has been cancelled. Please register again.",
    "next_step": "/myApp/register/"
}
```

The user account is deleted.

Because the OTP has a relationship with the user using cascading deletion, the associated OTP record is also deleted.

---

# Step 3 — Set Password

### Endpoint

```text
POST /myApp/set-password/
```

### Request

```json
{
    "uidb64": "MQ",
    "token": "password-reset-token",
    "password": "StrongPassword@123",
    "confirm_password": "StrongPassword@123",
    "accepted_terms_and_conditions": true,
    "accepted_privacy_policy": true
}
```

### Successful Response

```json
{
    "message": "Password set successfully. Your account is now active.",
    "login_api": "/myApp/login/"
}
```

After successful password setup:

```text
is_active = True
```

The password is stored securely using Django's password hashing mechanism.

---

# Step 4 — Login

### Endpoint

```text
POST /myApp/login/
```

### Request

```json
{
    "email": "bindu@example.com",
    "password": "StrongPassword@123"
}
```

### Successful Response

```json
{
    "message": "Login successful.",
    "tokens": {
        "refresh": "<refresh_token>",
        "access": "<access_token>"
    },
    "user": {
        "id": "user-uuid",
        "first_name": "Bindu",
        "last_name": "Bhatia",
        "age": 25,
        "dob": "2001-01-01",
        "email": "bindu@example.com",
        "mobile": "+919876543210",
        "hobby": "Reading",
        "gender": "Female",
        "is_mobile_verified": true,
        "is_active": true
    }
}
```

---

# Step 5 — Access Profile

### Endpoint

```text
GET /myApp/profile/
```

### Header

```text
Authorization: Bearer <access_token>
```

### Successful Response

```json
{
    "id": "user-uuid",
    "first_name": "Bindu",
    "last_name": "Bhatia",
    "age": 25,
    "dob": "2001-01-01",
    "email": "bindu@example.com",
    "mobile": "+919876543210",
    "hobby": "Reading",
    "gender": "Female",
    "is_mobile_verified": true,
    "is_active": true
}
```

---

# Step 6 — Logout

### Endpoint

```text
POST /myApp/logout/
```

### Header

```text
Authorization: Bearer <access_token>
```

### Request

```json
{
    "refresh": "<refresh_token>"
}
```

### Successful Response

```json
{
    "message": "Logged out successfully."
}
```

The refresh token is blacklisted and cannot be used again to obtain a new access token.

---

# Authentication Configuration

Configure Django REST Framework authentication in `settings.py`.

Example:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}
```

Configure JWT token lifetime using Simple JWT.

Example:

```python
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),

    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,

    "AUTH_HEADER_TYPES": ("Bearer",),
}
```

> The actual token expiration values should match the values configured in your project. The values above are examples based on the current implementation comments.

---

# Required Django Applications

Add the following applications to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # Django applications

    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",

    # Your application
    "myApp",
]
```

If CORS support is required:

```python
"corsheaders",
```

can also be added.

---

# Database

The project can use PostgreSQL as the production database.

Example configuration:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "django_authentication_system",
        "USER": "postgres",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

For security, database credentials should not be hardcoded in `settings.py`.

Use environment variables instead.

Example `.env`:

```env
DB_NAME=django_authentication_system
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

# Email Configuration

The password setup link is sent to the user's email after successful OTP verification.

Configure email settings using environment variables.

Example:

```env
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

For Gmail, use a **Google App Password** instead of your regular Gmail account password.

Never commit sensitive email credentials to GitHub.

---

# SMS / OTP Configuration

The system sends OTP messages to the user's mobile number.

The OTP service is called through:

```python
send_otp_sms(user, otp)
```

The implementation can be connected to an SMS provider such as Twilio or another SMS gateway.

Recommended environment variables:

```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_NUMBER=your_twilio_number
```

Keep these credentials inside `.env` and never commit them to source control.

---

# Environment Variables

Example `.env` file:

```env
# Django
SECRET_KEY=your_secret_key
DEBUG=True

# Database
DB_NAME=django_authentication_system
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# SMS
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_NUMBER=your_twilio_number
```

Add `.env` to `.gitignore`:

```text
.env
```

---

# Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
```

Navigate into the project:

```bash
cd StrongAuthenticationSystem
```

---

## 2. Create Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Example dependencies:

```text
Django
djangorestframework
djangorestframework-simplejwt
psycopg
python-decouple
django-cors-headers
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

Add:

```env
SECRET_KEY=your_secret_key
DEBUG=True
```

Add database, email, and SMS configuration as required.

---

## 5. Run Migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

---

## 6. Create Superuser

If you are using a custom user model:

```bash
python manage.py createsuperuser
```

Follow the prompts to create the admin account.

---

## 7. Run Development Server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

---

# Admin Panel

The Django admin panel can be accessed at:

```text
http://127.0.0.1:8000/admin/
```

The admin panel can be used to manage:

* Users
* OTP records

---

# Security Design

This project follows a multi-layer authentication approach.

### Layer 1 — User Registration

User profile information is collected without setting a password.

### Layer 2 — Mobile Verification

The user must verify ownership of their mobile number through OTP.

### Layer 3 — OTP Attempt Protection

The user has a maximum of 3 incorrect OTP attempts.

### Layer 4 — Email Authorization

After successful mobile verification, a secure tokenized password setup link is sent to the user's email.

### Layer 5 — Password Validation

Passwords are checked using:

* Custom password strength rules
* Django's built-in password validators
* Password confirmation

### Layer 6 — Account Activation

The account remains inactive until the password setup process is completed.

### Layer 7 — JWT Authentication

Successful login generates:

* Access Token
* Refresh Token

### Layer 8 — Protected APIs

Protected endpoints require:

```text
Authorization: Bearer <access_token>
```

### Layer 9 — Refresh Token Blacklisting

Logout blacklists the refresh token to prevent further token refresh operations.

---

# User Account States

The user progresses through the following states:

```text
New Registration
       │
       ▼
User Created
       │
       │ OTP Sent
       ▼
Waiting for OTP Verification
       │
       ├──────── Wrong OTP × 3 ────────► User Deleted
       │
       ▼
Mobile Verified
       │
       │ Password Setup Email Sent
       ▼
Waiting for Password Setup
       │
       ▼
Password Created
       │
       ▼
Account Activated
       │
       ▼
Login
       │
       ▼
JWT Authentication
       │
       ▼
Protected API Access
```

---

# API Authentication Header

For protected APIs, include the access token in the HTTP request header:

```text
Authorization: Bearer <access_token>
```

Example:

```text
GET /myApp/profile/
```

Header:

```text
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

---

# Error Handling

The API uses standard HTTP status codes.

| Status Code | Meaning                                  |
| ----------- | ---------------------------------------- |
| `200`       | Request successful                       |
| `201`       | Resource created successfully            |
| `400`       | Invalid request or validation error      |
| `401`       | Authentication required or invalid token |
| `403`       | Permission denied                        |
| `404`       | Resource not found                       |
| `500`       | Internal server error                    |

---

# Recommended Improvements

For production deployment, the following improvements can be added:

* OTP resend API with rate limiting
* OTP resend limit
* OTP expiration validation
* Email verification
* Password reset / forgot password flow
* Account lockout after repeated login failures
* JWT refresh token rotation
* Rate limiting for authentication endpoints
* API throttling
* HTTPS
* Secure cookie configuration where applicable
* CSRF protection where applicable
* Audit logging
* Login activity tracking
* Device/session management
* Two-factor authentication
* CAPTCHA for registration and login
* Structured logging and monitoring

---

# Important Security Notes

1. Never store passwords in plain text.
2. Never commit `.env` files to Git.
3. Never expose JWT secret keys publicly.
4. Never expose SMS provider credentials.
5. Never expose email credentials.
6. Use HTTPS in production.
7. Use a strong Django `SECRET_KEY`.
8. Keep dependencies updated.
9. Configure appropriate rate limiting for OTP and login APIs.
10. Use secure production database credentials.
11. Disable `DEBUG` in production.
12. Validate and sanitize all user input.
13. Consider using short-lived access tokens.
14. Protect refresh tokens carefully.
15. Use refresh token rotation for higher-security applications.

---

# Technology Stack

```text
Backend       : Python
Framework     : Django
API Framework : Django REST Framework
Authentication: JWT
Database      : PostgreSQL
OTP           : SMS-based OTP
Email         : SMTP / Email Service
API Testing   : Postman
Documentation : Swagger / OpenAPI
```

---

# Complete Authentication Sequence

```text
1. User Registration
        ↓
2. Create Inactive User
        ↓
3. Generate OTP
        ↓
4. Send OTP via SMS
        ↓
5. User Enters OTP
        ↓
6. Verify OTP
        ↓
7. Mark Mobile as Verified
        ↓
8. Send Password Setup Email
        ↓
9. User Opens Secure Password Link
        ↓
10. Validate UID + Token
        ↓
11. Validate Password
        ↓
12. Accept Terms & Privacy Policy
        ↓
13. Set Password
        ↓
14. Activate Account
        ↓
15. User Login
        ↓
16. Generate Access + Refresh JWT
        ↓
17. Access Protected APIs
        ↓
18. Logout
        ↓
19. Blacklist Refresh Token
```

---

# Conclusion

The **Strong Authentication System** provides a secure, multi-step authentication workflow using Django REST Framework.

The system combines:

* Mobile OTP verification
* Email-based password authorization
* Strong password validation
* Account activation controls
* JWT-based authentication
* Protected REST APIs
* Refresh token blacklisting

This architecture provides a strong foundation for building secure backend applications that require verified user registration and token-based API authentication.
